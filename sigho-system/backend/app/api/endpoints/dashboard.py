"""
Endpoints de Dashboard (Estadísticas y Métricas)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import date, datetime, timedelta
from typing import Dict, Any
from app.database.session import get_db
from app.models.reservation import Reservation, ReservationStatus
from app.models.room import Room, RoomStatus
from app.models.payment import Payment, PaymentStatus
from app.models.maintenance import Maintenance, MaintenanceStatus
from app.models.inventory import Inventory
from app.models.guest import Guest
from app.models.user import User
from app.api.dependencies.auth import get_current_active_user

router = APIRouter()


@router.get("/overview")
def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Obtiene un resumen general del estado del hotel
    """
    today = date.today()
    
    # Estadísticas de habitaciones
    total_rooms = db.query(Room).filter(Room.is_active == True).count()
    available_rooms = db.query(Room).filter(
        Room.is_active == True,
        Room.status == RoomStatus.AVAILABLE
    ).count()
    occupied_rooms = db.query(Room).filter(
        Room.status == RoomStatus.OCCUPIED
    ).count()
    cleaning_rooms = db.query(Room).filter(
        Room.status == RoomStatus.CLEANING
    ).count()
    maintenance_rooms = db.query(Room).filter(
        Room.status.in_([RoomStatus.MAINTENANCE, RoomStatus.OUT_OF_SERVICE])
    ).count()
    
    # Calcular ocupación
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    # Reservas de hoy
    today_checkins = db.query(Reservation).filter(
        Reservation.check_in_date == today,
        Reservation.status.in_([ReservationStatus.CONFIRMED, ReservationStatus.PENDING])
    ).count()
    
    today_checkouts = db.query(Reservation).filter(
        Reservation.check_out_date == today,
        Reservation.status == ReservationStatus.CHECKED_IN
    ).count()
    
    # Reservas activas
    active_reservations = db.query(Reservation).filter(
        Reservation.status.in_([
            ReservationStatus.CONFIRMED,
            ReservationStatus.CHECKED_IN
        ])
    ).count()
    
    # Reservas pendientes
    pending_reservations = db.query(Reservation).filter(
        Reservation.status == ReservationStatus.PENDING
    ).count()
    
    # Mantenimiento pendiente
    pending_maintenance = db.query(Maintenance).filter(
        Maintenance.status == MaintenanceStatus.PENDING
    ).count()
    
    in_progress_maintenance = db.query(Maintenance).filter(
        Maintenance.status == MaintenanceStatus.IN_PROGRESS
    ).count()
    
    # Inventario bajo
    low_stock_items = db.query(Inventory).filter(
        Inventory.current_quantity <= Inventory.minimum_quantity,
        Inventory.is_active == True
    ).count()
    
    # Ingresos del mes actual
    first_day_of_month = today.replace(day=1)
    monthly_revenue = db.query(func.sum(Payment.amount)).filter(
        Payment.status == PaymentStatus.COMPLETED,
        Payment.payment_date >= first_day_of_month,
        Payment.currency == "USD"  # Puedes ajustar esto
    ).scalar() or 0
    
    # Ingresos de hoy
    today_revenue = db.query(func.sum(Payment.amount)).filter(
        Payment.status == PaymentStatus.COMPLETED,
        func.date(Payment.payment_date) == today,
        Payment.currency == "USD"
    ).scalar() or 0
    
    return {
        "rooms": {
            "total": total_rooms,
            "available": available_rooms,
            "occupied": occupied_rooms,
            "cleaning": cleaning_rooms,
            "maintenance": maintenance_rooms,
            "occupancy_rate": round(occupancy_rate, 2)
        },
        "reservations": {
            "today_checkins": today_checkins,
            "today_checkouts": today_checkouts,
            "active": active_reservations,
            "pending": pending_reservations
        },
        "maintenance": {
            "pending": pending_maintenance,
            "in_progress": in_progress_maintenance
        },
        "inventory": {
            "low_stock_items": low_stock_items
        },
        "revenue": {
            "today": round(today_revenue, 2),
            "monthly": round(monthly_revenue, 2)
        }
    }


