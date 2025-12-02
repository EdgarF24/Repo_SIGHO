"""
Endpoints de Huéspedes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database.session import get_db
from app.schemas.guest import GuestCreate, GuestUpdate, GuestResponse, GuestSearch
from app.models.guest import Guest
from app.models.user import User, UserRole
from app.api.dependencies.auth import get_current_active_user, require_role

router = APIRouter()


@router.get("/", response_model=List[GuestResponse])
def get_guests(
    skip: int = 0,
    limit: int = 100,
    country: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la lista de huéspedes
    """
    query = db.query(Guest)
    
    if country:
        query = query.filter(Guest.country == country)
    
    query = query.order_by(Guest.created_at.desc())
    guests = query.offset(skip).limit(limit).all()
    
    return guests


@router.get("/search", response_model=List[GuestResponse])
def search_guests(
    query: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Busca huéspedes por nombre, documento, email o teléfono
    """
    guests = db.query(Guest).filter(
        or_(
            Guest.first_name.ilike(f"%{query}%"),
            Guest.last_name.ilike(f"%{query}%"),
            Guest.id_number.ilike(f"%{query}%"),
            Guest.email.ilike(f"%{query}%"),
            Guest.phone.ilike(f"%{query}%")
        )
    ).all()
    
    return guests


@router.get("/{guest_id}", response_model=GuestResponse)
def get_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene un huésped por ID
    """
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Huésped no encontrado"
        )
    return guest


@router.get("/by-document/{id_number}", response_model=GuestResponse)
def get_guest_by_document(
    id_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene un huésped por número de documento
    """
    guest = db.query(Guest).filter(Guest.id_number == id_number).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Huésped no encontrado"
        )
    return guest


@router.post("/", response_model=GuestResponse, status_code=status.HTTP_201_CREATED)
def create_guest(
    guest_in: GuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Crea un nuevo huésped
    """
    # Verificar que no existe un huésped con ese documento
    existing = db.query(Guest).filter(Guest.id_number == guest_in.id_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un huésped con ese número de documento"
        )
    
    # Verificar email único si se proporciona
    if guest_in.email:
        existing_email = db.query(Guest).filter(Guest.email == guest_in.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un huésped con ese email"
            )
    
    guest = Guest(**guest_in.model_dump())
    db.add(guest)
    db.commit()
    db.refresh(guest)
    
    return guest


@router.put("/{guest_id}", response_model=GuestResponse)
def update_guest(
    guest_id: int,
    guest_in: GuestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Actualiza un huésped
    """
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Huésped no encontrado"
        )
    
    update_data = guest_in.model_dump(exclude_unset=True)
    
    # Verificar email único si se actualiza
    if "email" in update_data and update_data["email"]:
        existing_email = db.query(Guest).filter(
            Guest.email == update_data["email"],
            Guest.id != guest_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un huésped con ese email"
            )
    
    for field, value in update_data.items():
        setattr(guest, field, value)
    
    db.commit()
    db.refresh(guest)
    
    return guest


@router.delete("/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Elimina un huésped (solo si no tiene reservas)
    """
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Huésped no encontrado"
        )
    
    # Verificar que no tenga reservas
    if guest.reservations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar. El huésped tiene {len(guest.reservations)} reserva(s) registrada(s)"
        )
    
    db.delete(guest)
    db.commit()
    
    return None