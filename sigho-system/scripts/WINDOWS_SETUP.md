# 🪟 Guía de Instalación y Uso - SIGHO para Windows

## 📋 Requisitos Previos

### 1. Instalar Python 3.8+

1. Descargar Python desde: https://www.python.org/downloads/
2. **IMPORTANTE**: Durante la instalación, marcar la casilla "Add Python to PATH"
3. Verificar instalación abriendo PowerShell y ejecutando:

```powershell
python --version
# Debe mostrar Python 3.8 o superior
```

### 2. Habilitar Ejecución de Scripts PowerShell (Primera vez)

Abrir PowerShell como **Administrador** y ejecutar:

```powershell
Set-ExecutionPolicy RemoteSigned
# Confirmar con "S" o "Y"
```

## 🚀 Instalación Rápida

### Paso 1: Crear la Estructura del Proyecto

```powershell
# Crear y ejecutar el script de estructura
.\crear_estructura.ps1
cd sigho-system
```

### Paso 2: Instalar el Sistema

```powershell
.\install_sigho.ps1
```

Este script:
- ✅ Crea entornos virtuales para backend y frontend
- ✅ Instala todas las dependencias necesarias
- ✅ Configura el archivo .env
- ✅ Prepara el sistema para su uso

## 🎮 Uso del Sistema

### Opción 1: Iniciar Todo el Sistema (Recomendado)

```powershell
.\start_sigho.ps1
```

Este script inicia automáticamente:
- Backend en http://127.0.0.1:8000
- Frontend (interfaz gráfica)

Para detener ambos servicios: **Ctrl+C**

### Opción 2: Iniciar Servicios Por Separado

#### PowerShell 1 - Backend:
```powershell
cd backend
.\start_backend.ps1
```

#### PowerShell 2 - Frontend:
```powershell
cd frontend
.\start_frontend.ps1
```

### Opción 3: Iniciar Manualmente

#### Backend:
```powershell
cd backend
venv\Scripts\activate
python main.py
```

#### Frontend:
```powershell
cd frontend
venv\Scripts\activate
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

```powershell
.\update_dependencies.ps1
```

### Limpiar Archivos Temporales

```powershell
.\clean.ps1
# Seleccione la opción deseada:
# 1 - Solo cache y temporales
# 2 - También entornos virtuales
# 3 - Limpieza completa (incluye BD)
```

### Ver Logs

```powershell
# Backend
Get-Content backend.log -Tail 50 -Wait

# Frontend
Get-Content frontend.log -Tail 50 -Wait
```

### Reiniciar Base de Datos

```powershell
cd backend
venv\Scripts\activate
Remove-Item sigho.db
python main.py
# La base de datos se recreará con datos de prueba
```

## 🐛 Solución de Problemas

### Error: "No se puede ejecutar scripts en este sistema"

**Solución:**
```powershell
# Opción 1 - Ejecutar con bypass temporal
PowerShell -ExecutionPolicy Bypass -File .\script.ps1

# Opción 2 - Cambiar política permanentemente (como Administrador)
Set-ExecutionPolicy RemoteSigned
```

### Error: "python no se reconoce como comando"

**Solución:**
1. Reinstalar Python desde https://www.python.org/downloads/
2. Marcar "Add Python to PATH" durante la instalación
3. Reiniciar PowerShell

### Error: "ModuleNotFoundError"

**Solución:**
```powershell
# Reinstalar dependencias
cd backend  # o frontend
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "Backend no responde"

**Solución:**
```powershell
# Verificar si el puerto 8000 está en uso
Get-NetTCPConnection -LocalPort 8000

# Detener el proceso (reemplazar PID con el ID del proceso)
Stop-Process -Id PID -Force

# Reiniciar backend
cd backend
.\start_backend.ps1
```

### Error: "Connection refused" en Frontend

