#!/bin/bash

# Script para iniciar el Backend del SIGHO en Linux

echo "================================================"
echo "🚀 Iniciando Backend SIGHO"
echo "================================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py no encontrado"
    echo "Por favor ejecute este script desde el directorio backend/"
    exit 1
fi

# Verificar que existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    echo "Por favor ejecute primero: python3 -m venv venv"
    exit 1
fi

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source venv/bin/activate

# Verificar instalación
if ! python -c "import fastapi" &> /dev/null; then
    echo "❌ Error: FastAPI no está instalado"
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Entorno configurado correctamente"
echo ""
echo "🌐 Iniciando servidor FastAPI..."
echo "   - URL: http://127.0.0.1:8000"
echo "   - Docs: http://127.0.0.1:8000/docs"
echo ""
echo "Presione Ctrl+C para detener el servidor"
echo ""
echo "================================================"
echo ""

# Iniciar el servidor
python main.py

# Desactivar entorno virtual al salir
deactivate