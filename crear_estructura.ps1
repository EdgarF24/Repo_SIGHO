# Script para crear la estructura del Sistema Integrado de Gestion Hotelera (SIGHO)
# Arquitectura: FastAPI Backend + CustomTkinter Frontend + SQLite3
# Python 3.12
# PowerShell para Windows

Write-Host "Creando estructura del proyecto SIGHO..." -ForegroundColor Cyan

# Crear directorio raiz
New-Item -ItemType Directory -Force -Path "sigho-system" | Out-Null
Set-Location "sigho-system"

# ========== BACKEND (FastAPI + SQLite3) ==========
Write-Host "Creando estructura del Backend (FastAPI)..." -ForegroundColor Yellow

# Crear directorios del backend
$backendDirs = @(
    "backend\app\api\endpoints",
    "backend\app\api\dependencies",
    "backend\app\core",
    "backend\app\models",
    "backend\app\schemas",
    "backend\app\services",
    "backend\app\database",
    "backend\tests",
    "backend\scripts"
)

foreach ($dir in $backendDirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# Archivos raiz del backend
$backendRootFiles = @(
    "backend\requirements.txt",
    "backend\.env",
    "backend\.gitignore",
    "backend\README.md",
    "backend\main.py"
)

foreach ($file in $backendRootFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Core
$coreFiles = @(
    "backend\app\__init__.py",
    "backend\app\core\__init__.py",
    "backend\app\core\config.py",
    "backend\app\core\security.py"
)

foreach ($file in $coreFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Database
$dbFiles = @(
    "backend\app\database\__init__.py",
    "backend\app\database\session.py",
    "backend\app\database\base.py",
    "backend\app\database\init_db.py"
)

foreach ($file in $dbFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Models (SQLAlchemy con SQLite3)
$modelFiles = @(
    "backend\app\models\__init__.py",
    "backend\app\models\user.py",
    "backend\app\models\room.py",
    "backend\app\models\room_type.py",
    "backend\app\models\reservation.py",
    "backend\app\models\guest.py",
    "backend\app\models\payment.py",
    "backend\app\models\maintenance.py",
    "backend\app\models\inventory.py",
    "backend\app\models\inventory_movement.py"
)

foreach ($file in $modelFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Schemas (Pydantic)
$schemaFiles = @(
    "backend\app\schemas\__init__.py",
    "backend\app\schemas\user.py",
    "backend\app\schemas\room.py",
    "backend\app\schemas\reservation.py",
    "backend\app\schemas\guest.py",
    "backend\app\schemas\payment.py",
    "backend\app\schemas\maintenance.py",
    "backend\app\schemas\inventory.py",
    "backend\app\schemas\report.py"
)

foreach ($file in $schemaFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Services (Logica de negocio)
$serviceFiles = @(
    "backend\app\services\__init__.py",
    "backend\app\services\auth_service.py",
    "backend\app\services\user_service.py",
    "backend\app\services\room_service.py",
    "backend\app\services\reservation_service.py",
    "backend\app\services\guest_service.py",
    "backend\app\services\payment_service.py",
    "backend\app\services\maintenance_service.py",
    "backend\app\services\inventory_service.py",
    "backend\app\services\report_service.py"
)

foreach ($file in $serviceFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# API Endpoints
$apiFiles = @(
    "backend\app\api\__init__.py",
    "backend\app\api\dependencies\__init__.py",
    "backend\app\api\dependencies\auth.py",
    "backend\app\api\endpoints\__init__.py",
    "backend\app\api\endpoints\auth.py",
    "backend\app\api\endpoints\users.py",
    "backend\app\api\endpoints\rooms.py",
    "backend\app\api\endpoints\reservations.py",
    "backend\app\api\endpoints\guests.py",
    "backend\app\api\endpoints\payments.py",
    "backend\app\api\endpoints\maintenance.py",
    "backend\app\api\endpoints\inventory.py",
    "backend\app\api\endpoints\reports.py",
    "backend\app\api\endpoints\dashboard.py"
)

foreach ($file in $apiFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Scripts utiles
$scriptFiles = @(
    "backend\scripts\create_admin.py",
    "backend\scripts\seed_data.py",
    "backend\scripts\backup_db.py"
)

foreach ($file in $scriptFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Tests
$testFiles = @(
    "backend\tests\__init__.py",
    "backend\tests\conftest.py"
)

foreach ($file in $testFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# ========== FRONTEND (CustomTkinter) ==========
Write-Host "Creando estructura del Frontend (CustomTkinter)..." -ForegroundColor Yellow

# Crear directorios del frontend
$frontendDirs = @(
    "frontend\app\views",
    "frontend\app\components",
    "frontend\app\utils",
    "frontend\app\services",
    "frontend\app\models",
    "frontend\app\assets\images",
    "frontend\app\assets\icons",
    "frontend\config"
)

foreach ($dir in $frontendDirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# Archivos raiz del frontend
$frontendRootFiles = @(
    "frontend\requirements.txt",
    "frontend\.env",
    "frontend\.gitignore",
    "frontend\README.md",
    "frontend\main.py"
)

foreach ($file in $frontendRootFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# App
$frontendAppFiles = @(
    "frontend\app\__init__.py",
    "frontend\app\app.py"
)

foreach ($file in $frontendAppFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Config
$configFiles = @(
    "frontend\config\__init__.py",
    "frontend\config\settings.py",
    "frontend\config\theme.py"
)

foreach ($file in $configFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Views (Ventanas principales)
$viewFiles = @(
    "frontend\app\views\__init__.py",
    "frontend\app\views\login_view.py",
    "frontend\app\views\main_window.py",
    "frontend\app\views\dashboard_view.py",
    "frontend\app\views\reservations_view.py",
    "frontend\app\views\rooms_view.py",
    "frontend\app\views\guests_view.py",
    "frontend\app\views\payments_view.py",
    "frontend\app\views\maintenance_view.py",
    "frontend\app\views\inventory_view.py",
    "frontend\app\views\reports_view.py",
    "frontend\app\views\users_view.py",
    "frontend\app\views\settings_view.py"
)

foreach ($file in $viewFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Components (Componentes reutilizables)
$componentFiles = @(
    "frontend\app\components\__init__.py",
    "frontend\app\components\sidebar.py",
    "frontend\app\components\topbar.py",
    "frontend\app\components\data_table.py",
    "frontend\app\components\form_builder.py",
    "frontend\app\components\dialog.py",
    "frontend\app\components\calendar_widget.py",
    "frontend\app\components\search_bar.py",
    "frontend\app\components\notification.py",
    "frontend\app\components\loading.py"
)

foreach ($file in $componentFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Utils
$utilFiles = @(
    "frontend\app\utils\__init__.py",
    "frontend\app\utils\validators.py",
    "frontend\app\utils\formatters.py",
    "frontend\app\utils\constants.py",
    "frontend\app\utils\helpers.py"
)

foreach ($file in $utilFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Services (Comunicacion con API)
$frontendServiceFiles = @(
    "frontend\app\services\__init__.py",
    "frontend\app\services\api_client.py",
    "frontend\app\services\auth_service.py",
    "frontend\app\services\reservation_service.py",
    "frontend\app\services\room_service.py",
    "frontend\app\services\guest_service.py",
    "frontend\app\services\payment_service.py",
    "frontend\app\services\maintenance_service.py",
    "frontend\app\services\inventory_service.py",
    "frontend\app\services\report_service.py"
)

foreach ($file in $frontendServiceFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# Models (Modelos de datos del frontend)
$frontendModelFiles = @(
    "frontend\app\models\__init__.py",
    "frontend\app\models\user.py",
    "frontend\app\models\reservation.py",
    "frontend\app\models\room.py"
)

foreach ($file in $frontendModelFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# ========== DOCUMENTACION ==========
Write-Host "Creando documentacion..." -ForegroundColor Yellow

# Crear directorios de documentacion
$docDirs = @(
    "docs\api",
    "docs\database",
    "docs\user_manual"
)

foreach ($dir in $docDirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$docFiles = @(
    "docs\README.md",
    "docs\INSTALL.md",
    "docs\API.md",
    "docs\DATABASE.md"
)

foreach ($file in $docFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# ========== ARCHIVOS RAIZ DEL PROYECTO ==========
$rootFiles = @(
    "README.md",
    ".gitignore",
    "docker-compose.yml",
    "setup.py"
)

foreach ($file in $rootFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

Write-Host ""
Write-Host "[OK] Estructura del proyecto SIGHO creada exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "Estructura:" -ForegroundColor Cyan
Write-Host "   sigho-system\"
Write-Host "   |-- backend\          (FastAPI + SQLite3)"
Write-Host "   |-- frontend\         (CustomTkinter)"
Write-Host "   |-- docs\             (Documentacion)"
Write-Host "   `-- README.md"
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Cyan
Write-Host "   1. cd sigho-system\backend && pip install -r requirements.txt"
Write-Host "   2. cd ..\frontend && pip install -r requirements.txt"
Write-Host "   3. Configurar variables de entorno (.env)"
Write-Host "   4. Iniciar el backend: python backend\main.py"
Write-Host "   5. Iniciar el frontend: python frontend\main.py"
Write-Host ""
