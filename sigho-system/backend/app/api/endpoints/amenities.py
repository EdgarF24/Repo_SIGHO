"""
Endpoints de API para Amenidades
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.amenity import Amenity
from app.schemas.amenity import AmenityCreate, AmenityUpdate, AmenityResponse
from app.core.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[AmenityResponse])
def get_amenities(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener lista de amenidades
    """
    query = db.query(Amenity)
    
    if is_active is not None:
        query = query.filter(Amenity.is_active == is_active)
    
    amenities = query.offset(skip).limit(limit).all()
    return amenities


@router.get("/{amenity_id}", response_model=AmenityResponse)
def get_amenity(
    amenity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener una amenidad por ID
    """
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Amenidad con ID {amenity_id} no encontrada"
        )
    return amenity


@router.post("/", response_model=AmenityResponse, status_code=status.HTTP_201_CREATED)
def create_amenity(
    amenity_in: AmenityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crear una nueva amenidad
    Requiere rol de admin o manager
    """
    # Verificar si ya existe una amenidad con ese nombre
    existing = db.query(Amenity).filter(Amenity.name == amenity_in.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una amenidad con el nombre '{amenity_in.name}'"
        )
    
    amenity = Amenity(**amenity_in.model_dump())
    db.add(amenity)
    db.commit()
    db.refresh(amenity)
    return amenity


@router.put("/{amenity_id}", response_model=AmenityResponse)
def update_amenity(
    amenity_id: int,
    amenity_in: AmenityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar una amenidad
    Requiere rol de admin o manager
    """
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Amenidad con ID {amenity_id} no encontrada"
        )
    
    # Si se está actualizando el nombre, verificar que no exista
    if amenity_in.name and amenity_in.name != amenity.name:
        existing = db.query(Amenity).filter(Amenity.name == amenity_in.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una amenidad con el nombre '{amenity_in.name}'"
            )
    
    # Actualizar campos
    update_data = amenity_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(amenity, field, value)
    
    db.commit()
    db.refresh(amenity)
    return amenity


@router.delete("/{amenity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_amenity(
    amenity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Eliminar una amenidad (soft delete)
    Requiere rol de admin
    """
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Amenidad con ID {amenity_id} no encontrada"
        )
    
    # Soft delete
    amenity.is_active = False
    db.commit()
    return None
