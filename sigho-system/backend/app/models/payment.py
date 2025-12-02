"""
Modelo de Pago
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
import enum


class PaymentMethod(str, enum.Enum):
    """Métodos de pago"""
    CASH_VES = "cash_ves"        # Efectivo en bolívares
    CASH_USD = "cash_usd"        # Efectivo en dólares
    CASH_EUR = "cash_eur"        # Efectivo en euros
    TRANSFER = "transfer"        # Transferencia bancaria
    MOBILE_PAYMENT = "mobile_payment"  # Pago móvil (Zelle, PayPal, etc)
    CREDIT_CARD = "credit_card"  # Tarjeta de crédito
    DEBIT_CARD = "debit_card"    # Tarjeta de débito
    OTHER = "other"              # Otro método


class PaymentStatus(str, enum.Enum):
    """Estados de un pago"""
    PENDING = "pending"          # Pendiente
    COMPLETED = "completed"      # Completado
    FAILED = "failed"            # Fallido
    REFUNDED = "refunded"        # Reembolsado


class Payment(Base):
    """Modelo de Pago"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    payment_code = Column(String(20), unique=True, nullable=False, index=True)
    
    # Relaciones
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Información del pago
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)  # VES, USD, EUR
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    
    # Detalles adicionales
    reference_number = Column(String(100), nullable=True)  # Número de referencia bancaria
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Auditoría
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reservation = relationship("Reservation", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment {self.payment_code} - {self.amount} {self.currency}>"