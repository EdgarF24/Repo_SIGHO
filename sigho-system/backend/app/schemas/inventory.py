"""
Schemas de Inventario (Pydantic)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.inventory import InventoryCategory
from app.models.inventory_movement import MovementType


# ========== INVENTORY ==========
class InventoryBase(BaseModel):
    """Schema base de inventario"""
    item_code: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    category: InventoryCategory
    unit_of_measure: str = Field(..., max_length=20)
    current_quantity: int = Field(0, ge=0)
    minimum_quantity: int = Field(0, ge=0)
    maximum_quantity: Optional[int] = Field(None, ge=0)
    unit_cost: float = Field(0.0, ge=0)
    currency: str = Field("VES", max_length=3)
    supplier_name: Optional[str] = Field(None, max_length=200)
    supplier_contact: Optional[str] = Field(None, max_length=100)
    storage_location: Optional[str] = Field(None, max_length=100)


class InventoryCreate(InventoryBase):
    """Schema para crear item de inventario"""
    pass


class InventoryUpdate(BaseModel):
    """Schema para actualizar item de inventario"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    category: Optional[InventoryCategory] = None
    unit_of_measure: Optional[str] = Field(None, max_length=20)
    minimum_quantity: Optional[int] = Field(None, ge=0)
    maximum_quantity: Optional[int] = Field(None, ge=0)
    unit_cost: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=3)
    supplier_name: Optional[str] = Field(None, max_length=200)
    supplier_contact: Optional[str] = Field(None, max_length=100)
    storage_location: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class InventoryResponse(InventoryBase):
    """Schema de respuesta de inventario"""
    id: int
    is_active: bool
    needs_restock: bool
    total_value: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_restock_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class InventoryInDB(InventoryResponse):
    """Schema de inventario en base de datos"""
    pass


# ========== INVENTORY MOVEMENT ==========
class InventoryMovementBase(BaseModel):
    """Schema base de movimiento de inventario"""
    inventory_id: int
    movement_type: MovementType
    quantity: int = Field(..., gt=0)
    reason: str = Field(..., min_length=5, max_length=200)
    notes: Optional[str] = None
    reference_document: Optional[str] = Field(None, max_length=100)


class InventoryMovementCreate(InventoryMovementBase):
    """Schema para crear movimiento"""
    pass


class InventoryMovementResponse(InventoryMovementBase):
    """Schema de respuesta de movimiento"""
    id: int
    movement_code: str
    user_id: int
    previous_quantity: int
    new_quantity: int
    movement_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class InventoryMovementInDB(InventoryMovementResponse):
    """Schema de movimiento en base de datos"""
    pass


class InventoryAdjustment(BaseModel):
    """Schema para ajustar inventario"""
    new_quantity: int = Field(..., ge=0)
    reason: str = Field(..., min_length=10)
    notes: Optional[str] = None