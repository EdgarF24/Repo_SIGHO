# 🐧 Guía de Instalación y Uso - SIGHO para Linux

## 📋 Requisitos Previos

### 1. Instalar Python 3.8+

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk

# Fedora/RHEL
sudo dnf install python3 python3-pip python3-tkinter

# Arch Linux
sudo pacman -S python python-pip tk
```

### 2. Verificar Instalación

```bash
python3 --version
# Debe mostrar Python 3.8 o superior
```

## 🚀 Instalación Rápida

### Paso 1: Crear la Estructura del Proyecto

```bash
# Crear y ejecutar el script de estructura
bash create_structure.sh
cd sigho-system
```

### Paso 2: Dar Permisos de Ejecución a los Scripts

```bash
chmod +x install_sigho.sh
chmod +x start_sigho.sh
chmod +x backend/start_backend.sh
chmod +x frontend/start_frontend.sh
chmod +x update_dependencies.sh
chmod +x clean.sh
```

### Paso 3: Instalar el Sistema

```bash
./install_sigho.sh
```

Este script:
- ✅ Crea entornos virtuales para backend y frontend
- ✅ Instala todas las dependencias necesarias
- ✅ Configura el archivo .env
- ✅ Prepara el sistema para su uso

## 🎮 Uso del Sistema

### Opción 1: Iniciar Todo el Sistema (Recomendado)

```bash
./start_sigho.sh
```

Este script inicia automáticamente:
- Backend en http://127.0.0.1:8000
- Frontend (interfaz gráfica)

Para detener ambos servicios: **Ctrl+C**

### Opción 2: Iniciar Servicios Por Separado

#### Terminal 1 - Backend:
```bash
cd backend
./start_backend.sh
```

#### Terminal 2 - Frontend:
```bash
cd frontend
./start_frontend.sh
```

### Opción 3: Iniciar Manualmente

#### Backend:
```bash
cd backend
source venv/bin/activate
python main.py
```

#### Frontend:
```bash
cd frontend
source venv/bin/activate
python main.py
```

## 📊 Acceso al Sistema

### Interfaz Gráfica (Frontend)
Se abre automáticamente al ejecutar el frontend

### Credenciales por Defecto:
- **Usuario:** `admin`
- **Contraseña:** `admin123`

### API REST (Backend)
- **URL:** http://127.0.0.1:8000
- **Documentación:** http://127.0.0.1:8000/docs
- **Swagger UI:** http://127.0.0.1:8000/redoc

## 🔧 Mantenimiento

### Actualizar Dependencias

```bash
./update_dependencies.sh
```

### Limpiar Archivos Temporales

```bash
./clean.sh
# Seleccione la opción deseada:
# 1 - Solo cache y temporales
# 2 - También entornos virtuales
# 3 - Limpieza completa (incluye BD)
```

### Ver Logs en Tiempo Real

```bash
# Backend
tail -f backend.log

# Frontend
tail -f frontend.log
```

### Reiniciar Base de Datos

```bash
cd backend
source venv/bin/activate
rm sigho.db
python main.py
# La base de datos se recreará con datos de prueba
```

## 🐛 Solución de Problemas

### Error: "No module named 'tkinter'"

```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Error: "Permission denied" al ejecutar scripts

```bash
chmod +x *.sh
chmod +x backend/*.sh
chmod +x frontend/*.sh
```

### Error: "Backend no responde"

```bash
# Verificar que el puerto 8000 esté libre
sudo netstat -tulpn | grep 8000

# Si está ocupado, detener el proceso
sudo kill -9 $(sudo lsof -t -i:8000)

# Reiniciar backend
cd backend
./start_backend.sh
```

### Error: "ModuleNotFoundError"

```bash
# Reinstalar dependencias
cd backend
source venv/bin/activate
pip install -r requirements.txt

cd ../frontend
source venv/bin/activate
pip install -r requirements.txt
```

### Problemas con Display en SSH

Si está conectado por SSH sin X11 forwarding:

```bash
# Opción 1: Habilitar X11 forwarding
ssh -X usuario@servidor

# Opción 2: Usar solo el backend
cd backend
./start_backend.sh
# Acceder desde navegador: http://IP_SERVIDOR:8000/docs
```

## 📦 Estructura de Directorios

```
sigho-system/
├── install_sigho.sh           # Script de instalación
├── start_sigho.sh             # Iniciar sistema completo
├── update_dependencies.sh     # Actualizar dependencias
├── clean.sh                   # Limpiar archivos
├── backend/
│   ├── venv/                  # Entorno virtual
│   ├── start_backend.sh       # Iniciar backend
│   ├── main.py               # App principal
│   └── sigho.db              # Base de datos
├── frontend/
│   ├── venv/                  # Entorno virtual
│   ├── start_frontend.sh      # Iniciar frontend
│   └── main.py               # App principal
├── backend.log                # Log del backend
└── frontend.log               # Log del frontend
```

## 🔐 Seguridad

### Cambiar SECRET_KEY en Producción

```bash
cd backend
nano .env

# Cambiar esta línea:
SECRET_KEY=tu_nueva_clave_secreta_muy_segura_y_larga
```

### Crear Nuevo Usuario Administrador

```bash
cd backend
source venv/bin/activate
python scripts/create_admin.py
```

## 🌐 Despliegue en Servidor

### Usando systemd (Servicio del Sistema)

1. Crear archivo de servicio para Backend:

```bash
sudo nano /etc/systemd/system/sigho-backend.service
```

```ini
[Unit]
Description=SIGHO Backend Service
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/ruta/a/sigho-system/backend
Environment="PATH=/ruta/a/sigho-system/backend/venv/bin"
ExecStart=/ruta/a/sigho-system/backend/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Activar servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable sigho-backend
sudo systemctl start sigho-backend
sudo systemctl status sigho-backend
```

## 📞 Soporte

Para problemas o consultas:
- Email: info@hotelsigho.com
- Documentación: http://127.0.0.1:8000/docs

---

**SIGHO** - Sistema Integrado de Gestión Hotelera © 2024