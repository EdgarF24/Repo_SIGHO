# Script para limpiar archivos temporales del SIGHO en Windows
# PowerShell Script

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Limpieza del Sistema SIGHO" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Que desea limpiar?" -ForegroundColor Yellow
Write-Host "1) Solo archivos temporales y cache"
Write-Host "2) Tambien eliminar entornos virtuales"
Write-Host "3) Limpieza completa (incluye base de datos)"
Write-Host ""

$option = Read-Host "Opcion (1-3)"

switch ($option) {
    "1" {
        Write-Host ""
        Write-Host "Limpiando archivos temporales..." -ForegroundColor Yellow
        
        # Eliminar __pycache__
        Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        
        # Eliminar archivos .pyc y .pyo
        Get-ChildItem -Path . -Recurse -File -Include "*.pyc", "*.pyo" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
        
        # Eliminar archivos .log
        Get-ChildItem -Path . -Recurse -File -Filter "*.log" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
        
        # Eliminar .pytest_cache
        Get-ChildItem -Path . -Recurse -Directory -Filter ".pytest_cache" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        
        # Eliminar .egg-info
        Get-ChildItem -Path . -Recurse -Directory -Filter "*.egg-info" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        
        Write-Host "[OK] Archivos temporales eliminados" -ForegroundColor Green
    }
    
    "2" {
        Write-Host ""
        Write-Host "Limpiando archivos temporales y entornos virtuales..." -ForegroundColor Yellow
        
        # Eliminar archivos temporales
        Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Path . -Recurse -File -Include "*.pyc", "*.pyo" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Path . -Recurse -File -Filter "*.log" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Path . -Recurse -Directory -Filter ".pytest_cache" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Path . -Recurse -Directory -Filter "*.egg-info" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        
        # Eliminar entornos virtuales
        if (Test-Path "backend\venv") {
            Remove-Item -Path "backend\venv" -Recurse -Force -ErrorAction SilentlyContinue
        }
        if (Test-Path "frontend\venv") {
            Remove-Item -Path "frontend\venv" -Recurse -Force -ErrorAction SilentlyContinue
        }
        
        Write-Host "[OK] Archivos temporales y entornos virtuales eliminados" -ForegroundColor Green
        Write-Host ""
        Write-Host "[ADVERTENCIA] Necesitara ejecutar .\install_sigho.ps1 nuevamente" -ForegroundColor Yellow
    }
    
    "3" {
        Write-Host ""
        $confirm = Read-Host "[ADVERTENCIA] Esto eliminara TODA la base de datos y configuraciones. Continuar? (s/n)"
        
        if ($confirm -eq "s" -or $confirm -eq "S") {
            Write-Host ""
            Write-Host "Realizando limpieza completa..." -ForegroundColor Yellow
            
            # Eliminar archivos temporales
            Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            Get-ChildItem -Path . -Recurse -File -Include "*.pyc", "*.pyo" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
            Get-ChildItem -Path . -Recurse -File -Filter "*.log" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
            Get-ChildItem -Path . -Recurse -Directory -Filter ".pytest_cache" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            Get-ChildItem -Path . -Recurse -Directory -Filter "*.egg-info" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            
            # Eliminar entornos virtuales
            if (Test-Path "backend\venv") {
                Remove-Item -Path "backend\venv" -Recurse -Force -ErrorAction SilentlyContinue
            }
            if (Test-Path "frontend\venv") {
                Remove-Item -Path "frontend\venv" -Recurse -Force -ErrorAction SilentlyContinue
            }
            
            # Eliminar base de datos
            if (Test-Path "backend\sigho.db") {
                Remove-Item -Path "backend\sigho.db" -Force -ErrorAction SilentlyContinue
            }
            Get-ChildItem -Path "backend" -Filter "sigho.db-*" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
            
            # Eliminar sesion
            if (Test-Path "frontend\.session") {
                Remove-Item -Path "frontend\.session" -Force -ErrorAction SilentlyContinue
            }
            
            Write-Host "[OK] Limpieza completa realizada" -ForegroundColor Green
            Write-Host ""
            Write-Host "[ADVERTENCIA] El sistema ha sido reiniciado completamente" -ForegroundColor Yellow
            Write-Host "   Ejecute .\install_sigho.ps1 para reinstalar" -ForegroundColor Yellow
        }
        else {
            Write-Host "[CANCELADO] Limpieza cancelada" -ForegroundColor Red
        }
    }
    
    default {
        Write-Host "[ERROR] Opcion invalida" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