@router.get("/occupancy-rate")
def get_occupancy_rate(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Obtiene la tasa de ocupación de los últimos N días
    """
    today = date.today()
    start_date = today - timedelta(days=days)
    
    total_rooms = db.query(Room).filter(Room.is_active == True).count()
    
    occupancy_data = []
    
    for i in range(days + 1):
        current_date = start_date + timedelta(days=i)
        
        # Contar habitaciones ocupadas en esa fecha
        occupied = db.query(Reservation).filter(
            Reservation.status.in_([ReservationStatus.CONFIRMED, ReservationStatus.CHECKED_IN]),
            Reservation.check_in_date <= current_date,
            Reservation.check_out_date > current_date
        ).count()
        
        rate = (occupied / total_rooms * 100) if total_rooms > 0 else 0
        
        occupancy_data.append({
            "date": current_date.isoformat(),
            "occupied_rooms": occupied,
            "occupancy_rate": round(rate, 2)
        })
    
    return {
        "period": f"Last {days} days",
        "total_rooms": total_rooms,
        "data": occupancy_data
    }


@router.get("/revenue-by-period")
def get_revenue_by_period(
    days: int = 30,
    currency: str = "USD",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Obtiene los ingresos por período
    """
    today = date.today()
    start_date = today - timedelta(days=days)
    
    # Ingresos por día
    daily_revenue = []
    
    for i in range(days + 1):
        current_date = start_date + timedelta(days=i)
        
        revenue = db.query(func.sum(Payment.amount)).filter(
            Payment.status == PaymentStatus.COMPLETED,
            func.date(Payment.payment_date) == current_date,
            Payment.currency == currency
        ).scalar() or 0
        
        daily_revenue.append({
            "date": current_date.isoformat(),
            "revenue": round(revenue, 2)
        })
    
    # Total del período
    total_revenue = db.query(func.sum(Payment.amount)).filter(
        Payment.status == PaymentStatus.COMPLETED,
        Payment.payment_date >= start_date,
        Payment.currency == currency
    ).scalar() or 0
    
    return {
        "period": f"Last {days} days",
        "currency": currency,
        "total_revenue": round(total_revenue, 2),
        "daily_data": daily_revenue
    }


@router.get("/reservations-by-status")
def get_reservations_by_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, int]:
    """
    Obtiene el número de reservas por estado
    """
    status_counts = {}
    
    for status in ReservationStatus:
        count = db.query(Reservation).filter(Reservation.status == status).count()
        status_counts[status.value] = count
    
    return status_counts


@router.get("/top-room-types")
def get_top_room_types(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> list:
    """
    Obtiene los tipos de habitación más reservados
    """
    from app.models.room_type import RoomType
    
    # Contar reservas por tipo de habitación
    results = db.query(
        RoomType.name,
        func.count(Reservation.id).label('reservation_count')
    ).join(
        Room, Room.room_type_id == RoomType.id
    ).join(
        Reservation, Reservation.room_id == Room.id
    ).filter(
        Reservation.status.in_([
            ReservationStatus.CONFIRMED,
            ReservationStatus.CHECKED_IN,
            ReservationStatus.CHECKED_OUT
        ])
    ).group_by(
        RoomType.id, RoomType.name
    ).order_by(
        func.count(Reservation.id).desc()
    ).limit(limit).all()
    
    return [
        {"room_type": name, "reservations": count}
        for name, count in results
    ]


@router.get("/upcoming-events")
def get_upcoming_events(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Obtiene eventos próximos (check-ins, check-outs, mantenimiento)
    """
    today = date.today()
    end_date = today + timedelta(days=days)
    
    # Próximos check-ins
    upcoming_checkins = db.query(Reservation).filter(
        Reservation.check_in_date >= today,
        Reservation.check_in_date <= end_date,
        Reservation.status.in_([ReservationStatus.CONFIRMED, ReservationStatus.PENDING])
    ).order_by(Reservation.check_in_date).all()
    
    # Próximos check-outs
    upcoming_checkouts = db.query(Reservation).filter(
        Reservation.check_out_date >= today,
        Reservation.check_out_date <= end_date,
        Reservation.status == ReservationStatus.CHECKED_IN
    ).order_by(Reservation.check_out_date).all()
    
    # Mantenimiento programado
    scheduled_maintenance = db.query(Maintenance).filter(
        Maintenance.scheduled_date >= today,
        Maintenance.scheduled_date <= end_date,
        Maintenance.status.in_([MaintenanceStatus.PENDING, MaintenanceStatus.IN_PROGRESS])
    ).order_by(Maintenance.scheduled_date).all()
    
    return {
        "period": f"Next {days} days",
        "checkins": [
            {
                "id": res.id,
                "confirmation_code": res.confirmation_code,
                "date": res.check_in_date.isoformat(),
                "guest_id": res.guest_id,
                "room_id": res.room_id
            }
            for res in upcoming_checkins
        ],
        "checkouts": [
            {
                "id": res.id,
                "confirmation_code": res.confirmation_code,
                "date": res.check_out_date.isoformat(),
                "guest_id": res.guest_id,
                "room_id": res.room_id
            }
            for res in upcoming_checkouts
        ],
        "maintenance": [
            {
                "id": mnt.id,
                "maintenance_code": mnt.maintenance_code,
                "date": mnt.scheduled_date.isoformat() if mnt.scheduled_date else None,
                "title": mnt.title,
                "priority": mnt.priority.value,
                "room_id": mnt.room_id
            }
            for mnt in scheduled_maintenance
        ]
    }


@router.get("/statistics")
def get_general_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Obtiene estadísticas generales del sistema
    """
    return {
        "total_rooms": db.query(Room).count(),
        "total_guests": db.query(Guest).count(),
        "total_reservations": db.query(Reservation).count(),
        "total_users": db.query(User).count(),
        "total_inventory_items": db.query(Inventory).count(),
        "completed_reservations": db.query(Reservation).filter(
            Reservation.status == ReservationStatus.CHECKED_OUT
        ).count(),
        "total_revenue_usd": round(
            db.query(func.sum(Payment.amount)).filter(
                Payment.status == PaymentStatus.COMPLETED,
                Payment.currency == "USD"
            ).scalar() or 0,
            2
        ),
        "total_revenue_ves": round(
            db.query(func.sum(Payment.amount)).filter(
                Payment.status == PaymentStatus.COMPLETED,
                Payment.currency == "VES"
            ).scalar() or 0,
            2
        )
    }