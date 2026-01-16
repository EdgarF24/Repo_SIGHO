"""
Schemas de Factura (Pydantic)
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from app.models.invoice import InvoiceStatus, DocumentType


# ========== INVOICE ITEM ==========
class InvoiceItemBase(BaseModel):
    """Schema base de item de factura"""
    description: str = Field(..., min_length=1, max_length=500)
    quantity: float = Field(1, ge=0.01)
    unit_price: float = Field(..., ge=0)


class InvoiceItemCreate(InvoiceItemBase):
    """Schema para crear item de factura"""
    pass


class InvoiceItemResponse(InvoiceItemBase):
    """Schema de respuesta de item de factura"""
    id: int
    invoice_id: int
    subtotal: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== INVOICE ==========
class InvoiceBase(BaseModel):
    """Schema base de factura"""
    guest_document_type: DocumentType = DocumentType.V
    guest_document_number: str = Field(..., min_length=1, max_length=20)
    guest_name: str = Field(..., min_length=1, max_length=200)
    guest_address: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None
    currency: str = Field("USD", pattern="^(VES|USD|EUR)$")
    tax_percentage: float = Field(16.0, ge=0, le=100)
    notes: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    """Schema para crear factura"""
    reservation_id: Optional[int] = None
    guest_id: int
    items: List[InvoiceItemCreate] = []
    due_date: Optional[date] = None


class InvoiceUpdate(BaseModel):
    """Schema para actualizar factura"""
    guest_document_type: Optional[DocumentType] = None
    guest_document_number: Optional[str] = Field(None, min_length=1, max_length=20)
    guest_name: Optional[str] = Field(None, min_length=1, max_length=200)
    guest_address: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None
    tax_percentage: Optional[float] = Field(None, ge=0, le=100)
    notes: Optional[str] = None
    due_date: Optional[date] = None


class InvoiceResponse(InvoiceBase):
    """Schema de respuesta de factura"""
    id: int
    invoice_number: str
    reservation_id: Optional[int]
    guest_id: int
    created_by: int
    subtotal: float
    tax_amount: float
    total_amount: float
    paid_amount: float
    balance: float
    status: InvoiceStatus
    issue_date: Optional[datetime]
    due_date: Optional[date]
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[InvoiceItemResponse] = []
    
    class Config:
        from_attributes = True


class InvoiceListResponse(BaseModel):
    """Schema de respuesta para lista de facturas (sin items)"""
    id: int
    invoice_number: str
    reservation_id: Optional[int]
    guest_id: int
    guest_name: str
    guest_document_number: str
    currency: str
    subtotal: float
    tax_amount: float
    total_amount: float
    paid_amount: float
    balance: float
    status: InvoiceStatus
    issue_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== GENERATE FROM RESERVATION ==========
class InvoiceGenerateRequest(BaseModel):
    """Schema para generar factura desde reserva"""
    reservation_id: int
    include_payments: bool = True  # Si True, registra los pagos existentes
    guest_document_type: Optional[DocumentType] = None
    guest_document_number: Optional[str] = None
    guest_address: Optional[str] = None
    notes: Optional[str] = None


# ========== ADD ITEM ==========
class InvoiceAddItemRequest(BaseModel):
    """Schema para agregar item a factura existente"""
    description: str = Field(..., min_length=1, max_length=500)
    quantity: float = Field(1, ge=0.01)
    unit_price: float = Field(..., ge=0)


# ========== REGISTER PAYMENT ==========
class InvoicePaymentRequest(BaseModel):
    """Schema para registrar pago en factura"""
    amount: float = Field(..., gt=0)
