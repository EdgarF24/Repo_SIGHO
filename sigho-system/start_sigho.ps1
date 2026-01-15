# Script para iniciar Backend y Frontend del SIGHO simultaneamente en Windows
# PowerShell Script

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "SIGHO - Sistema Integrado de Gestion Hotelera" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Iniciando sistema completo..." -ForegroundColor Yellow
Write-Host ""

# Verificar estructura
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "[ERROR] Directorios backend o frontend no encontrados" -ForegroundColor Red
    exit 1
}

# Variables para procesos
$backendJob = $null
$frontendJob = $null

# Funcion para limpiar procesos al salir
function Cleanup {
    Write-Host ""
    Write-Host "Deteniendo servicios..." -ForegroundColor Yellow
    
    if ($backendJob) {
        Stop-Job $backendJob -ErrorAction SilentlyContinue
        Remove-Job $backendJob -ErrorAction SilentlyContinue
    }
    
    if ($frontendJob) {
        Stop-Job $frontendJob -ErrorAction SilentlyContinue
        Remove-Job $frontendJob -ErrorAction SilentlyContinue
    }
    
    # Detener procesos Python en el puerto 8000
    Get-Process | Where-Object { $_.ProcessName -eq "python" } | ForEach-Object {
        $connections = Get-NetTCPConnection -OwningProcess $_.Id -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -eq 8000 }
        if ($connections) {
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
    }
    
    Write-Host "[OK] Servicios detenidos" -ForegroundColor Green
}

# Registrar manejador de Ctrl+C
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup }

try {
    # ========== BACKEND ==========
    Write-Host "Iniciando Backend..." -ForegroundColor Cyan
    
    # Verificar entorno virtual
    if (-not (Test-Path "backend\venv")) {
        Write-Host "[ERROR] Entorno virtual del backend no encontrado" -ForegroundColor Red
        Write-Host "Por favor ejecute primero: .\install_sigho.ps1" -ForegroundColor Yellow
        exit 1
    }
    
    # Iniciar backend en background job
    $backendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD\backend
        & "venv\Scripts\Activate.ps1"
        python main.py *>&1 | Tee-Object -FilePath "..\backend.log"
    }
    
    # Esperar a que el backend este listo
    Write-Host "Esperando a que el backend este listo..." -ForegroundColor Yellow
    
    $maxAttempts = 30
    $attempt = 0
    $backendReady = $false
    
    while ($attempt -lt $maxAttempts) {
        Start-Sleep -Seconds 1
        $attempt++
        
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $backendReady = $true
                break
            }
        }
        catch {
            # Continuar intentando
        }
        
        # Verificar si el job fallo
        if ($backendJob.State -eq "Failed" -or $backendJob.State -eq "Completed") {
            Write-Host "[ERROR] El backend fallo al iniciar" -ForegroundColor Red
            Write-Host "Revise el archivo backend.log para mas detalles" -ForegroundColor Yellow
            Cleanup
            exit 1
        }
    }
    
    if (-not $backendReady) {
        Write-Host "[ERROR] El backend no responde despues de 30 segundos" -ForegroundColor Red
        Write-Host "Revise el archivo backend.log para mas detalles" -ForegroundColor Yellow
        Cleanup
        exit 1
    }
    
    Write-Host "[OK] Backend iniciado correctamente (Job ID: $($backendJob.Id))" -ForegroundColor Green
    
    # ========== FRONTEND ==========
    Write-Host ""
    Write-Host "Iniciando Frontend..." -ForegroundColor Cyan
    Start-Sleep -Seconds 2
    
    # Verificar entorno virtual
    if (-not (Test-Path "frontend\venv")) {
        Write-Host "[ERROR] Entorno virtual del frontend no encontrado" -ForegroundColor Red
        Write-Host "Por favor ejecute primero: .\install_sigho.ps1" -ForegroundColor Yellow
        Cleanup
        exit 1
    }
    
    # Iniciar frontend en background job
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD\frontend
        & "venv\Scripts\Activate.ps1"
        python main.py *>&1 | Tee-Object -FilePath "..\frontend.log"
    }
    
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "[OK] Sistema SIGHO iniciado correctamente" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Estado de los servicios:" -ForegroundColor Yellow
    Write-Host "   Backend:  http://127.0.0.1:8000 (Job ID: $($backendJob.Id))"
    Write-Host "   Frontend: Interfaz grafica (Job ID: $($frontendJob.Id))"
    Write-Host ""
    Write-Host "Documentacion API: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Credenciales por defecto:" -ForegroundColor Yellow
    Write-Host "   Usuario: admin"
    Write-Host "   Contrasena: admin123"
    Write-Host ""
    Write-Host "Logs:" -ForegroundColor Yellow
    Write-Host "   Backend:  .\backend.log"
    Write-Host "   Frontend: .\frontend.log"
    Write-Host ""
    Write-Host "Presione Ctrl+C para detener todos los servicios" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Mantener el script corriendo y mostrar output de los jobs
    while ($true) {
        # Verificar estado de los jobs
        if ($backendJob.State -eq "Failed" -or $backendJob.State -eq "Completed") {
            Write-Host "Backend ha terminado inesperadamente" -ForegroundColor Yellow
            break
        }
        
        if ($frontendJob.State -eq "Failed" -or $frontendJob.State -eq "Completed") {
            Write-Host "Frontend ha terminado" -ForegroundColor Yellow
            break
        }
        
        Start-Sleep -Seconds 2
    }
    
}
finally {
    Cleanup
}
