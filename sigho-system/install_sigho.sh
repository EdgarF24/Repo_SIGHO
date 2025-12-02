#!/bin/bash

# Script de Instalación del Sistema SIGHO para Linux
# Sistema Integrado de Gestión Hotelera

set -e  # Detener en caso de error

echo "================================================"
echo "🏨 SIGHO - Sistema Integrado de Gestión Hotelera"
echo "================================================"
echo ""
echo "Instalando el sistema completo..."
echo ""

# Verificar Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "Por favor instale Python 3.8 o superior:"
    echo "sudo apt update && sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python versión: $PYTHON_VERSION detectado"
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Directorios backend o frontend no encontrados"
    echo "Por favor ejecute primero el script de estructura create_structure.sh"
    exit 1
fi

# ========== BACKEND ==========
echo "📦 Instalando Backend..."
echo ""

cd backend

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual del backend..."
    python3 -m venv venv
else
    echo "Entorno virtual del backend ya existe"
fi

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "Instalando dependencias del backend..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "Creando archivo de configuración .env..."
    cat > .env << 'EOF'
# Configuración del Backend - SIGHO

# Aplicación
APP_NAME=SIGHO - Sistema Integrado de Gestión Hotelera
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
EOF
    echo "✅ Archivo .env creado"
fi

deactivate
cd ..

echo "✅ Backend instalado correctamente"
echo ""

# ========== FRONTEND ==========
echo "🖥️  Instalando Frontend..."
echo ""

cd frontend

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual del frontend..."
    # CORRECCIÓN: Se usa 'venv' porque ya estamos dentro de la carpeta 'frontend'
    # Se añade --system-site-packages para usar python3-tk instalado en el sistema
    python3 -m venv venv --system-site-packages
else
    echo "Entorno virtual del frontend ya existe"
fi

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "Instalando dependencias del frontend..."
pip install -r requirements.txt

deactivate
cd ..

echo "✅ Frontend instalado correctamente"
echo ""

# ========== FINALIZACIÓN ==========
echo "================================================"
echo "✅ ¡Instalación completada exitosamente!"
echo "================================================"
echo ""
echo "📝 Próximos pasos:"
echo ""
echo "1️⃣  Iniciar el Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo "   (El backend estará en http://127.0.0.1:8000)"
echo ""
echo "2️⃣  En otra terminal, iniciar el Frontend:"
echo "   cd frontend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3️⃣  Credenciales por defecto:"
echo "   Usuario: admin"
echo "   Contraseña: admin123"
echo ""
echo "📚 Documentación API: http://127.0.0.1:8000/docs"
echo ""
echo "================================================"