"""
Dependencias del core - Alias para mantener compatibilidad
"""
from app.api.dependencies.auth import (
    get_current_user,
    get_current_active_user,
    require_role,
    require_admin
)

__all__ = [
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "require_admin"
]
