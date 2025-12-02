"""
Modelo de Tipo de Habitación
"""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class RoomType(Base):
    """Modelo de Tipo de Habitación"""
    __tablename__ = "room_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # Ej: "Individual", "Doble", "Suite"
    description = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=False)  # Capacidad de personas
    base_price_ves = Column(Float, nullable=False)  # Precio base en VES
    base_price_usd = Column(Float, nullable=False)  # Precio base en USD
    base_price_eur = Column(Float, nullable=True)   # Precio base en EUR
    
    # Estado
    is_active = Column(Boolean, default=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    rooms = relationship("Room", back_populates="room_type")
    amenities = relationship(
        "Amenity",
        secondary="room_type_amenities",
        back_populates="room_types"
    )
    
    def __repr__(self):
        return f"<RoomType {self.name} - Capacidad: {self.capacity}>"