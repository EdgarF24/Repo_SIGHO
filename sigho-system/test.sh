
echo "🔍 Diagnóstico del Sistema SIGHO"
echo "================================="
echo ""

echo "1️⃣ Verificando Backend..."
if curl -s http://127.0.0.1:8000/health > /dev/null; then
    echo "✅ Backend respondiendo"
else
    echo "❌ Backend NO responde"
    exit 1
fi

echo ""
echo "2️⃣ Probando Dashboard..."
DASH_RESPONSE=$(curl -s http://127.0.0.1:8000/api/dashboard/overview)
echo "Respuesta del Dashboard:"
echo "$DASH_RESPONSE" | head -20

if echo "$DASH_RESPONSE" | grep -q "rooms"; then
    echo "✅ Dashboard funcionando"
else
    echo "❌ Dashboard con problemas"
    echo ""
    echo "Ver error completo:"
    echo "$DASH_RESPONSE"
fi

echo ""
echo "3️⃣ Verificando Base de Datos..."
cd backend
if [ -f "sigho.db" ]; then
    echo "✅ Archivo sigho.db existe"
    echo "Tamaño: $(du -h sigho.db | cut -f1)"
    
    if command -v sqlite3 &> /dev/null; then
        echo ""
        echo "Contenido de la BD:"
        echo "- Usuarios: $(sqlite3 sigho.db 'SELECT COUNT(*) FROM users;')"
        echo "- Habitaciones: $(sqlite3 sigho.db 'SELECT COUNT(*) FROM rooms;')"
        echo "- Tipos Habitación: $(sqlite3 sigho.db 'SELECT COUNT(*) FROM room_types;')"
    else
        echo "⚠️  sqlite3 no instalado. Instalar con: sudo apt install sqlite3"
    fi
else
    echo "❌ sigho.db NO existe"
fi

echo ""
echo "4️⃣ Últimos errores del backend:"
cd ..
if [ -f "backend.log" ]; then
    echo "Últimas 10 líneas con ERROR:"
    grep -i "error" backend.log | tail -10
else
    echo "No hay archivo backend.log"
fi

echo ""
echo "================================="
echo "✅ Diagnóstico completado"
ENDSCRIPT
