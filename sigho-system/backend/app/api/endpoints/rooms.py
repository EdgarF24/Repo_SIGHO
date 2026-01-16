"""
Endpoints de Habitaciones
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import date
from app.database.session import get_db
from app.schemas.room import (
    RoomCreate, 
    RoomUpdate, 
    RoomResponse,
    RoomStatusUpdate,
    RoomTypeCreate,
    RoomTypeUpdate,
    RoomTypeResponse,
    RoomAvailabilityQuery,
    RoomAvailabilityResponse
)
from app.models.room import Room, RoomStatus
from app.models.room_type import RoomType
from app.models.reservation import Reservation, ReservationStatus
from app.models.user import User, UserRole
from app.api.dependencies.auth import get_current_active_user, require_role

router = APIRouter()


# ========== ROOM TYPES ==========
@router.get("/types", response_model=List[RoomTypeResponse])
def get_room_types(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la lista de tipos de habitación
    """
    query = db.query(RoomType)
    
    if is_active is not None:
        query = query.filter(RoomType.is_active == is_active)
    
    room_types = query.offset(skip).limit(limit).all()
    return room_types


@router.get("/types/{room_type_id}", response_model=RoomTypeResponse)
def get_room_type(
    room_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene un tipo de habitación por ID
    """
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de habitación no encontrado"
        )
    return room_type


@router.post("/types", response_model=RoomTypeResponse, status_code=status.HTTP_201_CREATED)
def create_room_type(
    room_type_in: RoomTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
):
    """
    Crea un nuevo tipo de habitación
    """
    # Verificar que no existe un tipo con ese nombre
    existing = db.query(RoomType).filter(RoomType.name == room_type_in.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un tipo de habitación con ese nombre"
        )
    
    room_type = RoomType(**room_type_in.model_dump())
    db.add(room_type)
    db.commit()
    db.refresh(room_type)
    
    return room_type


@router.put("/types/{room_type_id}", response_model=RoomTypeResponse)
def update_room_type(
    room_type_id: int,
    room_type_in: RoomTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
):
    """
    Actualiza un tipo de habitación
    """
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de habitación no encontrado"
        )
    
    update_data = room_type_in.model_dump(exclude_unset=True)
    
    # Verificar nombre único si se actualiza
    if "name" in update_data:
        existing = db.query(RoomType).filter(
            RoomType.name == update_data["name"],
            RoomType.id != room_type_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un tipo de habitación con ese nombre"
            )
    
    for field, value in update_data.items():
        setattr(room_type, field, value)
    
    db.commit()
    db.refresh(room_type)
    
    return room_type


@router.delete("/types/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_type(
    room_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Elimina un tipo de habitación (solo si no tiene habitaciones asociadas)
    """
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de habitación no encontrado"
        )
    
    # Verificar que no tenga habitaciones
    rooms_count = db.query(Room).filter(Room.room_type_id == room_type_id).count()
    if rooms_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar. Hay {rooms_count} habitación(es) asociada(s)"
        )
    
    db.delete(room_type)
    db.commit()
    
    return None


