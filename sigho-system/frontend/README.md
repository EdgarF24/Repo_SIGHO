# SIGHO Frontend - Interfaz Gráfica

Frontend del Sistema Integrado de Gestión Hotelera desarrollado con **CustomTkinter**.

## 🚀 Características

- ✅ Interfaz gráfica moderna con CustomTkinter
- ✅ Temas claro/oscuro
- ✅ Diseño responsivo
- ✅ Navegación intuitiva con sidebar
- ✅ Tablas de datos interactivas
- ✅ Formularios de validación
- ✅ Conexión con API REST
- ✅ Manejo de sesiones

## 📁 Estructura del Proyecto

```
frontend/
├── app/
│   ├── components/       # Componentes reutilizables
│   │   ├── sidebar.py
│   │   ├── tables.py
│   │   └── forms.py
│   ├── services/         # Servicios de API
│   │   └── api_client.py
│   ├── views/            # Vistas de la aplicación
│   │   ├── login.py
│   │   ├── dashboard.py
│   │   ├── rooms.py
│   │   ├── reservations.py
│   │   └── ...
│   └── app.py            # Aplicación principal
├── config/               # Configuración
│   ├── settings.py
│   └── theme.py
├── main.py               # Punto de entrada
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

Crear archivo `.env` con:

```env
BACKEND_URL=http://127.0.0.1:8000
APP_NAME=SIGHO
DEBUG=True
```

### 4. Iniciar la aplicación

```bash
python main.py
```

## 🎨 Temas

La aplicación soporta dos temas:
- **Claro** - Tema por defecto
- **Oscuro** - Tema oscuro moderno

Cambiar tema desde: `Configuración > Apariencia`

## 📱 Módulos de la Aplicación

### 1. Login
- Autenticación de usuarios
- Recordar sesión
- Recuperación de contraseña

### 2. Dashboard
- Estadísticas en tiempo real
- Gráficos de ocupación
- Ingresos del día/mes
- Alertas y notificaciones

### 3. Habitaciones
- Lista de habitaciones
- Crear/Editar/Eliminar
- Cambiar estado
- Ver disponibilidad

### 4. Reservas
- Lista de reservas
- Crear nueva reserva
- Check-in/Check-out
- Cancelar reserva
- Búsqueda avanzada

### 5. Huéspedes
- Registro de huéspedes
- Historial de reservas
- Búsqueda por documento/nombre

### 6. Pagos
- Registrar pagos
- Historial de pagos
- Multi-moneda (VES, USD, EUR)

### 7. Mantenimiento
- Solicitudes de mantenimiento
- Asignar a técnicos
- Seguimiento de estado

### 8. Inventario
- Control de stock
- Movimientos
- Alertas de stock bajo

### 9. Reportes
- Generar reportes
- Filtros avanzados
- Exportar datos

### 10. Usuarios
- Gestión de usuarios
- Roles y permisos
- Crear/Editar/Eliminar

## 🔑 Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Administrador |
| gerente | gerente123 | Gerente |
| recepcion | recepcion123 | Recepcionista |

## 🎯 Componentes Principales

### Sidebar
Navegación lateral con menú de módulos y usuario actual.

### Tables
Tablas interactivas con ordenamiento, filtrado y paginación.

### Forms
Formularios con validación y mensajes de error.

### API Client
Cliente HTTP para comunicación con el backend.

## 📦 Dependencias Principales

- **CustomTkinter** - Framework GUI moderno
- **Pillow** - Procesamiento de imágenes
- **requests** - Cliente HTTP
- **python-dotenv** - Variables de entorno

## 🔐 Seguridad

- Almacenamiento seguro de tokens
- Cierre de sesión automático
- Validación de permisos por rol
- Encriptación de datos sensibles

## 🐛 Solución de Problemas

### Error de conexión con el backend
```bash
# Verificar que el backend esté corriendo
# URL por defecto: http://127.0.0.1:8000
```

### Error de importación de CustomTkinter
```bash
pip install --upgrade customtkinter
```

### Problemas de visualización
```bash
# Verificar la versión de Python (>= 3.12)
python --version
```

## 📝 Desarrollo

### Agregar nueva vista

1. Crear archivo en `app/views/nueva_vista.py`
2. Importar en `app/app.py`
3. Agregar al sidebar
4. Implementar lógica de la vista

### Agregar nuevo componente

1. Crear archivo en `app/components/nuevo_componente.py`
2. Extender de `customtkinter.CTkFrame`
3. Implementar interfaz
4. Usar en las vistas necesarias

## 📄 Licencia

Proyecto académico - SIGHO © 2024

## 🤝 Equipo

- **Edgar Fermenio** - Backend
- **Andrés Sosa** - Frontend
- **Lino Gouveia** - Base de Datos
- **Santiago Mendez** - Tester
- **Santiago Martin** - Tester
