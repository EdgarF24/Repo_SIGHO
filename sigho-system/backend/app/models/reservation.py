"""
Modelo de Reserva
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
import enum


class ReservationStatus(str, enum.Enum):
    """Estados de una reserva"""
    PENDING = "pending"          # Pendiente (creada pero no confirmada)
    CONFIRMED = "confirmed"      # Confirmada
    CHECKED_IN = "checked_in"    # Check-in realizado
    CHECKED_OUT = "checked_out"  # Check-out realizado
    CANCELLED = "cancelled"      # Cancelada
    NO_SHOW = "no_show"         # No se presentó


class Reservation(Base):
    """Modelo de Reserva"""
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    confirmation_code = Column(String(20), unique=True, nullable=False, index=True)
    
    # Relaciones
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Fechas
    check_in_date = Column(Date, nullable=False, index=True)
    check_out_date = Column(Date, nullable=False, index=True)
    actual_check_in = Column(DateTime(timezone=True), nullable=True)
    actual_check_out = Column(DateTime(timezone=True), nullable=True)
    
    # Información de la reserva
    num_adults = Column(Integer, nullable=False, default=1)
    num_children = Column(Integer, nullable=False, default=0)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False)
    
    # Precios y moneda
    currency = Column(String(3), nullable=False, default="VES")  # VES, USD, EUR
    price_per_night = Column(Float, nullable=False)
    total_nights = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False, default=16.0)  # IVA 16%
    tax_amount = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Pagos
    paid_amount = Column(Float, nullable=False, default=0.0)
    balance = Column(Float, nullable=False)
    is_paid = Column(Boolean, default=False)
    
    # Observaciones
    special_requests = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    guest = relationship("Guest", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")
    payments = relationship("Payment", back_populates="reservation")
    
    def __repr__(self):
        return f"<Reservation {self.confirmation_code} - {self.status}>"