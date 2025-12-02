"""
Modelo de Huésped
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class Guest(Base):
    """Modelo de Huésped"""
    __tablename__ = "guests"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Información personal
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    id_type = Column(String(20), nullable=False)  # CI, Pasaporte, RIF
    id_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Contacto
    email = Column(String(100), nullable=True, index=True)
    phone = Column(String(20), nullable=False)
    phone_alternative = Column(String(20), nullable=True)
    
    # Dirección
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=False, default="Venezuela")
    
    # Información adicional
    date_of_birth = Column(Date, nullable=True)
    nationality = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reservations = relationship("Reservation", back_populates="guest")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<Guest {self.full_name} - {self.id_number}>"