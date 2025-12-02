"""
Configuración del Frontend - SIGHO
CustomTkinter + FastAPI Backend
"""
import os
from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "app" / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
ICONS_DIR = ASSETS_DIR / "icons"

# API Backend
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
API_TIMEOUT = 30  # segundos

# Aplicación
APP_NAME = "SIGHO - Sistema Integrado de Gestión Hotelera"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 1200
MIN_WINDOW_HEIGHT = 700

# Tema
DEFAULT_THEME = "dark"  # "dark" o "light"
ACCENT_COLOR = "#1f6aa5"

# Sesión
SESSION_FILE = BASE_DIR / ".session"
TOKEN_KEY = "access_token"
USER_KEY = "user_data"

# Formato de fechas
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT = "%d/%m/%Y"
DISPLAY_DATETIME_FORMAT = "%d/%m/%Y %H:%M"

# Monedas
CURRENCIES = ["VES", "USD", "EUR"]
DEFAULT_CURRENCY = "USD"

# Paginación
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100

# Validación
MIN_PASSWORD_LENGTH = 6
MIN_USERNAME_LENGTH = 3

# Estados de habitación
ROOM_STATUS_COLORS = {
    "available": "#2ecc71",
    "occupied": "#e74c3c",
    "cleaning": "#f39c12",
    "maintenance": "#9b59b6",
    "out_of_service": "#34495e"
}

# Estados de reserva
RESERVATION_STATUS_COLORS = {
    "pending": "#f39c12",
    "confirmed": "#3498db",
    "checked_in": "#2ecc71",
    "checked_out": "#95a5a6",
    "cancelled": "#e74c3c",
    "no_show": "#34495e"
}

# Prioridades de mantenimiento
MAINTENANCE_PRIORITY_COLORS = {
    "low": "#95a5a6",
    "medium": "#3498db",
    "high": "#f39c12",
    "urgent": "#e74c3c"
}