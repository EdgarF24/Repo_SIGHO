# 🏨 SIGHO - Sistema Integrado de Gestión Hotelera

Sistema completo de gestión hotelera desarrollado con **FastAPI** (Backend) y **CustomTkinter** (Frontend), utilizando **SQLite3** como base de datos.

## 📋 Características Principales

### Backend (FastAPI + SQLite3)
- ✅ API REST completa con FastAPI
- ✅ Base de datos SQLite3 embebida
- ✅ Autenticación JWT con roles de usuario
- ✅ Gestión completa de reservas (check-in, check-out, cancelaciones)
- ✅ Control de habitaciones y disponibilidad
- ✅ Gestión de huéspedes
- ✅ Sistema de pagos multi-moneda (VES, USD, EUR)
- ✅ Mantenimiento preventivo y correctivo
- ✅ Control de inventario con movimientos
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Sistema de reportes avanzados

### Frontend (CustomTkinter)
- ✅ Interfaz gráfica moderna con CustomTkinter
- ✅ Temas claro/oscuro
- ✅ Sidebar con navegación intuitiva
- ✅ Dashboard con métricas en tiempo real
- ✅ Gestión visual de reservas, habitaciones y huéspedes
- ✅ Sistema de búsqueda y filtros
- ✅ Tablas de datos interactivas
- ✅ Control de acceso basado en roles

## 🏗️ Arquitectura del Sistema

```
sigho-system/
├── backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── core/           # Configuración y seguridad
│   │   ├── database/       # Sesión y base de datos
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   └── services/       # Lógica de negocio
│   ├── main.py             # Aplicación principal
│   └── requirements.txt    # Dependencias
│
├── frontend/               # Frontend CustomTkinter
│   ├── app/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── services/       # Servicios de API
│   │   └── views/          # Vistas de la aplicación
│   ├── config/             # Configuración
│   ├── main.py             # Aplicación principal
│   └── requirements.txt    # Dependencias
│
└── docs/                   # Documentación
```

## 🚀 Instalación y Configuración

### Requisitos
- Python 3.12+
- pip

### 1. Clonar el Repositorio

```bash
# Primero crear la estructura usando el script
# Linux/Mac:
bash crear_estructura.sh

# Windows PowerShell:
.\crear_estructura.ps1
```

### 2. Configurar el Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows PowerShell:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu configuración

# Iniciar el backend
python main.py
```

El backend estará disponible en: `http://127.0.0.1:8000`

Documentación API: `http://127.0.0.1:8000/docs`

### 3. Configurar el Frontend

```bash
cd frontend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows PowerShell:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el frontend
python main.py
```

## 🚀 Inicio Rápido con Scripts

### Windows (PowerShell)

```powershell
# Instalación
.\install_sigho.ps1

# Iniciar sistema completo
.\start_sigho.ps1
```

### Linux/Mac (Bash)

```bash
# Instalación
./install_sigho.sh

# Iniciar sistema completo
./start_sigho.sh
```

## 👥 Usuarios por Defecto

El sistema crea automáticamente estos usuarios de prueba:

| Usuario | Contraseña | Rol | Permisos |
|---------|-----------|-----|----------|
| admin | admin123 | Administrador | Acceso total |
| gerente | gerente123 | Gerente | Gestión completa |
| recepcion | recepcion123 | Recepcionista | Reservas, huéspedes, pagos |
| mantenimiento | manten123 | Mantenimiento | Gestión de mantenimiento |
| inventario | inventario123 | Inventario | Gestión de inventario |

## 📊 Módulos del Sistema

### 1. Dashboard
- Estadísticas en tiempo real
- Tasa de ocupación
- Ingresos del día/mes
- Check-ins y check-outs pendientes
- Alertas de mantenimiento e inventario

### 2. Gestión de Habitaciones
- CRUD de habitaciones
- Tipos de habitación con precios
- Estados (disponible, ocupada, limpieza, mantenimiento)
- Verificación de disponibilidad
- Gestión por pisos

