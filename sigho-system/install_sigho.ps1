# Script de Instalacion del Sistema SIGHO para Windows
# Sistema Integrado de Gestion Hotelera
# PowerShell Script

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "SIGHO - Sistema Integrado de Gestion Hotelera" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Instalando el sistema completo..." -ForegroundColor Yellow
Write-Host ""

# Verificar Python 3.12
try {
    $pythonVersion = py -3.12 --version 2>&1
    Write-Host "[OK] $pythonVersion detectado" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Python 3.12 no esta instalado" -ForegroundColor Red
    Write-Host "Por favor instale Python 3.12 desde:" -ForegroundColor Red
    Write-Host "https://www.python.org/downloads/release/python-3120/" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verificar si estamos en el directorio correcto
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "[ERROR] Directorios backend o frontend no encontrados" -ForegroundColor Red
    Write-Host "Por favor ejecute primero el script de estructura crear_estructura.ps1" -ForegroundColor Red
    exit 1
}

# ========== BACKEND ==========
Write-Host "Instalando Backend...\" -ForegroundColor Yellow
Write-Host ""

Set-Location backend

# Crear entorno virtual si no existe
if (-not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual del backend..." -ForegroundColor Cyan
    py -3.12 -m venv venv
}
else {
    Write-Host "Entorno virtual del backend ya existe" -ForegroundColor Gray
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"

# Actualizar pip
Write-Host "Actualizando pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

# Instalar dependencias
Write-Host "Instalando dependencias del backend..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

# Crear archivo .env si no existe
if (-not (Test-Path ".env")) {
    Write-Host "Creando archivo de configuracion .env..." -ForegroundColor Cyan
    
    $envContent = @'
# Configuracion del Backend - SIGHO

# Aplicacion
APP_NAME=SIGHO - Sistema Integrado de Gestion Hotelera
APP_VERSION=1.0.0
DEBUG=True
HOST=127.0.0.1
PORT=8000

# Base de datos SQLite3
DATABASE_URL=sqlite:///./sigho.db

# Seguridad
SECRET_KEY=tu_clave_secreta_super_segura_cambiala_en_produccion_12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:*,http://127.0.0.1:*

# Hotel Info
HOTEL_NAME=Hotel SIGHO
HOTEL_ADDRESS=Nueva Esparta, Venezuela
HOTEL_PHONE=+58 424 1234567
HOTEL_EMAIL=info@hotelsigho.com

# Monedas
CURRENCIES=VES,USD,EUR

# Zona horaria
TIMEZONE=America/Caracas
'@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "[OK] Archivo .env creado" -ForegroundColor Green
}

deactivate
Set-Location ..

Write-Host "[OK] Backend instalado correctamente" -ForegroundColor Green
Write-Host ""

# ========== FRONTEND ==========
Write-Host "Instalando Frontend..." -ForegroundColor Yellow
Write-Host ""

Set-Location frontend

# Crear entorno virtual si no existe
if (-not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual del frontend..." -ForegroundColor Cyan
    py -3.12 -m venv venv
}
else {
    Write-Host "Entorno virtual del frontend ya existe" -ForegroundColor Gray
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"

# Actualizar pip
Write-Host "Actualizando pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

# Instalar dependencias
Write-Host "Instalando dependencias del frontend..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

deactivate
Set-Location ..

Write-Host "[OK] Frontend instalado correctamente" -ForegroundColor Green
Write-Host ""

# ========== FINALIZACION ==========
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "[OK] Instalacion completada exitosamente!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Iniciar el Backend:" -ForegroundColor Cyan
Write-Host "   cd backend"
Write-Host "   venv\Scripts\activate"
Write-Host "   python main.py"
Write-Host "   (El backend estara en http://127.0.0.1:8000)"
Write-Host ""
Write-Host "2. En otra ventana PowerShell, iniciar el Frontend:" -ForegroundColor Cyan
Write-Host "   cd frontend"
Write-Host "   venv\Scripts\activate"
Write-Host "   python main.py"
Write-Host ""
Write-Host "3. Credenciales por defecto:" -ForegroundColor Cyan
Write-Host "   Usuario: admin"
Write-Host "   Contrasena: admin123"
Write-Host ""
Write-Host "Documentacion API: http://127.0.0.1:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
