"""
Schemas de Mantenimiento (Pydantic)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from app.models.maintenance import MaintenanceType, MaintenancePriority, MaintenanceStatus


class MaintenanceBase(BaseModel):
    """Schema base de mantenimiento"""
    room_id: int
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    maintenance_type: MaintenanceType
    priority: MaintenancePriority = MaintenancePriority.MEDIUM
    scheduled_date: Optional[date] = None
    estimated_cost: Optional[float] = Field(None, ge=0)
    currency: str = Field("VES", max_length=3)


class MaintenanceCreate(MaintenanceBase):
    """Schema para crear mantenimiento"""
    pass


class MaintenanceUpdate(BaseModel):
    """Schema para actualizar mantenimiento"""
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    maintenance_type: Optional[MaintenanceType] = None
    priority: Optional[MaintenancePriority] = None
    status: Optional[MaintenanceStatus] = None
    scheduled_date: Optional[date] = None
    assigned_to: Optional[int] = None
    estimated_cost: Optional[float] = Field(None, ge=0)
    actual_cost: Optional[float] = Field(None, ge=0)
    resolution_notes: Optional[str] = None
    materials_used: Optional[str] = None


class MaintenanceResponse(MaintenanceBase):
    """Schema de respuesta de mantenimiento"""
    id: int
    maintenance_code: str
    status: MaintenanceStatus
    reported_by: int
    assigned_to: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    actual_cost: Optional[float] = None
    resolution_notes: Optional[str] = None
    materials_used: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MaintenanceAssign(BaseModel):
    """Schema para asignar mantenimiento"""
    assigned_to: int


class MaintenanceComplete(BaseModel):
    """Schema para completar mantenimiento"""
    actual_cost: float = Field(..., ge=0)
    resolution_notes: str = Field(..., min_length=10)
    materials_used: Optional[str] = None