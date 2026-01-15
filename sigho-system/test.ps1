# Diagnostico del Sistema SIGHO
# PowerShell Script para Windows

Write-Host "Diagnostico del Sistema SIGHO" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Verificando Backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "[OK] Backend respondiendo" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Backend NO responde" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "2. Probando Dashboard..." -ForegroundColor Yellow
try {
    $dashResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/dashboard/overview" -TimeoutSec 5 -ErrorAction Stop
    $dashContent = $dashResponse.Content
    
    Write-Host "Respuesta del Dashboard:" -ForegroundColor Cyan
    # Mostrar primeras 500 caracteres
    if ($dashContent.Length -gt 500) {
        Write-Host $dashContent.Substring(0, 500)
    }
    else {
        Write-Host $dashContent
    }
    
    if ($dashContent -match "rooms") {
        Write-Host "[OK] Dashboard funcionando" -ForegroundColor Green
    }
    else {
        Write-Host "[ERROR] Dashboard con problemas" -ForegroundColor Red
        Write-Host ""
        Write-Host "Ver error completo:"
        Write-Host $dashContent
    }
}
catch {
    Write-Host "[ERROR] Error al acceder al Dashboard" -ForegroundColor Red
    Write-Host $_.Exception.Message
}

Write-Host ""
Write-Host "3. Verificando Base de Datos..." -ForegroundColor Yellow
Set-Location backend

if (Test-Path "sigho.db") {
    $dbSize = (Get-Item "sigho.db").Length
    $dbSizeMB = [math]::Round($dbSize / 1MB, 2)
    
    Write-Host "[OK] Archivo sigho.db existe" -ForegroundColor Green
    Write-Host "Tamanio: $dbSizeMB MB" -ForegroundColor Cyan
    
    # Verificar si sqlite3 esta disponible
    if (Get-Command sqlite3 -ErrorAction SilentlyContinue) {
        Write-Host ""
        Write-Host "Contenido de la BD:" -ForegroundColor Cyan
        $userCount = sqlite3 sigho.db "SELECT COUNT(*) FROM users;"
        $roomCount = sqlite3 sigho.db "SELECT COUNT(*) FROM rooms;"
        $roomTypeCount = sqlite3 sigho.db "SELECT COUNT(*) FROM room_types;"
        
        Write-Host "- Usuarios: $userCount"
        Write-Host "- Habitaciones: $roomCount"
        Write-Host "- Tipos Habitacion: $roomTypeCount"
    }
    else {
        Write-Host "[INFO] sqlite3 no instalado. Para analisis detallado, instalar SQLite:" -ForegroundColor Yellow
        Write-Host "   https://www.sqlite.org/download.html" -ForegroundColor Gray
    }
}
else {
    Write-Host "[ERROR] sigho.db NO existe" -ForegroundColor Red
}

Write-Host ""
Write-Host "4. Ultimos errores del backend:" -ForegroundColor Yellow
Set-Location ..

if (Test-Path "backend.log") {
    Write-Host "Ultimas 10 lineas con ERROR:" -ForegroundColor Cyan
    $errors = Get-Content "backend.log" | Select-String -Pattern "error" -SimpleMatch | Select-Object -Last 10
    
    if ($errors) {
        $errors | ForEach-Object { Write-Host $_ }
    }
    else {
        Write-Host "No se encontraron errores en el log" -ForegroundColor Green
    }
}
else {
    Write-Host "No hay archivo backend.log" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "[OK] Diagnostico completado" -ForegroundColor Green
