"""
Endpoints de Reservas
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime, date
import random
import string
from app.database.session import get_db
from app.schemas.reservation import (
    ReservationCreate, 
    ReservationUpdate, 
    ReservationResponse,
    ReservationCheckIn,
    ReservationCheckOut,
    ReservationCancel,
    ReservationSearchFilters
)
from app.models.reservation import Reservation, ReservationStatus
from app.models.room import Room, RoomStatus
from app.models.guest import Guest
from app.models.user import User, UserRole
from app.api.dependencies.auth import get_current_active_user, require_role

router = APIRouter()


def generate_confirmation_code() -> str:
    """Genera un código de confirmación único"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def calculate_reservation_prices(
    room: Room,
    check_in: date,
    check_out: date,
    currency: str
) -> dict:
    """Calcula los precios de la reserva"""
    # Calcular noches
    total_nights = (check_out - check_in).days
    if total_nights <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de salida debe ser posterior a la fecha de entrada"
        )
    
    # Obtener precio por noche según la moneda
    if currency == "VES":
        price_per_night = room.room_type.base_price_ves
    elif currency == "USD":
        price_per_night = room.room_type.base_price_usd
    elif currency == "EUR":
        price_per_night = room.room_type.base_price_eur or room.room_type.base_price_usd * 0.92
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Moneda no válida"
        )
    
    # Calcular subtotal
    subtotal = price_per_night * total_nights
    
    # Calcular impuestos (16% IVA)
    tax_percentage = 16.0
    tax_amount = subtotal * (tax_percentage / 100)
    
    # Total
    total_amount = subtotal + tax_amount
    
    return {
        "price_per_night": price_per_night,
        "total_nights": total_nights,
        "subtotal": subtotal,
        "tax_percentage": tax_percentage,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "balance": total_amount
    }


def check_room_availability(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
    exclude_reservation_id: Optional[int] = None
) -> bool:
    """Verifica si una habitación está disponible en las fechas dadas"""
    query = db.query(Reservation).filter(
        Reservation.room_id == room_id,
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
    )
    
    if exclude_reservation_id:
        query = query.filter(Reservation.id != exclude_reservation_id)
    
    conflicting_reservation = query.first()
    return conflicting_reservation is None


@router.get("/", response_model=List[ReservationResponse])
def get_reservations(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ReservationStatus] = None,
    check_in_date_from: Optional[date] = None,
    check_in_date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la lista de reservas con filtros opcionales
    """
    query = db.query(Reservation)
    
    # Aplicar filtros
    if status:
        query = query.filter(Reservation.status == status)
    
    if check_in_date_from:
        query = query.filter(Reservation.check_in_date >= check_in_date_from)
    
    if check_in_date_to:
        query = query.filter(Reservation.check_in_date <= check_in_date_to)
    
    # Ordenar por fecha de creación descendente
    query = query.order_by(Reservation.created_at.desc())
    
    reservations = query.offset(skip).limit(limit).all()
    return reservations


@router.get("/today", response_model=List[ReservationResponse])
def get_today_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene las reservas de hoy (check-ins y check-outs)
    """
    today = date.today()
    
    reservations = db.query(Reservation).filter(
        or_(
            Reservation.check_in_date == today,
            Reservation.check_out_date == today
        ),
        Reservation.status.in_([
            ReservationStatus.CONFIRMED,
            ReservationStatus.CHECKED_IN
        ])
    ).all()
    
    return reservations


@router.get("/search", response_model=List[ReservationResponse])
def search_reservations(
    query: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Busca reservas por código de confirmación, nombre de huésped o número de habitación
    """
    # Buscar por código de confirmación
    by_code = db.query(Reservation).filter(
        Reservation.confirmation_code.ilike(f"%{query}%")
    )
    
    # Buscar por nombre de huésped
    by_guest = db.query(Reservation).join(Guest).filter(
        or_(
            Guest.first_name.ilike(f"%{query}%"),
            Guest.last_name.ilike(f"%{query}%"),
            Guest.id_number.ilike(f"%{query}%")
        )
    )
    
    # Buscar por número de habitación
    by_room = db.query(Reservation).join(Room).filter(
        Room.room_number.ilike(f"%{query}%")
    )
    
    # Combinar resultados
    results = by_code.union(by_guest, by_room).all()
    
    return results


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene una reserva por ID
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    return reservation


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_in: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Crea una nueva reserva
    """
    # Verificar que el huésped existe
    guest = db.query(Guest).filter(Guest.id == reservation_in.guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Huésped no encontrado"
        )
    
    # Verificar que la habitación existe
    room = db.query(Room).filter(Room.id == reservation_in.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habitación no encontrada"
        )
    
    # Verificar que la habitación está activa
    if not room.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La habitación no está disponible"
        )
    
    # Verificar capacidad
    total_guests = reservation_in.num_adults + reservation_in.num_children
    if total_guests > room.room_type.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La habitación solo tiene capacidad para {room.room_type.capacity} personas"
        )
    
    # Verificar disponibilidad
    if not check_room_availability(
        db,
        reservation_in.room_id,
        reservation_in.check_in_date,
        reservation_in.check_out_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La habitación no está disponible en las fechas seleccionadas"
        )
    
    # Calcular precios
    prices = calculate_reservation_prices(
        room,
        reservation_in.check_in_date,
        reservation_in.check_out_date,
        reservation_in.currency
    )
    
    # Generar código de confirmación único
    confirmation_code = generate_confirmation_code()
    while db.query(Reservation).filter(Reservation.confirmation_code == confirmation_code).first():
        confirmation_code = generate_confirmation_code()
    
    # Crear reserva
    reservation = Reservation(
        confirmation_code=confirmation_code,
        guest_id=reservation_in.guest_id,
        room_id=reservation_in.room_id,
        created_by=current_user.id,
        check_in_date=reservation_in.check_in_date,
        check_out_date=reservation_in.check_out_date,
        num_adults=reservation_in.num_adults,
        num_children=reservation_in.num_children,
        currency=reservation_in.currency,
        special_requests=reservation_in.special_requests,
        **prices
    )
    
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    
    return reservation


