#!/bin/bash

# Script para crear la estructura del Sistema Integrado de Gestión Hotelera (SIGHO)
# Arquitectura: FastAPI Backend + CustomTkinter Frontend + SQLite3
# Python 3.12

echo "🏨 Creando estructura del proyecto SIGHO..."

# Crear directorio raíz
mkdir -p sigho-system
cd sigho-system

# ========== BACKEND (FastAPI + SQLite3) ==========
echo "📁 Creando estructura del Backend (FastAPI)..."

mkdir -p backend/{app/{api/{endpoints,dependencies},core,models,schemas,services,database},tests,scripts}

# Archivos raíz del backend
touch backend/requirements.txt
touch backend/.env
touch backend/.gitignore
touch backend/README.md
touch backend/main.py

# Core
touch backend/app/__init__.py
touch backend/app/core/__init__.py
touch backend/app/core/config.py
touch backend/app/core/security.py

# Database
touch backend/app/database/__init__.py
touch backend/app/database/session.py
touch backend/app/database/base.py
touch backend/app/database/init_db.py

# Models (SQLAlchemy con SQLite3)
touch backend/app/models/__init__.py
touch backend/app/models/user.py
touch backend/app/models/room.py
touch backend/app/models/room_type.py
touch backend/app/models/reservation.py
touch backend/app/models/guest.py
touch backend/app/models/payment.py
touch backend/app/models/maintenance.py
touch backend/app/models/inventory.py
touch backend/app/models/inventory_movement.py

# Schemas (Pydantic)
touch backend/app/schemas/__init__.py
touch backend/app/schemas/user.py
touch backend/app/schemas/room.py
touch backend/app/schemas/reservation.py
touch backend/app/schemas/guest.py
touch backend/app/schemas/payment.py
touch backend/app/schemas/maintenance.py
touch backend/app/schemas/inventory.py
touch backend/app/schemas/report.py

# Services (Lógica de negocio)
touch backend/app/services/__init__.py
touch backend/app/services/auth_service.py
touch backend/app/services/user_service.py
touch backend/app/services/room_service.py
touch backend/app/services/reservation_service.py
touch backend/app/services/guest_service.py
touch backend/app/services/payment_service.py
touch backend/app/services/maintenance_service.py
touch backend/app/services/inventory_service.py
touch backend/app/services/report_service.py

# API Endpoints
touch backend/app/api/__init__.py
touch backend/app/api/dependencies/__init__.py
touch backend/app/api/dependencies/auth.py
touch backend/app/api/endpoints/__init__.py
touch backend/app/api/endpoints/auth.py
touch backend/app/api/endpoints/users.py
touch backend/app/api/endpoints/rooms.py
touch backend/app/api/endpoints/reservations.py
touch backend/app/api/endpoints/guests.py
touch backend/app/api/endpoints/payments.py
touch backend/app/api/endpoints/maintenance.py
touch backend/app/api/endpoints/inventory.py
touch backend/app/api/endpoints/reports.py
touch backend/app/api/endpoints/dashboard.py

# Scripts útiles
touch backend/scripts/create_admin.py
touch backend/scripts/seed_data.py
touch backend/scripts/backup_db.py

# Tests
touch backend/tests/__init__.py
touch backend/tests/conftest.py

# ========== FRONTEND (CustomTkinter) ==========
echo "📁 Creando estructura del Frontend (CustomTkinter)..."

mkdir -p frontend/{app/{views,components,utils,services,models,assets/{images,icons}},config}

# Archivos raíz del frontend
touch frontend/requirements.txt
touch frontend/.env
touch frontend/.gitignore
touch frontend/README.md
touch frontend/main.py

# App
touch frontend/app/__init__.py
touch frontend/app/app.py

# Config
touch frontend/config/__init__.py
touch frontend/config/settings.py
touch frontend/config/theme.py

# Views (Ventanas principales)
touch frontend/app/views/__init__.py
touch frontend/app/views/login_view.py
touch frontend/app/views/main_window.py
touch frontend/app/views/dashboard_view.py
touch frontend/app/views/reservations_view.py
touch frontend/app/views/rooms_view.py
touch frontend/app/views/guests_view.py
touch frontend/app/views/payments_view.py
touch frontend/app/views/maintenance_view.py
touch frontend/app/views/inventory_view.py
touch frontend/app/views/reports_view.py
touch frontend/app/views/users_view.py
touch frontend/app/views/settings_view.py

# Components (Componentes reutilizables)
touch frontend/app/components/__init__.py
touch frontend/app/components/sidebar.py
touch frontend/app/components/topbar.py
touch frontend/app/components/data_table.py
touch frontend/app/components/form_builder.py
touch frontend/app/components/dialog.py
touch frontend/app/components/calendar_widget.py
touch frontend/app/components/search_bar.py
touch frontend/app/components/notification.py
touch frontend/app/components/loading.py

# Utils
touch frontend/app/utils/__init__.py
touch frontend/app/utils/validators.py
touch frontend/app/utils/formatters.py
touch frontend/app/utils/constants.py
touch frontend/app/utils/helpers.py

# Services (Comunicación con API)
touch frontend/app/services/__init__.py
touch frontend/app/services/api_client.py
touch frontend/app/services/auth_service.py
touch frontend/app/services/reservation_service.py
touch frontend/app/services/room_service.py
touch frontend/app/services/guest_service.py
touch frontend/app/services/payment_service.py
touch frontend/app/services/maintenance_service.py
touch frontend/app/services/inventory_service.py
touch frontend/app/services/report_service.py

# Models (Modelos de datos del frontend)
touch frontend/app/models/__init__.py
touch frontend/app/models/user.py
touch frontend/app/models/reservation.py
touch frontend/app/models/room.py

# ========== DOCUMENTACIÓN ==========
echo "📁 Creando documentación..."

mkdir -p docs/{api,database,user_manual}

touch docs/README.md
touch docs/INSTALL.md
touch docs/API.md
touch docs/DATABASE.md

# ========== ARCHIVOS RAÍZ DEL PROYECTO ==========
touch README.md
touch .gitignore
touch docker-compose.yml
touch setup.py

echo ""
echo "✅ Estructura del proyecto SIGHO creada exitosamente!"
echo ""
echo "📂 Estructura:"
echo "   sigho-system/"
echo "   ├── backend/          (FastAPI + SQLite3)"
echo "   ├── frontend/         (CustomTkinter)"
echo "   ├── docs/            (Documentación)"
echo "   └── README.md"
echo ""
echo "🚀 Próximos pasos:"
echo "   1. cd sigho-system/backend && pip install -r requirements.txt"
echo "   2. cd ../frontend && pip install -r requirements.txt"
echo "   3. Configurar variables de entorno (.env)"
echo "   4. Iniciar el backend: python backend/main.py"
echo "   5. Iniciar el frontend: python frontend/main.py"
echo ""