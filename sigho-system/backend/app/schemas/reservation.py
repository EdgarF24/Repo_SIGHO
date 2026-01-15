"""
Schemas de Reserva (Pydantic)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from app.models.reservation import ReservationStatus


class ReservationBase(BaseModel):
    """Schema base de reserva"""
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    num_adults: int = Field(1, ge=1)
    num_children: int = Field(0, ge=0)
    currency: str = Field("VES", max_length=3)
    special_requests: Optional[str] = None


class ReservationCreate(ReservationBase):
    """Schema para crear reserva"""
    pass


class ReservationUpdate(BaseModel):
    """Schema para actualizar reserva"""
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    num_adults: Optional[int] = Field(None, ge=1)
    num_children: Optional[int] = Field(None, ge=0)
    status: Optional[ReservationStatus] = None
    special_requests: Optional[str] = None
    notes: Optional[str] = None


class ReservationResponse(ReservationBase):
    """Schema de respuesta de reserva"""
    id: int
    confirmation_code: str
    status: ReservationStatus
    price_per_night: float
    total_nights: int
    subtotal: float
    tax_percentage: float
    tax_amount: float
    total_amount: float
    paid_amount: float
    balance: float
    is_paid: bool
    actual_check_in: Optional[datetime] = None
    actual_check_out: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ReservationInDB(ReservationResponse):
    """Schema de reserva en base de datos"""
    pass


class ReservationCheckIn(BaseModel):
    """Schema para hacer check-in"""
    notes: Optional[str] = None


class ReservationCheckOut(BaseModel):
    """Schema para hacer check-out"""
    notes: Optional[str] = None


class ReservationCancel(BaseModel):
    """Schema para cancelar reserva"""
    cancellation_reason: str = Field(..., min_length=3)


class ReservationSearchFilters(BaseModel):
    """Filtros para buscar reservas"""
    status: Optional[ReservationStatus] = None
    check_in_date_from: Optional[date] = None
    check_in_date_to: Optional[date] = None
    guest_name: Optional[str] = None
    room_number: Optional[str] = None
    confirmation_code: Optional[str] = None
