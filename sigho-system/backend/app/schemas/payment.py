"""
Schemas de Pago (Pydantic)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.payment import PaymentMethod, PaymentStatus


class PaymentBase(BaseModel):
    """Schema base de pago"""
    reservation_id: int
    amount: float = Field(..., gt=0)
    currency: str = Field(..., max_length=3)
    payment_method: PaymentMethod
    reference_number: Optional[str] = Field(None, max_length=100)
    bank_name: Optional[str] = Field(None, max_length=100)
    account_number: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    """Schema para crear pago"""
    pass


class PaymentUpdate(BaseModel):
    """Schema para actualizar pago"""
    status: Optional[PaymentStatus] = None
    notes: Optional[str] = None


class PaymentResponse(PaymentBase):
    """Schema de respuesta de pago"""
    id: int
    payment_code: str
    status: PaymentStatus
    processed_by: int
    payment_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PaymentInDB(PaymentResponse):
    """Schema de pago en base de datos"""
    pass