# ========== ROOMS ==========
@router.get("/", response_model=List[RoomResponse])
def get_rooms(
    skip: int = 0,
    limit: int = 100,
    floor: Optional[int] = None,
    status: Optional[RoomStatus] = None,
    room_type_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la lista de habitaciones con filtros opcionales
    """
    query = db.query(Room)
    
    if floor is not None:
        query = query.filter(Room.floor == floor)
    
    if status is not None:
        query = query.filter(Room.status == status)
    
    if room_type_id is not None:
        query = query.filter(Room.room_type_id == room_type_id)
    
    if is_active is not None:
        query = query.filter(Room.is_active == is_active)
    
    query = query.order_by(Room.room_number)
    rooms = query.offset(skip).limit(limit).all()
    
    return rooms


@router.get("/available", response_model=List[RoomResponse])
def get_available_rooms(
    check_in: date = Query(...),
    check_out: date = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene habitaciones disponibles para un rango de fechas
    """
    # Obtener todas las habitaciones activas y disponibles
    all_rooms = db.query(Room).filter(
        Room.is_active == True,
        Room.status.in_([RoomStatus.AVAILABLE, RoomStatus.CLEANING])
    ).all()
    
    available_rooms = []
    
    for room in all_rooms:
        # Verificar si tiene reservas en conflicto
        conflicting = db.query(Reservation).filter(
            Reservation.room_id == room.id,
            Reservation.status.in_([
                ReservationStatus.CONFIRMED,
                ReservationStatus.CHECKED_IN,
                ReservationStatus.PENDING
            ]),
            or_(
                and_(
                    Reservation.check_in_date <= check_in,
                    Reservation.check_out_date > check_in
                ),
                and_(
                    Reservation.check_in_date < check_out,
                    Reservation.check_out_date >= check_out
                ),
                and_(
                    Reservation.check_in_date >= check_in,
                    Reservation.check_out_date <= check_out
                )
            )
        ).first()
        
        if not conflicting:
            available_rooms.append(room)
    
    return available_rooms


@router.post("/check-availability", response_model=List[RoomAvailabilityResponse])
def check_availability(
    availability_query: RoomAvailabilityQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Verifica disponibilidad y precios por tipo de habitación
    """
    from datetime import datetime
    
    # Convertir strings a dates
    check_in = datetime.strptime(availability_query.check_in_date, "%Y-%m-%d").date()
    check_out = datetime.strptime(availability_query.check_out_date, "%Y-%m-%d").date()
    
    # Validar fechas
    if check_out <= check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de salida debe ser posterior a la fecha de entrada"
        )
    
    total_nights = (check_out - check_in).days
    
    # Obtener todos los tipos de habitación activos
    room_types = db.query(RoomType).filter(RoomType.is_active == True).all()
    
    availability_results = []
    
    for room_type in room_types:
        # Verificar capacidad
        total_guests = availability_query.num_adults + availability_query.num_children
        if total_guests > room_type.capacity:
            continue
        
        # Contar habitaciones disponibles de este tipo
        rooms_of_type = db.query(Room).filter(
            Room.room_type_id == room_type.id,
            Room.is_active == True
        ).all()
        
        available_count = 0
        
        for room in rooms_of_type:
            # Verificar disponibilidad
            conflicting = db.query(Reservation).filter(
                Reservation.room_id == room.id,
                Reservation.status.in_([
                    ReservationStatus.CONFIRMED,
                    ReservationStatus.CHECKED_IN,
                    ReservationStatus.PENDING
                ]),
                or_(
                    and_(
                        Reservation.check_in_date <= check_in,
                        Reservation.check_out_date > check_in
                    ),
                    and_(
                        Reservation.check_in_date < check_out,
                        Reservation.check_out_date >= check_out
                    ),
                    and_(
                        Reservation.check_in_date >= check_in,
                        Reservation.check_out_date <= check_out
                    )
                )
            ).first()
            
            if not conflicting:
                available_count += 1
        
        if available_count > 0:
            availability_results.append(
                RoomAvailabilityResponse(
                    room_type_id=room_type.id,
                    room_type_name=room_type.name,
                    available_rooms=available_count,
                    price_per_night_ves=room_type.base_price_ves,
                    price_per_night_usd=room_type.base_price_usd,
                    price_per_night_eur=room_type.base_price_eur,
                    total_nights=total_nights,
                    total_price_ves=room_type.base_price_ves * total_nights,
                    total_price_usd=room_type.base_price_usd * total_nights,
                    total_price_eur=(room_type.base_price_eur * total_nights) if room_type.base_price_eur else None
                )
            )
    
    return availability_results


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene una habitación por ID
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habitación no encontrada"
        )
    return room


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    room_in: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
):
    """
    Crea una nueva habitación
    """
    # Verificar que no existe una habitación con ese número
    existing = db.query(Room).filter(Room.room_number == room_in.room_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una habitación con ese número"
        )
    
    # Verificar que el tipo de habitación existe
    room_type = db.query(RoomType).filter(RoomType.id == room_in.room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de habitación no encontrado"
        )
    
    room = Room(**room_in.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    
    return room


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    room_in: RoomUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Actualiza una habitación
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habitación no encontrada"
        )
    
    update_data = room_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(room, field, value)
    
    db.commit()
    db.refresh(room)
    
    return room


@router.put("/{room_id}/status", response_model=RoomResponse)
def change_room_status(
    room_id: int,
    status_in: RoomStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Cambia el estado de una habitación.
    Si la habitación está ocupada, verifica que no tenga reservas con check-in activo.
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habitación no encontrada"
        )
    
    # Si la habitación está ocupada y se intenta cambiar a otro estado,
    # verificar que no tenga una reserva con check-in activo
    if room.status == RoomStatus.OCCUPIED and status_in.status != RoomStatus.OCCUPIED:
        active_checkin = db.query(Reservation).filter(
            Reservation.room_id == room_id,
            Reservation.status == ReservationStatus.CHECKED_IN
        ).first()
        
        if active_checkin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede cambiar el estado. La habitación tiene una reserva activa con check-in. "
                       "Primero debe realizar el check-out de la reserva."
            )
    
    room.status = status_in.status
    db.commit()
    db.refresh(room)
    
    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Elimina una habitación (solo si no tiene reservas activas)
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habitación no encontrada"
        )
    
    # Verificar que no tenga reservas activas
    active_reservations = db.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.status.in_([
            ReservationStatus.PENDING,
            ReservationStatus.CONFIRMED,
            ReservationStatus.CHECKED_IN
        ])
    ).count()
    
    if active_reservations > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar. Hay {active_reservations} reserva(s) activa(s)"
        )
    
    db.delete(room)
    db.commit()
    
    return None