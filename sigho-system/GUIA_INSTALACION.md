# 🏨 SIGHO - Guía de Instalación para Desarrolladores

Esta guía te llevará paso a paso para instalar y ejecutar el Sistema Integrado de Gestión Hotelera (SIGHO) en tu máquina local.

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

| Software | Versión Mínima | Descarga |
|----------|----------------|----------|
| Python | 3.12+ | [python.org](https://www.python.org/downloads/) |
| Git | 2.40+ | [git-scm.com](https://git-scm.com/downloads) |
| pip | 23.0+ | Incluido con Python |

### Verificar instalaciones

Abre PowerShell o CMD y ejecuta:

```powershell
python --version
# Debe mostrar: Python 3.12.x o superior

git --version
# Debe mostrar: git version 2.x.x

pip --version
# Debe mostrar: pip 23.x.x
```

---

## 🚀 Instalación Paso a Paso

### Paso 1: Clonar el Repositorio

```powershell
# Navegar a la carpeta donde quieres instalar el proyecto
cd C:\Users\TuUsuario\Documents

# Clonar el repositorio
git clone https://github.com/EdgarF24/Repo_SIGHO.git

# Entrar a la carpeta del proyecto
cd Repo_SIGHO\sigho-system
```

---

### Paso 2: Configurar el Backend

```powershell
# Entrar a la carpeta del backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (PowerShell)
.\venv\Scripts\Activate.ps1

# Si usas CMD en lugar de PowerShell:
# .\venv\Scripts\activate.bat

# Instalar dependencias
pip install -r requirements.txt
```

#### Configurar variables de entorno

```powershell
# Copiar archivo de ejemplo
Copy-Item .env.example .env

# Editar el archivo .env con tus configuraciones (opcional)
notepad .env
```

El archivo `.env` contiene:
```env
# Configuración del servidor
HOST=127.0.0.1
PORT=8000

# Clave secreta JWT (cambiar en producción)
SECRET_KEY=tu_clave_secreta_aqui

# Base de datos
DATABASE_URL=sqlite:///./sigho.db
```

---

### Paso 3: Configurar el Frontend

```powershell
# Volver a la raíz del proyecto
cd ..

# Entrar a la carpeta del frontend
cd frontend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

---

### Paso 4: Iniciar la Base de Datos

El sistema utiliza SQLite3, que se crea automáticamente al iniciar el backend por primera vez. No necesitas instalar nada adicional.

---

## ▶️ Ejecutar el Sistema

### Opción A: Usando el Script de Inicio (Recomendado)

Desde la raíz del proyecto (`sigho-system`):

```powershell
.\start_sigho.ps1
```

Esto iniciará automáticamente tanto el backend como el frontend.

---

### Opción B: Inicio Manual

#### Terminal 1 - Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

Deberías ver:
```
[OK] Servidor iniciado en http://127.0.0.1:8000
[DOCS] Documentacion API: http://127.0.0.1:8000/docs
```

#### Terminal 2 - Frontend

```powershell
cd frontend
.\venv\Scripts\Activate.ps1
python main.py
```

Se abrirá la interfaz gráfica de SIGHO.

---

## 🔐 Credenciales de Acceso

El sistema viene con usuarios predeterminados:

| Usuario | Contraseña | Rol | Permisos |
|---------|-----------|-----|----------|
| `admin` | `admin123` | Administrador | Acceso total |
| `gerente` | `gerente123` | Gerente | Gestión completa |
| `recepcion` | `recepcion123` | Recepcionista | Reservas, huéspedes, pagos |
| `mantenimiento` | `manten123` | Mantenimiento | Gestión de mantenimiento |
| `inventario` | `inventario123` | Inventario | Gestión de inventario |

---

## 📡 Endpoints de la API

Una vez el backend esté corriendo:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **API Base**: http://127.0.0.1:8000/api

---

## 🔧 Comandos Útiles

### Actualizar dependencias

```powershell
.\update_dependencies.ps1
```

### Limpiar archivos temporales

```powershell
.\clean.ps1
```

### Ejecutar pruebas

```powershell
.\test.ps1
```

### Resetear contraseña de admin

```powershell
python reset_admin_password.py
```

---

## 📁 Estructura del Proyecto

```
sigho-system/
├── backend/                 # API REST (FastAPI)
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── core/           # Configuración y seguridad
│   │   ├── database/       # Sesión de BD
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   └── services/       # Lógica de negocio
│   ├── main.py             # Punto de entrada
│   └── requirements.txt    # Dependencias
│
├── frontend/               # Interfaz Gráfica (CustomTkinter)
│   ├── app/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── services/       # Servicios de API
│   │   └── views/          # Vistas de la aplicación
│   ├── config/             # Configuración de temas
│   ├── main.py             # Punto de entrada
│   └── requirements.txt    # Dependencias
│
├── docs/                   # Documentación
├── scripts/                # Scripts de configuración
└── README.md               # Documentación principal
```

---

## ❓ Solución de Problemas Comunes

### Error: "python no se reconoce como comando"

**Solución**: Asegúrate de que Python esté en el PATH del sistema.

1. Busca "Variables de entorno" en Windows
2. Edita la variable `Path`
3. Agrega la ruta de Python (ej: `C:\Python312\`)

---

### Error: "No se puede ejecutar scripts" en PowerShell

**Solución**: Cambiar la política de ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Error: "ModuleNotFoundError"

**Solución**: Asegúrate de tener el entorno virtual activado:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### El frontend no conecta con el backend

**Solución**: Verifica que el backend esté corriendo en el puerto 8000:

1. Abre http://127.0.0.1:8000/docs en tu navegador
2. Si no carga, revisa la terminal del backend por errores

---

### La base de datos está vacía

**Solución**: Los datos iniciales se crean automáticamente. Si necesitas repoblar:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python populate_db.py
```

---

## 👨‍💻 Desarrollo

### Agregar nuevas dependencias

```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
pip install nueva-libreria
pip freeze > requirements.txt

# Frontend
cd frontend
.\venv\Scripts\Activate.ps1
pip install nueva-libreria
pip freeze > requirements.txt
```

### Crear una nueva vista

1. Crea un archivo en `frontend/app/views/nueva_vista.py`
2. Importa en `frontend/app/views/__init__.py`
3. Agrega al sidebar en `frontend/app/components/sidebar.py`

### Crear un nuevo endpoint

1. Crea el modelo en `backend/app/models/`
2. Crea el schema en `backend/app/schemas/`
3. Crea el endpoint en `backend/app/api/endpoints/`
4. Registra en `backend/app/api/endpoints/__init__.py`

---

## 📞 Soporte

Si tienes problemas con la instalación:

1. Revisa la sección de "Solución de Problemas"
2. Abre un Issue en GitHub: https://github.com/EdgarF24/Repo_SIGHO/issues
3. Contacta al equipo de desarrollo

---

## 📄 Licencia

Proyecto académico desarrollado para la gestión hotelera en Venezuela.

---

**SIGHO** - Sistema Integrado de Gestión Hotelera © 2024
