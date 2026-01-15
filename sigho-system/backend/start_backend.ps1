# Script para iniciar el Backend del SIGHO en Windows
# PowerShell Script

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Iniciando Backend SIGHO" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "main.py")) {
    Write-Host "[ERROR] main.py no encontrado" -ForegroundColor Red
    Write-Host "Por favor ejecute este script desde el directorio backend\" -ForegroundColor Yellow
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
    python -c "import fastapi" 2>&1 | Out-Null
}
catch {
    Write-Host "[ERROR] FastAPI no esta instalado" -ForegroundColor Red
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "[OK] Entorno configurado correctamente" -ForegroundColor Green
Write-Host ""
Write-Host "Iniciando servidor FastAPI..." -ForegroundColor Cyan
Write-Host "   - URL: http://127.0.0.1:8000"
Write-Host "   - Docs: http://127.0.0.1:8000/docs"
Write-Host ""
Write-Host "Presione Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Iniciar el servidor
try {
    python main.py
}
finally {
    # Desactivar entorno virtual al salir
    deactivate
}
