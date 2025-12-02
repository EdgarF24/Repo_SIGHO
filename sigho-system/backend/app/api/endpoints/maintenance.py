"""
Endpoints de Mantenimiento
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import random
import string
from app.database.session import get_db
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
    MaintenanceResponse,
    MaintenanceAssign,
    MaintenanceComplete
)
from app.models.maintenance import Maintenance, MaintenanceStatus, MaintenancePriority, MaintenanceType
from app.models.room import Room, RoomStatus
from app.models.user import User, UserRole
from app.api.dependencies.auth import get_current_active_user, require_role

router = APIRouter()


def generate_maintenance_code() -> str:
    """Genera un código de mantenimiento único"""
    return 'MNT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


@router.get("/", response_model=List[MaintenanceResponse])
def get_maintenance_records(
    skip: int = 0,
    limit: int = 100,
    status: Optional[MaintenanceStatus] = None,
    priority: Optional[MaintenancePriority] = None,
    room_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la lista de registros de mantenimiento
    """
    query = db.query(Maintenance)
    
    if status:
        query = query.filter(Maintenance.status == status)
    
    if priority:
        query = query.filter(Maintenance.priority == priority)
    
    if room_id:
        query = query.filter(Maintenance.room_id == room_id)
    
    # Si es personal de mantenimiento, solo ver sus asignaciones
    if current_user.role == UserRole.MAINTENANCE:
        query = query.filter(Maintenance.assigned_to == current_user.id)
    
    query = query.order_by(
        Maintenance.priority.desc(),
        Maintenance.created_at.desc()
    )
    
    maintenance_records = query.offset(skip).limit(limit).all()
    return maintenance_records


@router.get("/pending", response_model=List[MaintenanceResponse])
def get_pending_maintenance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene tareas de mantenimiento pendientes
    """
    query = db.query(Maintenance).filter(
        Maintenance.status == MaintenanceStatus.PENDING
    )
    
    # Si es personal de mantenimiento, solo ver sus asignaciones
    if current_user.role == UserRole.MAINTENANCE:
        query = query.filter(Maintenance.assigned_to == current_user.id)
    
    maintenance_records = query.order_by(
        Maintenance.priority.desc(),
        Maintenance.created_at.asc()
    ).all()
    
    return maintenance_records


@router.get("/in-progress", response_model=List[MaintenanceResponse])
def get_in_progress_maintenance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene tareas de mantenimiento en progreso
    """
    query = db.query(Maintenance).filter(
        Maintenance.status == MaintenanceStatus.IN_PROGRESS
    )
    
    # Si es personal de mantenimiento, solo ver sus asignaciones
    if current_user.role == UserRole.MAINTENANCE:
        query = query.filter(Maintenance.assigned_to == current_user.id)
    
    maintenance_records = query.order_by(Maintenance.started_at.desc()).all()
    
    return maintenance_records


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene un registro de mantenimiento por ID
    """
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de mantenimiento no encontrado"
        )
    return maintenance


@router.post("/", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(
    maintenance_in: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crea un nuevo registro de mantenimiento
    """
    # Verificar que la habitación existe
    room = db.query(Room).filter(Room.id == maintenance_in.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habitación no encontrada"
        )
    
    # Generar código único
    maintenance_code = generate_maintenance_code()
    while db.query(Maintenance).filter(Maintenance.maintenance_code == maintenance_code).first():
        maintenance_code = generate_maintenance_code()
    
    # Crear registro
    maintenance = Maintenance(
        maintenance_code=maintenance_code,
        room_id=maintenance_in.room_id,
        reported_by=current_user.id,
        title=maintenance_in.title,
        description=maintenance_in.description,
        maintenance_type=maintenance_in.maintenance_type,
        priority=maintenance_in.priority,
        scheduled_date=maintenance_in.scheduled_date,
        estimated_cost=maintenance_in.estimated_cost,
        currency=maintenance_in.currency
    )
    
    db.add(maintenance)
    
    # Si es urgente o emergencia, cambiar estado de la habitación
    if maintenance_in.priority in [MaintenancePriority.URGENT, MaintenancePriority.HIGH]:
        if maintenance_in.maintenance_type == MaintenanceType.EMERGENCY:
            room.status = RoomStatus.OUT_OF_SERVICE
        elif room.status == RoomStatus.AVAILABLE:
            room.status = RoomStatus.MAINTENANCE
    
    db.commit()
    db.refresh(maintenance)
    
    return maintenance