**Solución:**
1. Verificar que el backend esté corriendo primero
2. Verificar que el backend esté en http://127.0.0.1:8000
3. Verificar firewall de Windows no bloquee el puerto 8000

### Problemas con tkinter

**Solución:**
1. Ir a "Configuración" > "Aplicaciones" > "Python"
2. Hacer clic en "Modificar"
3. Marcar "tcl/tk and IDLE"
4. Completar la modificación

### El puerto 8000 ya está en uso

**Solución:**
```powershell
# Abrir PowerShell como Administrador
# Ver qué proceso usa el puerto
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess

# Detener el proceso (reemplazar PID)
Stop-Process -Id PID -Force
```

## 📦 Estructura de Directorios

```
sigho-system\
├── install_sigho.ps1           # Script de instalación
├── start_sigho.ps1             # Iniciar sistema completo
├── update_dependencies.ps1     # Actualizar dependencias
├── clean.ps1                   # Limpiar archivos
├── backend\
│   ├── venv\                   # Entorno virtual
│   ├── start_backend.ps1       # Iniciar backend
│   ├── main.py                 # App principal
│   └── sigho.db                # Base de datos
├── frontend\
│   ├── venv\                   # Entorno virtual
│   ├── start_frontend.ps1      # Iniciar frontend
│   └── main.py                 # App principal
├── backend.log                 # Log del backend
└── frontend.log                # Log del frontend
```

## 🔐 Seguridad

### Cambiar SECRET_KEY en Producción

```powershell
cd backend
notepad .env

# Cambiar esta línea:
# SECRET_KEY=tu_nueva_clave_secreta_muy_segura_y_larga
```

### Crear Nuevo Usuario Administrador

```powershell
cd backend
venv\Scripts\activate
python scripts\create_admin.py
```

## 🌐 Despliegue como Servicio de Windows

### Usando NSSM (Non-Sucking Service Manager)

1. Descargar NSSM: https://nssm.cc/download

2. Instalar servicio para Backend:

```powershell
# Como Administrador
nssm install SIGHO-Backend "C:\ruta\a\python.exe" "C:\ruta\a\sigho-system\backend\main.py"
nssm set SIGHO-Backend AppDirectory "C:\ruta\a\sigho-system\backend"
nssm start SIGHO-Backend
```

3. Ver servicios instalados:

```powershell
Get-Service | Where-Object {$_.Name -like "SIGHO*"}
```

## 💡 Consejos de Uso

### Atajos de Teclado en PowerShell

- **Ctrl+C**: Detener proceso actual
- **Tab**: Autocompletar comandos
- **↑/↓**: Navegar historial de comandos
- **Ctrl+R**: Buscar en historial

### Crear Acceso Directo

1. Crear archivo `Iniciar SIGHO.bat`:

```batch
@echo off
cd /d C:\Users\ferme\Documents\SIGHO\sigho-system
powershell -ExecutionPolicy Bypass -File .\start_sigho.ps1
pause
```

2. Crear acceso directo en el escritorio a este archivo `.bat`

### Logs en Tiempo Real

```powershell
# Ver logs mientras se ejecuta
Get-Content .\backend.log -Wait -Tail 20
```

## 📞 Soporte

Para problemas o consultas:
- Email: info@hotelsigho.com
- Documentación: http://127.0.0.1:8000/docs

## 🔄 Diferencias con Linux

| Aspecto | Windows | Linux |
|---------|---------|-------|
| Scripts | `.ps1` (PowerShell) | `.sh` (Bash) |
| Activar venv | `venv\Scripts\activate` | `source venv/bin/activate` |
| Rutas | `C:\Users\...` | `/home/...` |
| Separador | `\` (backslash) | `/` (forward slash) |
| Puerto en uso | `Get-NetTCPConnection` | `lsof -i :8000` |
| Detener proceso | `Stop-Process` | `kill` |
| Python | `python` | `python3` |

---

**SIGHO** - Sistema Integrado de Gestión Hotelera © 2024
