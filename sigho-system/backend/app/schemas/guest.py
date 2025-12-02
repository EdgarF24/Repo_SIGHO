"""
Schemas de Huésped (Pydantic)
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime


class GuestBase(BaseModel):
    """Schema base de huésped"""
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    id_type: str = Field(..., min_length=2, max_length=20)  # CI, Pasaporte, RIF
    id_number: str = Field(..., min_length=5, max_length=50)
    email: Optional[EmailStr] = None
    phone: str = Field(..., min_length=7, max_length=20)
    phone_alternative: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: str = Field("Venezuela", max_length=100)
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class GuestCreate(GuestBase):
    """Schema para crear huésped"""
    pass


class GuestUpdate(BaseModel):
    """Schema para actualizar huésped"""
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=7, max_length=20)
    phone_alternative: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class GuestResponse(GuestBase):
    """Schema de respuesta de huésped"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class GuestSearch(BaseModel):
    """Schema para buscar huéspedes"""
    query: str = Field(..., min_length=2)  # Buscar por nombre, documento, email, teléfono