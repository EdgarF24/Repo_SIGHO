"""
Endpoints de Inventario
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import random
import string
from app.database.session import get_db
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    InventoryMovementCreate,
    InventoryMovementResponse,
    InventoryAdjustment
)
from app.models.inventory import Inventory, InventoryCategory
from app.models.inventory_movement import InventoryMovement, MovementType
from app.models.user import User, UserRole
from app.api.dependencies.auth import get_current_active_user, require_role

router = APIRouter()


def generate_item_code() -> str:
    """Genera un código de item único"""
    return 'ITM-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def generate_movement_code() -> str:
    """Genera un código de movimiento único"""
    return 'MOV-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


# ========== INVENTORY ==========
@router.get("/", response_model=List[InventoryResponse])
def get_inventory_items(
    skip: int = 0,
    limit: int = 100,
    category: Optional[InventoryCategory] = None,
    is_active: Optional[bool] = None,
    needs_restock: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la lista de items de inventario
    """
    query = db.query(Inventory)
    
    if category:
        query = query.filter(Inventory.category == category)
    
    if is_active is not None:
        query = query.filter(Inventory.is_active == is_active)
    
    if needs_restock:
        query = query.filter(Inventory.current_quantity <= Inventory.minimum_quantity)
    
    query = query.order_by(Inventory.name)
    items = query.offset(skip).limit(limit).all()
    
    return items


@router.get("/low-stock", response_model=List[InventoryResponse])
def get_low_stock_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene items con stock bajo (necesitan reabastecimiento)
    """
    items = db.query(Inventory).filter(
        Inventory.current_quantity <= Inventory.minimum_quantity,
        Inventory.is_active == True
    ).order_by(Inventory.current_quantity.asc()).all()
    
    return items


@router.get("/by-category/{category}", response_model=List[InventoryResponse])
def get_items_by_category(
    category: InventoryCategory,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene items por categoría
    """
    items = db.query(Inventory).filter(
        Inventory.category == category,
        Inventory.is_active == True
    ).order_by(Inventory.name).all()
    
    return items


@router.get("/{item_id}", response_model=InventoryResponse)
def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene un item de inventario por ID
    """
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de inventario no encontrado"
        )
    return item


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    item_in: InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.INVENTORY]))
):
    """
    Crea un nuevo item de inventario
    """
    # Verificar que no existe un item con ese código
    existing = db.query(Inventory).filter(Inventory.item_code == item_in.item_code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un item con ese código"
        )
    
    item = Inventory(**item_in.model_dump())
    
    # Si tiene cantidad inicial, registrar movimiento de entrada
    if item.current_quantity > 0:
        item.last_restock_date = datetime.utcnow()
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    # Registrar movimiento inicial si hay cantidad
    if item.current_quantity > 0:
        movement_code = generate_movement_code()
        movement = InventoryMovement(
            movement_code=movement_code,
            inventory_id=item.id,
            user_id=current_user.id,
            movement_type=MovementType.IN,
            quantity=item.current_quantity,
            previous_quantity=0,
            new_quantity=item.current_quantity,
            reason="Stock inicial"
        )
        db.add(movement)
        db.commit()
    
    return item


@router.put("/{item_id}", response_model=InventoryResponse)
def update_inventory_item(
    item_id: int,
    item_in: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.INVENTORY]))
):
    """
    Actualiza un item de inventario
    """
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de inventario no encontrado"
        )
    
    update_data = item_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return item


@router.post("/{item_id}/adjust", response_model=InventoryResponse)
def adjust_inventory(
    item_id: int,
    adjustment: InventoryAdjustment,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.INVENTORY]))
):
    """
    Ajusta la cantidad de un item de inventario
    """
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de inventario no encontrado"
        )
    
    previous_quantity = item.current_quantity
    new_quantity = adjustment.new_quantity
    
    # Calcular la diferencia
    difference = new_quantity - previous_quantity
    
    # Determinar tipo de movimiento
    if difference > 0:
        movement_type = MovementType.IN
        quantity = difference
        item.last_restock_date = datetime.utcnow()
    elif difference < 0:
        movement_type = MovementType.OUT
        quantity = abs(difference)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva cantidad es igual a la actual"
        )
    
    # Actualizar cantidad
    item.current_quantity = new_quantity
    
    # Registrar movimiento
    movement_code = generate_movement_code()
    movement = InventoryMovement(
        movement_code=movement_code,
        inventory_id=item.id,
        user_id=current_user.id,
        movement_type=MovementType.ADJUSTMENT,
        quantity=quantity,
        previous_quantity=previous_quantity,
        new_quantity=new_quantity,
        reason=adjustment.reason,
        notes=adjustment.notes
    )
    
    db.add(movement)
    db.commit()
    db.refresh(item)
    
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Elimina un item de inventario
    """
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de inventario no encontrado"
        )
    
    db.delete(item)
    db.commit()
    
    return None


# ========== INVENTORY MOVEMENTS ==========
@router.get("/movements/", response_model=List[InventoryMovementResponse])
def get_inventory_movements(
    skip: int = 0,
    limit: int = 100,
    inventory_id: Optional[int] = None,
    movement_type: Optional[MovementType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la lista de movimientos de inventario
    """
    query = db.query(InventoryMovement)
    
    if inventory_id:
        query = query.filter(InventoryMovement.inventory_id == inventory_id)
    
    if movement_type:
        query = query.filter(InventoryMovement.movement_type == movement_type)
    
    query = query.order_by(InventoryMovement.movement_date.desc())
    movements = query.offset(skip).limit(limit).all()
    
    return movements


@router.get("/movements/{item_id}/history", response_model=List[InventoryMovementResponse])
def get_item_movement_history(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene el historial de movimientos de un item específico
    """
    # Verificar que el item existe
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de inventario no encontrado"
        )
    
    movements = db.query(InventoryMovement).filter(
        InventoryMovement.inventory_id == item_id
    ).order_by(InventoryMovement.movement_date.desc()).all()
    
    return movements


@router.post("/movements/", response_model=InventoryMovementResponse, status_code=status.HTTP_201_CREATED)
def create_inventory_movement(
    movement_in: InventoryMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.INVENTORY]))
):
    """
    Registra un movimiento de inventario (entrada o salida)
    """
    # Verificar que el item existe
    item = db.query(Inventory).filter(Inventory.id == movement_in.inventory_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item de inventario no encontrado"
        )
    
    previous_quantity = item.current_quantity
    
    # Calcular nueva cantidad según el tipo de movimiento
    if movement_in.movement_type == MovementType.IN:
        new_quantity = previous_quantity + movement_in.quantity
        item.last_restock_date = datetime.utcnow()
    elif movement_in.movement_type == MovementType.OUT:
        if previous_quantity < movement_in.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cantidad insuficiente. Disponible: {previous_quantity}"
            )
        new_quantity = previous_quantity - movement_in.quantity
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use el endpoint de ajuste para movimientos de tipo ADJUSTMENT"
        )
    
    # Actualizar cantidad en inventario
    item.current_quantity = new_quantity
    
    # Generar código de movimiento
    movement_code = generate_movement_code()
    
    # Crear movimiento
    movement = InventoryMovement(
        movement_code=movement_code,
        inventory_id=movement_in.inventory_id,
        user_id=current_user.id,
        movement_type=movement_in.movement_type,
        quantity=movement_in.quantity,
        previous_quantity=previous_quantity,
        new_quantity=new_quantity,
        reason=movement_in.reason,
        notes=movement_in.notes,
        reference_document=movement_in.reference_document
    )
    
    db.add(movement)
    db.commit()
    db.refresh(movement)
    
    return movement