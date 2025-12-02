"""
Modelo de Inventario
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
import enum


class InventoryCategory(str, enum.Enum):
    """Categorías de inventario"""
    CLEANING = "cleaning"            # Limpieza
    MAINTENANCE = "maintenance"      # Mantenimiento
    BEDDING = "bedding"             # Ropa de cama
    BATHROOM = "bathroom"           # Baño
    KITCHEN = "kitchen"             # Cocina
    ELECTRONICS = "electronics"     # Electrónica
    FURNITURE = "furniture"         # Muebles
    FOOD_BEVERAGE = "food_beverage" # Alimentos y bebidas
    OTHER = "other"                 # Otro


class Inventory(Base):
    """Modelo de Inventario"""
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Información del producto
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(InventoryCategory), nullable=False)
    
    # Unidades
    unit_of_measure = Column(String(20), nullable=False)  # unidad, caja, litro, kg, etc.
    current_quantity = Column(Integer, nullable=False, default=0)
    minimum_quantity = Column(Integer, nullable=False, default=0)  # Stock mínimo
    maximum_quantity = Column(Integer, nullable=True)  # Stock máximo
    
    # Precios
    unit_cost = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), nullable=False, default="VES")
    
    # Proveedor
    supplier_name = Column(String(200), nullable=True)
    supplier_contact = Column(String(100), nullable=True)
    
    # Estado
    is_active = Column(Boolean, default=True)
    
    # Ubicación
    storage_location = Column(String(100), nullable=True)
    
    # Auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_restock_date = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    movements = relationship("InventoryMovement", back_populates="inventory_item")
    
    @property
    def needs_restock(self):
        """Verifica si el item necesita reabastecimiento"""
        return self.current_quantity <= self.minimum_quantity
    
    @property
    def total_value(self):
        """Calcula el valor total del inventario"""
        return self.current_quantity * self.unit_cost
    
    def __repr__(self):
        return f"<Inventory {self.item_code} - {self.name}>"