@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(
    reservation_id: int,
    reservation_in: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Actualiza una reserva
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # No permitir actualizar reservas canceladas o completadas
    if reservation.status in [ReservationStatus.CANCELLED, ReservationStatus.CHECKED_OUT]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede actualizar una reserva cancelada o completada"
        )
    
    update_data = reservation_in.model_dump(exclude_unset=True)
    
    # Si se actualizan las fechas, recalcular precios y verificar disponibilidad
    if "check_in_date" in update_data or "check_out_date" in update_data:
        new_check_in = update_data.get("check_in_date", reservation.check_in_date)
        new_check_out = update_data.get("check_out_date", reservation.check_out_date)
        
        # Verificar disponibilidad
        if not check_room_availability(
            db,
            reservation.room_id,
            new_check_in,
            new_check_out,
            exclude_reservation_id=reservation_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La habitación no está disponible en las nuevas fechas"
            )
        
        # Recalcular precios
        room = db.query(Room).filter(Room.id == reservation.room_id).first()
        prices = calculate_reservation_prices(
            room,
            new_check_in,
            new_check_out,
            reservation.currency
        )
        
        # Actualizar balance
        prices["balance"] = prices["total_amount"] - reservation.paid_amount
        update_data.update(prices)
    
    # Actualizar campos
    for field, value in update_data.items():
        setattr(reservation, field, value)
    
    db.commit()
    db.refresh(reservation)
    
    return reservation


@router.post("/{reservation_id}/check-in", response_model=ReservationResponse)
def check_in_reservation(
    reservation_id: int,
    check_in_data: ReservationCheckIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Realiza el check-in de una reserva
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Verificar que la reserva esté confirmada
    if reservation.status != ReservationStatus.CONFIRMED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se puede hacer check-in de reservas confirmadas"
        )
    
    # Verificar que el pago esté completo o parcial
    if reservation.paid_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe registrar al menos un pago antes del check-in"
        )
    
    # Actualizar reserva
    reservation.status = ReservationStatus.CHECKED_IN
    reservation.actual_check_in = datetime.utcnow()
    if check_in_data.notes:
        reservation.notes = check_in_data.notes
    
    # Actualizar estado de la habitación
    room = db.query(Room).filter(Room.id == reservation.room_id).first()
    room.status = RoomStatus.OCCUPIED
    
    db.commit()
    db.refresh(reservation)
    
    return reservation


@router.post("/{reservation_id}/check-out", response_model=ReservationResponse)
def check_out_reservation(
    reservation_id: int,
    check_out_data: ReservationCheckOut,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Realiza el check-out de una reserva
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Verificar que la reserva tenga check-in
    if reservation.status != ReservationStatus.CHECKED_IN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se puede hacer check-out de reservas con check-in"
        )
    
    # Verificar que el pago esté completo
    if reservation.balance > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe completar el pago antes del check-out"
        )
    
    # Actualizar reserva
    reservation.status = ReservationStatus.CHECKED_OUT
    reservation.actual_check_out = datetime.utcnow()
    if check_out_data.notes:
        reservation.notes = f"{reservation.notes or ''}\n{check_out_data.notes}".strip()
    
    # Actualizar estado de la habitación
    room = db.query(Room).filter(Room.id == reservation.room_id).first()
    room.status = RoomStatus.CLEANING
    
    db.commit()
    db.refresh(reservation)
    
    return reservation


@router.post("/{reservation_id}/cancel", response_model=ReservationResponse)
def cancel_reservation(
    reservation_id: int,
    cancel_data: ReservationCancel,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Cancela una reserva
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # No permitir cancelar reservas ya completadas
    if reservation.status == ReservationStatus.CHECKED_OUT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede cancelar una reserva completada"
        )
    
    # Actualizar reserva
    reservation.status = ReservationStatus.CANCELLED
    reservation.cancellation_reason = cancel_data.cancellation_reason
    
    # Si la habitación estaba ocupada, cambiar a limpieza
    room = db.query(Room).filter(Room.id == reservation.room_id).first()
    if room.status == RoomStatus.OCCUPIED:
        room.status = RoomStatus.CLEANING
    
    db.commit()
    db.refresh(reservation)
    
    return reservation


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Elimina una reserva (solo admin y solo si está pendiente o cancelada)
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Solo permitir eliminar reservas pendientes o canceladas
    if reservation.status not in [ReservationStatus.PENDING, ReservationStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden eliminar reservas pendientes o canceladas"
        )
    
    db.delete(reservation)
    db.commit()
    
    return None