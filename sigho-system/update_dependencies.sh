#!/bin/bash

# Script para actualizar dependencias del SIGHO en Linux

echo "================================================"
echo "🔄 Actualizando Dependencias del Sistema SIGHO"
echo "================================================"
echo ""

# ========== BACKEND ==========
echo "📦 Actualizando Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    exit 1
fi

source venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
deactivate

echo "✅ Backend actualizado"
echo ""

cd ..

# ========== FRONTEND ==========
echo "🖥️  Actualizando Frontend..."
cd frontend

if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    exit 1
fi

source venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
deactivate

echo "✅ Frontend actualizado"
echo ""

cd ..

echo "================================================"
echo "✅ Todas las dependencias actualizadas"
echo "================================================"