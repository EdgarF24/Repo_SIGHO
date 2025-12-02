"""
Modelo de Habitación
"""
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
import enum


class RoomStatus(str, enum.Enum):
    """Estados de una habitación"""
    AVAILABLE = "available"          # Disponible
    OCCUPIED = "occupied"            # Ocupada
    CLEANING = "cleaning"            # En limpieza
    MAINTENANCE = "maintenance"      # En mantenimiento
    OUT_OF_SERVICE = "out_of_service"  # Fuera de servicio


class Room(Base):
    """Modelo de Habitación"""
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(10), unique=True, nullable=False, index=True)
    floor = Column(Integer, nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.AVAILABLE, nullable=False)
    
    # Observaciones
    notes = Column(Text, nullable=True)
    
    # Estado
    is_active = Column(Boolean, default=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    room_type = relationship("RoomType", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room")
    maintenance_records = relationship("Maintenance", back_populates="room")
    
    def __repr__(self):
        return f"<Room {self.room_number} - {self.status}>"