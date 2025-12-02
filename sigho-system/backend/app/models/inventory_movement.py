"""
Modelo de Movimiento de Inventario
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
import enum


class MovementType(str, enum.Enum):
    """Tipos de movimiento"""
    IN = "in"            # Entrada (compra, donación)
    OUT = "out"          # Salida (uso, venta)
    ADJUSTMENT = "adjustment"  # Ajuste (corrección de inventario)
    TRANSFER = "transfer"      # Transferencia entre ubicaciones


class InventoryMovement(Base):
    """Modelo de Movimiento de Inventario"""
    __tablename__ = "inventory_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    movement_code = Column(String(20), unique=True, nullable=False, index=True)
    
    # Relaciones
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Información del movimiento
    movement_type = Column(Enum(MovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    previous_quantity = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    
    # Detalles
    reason = Column(String(200), nullable=False)
    notes = Column(Text, nullable=True)
    reference_document = Column(String(100), nullable=True)  # Factura, orden de compra, etc.
    
    # Auditoría
    movement_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    inventory_item = relationship("Inventory", back_populates="movements")
    
    def __repr__(self):
        return f"<InventoryMovement {self.movement_code} - {self.movement_type}>"