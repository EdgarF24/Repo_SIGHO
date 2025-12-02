#!/bin/bash

# Script para iniciar Backend y Frontend del SIGHO simultáneamente en Linux

echo "================================================"
echo "🏨 SIGHO - Sistema Integrado de Gestión Hotelera"
echo "================================================"
echo ""
echo "Iniciando sistema completo..."
echo ""

# Verificar estructura
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Directorios backend o frontend no encontrados"
    exit 1
fi

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

trap cleanup SIGINT SIGTERM

# ========== BACKEND ==========
echo "🚀 Iniciando Backend..."
cd backend

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual del backend no encontrado"
    echo "Por favor ejecute primero: ./install_sigho.sh"
    exit 1
fi

# Iniciar backend en segundo plano
source venv/bin/activate
python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
deactivate

# Esperar a que el backend esté listo
echo "⏳ Esperando a que el backend esté listo..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "✅ Backend iniciado correctamente (PID: $BACKEND_PID)"
        break
    fi
    
    if [ $i -eq 30 ]; then
        echo "❌ Error: El backend no responde después de 30 segundos"
        echo "Revise el archivo backend.log para más detalles"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    
    sleep 1
done

cd ..

# ========== FRONTEND ==========
echo ""
echo "🖥️  Iniciando Frontend..."
sleep 2

cd frontend

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual del frontend no encontrado"
    echo "Por favor ejecute primero: ./install_sigho.sh"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Iniciar frontend en segundo plano
source venv/bin/activate
python main.py > ../frontend.log 2>&1 &
FRONTEND_PID=$!
deactivate

cd ..

echo ""
echo "================================================"
echo "✅ Sistema SIGHO iniciado correctamente"
echo "================================================"
echo ""
echo "📊 Estado de los servicios:"
echo "   Backend:  http://127.0.0.1:8000 (PID: $BACKEND_PID)"
echo "   Frontend: Interfaz gráfica (PID: $FRONTEND_PID)"
echo ""
echo "📚 Documentación API: http://127.0.0.1:8000/docs"
echo ""
echo "📝 Credenciales por defecto:"
echo "   Usuario: admin"
echo "   Contraseña: admin123"
echo ""
echo "📄 Logs:"
echo "   Backend:  ./backend.log"
echo "   Frontend: ./frontend.log"
echo ""
echo "🛑 Presione Ctrl+C para detener todos los servicios"
echo "================================================"
echo ""

# Mantener el script corriendo
wait $BACKEND_PID $FRONTEND_PID