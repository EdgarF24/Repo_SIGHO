"""
Importar todos los modelos aquí para que Alembic los detecte
"""
from app.database.session import Base

# Importar todos los modelos
from app.models.user import User
from app.models.room_type import RoomType
from app.models.room import Room
from app.models.guest import Guest
from app.models.reservation import Reservation
from app.models.payment import Payment
from app.models.maintenance import Maintenance
from app.models.inventory import Inventory
from app.models.inventory_movement import InventoryMovement