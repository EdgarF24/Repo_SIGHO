"""
Modelo de Factura y Items de Factura
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
import enum


class InvoiceStatus(str, enum.Enum):
    """Estados de una factura"""
    DRAFT = "draft"           # Borrador
    ISSUED = "issued"         # Emitida
    PAID = "paid"             # Pagada
    CANCELLED = "cancelled"   # Cancelada
    VOID = "void"             # Anulada


class DocumentType(str, enum.Enum):
    """Tipos de documento de identificación"""
    V = "V"  # Venezolano
    E = "E"  # Extranjero
    J = "J"  # Jurídico (empresa)
    G = "G"  # Gobierno
    P = "P"  # Pasaporte


class Invoice(Base):
    """Modelo de Factura"""
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(30), unique=True, nullable=False, index=True)  # FAC-YYYYMMDD-XXXX
    
    # Relaciones
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=True)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Información fiscal del cliente
    guest_document_type = Column(Enum(DocumentType), default=DocumentType.V, nullable=False)
    guest_document_number = Column(String(20), nullable=False)
    guest_name = Column(String(200), nullable=False)
    guest_address = Column(Text, nullable=True)
    guest_phone = Column(String(30), nullable=True)
    guest_email = Column(String(100), nullable=True)
    
    # Montos
    currency = Column(String(3), nullable=False, default="USD")  # VES, USD, EUR
    subtotal = Column(Float, nullable=False, default=0.0)
    tax_percentage = Column(Float, nullable=False, default=16.0)  # IVA 16%
    tax_amount = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    paid_amount = Column(Float, nullable=False, default=0.0)
    balance = Column(Float, nullable=False, default=0.0)
    
    # Estado
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, nullable=False)
    issue_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(Date, nullable=True)
    
    # Notas
    notes = Column(Text, nullable=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reservation = relationship("Reservation", backref="invoices")
    guest = relationship("Guest", backref="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Invoice {self.invoice_number} - {self.status}>"
    
    def calculate_totals(self):
        """Calcula los totales basándose en los items"""
        self.subtotal = sum(item.subtotal for item in self.items)
        self.tax_amount = self.subtotal * (self.tax_percentage / 100)
        self.total_amount = self.subtotal + self.tax_amount
        self.balance = self.total_amount - self.paid_amount


class InvoiceItem(Base):
    """Modelo de Item de Factura"""
    __tablename__ = "invoice_items"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    
    # Descripción del item
    description = Column(String(500), nullable=False)
    quantity = Column(Float, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    invoice = relationship("Invoice", back_populates="items")
    
    def __repr__(self):
        return f"<InvoiceItem {self.description[:30]} - {self.subtotal}>"
    
    def calculate_subtotal(self):
        """Calcula el subtotal del item"""
        self.subtotal = self.quantity * self.unit_price
