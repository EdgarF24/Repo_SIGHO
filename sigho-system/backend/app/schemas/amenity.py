"""
Schemas para Amenidades (Servicios)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AmenityBase(BaseModel):
    """Schema base de Amenidad"""
    name: str = Field(..., max_length=100, description="Nombre de la amenidad")
    description: Optional[str] = Field(None, description="Descripción detallada")
    icon: Optional[str] = Field(None, max_length=50, description="Nombre del icono")
    category: str = Field("básico", description="Categoría: básico, premium, lujo")
    is_active: bool = Field(True, description="Si la amenidad está activa")


class AmenityCreate(AmenityBase):
    """Schema para crear Amenidad"""
    pass


class AmenityUpdate(BaseModel):
    """Schema para actualizar Amenidad"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = None
    is_active: Optional[bool] = None


class AmenityResponse(AmenityBase):
    """Schema de respuesta de Amenidad"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AmenityInDB(AmenityResponse):
    """Schema de Amenidad en base de datos"""
    pass
