#!/bin/bash

# Script para limpiar archivos temporales del SIGHO en Linux

echo "================================================"
echo "🧹 Limpieza del Sistema SIGHO"
echo "================================================"
echo ""

read -p "¿Qué desea limpiar? 
1) Solo archivos temporales y cache
2) También eliminar entornos virtuales
3) Limpieza completa (incluye base de datos)
Opción (1-3): " option

case $option in
    1)
        echo ""
        echo "🧹 Limpiando archivos temporales..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
        find . -type f -name "*.pyc" -delete 2>/dev/null
        find . -type f -name "*.pyo" -delete 2>/dev/null
        find . -type f -name "*.log" -delete 2>/dev/null
        find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
        find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
        echo "✅ Archivos temporales eliminados"
        ;;
    
    2)
        echo ""
        echo "🧹 Limpiando archivos temporales y entornos virtuales..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
        find . -type f -name "*.pyc" -delete 2>/dev/null
        find . -type f -name "*.pyo" -delete 2>/dev/null
        find . -type f -name "*.log" -delete 2>/dev/null
        find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
        find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
        
        rm -rf backend/venv 2>/dev/null
        rm -rf frontend/venv 2>/dev/null
        
        echo "✅ Archivos temporales y entornos virtuales eliminados"
        echo ""
        echo "⚠️  Necesitará ejecutar ./install_sigho.sh nuevamente"
        ;;
    
    3)
        echo ""
        read -p "⚠️  ADVERTENCIA: Esto eliminará TODA la base de datos y configuraciones. ¿Continuar? (s/n): " confirm
        if [[ $confirm == [sS] ]]; then
            echo ""
            echo "🧹 Realizando limpieza completa..."
            
            # Archivos temporales
            find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
            find . -type f -name "*.pyc" -delete 2>/dev/null
            find . -type f -name "*.pyo" -delete 2>/dev/null
            find . -type f -name "*.log" -delete 2>/dev/null
            find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
            find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
            
            # Entornos virtuales
            rm -rf backend/venv 2>/dev/null
            rm -rf frontend/venv 2>/dev/null
            
            # Base de datos
            rm -f backend/sigho.db 2>/dev/null
            rm -f backend/sigho.db-* 2>/dev/null
            
            # Sesión
            rm -f frontend/.session 2>/dev/null
            
            echo "✅ Limpieza completa realizada"
            echo ""
            echo "⚠️  El sistema ha sido reiniciado completamente"
            echo "   Ejecute ./install_sigho.sh para reinstalar"
        else
            echo "❌ Limpieza cancelada"
        fi
        ;;
    
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "================================================"