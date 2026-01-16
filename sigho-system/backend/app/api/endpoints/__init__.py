"""
Inicialización de endpoints de la API
"""
from . import (
    auth,
    users,
    amenities,
    room_types,
    rooms,
    reservations,
    guests,
    payments,
    maintenance,
    inventory,
    reports,
    dashboard,
    invoices
)

__all__ = [
    "auth",
    "users",
    "amenities",
    "room_types",
    "rooms",
    "reservations",
    "guests",
    "payments",
    "maintenance",
    "inventory",
    "reports",
    "dashboard",
    "invoices"
]
