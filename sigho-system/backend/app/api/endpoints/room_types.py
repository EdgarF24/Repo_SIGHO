"""
Endpoints de API para Tipos de Habitación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.room_type import RoomType
from app.models.amenity import Amenity
from app.schemas.room_type import RoomTypeCreate, RoomTypeUpdate, RoomTypeResponse
from app.core.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[RoomTypeResponse])
def get_room_types(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener lista de tipos de habitación
    """
    query = db.query(RoomType)
    
    if is_active is not None:
        query = query.filter(RoomType.is_active == is_active)
    
    room_types = query.offset(skip).limit(limit).all()
    return room_types


@router.get("/{room_type_id}", response_model=RoomTypeResponse)
def get_room_type(
    room_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener un tipo de habitación por ID
    """
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {room_type_id} no encontrado"
        )
    return room_type


@router.post("/", response_model=RoomTypeResponse, status_code=status.HTTP_201_CREATED)
def create_room_type(
    room_type_in: RoomTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crear un nuevo tipo de habitación
    Requiere rol de admin o manager
    """
    # Verificar si ya existe un tipo con ese nombre
    existing = db.query(RoomType).filter(RoomType.name == room_type_in.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un tipo de habitación con el nombre '{room_type_in.name}'"
        )
    
    # Extraer amenity_ids del input
    amenity_ids = room_type_in.amenity_ids
    room_type_data = room_type_in.model_dump(exclude={"amenity_ids"})
    
    # Crear el tipo de habitación
    room_type = RoomType(**room_type_data)
    
    # Agregar amenidades si existen
    if amenity_ids:
        amenities = db.query(Amenity).filter(Amenity.id.in_(amenity_ids)).all()
        if len(amenities) != len(amenity_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Una o más amenidades no existen"
            )
        room_type.amenities = amenities
    
    db.add(room_type)
    db.commit()
    db.refresh(room_type)
    return room_type


@router.put("/{room_type_id}", response_model=RoomTypeResponse)
def update_room_type(
    room_type_id: int,
    room_type_in: RoomTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar un tipo de habitación
    Requiere rol de admin o manager
    """
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {room_type_id} no encontrado"
        )
    
    # Si se está actualizando el nombre, verificar que no exista
    if room_type_in.name and room_type_in.name != room_type.name:
        existing = db.query(RoomType).filter(RoomType.name == room_type_in.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un tipo de habitación con el nombre '{room_type_in.name}'"
            )
    
    # Actualizar campos básicos
    update_data = room_type_in.model_dump(exclude_unset=True, exclude={"amenity_ids"})
    for field, value in update_data.items():
        setattr(room_type, field, value)
    
    # Actualizar amenidades si se proporcionaron
    if room_type_in.amenity_ids is not None:
        amenities = db.query(Amenity).filter(Amenity.id.in_(room_type_in.amenity_ids)).all()
        if len(amenities) != len(room_type_in.amenity_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Una o más amenidades no existen"
            )
        room_type.amenities = amenities
    
    db.commit()
    db.refresh(room_type)
    return room_type


@router.delete("/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_type(
    room_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Eliminar un tipo de habitación (soft delete)
    Requiere rol de admin
    """
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {room_type_id} no encontrado"
        )
    
    # Verificar si hay habitaciones usando este tipo
    if room_type.rooms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un tipo de habitación que tiene habitaciones asociadas"
        )
    
    # Soft delete
    room_type.is_active = False
    db.commit()
    return None