@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance(
    maintenance_id: int,
    maintenance_in: MaintenanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.MAINTENANCE]))
):
    """
    Actualiza un registro de mantenimiento
    """
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de mantenimiento no encontrado"
        )
    
    # Si es personal de mantenimiento, solo puede actualizar sus asignaciones
    if current_user.role == UserRole.MAINTENANCE:
        if maintenance.assigned_to != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para actualizar este registro"
            )
    
    update_data = maintenance_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(maintenance, field, value)
    
    db.commit()
    db.refresh(maintenance)
    
    return maintenance


@router.post("/{maintenance_id}/assign", response_model=MaintenanceResponse)
def assign_maintenance(
    maintenance_id: int,
    assign_data: MaintenanceAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
):
    """
    Asigna una tarea de mantenimiento a un usuario
    """
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de mantenimiento no encontrado"
        )
    
    # Verificar que el usuario existe y tiene rol de mantenimiento
    assigned_user = db.query(User).filter(User.id == assign_data.assigned_to).first()
    if not assigned_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    if assigned_user.role not in [UserRole.MAINTENANCE, UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no tiene permisos de mantenimiento"
        )
    
    maintenance.assigned_to = assign_data.assigned_to
    
    db.commit()
    db.refresh(maintenance)
    
    return maintenance


@router.post("/{maintenance_id}/start", response_model=MaintenanceResponse)
def start_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.MAINTENANCE]))
):
    """
    Inicia una tarea de mantenimiento
    """
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de mantenimiento no encontrado"
        )
    
    if maintenance.status != MaintenanceStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden iniciar tareas pendientes"
        )
    
    # Si no está asignado, asignar al usuario actual
    if not maintenance.assigned_to:
        maintenance.assigned_to = current_user.id
    
    maintenance.status = MaintenanceStatus.IN_PROGRESS
    maintenance.started_at = datetime.utcnow()
    
    # Cambiar estado de la habitación
    room = db.query(Room).filter(Room.id == maintenance.room_id).first()
    if room.status != RoomStatus.OUT_OF_SERVICE:
        room.status = RoomStatus.MAINTENANCE
    
    db.commit()
    db.refresh(maintenance)
    
    return maintenance


@router.post("/{maintenance_id}/complete", response_model=MaintenanceResponse)
def complete_maintenance(
    maintenance_id: int,
    complete_data: MaintenanceComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.MAINTENANCE]))
):
    """
    Completa una tarea de mantenimiento
    """
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de mantenimiento no encontrado"
        )
    
    if maintenance.status not in [MaintenanceStatus.PENDING, MaintenanceStatus.IN_PROGRESS]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden completar tareas pendientes o en progreso"
        )
    
    maintenance.status = MaintenanceStatus.COMPLETED
    maintenance.completed_at = datetime.utcnow()
    maintenance.actual_cost = complete_data.actual_cost
    maintenance.resolution_notes = complete_data.resolution_notes
    maintenance.materials_used = complete_data.materials_used
    
    # Si no se había iniciado, marcar como iniciado también
    if not maintenance.started_at:
        maintenance.started_at = datetime.utcnow()
    
    # Cambiar estado de la habitación a limpieza
    room = db.query(Room).filter(Room.id == maintenance.room_id).first()
    room.status = RoomStatus.CLEANING
    
    db.commit()
    db.refresh(maintenance)
    
    return maintenance


@router.post("/{maintenance_id}/cancel", response_model=MaintenanceResponse)
def cancel_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
):
    """
    Cancela una tarea de mantenimiento
    """
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de mantenimiento no encontrado"
        )
    
    if maintenance.status == MaintenanceStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede cancelar una tarea completada"
        )
    
    maintenance.status = MaintenanceStatus.CANCELLED
    
    # Restaurar estado de la habitación si estaba en mantenimiento
    room = db.query(Room).filter(Room.id == maintenance.room_id).first()
    if room.status == RoomStatus.MAINTENANCE:
        room.status = RoomStatus.AVAILABLE
    
    db.commit()
    db.refresh(maintenance)
    
    return maintenance


@router.delete("/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Elimina un registro de mantenimiento (solo admin)
    """
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de mantenimiento no encontrado"
        )
    
    db.delete(maintenance)
    db.commit()
    
    return None