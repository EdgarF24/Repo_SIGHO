# SIGHO Backend - API REST

Backend del Sistema Integrado de Gestión Hotelera desarrollado con **FastAPI** y **SQLite3**.

## 🚀 Características

- ✅ API REST completa con FastAPI
- ✅ Base de datos SQLite3 embebida
- ✅ Autenticación JWT con roles de usuario
- ✅ Documentación automática con Swagger UI
- ✅ Validación de datos con Pydantic
- ✅ ORM con SQLAlchemy
- ✅ Migraciones de base de datos
- ✅ Tests unitarios y de integración

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── api/              # Endpoints REST
│   │   └── endpoints/    # Routers por módulo
│   ├── core/             # Configuración y seguridad
│   ├── database/         # Base de datos y sesión
│   ├── models/           # Modelos SQLAlchemy
│   ├── schemas/          # Schemas Pydantic
│   └── services/         # Lógica de negocio
├── scripts/              # Scripts de utilidad
├── tests/                # Tests
├── main.py               # Aplicación principal
├── requirements.txt      # Dependencias
└── .env                  # Variables de entorno
```

## 🛠️ Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tu configuración
```

### 4. Iniciar el servidor

```bash
python main.py
# o
uvicorn main:app --reload
```

El servidor estará disponible en: `http://127.0.0.1:8000`

Documentación API: `http://127.0.0.1:8000/docs`

## 📡 Endpoints Principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Usuario actual
- `POST /api/auth/logout` - Cerrar sesión

### Habitaciones
- `GET /api/rooms/` - Listar habitaciones
- `POST /api/rooms/` - Crear habitación
- `PUT /api/rooms/{id}` - Actualizar habitación
- `DELETE /api/rooms/{id}` - Eliminar habitación

### Reservas
- `GET /api/reservations/` - Listar reservas
- `POST /api/reservations/` - Crear reserva
- `POST /api/reservations/{id}/check-in` - Check-in
- `POST /api/reservations/{id}/check-out` - Check-out

### Dashboard
- `GET /api/dashboard/overview` - Resumen general
- `GET /api/dashboard/occupancy-rate` - Tasa de ocupación
- `GET /api/dashboard/revenue-by-period` - Ingresos

Ver documentación completa en `/docs`

## 🧪 Tests

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_auth.py
```

## 📦 Dependencias Principales

- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM
- **Pydantic** - Validación de datos
- **python-jose** - JWT
- **passlib** - Hashing de contraseñas
- **uvicorn** - Servidor ASGI

## 🔐 Seguridad

- Autenticación JWT
- Contraseñas hasheadas con bcrypt
- Control de acceso basado en roles
- Validación de entrada con Pydantic
- CORS configurado

## 🗄️ Base de Datos

El sistema utiliza SQLite3 como base de datos embebida. La base de datos se crea automáticamente al iniciar la aplicación.

### Modelos principales:
- User - Usuarios del sistema
- Room - Habitaciones
- Reservation - Reservas
- Guest - Huéspedes
- Payment - Pagos
- Maintenance - Mantenimiento
- Inventory - Inventario

## 👥 Usuarios por Defecto

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Administrador |
| gerente | gerente123 | Gerente |
| recepcion | recepcion123 | Recepcionista |

## 📝 Scripts Útiles

```bash
# Crear usuario administrador
python scripts/create_admin.py

# Poblar base de datos con datos de prueba
python scripts/seed_data.py

# Backup de base de datos
python scripts/backup_db.py
```

## 🐳 Docker

```bash
# Construir imagen
docker build -t sigho-backend .

# Ejecutar contenedor
docker run -p 8000:8000 sigho-backend
```

## 📄 Licencia

Proyecto académico - SIGHO © 2024
