"""
Modelo de Amenidades (Servicios de Habitaciones)
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
import enum


class AmenityCategory(str, enum.Enum):
    """Categorías de amenidades"""
    BASIC = "básico"       # Servicios básicos
    PREMIUM = "premium"    # Servicios premium
    LUXURY = "lujo"        # Servicios de lujo


class Amenity(Base):
    """Modelo de Amenidad/Servicio"""
    __tablename__ = "amenities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # Nombre del icono (opcional)
    category = Column(Enum(AmenityCategory), default=AmenityCategory.BASIC, nullable=False)
    
    # Estado
    is_active = Column(Boolean, default=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación muchos-a-muchos con room_types
    room_types = relationship(
        "RoomType",
        secondary="room_type_amenities",
        back_populates="amenities"
    )
    
    def __repr__(self):
        return f"<Amenity {self.name} - {self.category}>"


class RoomTypeAmenity(Base):
    """Tabla asociativa entre RoomType y Amenity"""
    __tablename__ = "room_type_amenities"
    
    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    amenity_id = Column(Integer, ForeignKey("amenities.id"), nullable=False)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<RoomTypeAmenity room_type_id={self.room_type_id} amenity_id={self.amenity_id}>"
