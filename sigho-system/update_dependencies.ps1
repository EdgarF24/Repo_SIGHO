# Script de Actualizacion de Dependencias - SIGHO
# PowerShell Script para Windows

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Actualizacion de Dependencias - SIGHO" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Backend
Write-Host "Actualizando dependencias del Backend..." -ForegroundColor Yellow
Set-Location backend

if (Test-Path "venv") {
    & "venv\Scripts\Activate.ps1"
    pip install --upgrade -r requirements.txt
    deactivate
    Write-Host "[OK] Backend actualizado" -ForegroundColor Green
}
else {
    Write-Host "[ERROR] Entorno virtual del backend no encontrado" -ForegroundColor Red
}

Set-Location ..
Write-Host ""

# Frontend
Write-Host "Actualizando dependencias del Frontend..." -ForegroundColor Yellow
Set-Location frontend

if (Test-Path "venv") {
    & "venv\Scripts\Activate.ps1"
    pip install --upgrade -r requirements.txt
    deactivate
    Write-Host "[OK] Frontend actualizado" -ForegroundColor Green
}
else {
    Write-Host "[ERROR] Entorno virtual del frontend no encontrado" -ForegroundColor Red
}

Set-Location ..
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "[OK] Actualizacion completada" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
