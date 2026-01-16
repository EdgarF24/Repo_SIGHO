"""
Schemas de Habitación y Tipo de Habitación (Pydantic)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.room import RoomStatus


# ========== ROOM TYPE ==========
class RoomTypeBase(BaseModel):
    """Schema base de tipo de habitación"""
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    capacity: int = Field(..., ge=1, le=10)
    base_price_ves: float = Field(..., ge=0)
    base_price_usd: float = Field(..., ge=0)
    base_price_eur: Optional[float] = Field(None, ge=0)
    has_wifi: bool = True
    has_tv: bool = True
    has_ac: bool = True
    has_minibar: bool = False
    has_balcony: bool = False
    has_kitchen: bool = False


class RoomTypeCreate(RoomTypeBase):
    """Schema para crear tipo de habitación"""
    pass


class RoomTypeUpdate(BaseModel):
    """Schema para actualizar tipo de habitación"""
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=1, le=10)
    base_price_ves: Optional[float] = Field(None, ge=0)
    base_price_usd: Optional[float] = Field(None, ge=0)
    base_price_eur: Optional[float] = Field(None, ge=0)
    has_wifi: Optional[bool] = None
    has_tv: Optional[bool] = None
    has_ac: Optional[bool] = None
    has_minibar: Optional[bool] = None
    has_balcony: Optional[bool] = None
    has_kitchen: Optional[bool] = None
    is_active: Optional[bool] = None


class RoomTypeResponse(RoomTypeBase):
    """Schema de respuesta de tipo de habitación"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RoomTypeInDB(RoomTypeResponse):
    """Schema de tipo de habitación en base de datos"""
    pass


# ========== ROOM ==========
class RoomBase(BaseModel):
    """Schema base de habitación"""
    room_number: str = Field(..., min_length=1, max_length=10)
    floor: int = Field(..., ge=1)
    room_type_id: int
    status: RoomStatus = RoomStatus.AVAILABLE
    notes: Optional[str] = None


class RoomCreate(RoomBase):
    """Schema para crear habitación"""
    pass


class RoomUpdate(BaseModel):
    """Schema para actualizar habitación"""
    status: Optional[RoomStatus] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class RoomStatusUpdate(BaseModel):
    """Schema para cambiar solo el estado de una habitación"""
    status: RoomStatus


class RoomResponse(RoomBase):
    """Schema de respuesta de habitación"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    room_type: RoomTypeResponse
    
    class Config:
        from_attributes = True


class RoomInDB(RoomResponse):
    """Schema de habitación en base de datos"""
    pass


# ========== AVAILABILITY ==========
class RoomAvailabilityQuery(BaseModel):
    """Schema para consultar disponibilidad"""
    check_in_date: str  # formato: YYYY-MM-DD
    check_out_date: str  # formato: YYYY-MM-DD
    num_adults: int = Field(1, ge=1)
    num_children: int = Field(0, ge=0)


class RoomAvailabilityResponse(BaseModel):
    """Schema de respuesta de disponibilidad"""
    room_type_id: int
    room_type_name: str
    available_rooms: int
    price_per_night_ves: float
    price_per_night_usd: float
    price_per_night_eur: Optional[float]
    total_nights: int
    total_price_ves: float
    total_price_usd: float
    total_price_eur: Optional[float]