### 3. Gestión de Reservas
- Crear, editar y cancelar reservas
- Check-in y check-out
- Código de confirmación único
- Cálculo automático de precios
- Multi-moneda (VES, USD, EUR)
- Búsqueda avanzada

### 4. Gestión de Huéspedes
- Registro de huéspedes
- Historial de reservas
- Información de contacto
- Búsqueda por documento, nombre, email

### 5. Gestión de Pagos
- Múltiples métodos de pago
- Multi-moneda
- Control de balance
- Historial de pagos
- Reembolsos

### 6. Mantenimiento
- Solicitudes de mantenimiento
- Preventivo y correctivo
- Asignación a técnicos
- Seguimiento de costos
- Prioridades (baja, media, alta, urgente)

### 7. Inventario
- Control de stock
- Movimientos (entradas/salidas)
- Alertas de stock bajo
- Categorías
- Valorización

### 8. Reportes
- Reporte de ocupación
- Reporte de ingresos
- Reporte de reservas
- Reporte de mantenimiento
- Reporte de inventario
- Exportación de datos

### 9. Usuarios
- Gestión de usuarios del sistema
- Roles y permisos
- Control de acceso

## 🔐 Seguridad

- Autenticación JWT
- Contraseñas hasheadas con bcrypt
- Control de acceso basado en roles
- Validación de entrada con Pydantic
- CORS configurado

## 📡 API Endpoints

### Autenticación
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Usuario actual
- `POST /api/auth/logout` - Logout

### Habitaciones
- `GET /api/rooms/` - Listar habitaciones
- `GET /api/rooms/{id}` - Obtener habitación
- `POST /api/rooms/` - Crear habitación
- `PUT /api/rooms/{id}` - Actualizar habitación
- `DELETE /api/rooms/{id}` - Eliminar habitación
- `POST /api/rooms/check-availability` - Verificar disponibilidad

### Reservas
- `GET /api/reservations/` - Listar reservas
- `GET /api/reservations/{id}` - Obtener reserva
- `POST /api/reservations/` - Crear reserva
- `PUT /api/reservations/{id}` - Actualizar reserva
- `POST /api/reservations/{id}/check-in` - Check-in
- `POST /api/reservations/{id}/check-out` - Check-out
- `POST /api/reservations/{id}/cancel` - Cancelar

### Dashboard
- `GET /api/dashboard/overview` - Resumen general
- `GET /api/dashboard/occupancy-rate` - Tasa de ocupación
- `GET /api/dashboard/revenue-by-period` - Ingresos

Ver documentación completa en: `http://127.0.0.1:8000/docs`

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM
- **SQLite3** - Base de datos
- **Pydantic** - Validación de datos
- **python-jose** - JWT
- **passlib** - Hashing de contraseñas
- **uvicorn** - Servidor ASGI

### Frontend
- **CustomTkinter** - Framework GUI moderno
- **requests** - Cliente HTTP
- **Pillow** - Procesamiento de imágenes

## 👨‍💻 Equipo de Desarrollo

- **Edgar Fermenio** - Backend
- **Andrés Sosa** - Frontend
- **Lino Gouveia** - Base de Datos
- **Santiago Mendez** - Tester
- **Santiago Martin** - Tester

## 📝 Metodología

Desarrollo basado en **Modelo en Cascada**:
1. Análisis de Requerimientos
2. Diseño del Sistema
3. Implementación
4. Pruebas
5. Despliegue
6. Mantenimiento

## 📄 Licencia

Este proyecto fue desarrollado como proyecto académico para la gestión hotelera en Venezuela.

## 🤝 Contribuciones

Este es un proyecto académico. Para consultas o sugerencias, contactar al equipo de desarrollo.

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema:
- Email: info@hotelsigho.com
- Teléfono: +58 424 1234567

---

**SIGHO** - Sistema Integrado de Gestión Hotelera © 2024