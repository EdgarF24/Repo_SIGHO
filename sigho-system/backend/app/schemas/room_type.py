"""
Schemas para Tipos de Habitación
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RoomTypeBase(BaseModel):
    """Schema base de Tipo de Habitación"""
    name: str = Field(..., max_length=50, description="Nombre del tipo de habitación")
    description: Optional[str] = Field(None, description="Descripción del tipo")
    capacity: int = Field(..., gt=0, description="Capacidad de personas")
    base_price_ves: float = Field(..., ge=0, description="Precio base en VES")
    base_price_usd: float = Field(..., ge=0, description="Precio base en USD")
    base_price_eur: Optional[float] = Field(None, ge=0, description="Precio base en EUR")
    is_active: bool = Field(True, description="Si el tipo está activo")


class RoomTypeCreate(RoomTypeBase):
    """Schema para crear Tipo de Habitación"""
    amenity_ids: List[int] = Field(default_factory=list, description="IDs de amenidades")


class RoomTypeUpdate(BaseModel):
    """Schema para actualizar Tipo de Habitación"""
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    base_price_ves: Optional[float] = Field(None, ge=0)
    base_price_usd: Optional[float] = Field(None, ge=0)
    base_price_eur: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None
    amenity_ids: Optional[List[int]] = Field(None, description="IDs de amenidades para actualizar")


class RoomTypeAmenityResponse(BaseModel):
    """Schema de amenidad en la respuesta de tipo de habitación"""
    id: int
    name: str
    category: str
    
    class Config:
        from_attributes = True


class RoomTypeResponse(RoomTypeBase):
    """Schema de respuesta de Tipo de Habitación"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    amenities: List[RoomTypeAmenityResponse] = Field(default_factory=list, description="Lista de amenidades")
    
    class Config:
        from_attributes = True


class RoomTypeInDB(RoomTypeResponse):
    """Schema de Tipo de Habitación en base de datos"""
    pass
