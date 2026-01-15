# SIGHO - Documentación Técnica

## Sistema Integrado de Gestión Hotelera

**Versión:** 1.0.0  
**Fecha:** Diciembre 2025  
**Plataforma:** Windows  
**Python:** 3.12+

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Requisitos del Sistema](#3-requisitos-del-sistema)
4. [Instalación](#4-instalación)
5. [Estructura del Proyecto](#5-estructura-del-proyecto)
6. [Backend API](#6-backend-api)
7. [Frontend GUI](#7-frontend-gui)
8. [Base de Datos](#8-base-de-datos)
9. [Autenticación y Seguridad](#9-autenticación-y-seguridad)
10. [Guía de Desarrollo](#10-guía-de-desarrollo)
11. [API Reference](#11-api-reference)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Introducción

### 1.1 Descripción del Sistema

SIGHO es un sistema completo de gestión hotelera desarrollado en Python que combina:
- **Backend:** API REST construida con FastAPI
- **Frontend:** Interfaz gráfica usando CustomTkinter
- **Base de Datos:** SQLite3 para persistencia de datos

### 1.2 Características Principales

- Gestión de usuarios con roles y permisos
- Administración de habitaciones y tipos de habitación
- Sistema de reservas con códigos de confirmación
- Gestión de huéspedes y su información
- Procesamiento de pagos en múltiples monedas (VES, USD, EUR)
- Control de mantenimiento de habitaciones
- Inventario de suministros
- Generación de reportes
- Dashboard con estadísticas en tiempo real

---

## 2. Arquitectura del Sistema

### 2.1 Diagrama de Arquitectura

```
[Frontend CustomTkinter] <--HTTP--> [Backend FastAPI] <--> [SQLite Database]
         |                              |
    [Views/Components]            [Endpoints/Services]
                                        |
                                   [Models/Schemas]
```

### 2.2 Componentes Principales

#### Backend (FastAPI)
- **API REST:** endpoints para todas las operaciones CRUD
- **Autenticación:** JWT tokens para seguridad
- **ORM:** SQLAlchemy para mapeo objeto-relacional
- **Validación:** Pydantic para validación de datos
- **Documentación:** Swagger UI generada automáticamente

#### Frontend (CustomTkinter)
- **GUI moderna:** Interfaz gráfica con tema oscuro/claro
- **Vistas modulares:** Componentes reutilizables
- **Cliente API:** Comunicación HTTP con el backend
- **Gestión de sesión:** Persistencia de sesión de usuario

#### Base de Datos (SQLite3)
- **Tablas:** 11 tablas principales
- **Relaciones:** Claves foráneas y constraints
- **Índices:** Optimización de consultas frecuentes

---

## 3. Requisitos del Sistema

### 3.1 Hardware Mínimo
- **Procesador:** Intel Core i3 o equivalente
- **RAM:** 4 GB
- **Disco:** 500 MB libres
- **Pantalla:** 1366x768 mínimo

### 3.2 Software Requerido
- **OS:** Windows 10/11
- **Python:** 3.12.0 o superior
- **PowerShell:** 5.1 o superior (incluido en Windows)

### 3.3 Dependencias Python

#### Backend
```
fastapi==0.123.5
uvicorn==0.38.0
sqlalchemy==2.0.44
pydantic==2.12.5
pydantic-settings==2.12.0
python-jose==3.5.0
passlib==1.7.4
python-multipart==0.0.20
email-validator==2.3.0
bcrypt==5.0.0
```

#### Frontend
```
customtkinter==5.2.2
pillow==12.0.0
requests==2.32.5
python-dotenv==1.2.1
```

---

## 4. Instalación

### 4.1 Instalación Rápida

```powershell
# 1. Clonar/descargar el repositorio
cd C:\Users\tu_usuario\Documents\SIGHO\SIGHO-

# 2. Ejecutar script de instalación
cd sigho-system
.\install_sigho.ps1

# 3. Iniciar el sistema
.\start_sigho.ps1
```

### 4.2 Instalación Manual

#### Paso 1: Instalar Python 3.12
1. Descargar desde python.org
2. Marcar "Add Python to PATH"
3. Completar instalación

#### Paso 2: Configurar Backend
```powershell
cd backend
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Paso 3: Configurar Frontend
```powershell
cd ../frontend
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Paso 4: Iniciar Servicios
```powershell
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
python main.py

# Terminal 2 - Frontend
cd frontend
venv\Scripts\activate
python main.py
```

---

## 5. Estructura del Proyecto

```
sigho-system/
├── backend/                    # Aplicación FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints de la API
│   │   │   ├── endpoints/     # Controladores
│   │   │   └── dependencies/  # Dependencias compartidas
│   │   ├── core/              # Configuración central
│   │   ├── database/          # Setup de base de datos
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   └── services/          # Lógica de negocio
│   ├── tests/                 # Tests unitarios
│   ├── main.py               # Punto de entrada
│   └── requirements.txt       # Dependencias
│
├── frontend/                   # Aplicación CustomTkinter
│   ├── app/
│   │   ├── views/            # Vistas de la aplicación
│   │   ├── components/       # Componentes reutilizables
│   │   ├── services/         # Servicios (API client)
│   │   └── utils/            # Utilidades
│   ├── config/               # Configuración
│   ├── main.py              # Punto de entrada
│   └── requirements.txt      # Dependencias
│
├── docs/                       # Documentación
├── install_sigho.ps1          # Script de instalación
├── start_sigho.ps1            # Script de inicio
├── clean.ps1                  # Script de limpieza
└── README.md                  # Readme del proyecto
```

---

## 6. Backend API

### 6.1 Arquitectura del Backend

#### Capas de la Aplicación

1. **Capa de Presentación** (Endpoints)
   - Recibe requests HTTP
   - Valida entrada con Pydantic
   - Retorna responses JSON

2. **Capa de Negocio** (Services)
   - Lógica de negocio
   - Validaciones complejas
   - Orquestación de operaciones

3. **Capa de Datos** (Models)
   - Modelos SQLAlchemy
   - Operaciones CRUD
   - Relaciones entre entidades

### 6.2 Configuración

Archivo: `backend/app/core/config.py`

```python
class Settings(BaseSettings):
    APP_NAME: str = "SIGHO"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    DATABASE_URL: str = "sqlite:///./sigho.db"
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

### 6.3 Modelos de Datos

#### User Model
```python
class User(Base):
    __tablename__ = "users"
    
    id: int (PK)
    username: str (unique)
    email: str (unique)
    full_name: str
    hashed_password: str
    role: UserRole (enum)
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime
```

#### Room Model
```python
class Room(Base):
    __tablename__ = "rooms"
    
    id: int (PK)
    room_number: str (unique)
    floor: int
    room_type_id: int (FK -> room_types)
    status: RoomStatus (enum)
    is_active: bool
    notes: str
    created_at: datetime
    updated_at: datetime
```

#### Reservation Model
```python
class Reservation(Base):
    __tablename__ = "reservations"
    
    id: int (PK)
    confirmation_code: str (unique)
    guest_id: int (FK -> guests)
    room_id: int (FK -> rooms)
    check_in_date: date
    check_out_date: date
    num_adults: int
    num_children: int
    status: ReservationStatus (enum)
    currency: str
    price_per_night: float
    total_amount: float
    paid_amount: float
    is_paid: bool
    ...
```

### 6.4 Schemas Pydantic

Cada entidad tiene schemas para:
- **Base:** Campos comunes
- **Create:** Para crear nuevos registros
- **Update:** Para actualizar registros
- **Response:** Para retornar datos al cliente
- **InDB:** Representación en base de datos

Ejemplo:
```python
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool = True

class UserCreate(UserBase):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    hashed_password: str
```

### 6.5 Endpoints Principales

#### Autenticación
- `POST /api/auth/login` - Login de usuario
- `POST /api/auth/refresh` - Refrescar token
- `GET /api/auth/me` - Información del usuario actual

#### Usuarios
- `GET /api/users` - Listar usuarios
- `POST /api/users` - Crear usuario
- `GET /api/users/{id}` - Obtener usuario
- `PUT /api/users/{id}` - Actualizar usuario
- `DELETE /api/users/{id}` - Eliminar usuario

#### Habitaciones
- `GET /api/rooms` - Listar habitaciones
- `POST /api/rooms` - Crear habitación
- `GET /api/rooms/{id}` - Obtener habitación
- `PUT /api/rooms/{id}` - Actualizar habitación
- `GET /api/rooms/available` - Habitaciones disponibles

#### Reservas
- `GET /api/reservations` - Listar reservas
- `POST /api/reservations` - Crear reserva
- `GET /api/reservations/{id}` - Obtener reserva
- `PUT /api/reservations/{id}` - Actualizar reserva
- `POST /api/reservations/{id}/check-in` - Hacer check-in
- `POST /api/reservations/{id}/check-out` - Hacer check-out
- `POST /api/reservations/{id}/cancel` - Cancelar reserva

---

## 7. Frontend GUI

### 7.1 Estructura del Frontend

```
frontend/app/
├── views/              # Vistas principales
│   ├── login_view.py
│   ├── main_window.py
│   ├── dashboard_view.py
│   ├── reservations_view.py
│   ├── rooms_view.py
│   ├── guests_view.py
│   ├── payments_view.py
│   ├── maintenance_view.py
│   ├── inventory_view.py
│   ├── reports_view.py
│   ├── users_view.py
│   └── settings_view.py
│
├── components/         # Componentes reutilizables
│   ├── sidebar.py
│   ├── topbar.py
│   ├── data_table.py
│   └── dialog.py
│
├── services/          # Servicios
│   └── api_client.py
│
└── utils/             # Utilidades
    └── validators.py
```

### 7.2 Configuración del Theme

```python
# config/theme.py
COLORS = {
    "primary": "#1f538d",
    "secondary": "#14a085",
    "success": "#27ae60",
    "danger": "#c0392b",
    "warning": "#f39c12",
    "dark": "#2c3e50",
    "light": "#ecf0f1"
}
```

### 7.3 API Client

```python
class APIClient:
    BASE_URL = "http://127.0.0.1:8000"
    
    def __init__(self):
        self.token = None
    
    def login(self, username, password):
        response = requests.post(
            f"{self.BASE_URL}/api/auth/login",
            data={"username": username, "password": password}
        )
        self.token = response.json()["access_token"]
        return self.token
    
    def get(self, endpoint):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.get(
            f"{self.BASE_URL}{endpoint}",
            headers=headers
        )
```

---

## 8. Base de Datos

### 8.1 Esquema de la Base de Datos

#### Tablas Principales

1. **users** - Usuarios del sistema
2. **room_types** - Tipos de habitación
3. **rooms** - Habitaciones
4. **guests** - Huéspedes
5. **reservations** - Reservas
6. **payments** - Pagos
7. **maintenance** - Mantenimiento
8. **inventory** - Inventario
9. **inventory_movements** - Movimientos de inventario
10. **amenities** - Amenidades
11. **room_type_amenities** - Relación tipos-amenidades

### 8.2 Relaciones

```
users (1) ---> (*) reservations
users (1) ---> (*) payments
users (1) ---> (*) maintenance

room_types (1) ---> (*) rooms
room_types (*) <---> (*) amenities

rooms (1) ---> (*) reservations
rooms (1) ---> (*) maintenance

guests (1) ---> (*) reservations

reservations (1) ---> (*) payments

inventory (1) ---> (*) inventory_movements
```

### 8.3 Índices

```sql
CREATE INDEX ix_users_username ON users(username);
CREATE INDEX ix_users_email ON users(email);
CREATE INDEX ix_rooms_room_number ON rooms(room_number);
CREATE INDEX ix_reservations_confirmation_code ON reservations(confirmation_code);
CREATE INDEX ix_payments_payment_code ON payments(payment_code);
```

---

## 9. Autenticación y Seguridad

### 9.1 Sistema de Autenticación

- **Método:** JWT (JSON Web Tokens)
- **Algoritmo:** HS256
- **Expiración:** 30 minutos
- **Hash de contraseñas:** bcrypt

### 9.2 Roles de Usuario

```python
class UserRole(str, Enum):
    ADMIN = "admin"              # Acceso completo
    MANAGER = "manager"          # Gestión general
    RECEPTIONIST = "receptionist" # Reservas y huéspedes
    MAINTENANCE = "maintenance"   # Mantenimiento
    INVENTORY = "inventory"       # Inventario
    VIEWER = "viewer"            # Solo lectura
```

### 9.3 Flujo de Autenticación

1. Usuario envía credenciales a `/api/auth/login`
2. Backend valida credenciales
3. Backend genera JWT token
4. Frontend almacena token
5. Frontend incluye token en cada request subsecuente
6. Backend valida token en cada endpoint protegido

---

## 10. Guía de Desarrollo

### 10.1 Agregar un Nuevo Endpoint

1. **Crear Schema** (`app/schemas/`)
```python
class NewEntityBase(BaseModel):
    name: str
    description: str

class NewEntityCreate(NewEntityBase):
    pass

class NewEntityResponse(NewEntityBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

2. **Crear Model** (`app/models/`)
```python
class NewEntity(Base):
    __tablename__ = "new_entities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
```

3. **Crear Service** (`app/services/`)
```python
class NewEntityService:
    def get_all(db: Session):
        return db.query(NewEntity).all()
    
    def create(db: Session, data: NewEntityCreate):
        entity = NewEntity(**data.dict())
        db.add(entity)
        db.commit()
        return entity
```

4. **Crear Endpoint** (`app/api/endpoints/`)
```python
router = APIRouter()

@router.get("/", response_model=List[NewEntityResponse])
def list_entities(db: Session = Depends(get_db)):
    return NewEntityService.get_all(db)

@router.post("/", response_model=NewEntityResponse)
def create_entity(
    data: NewEntityCreate,
    db: Session = Depends(get_db)
):
    return NewEntityService.create(db, data)
```

5. **Registrar Router** (`main.py`)
```python
from app.api.endpoints import new_entity

app.include_router(
    new_entity.router,
    prefix="/api/new-entities",
    tags=["New Entities"]
)
```

### 10.2 Agregar una Nueva Vista

1. **Crear Vista** (`frontend/app/views/new_view.py`)
```python
class NewView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
    
    def create_widgets(self):
        # Crear interfaz
        pass
```

2. **Agregar al Menú** (`main_window.py`)
```python
self.menu_items = [
    # ...
    ("Nueva Vista", self.show_new_view, "icon.png")
]

def show_new_view(self):
    self.clear_content()
    view = NewView(self.content_frame)
    view.pack(fill="both", expand=True)
```

### 10.3 Testing

```python
# backend/tests/test_endpoints.py
def test_create_user():
    response = client.post(
        "/api/users",
        json={
            "username": "test",
            "email": "test@test.com",
            "full_name": "Test User",
            "password": "test123",
            "role": "viewer"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "test"
```

---

## 11. API Reference

### 11.1 Authentication Endpoints

#### POST /api/auth/login
Login de usuario.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 11.2 Users Endpoints

#### GET /api/users
Lista todos los usuarios.

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@hotel.com",
    "full_name": "Administrator",
    "role": "admin",
    "is_active": true,
    "created_at": "2025-12-03T10:00:00"
  }
]
```

### 11.3 Rooms Endpoints

#### GET /api/rooms/available
Lista habitaciones disponibles.

**Query Parameters:**
- `check_in`: Fecha de entrada (YYYY-MM-DD)
- `check_out`: Fecha de salida (YYYY-MM-DD)
- `num_adults`: Número de adultos
- `num_children`: Número de niños

**Response:**
```json
[
  {
    "room_type_id": 1,
    "room_type_name": "Doble",
    "available_rooms": 5,
    "price_per_night_usd": 40.0,
    "total_nights": 3,
    "total_price_usd": 120.0
  }
]
```

---

## 12. Troubleshooting

### 12.1 Problemas Comunes

#### Error: "Python no está instalado"
**Solución:** Instalar Python 3.12 y asegurarse de marcar "Add to PATH"

#### Error: "Module not found"
**Solución:**
```powershell
pip install -r requirements.txt
```

#### Error: "Puerto 8000 en uso"
**Solución:** Cambiar puerto en `backend/.env` o matar proceso:
```powershell
netstat -ano | findstr :8000
taskkill /PID [PID] /F
```

#### Error: "No se puede conectar al backend"
**Solución:** Verificar que el backend esté corriendo:
```powershell
Invoke-WebRequest http://127.0.0.1:8000/health
```

### 12.2 Logs

- **Backend logs:** Consola donde corre `python main.py`
- **Frontend logs:** Consola donde corre el frontend
- **Database:** `backend/sigho.db`
- **Session:** `frontend/.session`

### 12.3 Comandos Útiles

```powershell
# Verificar version de Python
python --version

# Listar dependencias instaladas
pip list

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Limpiar archivos temporales
.\clean.ps1

# Diagnosticar sistema
.\test.ps1
```

---

## Apéndices

### A. Variables de Entorno

**Backend (.env):**
```env
APP_NAME=SIGHO
APP_VERSION=1.0.0
DEBUG=True
HOST=127.0.0.1
PORT=8000
DATABASE_URL=sqlite:///./sigho.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### B. Estructura de Respuestas API

Todas las respuestas exitosas siguen el formato:
```json
{
  "data": {...},
  "message": "Success"
}
```

Errores:
```json
{
  "detail": "Error message"
}
```

### C. Códigos de Estado HTTP

- `200` OK - Operación exitosa
- `201` Created - Recurso creado
- `400` Bad Request - Datos inválidos
- `401` Unauthorized - No autenticado
- `403` Forbidden - Sin permisos
- `404` Not Found - Recurso no encontrado
- `500` Internal Server Error - Error del servidor

---

**Fin de Documentación Técnica**
