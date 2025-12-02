"""
Modelo de Mantenimiento
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
import enum


class MaintenanceType(str, enum.Enum):
    """Tipos de mantenimiento"""
    PREVENTIVE = "preventive"    # Preventivo
    CORRECTIVE = "corrective"    # Correctivo
    EMERGENCY = "emergency"      # Emergencia


class MaintenancePriority(str, enum.Enum):
    """Prioridad del mantenimiento"""
    LOW = "low"          # Baja
    MEDIUM = "medium"    # Media
    HIGH = "high"        # Alta
    URGENT = "urgent"    # Urgente


class MaintenanceStatus(str, enum.Enum):
    """Estados del mantenimiento"""
    PENDING = "pending"          # Pendiente
    IN_PROGRESS = "in_progress"  # En progreso
    COMPLETED = "completed"      # Completado
    CANCELLED = "cancelled"      # Cancelado


class Maintenance(Base):
    """Modelo de Mantenimiento"""
    __tablename__ = "maintenance"
    
    id = Column(Integer, primary_key=True, index=True)
    maintenance_code = Column(String(20), unique=True, nullable=False, index=True)
    
    # Relaciones
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Información del mantenimiento
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    maintenance_type = Column(Enum(MaintenanceType), nullable=False)
    priority = Column(Enum(MaintenancePriority), default=MaintenancePriority.MEDIUM, nullable=False)
    status = Column(Enum(MaintenanceStatus), default=MaintenanceStatus.PENDING, nullable=False)
    
    # Fechas
    scheduled_date = Column(Date, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Costos
    estimated_cost = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)
    currency = Column(String(3), nullable=False, default="VES")
    
    # Resolución
    resolution_notes = Column(Text, nullable=True)
    materials_used = Column(Text, nullable=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    room = relationship("Room", back_populates="maintenance_records")
    
    def __repr__(self):
        return f"<Maintenance {self.maintenance_code} - {self.status}>"