"""
Schemas de la aplicación
"""
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse, UserInDB
from app.schemas.guest import GuestBase, GuestCreate, GuestUpdate, GuestResponse, GuestInDB
from app.schemas.room import RoomBase, RoomCreate, RoomUpdate, RoomResponse, RoomInDB
from app.schemas.room_type import (
    RoomTypeBase, RoomTypeCreate, RoomTypeUpdate, RoomTypeResponse, RoomTypeInDB
)
from app.schemas.reservation import (
    ReservationBase, ReservationCreate, ReservationUpdate, ReservationResponse, ReservationInDB
)
from app.schemas.payment import PaymentBase, PaymentCreate, PaymentUpdate, PaymentResponse, PaymentInDB
from app.schemas.maintenance import (
    MaintenanceBase, MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse, MaintenanceInDB
)
from app.schemas.inventory import (
    InventoryBase, InventoryCreate, InventoryUpdate, InventoryResponse, InventoryInDB
)
from app.schemas.amenity import AmenityBase, AmenityCreate, AmenityUpdate, AmenityResponse, AmenityInDB

__all__ = [
    "UserBase", "UserCreate", "UserUpdate", "UserResponse", "UserInDB",
    "GuestBase", "GuestCreate", "GuestUpdate", "GuestResponse", "GuestInDB",
    "RoomBase", "RoomCreate", "RoomUpdate", "RoomResponse", "RoomInDB",
    "RoomTypeBase", "RoomTypeCreate", "RoomTypeUpdate", "RoomTypeResponse", "RoomTypeInDB",
    "ReservationBase", "ReservationCreate", "ReservationUpdate", "ReservationResponse", "ReservationInDB",
    "PaymentBase", "PaymentCreate", "PaymentUpdate", "PaymentResponse", "PaymentInDB",
    "MaintenanceBase", "MaintenanceCreate", "MaintenanceUpdate", "MaintenanceResponse", "MaintenanceInDB",
    "InventoryBase", "InventoryCreate", "InventoryUpdate", "InventoryResponse", "InventoryInDB",
    "AmenityBase", "AmenityCreate", "AmenityUpdate", "AmenityResponse", "AmenityInDB",
]
