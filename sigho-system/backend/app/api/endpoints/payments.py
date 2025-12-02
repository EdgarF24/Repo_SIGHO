"""
Endpoints de Pagos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random
import string
from app.database.session import get_db
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.models.payment import Payment, PaymentStatus
from app.models.reservation import Reservation, ReservationStatus
from app.models.user import User, UserRole
from app.api.dependencies.auth import get_current_active_user, require_role

router = APIRouter()


def generate_payment_code() -> str:
    """Genera un código de pago único"""
    return 'PAY-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


@router.get("/", response_model=List[PaymentResponse])
def get_payments(
    skip: int = 0,
    limit: int = 100,
    reservation_id: int = None,
    status: PaymentStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la lista de pagos con filtros opcionales
    """
    query = db.query(Payment)
    
    if reservation_id:
        query = query.filter(Payment.reservation_id == reservation_id)
    
    if status:
        query = query.filter(Payment.status == status)
    
    query = query.order_by(Payment.created_at.desc())
    payments = query.offset(skip).limit(limit).all()
    
    return payments


@router.get("/reservation/{reservation_id}", response_model=List[PaymentResponse])
def get_payments_by_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene todos los pagos de una reserva
    """
    # Verificar que la reserva existe
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    payments = db.query(Payment).filter(
        Payment.reservation_id == reservation_id
    ).order_by(Payment.payment_date.desc()).all()
    
    return payments


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene un pago por ID
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )
    return payment


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Registra un nuevo pago
    """
    # Verificar que la reserva existe
    reservation = db.query(Reservation).filter(
        Reservation.id == payment_in.reservation_id
    ).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Verificar que la reserva no esté cancelada o completada
    if reservation.status in [ReservationStatus.CANCELLED, ReservationStatus.CHECKED_OUT]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden registrar pagos en reservas canceladas o completadas"
        )
    
    # Verificar que el monto no exceda el balance pendiente
    if payment_in.amount > reservation.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El monto excede el balance pendiente ({reservation.balance} {reservation.currency})"
        )
    
    # Generar código de pago único
    payment_code = generate_payment_code()
    while db.query(Payment).filter(Payment.payment_code == payment_code).first():
        payment_code = generate_payment_code()
    
    # Crear pago
    payment = Payment(
        payment_code=payment_code,
        reservation_id=payment_in.reservation_id,
        processed_by=current_user.id,
        amount=payment_in.amount,
        currency=payment_in.currency,
        payment_method=payment_in.payment_method,
        status=PaymentStatus.COMPLETED,
        reference_number=payment_in.reference_number,
        bank_name=payment_in.bank_name,
        account_number=payment_in.account_number,
        notes=payment_in.notes
    )
    
    db.add(payment)
    
    # Actualizar el balance de la reserva
    reservation.paid_amount += payment_in.amount
    reservation.balance = reservation.total_amount - reservation.paid_amount
    
    # Si el balance es 0, marcar como pagado
    if reservation.balance <= 0:
        reservation.is_paid = True
        reservation.balance = 0  # Asegurar que no quede negativo
    
    # Si la reserva está pendiente, cambiarla a confirmada
    if reservation.status == ReservationStatus.PENDING and reservation.paid_amount > 0:
        reservation.status = ReservationStatus.CONFIRMED
    
    db.commit()
    db.refresh(payment)
    
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment_in: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
):
    """
    Actualiza un pago (solo para correcciones administrativas)
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )
    
    update_data = payment_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(payment, field, value)
    
    db.commit()
    db.refresh(payment)
    
    return payment


@router.post("/{payment_id}/refund", response_model=PaymentResponse)
def refund_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
):
    """
    Reembolsa un pago
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )
    
    if payment.status == PaymentStatus.REFUNDED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El pago ya fue reembolsado"
        )
    
    if payment.status != PaymentStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden reembolsar pagos completados"
        )
    
    # Actualizar el pago
    payment.status = PaymentStatus.REFUNDED
    
    # Actualizar el balance de la reserva
    reservation = db.query(Reservation).filter(
        Reservation.id == payment.reservation_id
    ).first()
    
    reservation.paid_amount -= payment.amount
    reservation.balance = reservation.total_amount - reservation.paid_amount
    reservation.is_paid = False
    
    db.commit()
    db.refresh(payment)
    
    return payment


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Elimina un pago (solo admin y solo si está en estado pendiente)
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )
    
    if payment.status not in [PaymentStatus.PENDING, PaymentStatus.FAILED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden eliminar pagos pendientes o fallidos"
        )
    
    # Si el pago afectó el balance, revertirlo
    if payment.status == PaymentStatus.COMPLETED:
        reservation = db.query(Reservation).filter(
            Reservation.id == payment.reservation_id
        ).first()
        reservation.paid_amount -= payment.amount
        reservation.balance = reservation.total_amount - reservation.paid_amount
        reservation.is_paid = False
    
    db.delete(payment)
    db.commit()
    
    return None