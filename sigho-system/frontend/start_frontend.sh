#!/bin/bash

# Script para iniciar el Frontend del SIGHO en Linux

echo "================================================"
echo "🖥️  Iniciando Frontend SIGHO"
echo "================================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py no encontrado"
    echo "Por favor ejecute este script desde el directorio frontend/"
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
if ! python -c "import customtkinter" &> /dev/null; then
    echo "❌ Error: CustomTkinter no está instalado"
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar que el backend está corriendo
echo ""
echo "🔍 Verificando conexión con el backend..."
if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
    echo "✅ Backend detectado en http://127.0.0.1:8000"
else
    echo "⚠️  Advertencia: No se puede conectar con el backend"
    echo "   Por favor asegúrese de que el backend esté ejecutándose"
    echo "   Puede iniciarlo con: cd backend && ./start_backend.sh"
    echo ""
    read -p "¿Desea continuar de todos modos? (s/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        deactivate
        exit 1
    fi
fi

echo ""
echo "✅ Entorno configurado correctamente"
echo ""
echo "🎨 Iniciando interfaz gráfica..."
echo ""
echo "📝 Credenciales por defecto:"
echo "   Usuario: admin"
echo "   Contraseña: admin123"
echo ""
echo "Presione Ctrl+C para cerrar la aplicación"
echo ""
echo "================================================"
echo ""

# Iniciar la aplicación
python main.py

# Desactivar entorno virtual al salir
deactivate