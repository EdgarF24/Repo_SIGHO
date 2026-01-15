# Script para iniciar el Frontend del SIGHO en Windows
# PowerShell Script

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Iniciando Frontend SIGHO" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "main.py")) {
    Write-Host "[ERROR] main.py no encontrado" -ForegroundColor Red
    Write-Host "Por favor ejecute este script desde el directorio frontend\" -ForegroundColor Yellow
    exit 1
}

# Verificar que existe el entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "[ERROR] Entorno virtual no encontrado" -ForegroundColor Red
    Write-Host "Por favor ejecute primero: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"

# Verificar instalacion
try {
    python -c "import customtkinter" 2>&1 | Out-Null
}
catch {
    Write-Host "[ERROR] CustomTkinter no esta instalado" -ForegroundColor Red
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Verificar que el backend esta corriendo
Write-Host ""
Write-Host "Verificando conexion con el backend..." -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
    Write-Host "[OK] Backend detectado en http://127.0.0.1:8000" -ForegroundColor Green
}
catch {
    Write-Host "[ADVERTENCIA] No se puede conectar con el backend" -ForegroundColor Yellow
    Write-Host "   Por favor asegurese de que el backend este ejecutandose" -ForegroundColor Yellow
    Write-Host "   Puede iniciarlo con: cd backend && .\start_backend.ps1" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Desea continuar de todos modos? (s/n)"
    
    if ($continue -ne "s" -and $continue -ne "S") {
        deactivate
        exit 1
    }
}

Write-Host ""
Write-Host "[OK] Entorno configurado correctamente" -ForegroundColor Green
Write-Host ""
Write-Host "Iniciando interfaz grafica..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Credenciales por defecto:" -ForegroundColor Yellow
Write-Host "   Usuario: admin"
Write-Host "   Contrasena: admin123"
Write-Host ""
Write-Host "Presione Ctrl+C para cerrar la aplicacion" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Iniciar la aplicacion
try {
    python main.py
}
finally {
    # Desactivar entorno virtual al salir
    deactivate
}
