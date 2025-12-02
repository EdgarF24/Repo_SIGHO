"""
Endpoints de Reportes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date, datetime, timedelta
from typing import Dict, Any, List, Optional
from app.database.session import get_db
from app.models.reservation import Reservation, ReservationStatus
from app.models.room import Room, RoomStatus
from app.models.room_type import RoomType
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.models.maintenance import Maintenance, MaintenanceStatus
from app.models.inventory import Inventory, InventoryCategory
from app.models.inventory_movement import InventoryMovement, MovementType
from app.models.guest import Guest
from app.models.user import User, UserRole
from app.api.dependencies.auth import get_current_active_user, require_role

router = APIRouter()


@router.get("/reservations")
def generate_reservations_report(
    start_date: date,
    end_date: date,
    status: Optional[ReservationStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Genera un reporte de reservas en un período
    """
    query = db.query(Reservation).filter(
        Reservation.check_in_date >= start_date,
        Reservation.check_in_date <= end_date
    )
    
    if status:
        query = query.filter(Reservation.status == status)
    
    reservations = query.all()
    
    # Estadísticas
    total_reservations = len(reservations)
    total_revenue_usd = sum(r.total_amount for r in reservations if r.currency == "USD")
    total_revenue_ves = sum(r.total_amount for r in reservations if r.currency == "VES")
    total_paid_usd = sum(r.paid_amount for r in reservations if r.currency == "USD")
    total_paid_ves = sum(r.paid_amount for r in reservations if r.currency == "VES")
    
    # Agrupar por estado
    by_status = {}
    for res_status in ReservationStatus:
        count = sum(1 for r in reservations if r.status == res_status)
        by_status[res_status.value] = count
    
    # Promedio de noches
    avg_nights = sum(r.total_nights for r in reservations) / total_reservations if total_reservations > 0 else 0
    
    # Tasa de ocupación promedio
    total_rooms = db.query(Room).filter(Room.is_active == True).count()
    days_in_period = (end_date - start_date).days + 1
    max_room_nights = total_rooms * days_in_period
    occupied_room_nights = sum(r.total_nights for r in reservations if r.status in [ReservationStatus.CHECKED_IN, ReservationStatus.CHECKED_OUT])
    avg_occupancy = (occupied_room_nights / max_room_nights * 100) if max_room_nights > 0 else 0
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days_in_period
        },
        "summary": {
            "total_reservations": total_reservations,
            "total_revenue_usd": round(total_revenue_usd, 2),
            "total_revenue_ves": round(total_revenue_ves, 2),
            "total_paid_usd": round(total_paid_usd, 2),
            "total_paid_ves": round(total_paid_ves, 2),
            "avg_nights_per_reservation": round(avg_nights, 2),
            "avg_occupancy_rate": round(avg_occupancy, 2)
        },
        "by_status": by_status,
        "reservations": [
            {
                "id": r.id,
                "confirmation_code": r.confirmation_code,
                "guest_id": r.guest_id,
                "room_id": r.room_id,
                "check_in_date": r.check_in_date.isoformat(),
                "check_out_date": r.check_out_date.isoformat(),
                "total_nights": r.total_nights,
                "status": r.status.value,
                "total_amount": r.total_amount,
                "paid_amount": r.paid_amount,
                "balance": r.balance,
                "currency": r.currency
            }
            for r in reservations
        ]
    }


@router.get("/revenue")
def generate_revenue_report(
    start_date: date,
    end_date: date,
    currency: Optional[str] = None,
    payment_method: Optional[PaymentMethod] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
) -> Dict[str, Any]:
    """
    Genera un reporte de ingresos
    """
    query = db.query(Payment).filter(
        Payment.status == PaymentStatus.COMPLETED,
        func.date(Payment.payment_date) >= start_date,
        func.date(Payment.payment_date) <= end_date
    )
    
    if currency:
        query = query.filter(Payment.currency == currency)
    
    if payment_method:
        query = query.filter(Payment.payment_method == payment_method)
    
    payments = query.all()
    
    # Agrupar por moneda
    by_currency = {}
    for payment in payments:
        if payment.currency not in by_currency:
            by_currency[payment.currency] = 0
        by_currency[payment.currency] += payment.amount
    
    # Agrupar por método de pago
    by_payment_method = {}
    for method in PaymentMethod:
        amount = sum(p.amount for p in payments if p.payment_method == method)
        if amount > 0:
            by_payment_method[method.value] = round(amount, 2)
    
    # Ingresos por día
    daily_revenue = {}
    for payment in payments:
        payment_date = payment.payment_date.date()
        date_str = payment_date.isoformat()
        if date_str not in daily_revenue:
            daily_revenue[date_str] = {"VES": 0, "USD": 0, "EUR": 0}
        daily_revenue[date_str][payment.currency] += payment.amount
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        },
        "summary": {
            "total_payments": len(payments),
            "by_currency": {k: round(v, 2) for k, v in by_currency.items()},
            "by_payment_method": by_payment_method
        },
        "daily_revenue": [
            {
                "date": date_str,
                "ves": round(amounts["VES"], 2),
                "usd": round(amounts["USD"], 2),
                "eur": round(amounts["EUR"], 2)
            }
            for date_str, amounts in sorted(daily_revenue.items())
        ]
    }


@router.get("/occupancy")
def generate_occupancy_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Genera un reporte de ocupación
    """
    total_rooms = db.query(Room).filter(Room.is_active == True).count()
    days_in_period = (end_date - start_date).days + 1
    
    daily_occupancy = []
    
    for i in range(days_in_period):
        current_date = start_date + timedelta(days=i)
        
        # Contar habitaciones ocupadas
        occupied = db.query(Reservation).filter(
            Reservation.status.in_([ReservationStatus.CHECKED_IN, ReservationStatus.CHECKED_OUT]),
            Reservation.check_in_date <= current_date,
            Reservation.check_out_date > current_date
        ).count()
        
        occupancy_rate = (occupied / total_rooms * 100) if total_rooms > 0 else 0
        
        daily_occupancy.append({
            "date": current_date.isoformat(),
            "occupied_rooms": occupied,
            "available_rooms": total_rooms - occupied,
            "occupancy_rate": round(occupancy_rate, 2)
        })
    
    # Promedios
    avg_occupied = sum(d["occupied_rooms"] for d in daily_occupancy) / days_in_period
    avg_occupancy_rate = sum(d["occupancy_rate"] for d in daily_occupancy) / days_in_period
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days_in_period
        },
        "summary": {
            "total_rooms": total_rooms,
            "avg_occupied_rooms": round(avg_occupied, 2),
            "avg_occupancy_rate": round(avg_occupancy_rate, 2)
        },
        "daily_data": daily_occupancy
    }


@router.get("/maintenance")
def generate_maintenance_report(
    start_date: date,
    end_date: date,
    status: Optional[MaintenanceStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Genera un reporte de mantenimiento
    """
    query = db.query(Maintenance).filter(
        Maintenance.created_at >= datetime.combine(start_date, datetime.min.time()),
        Maintenance.created_at <= datetime.combine(end_date, datetime.max.time())
    )
    
    if status:
        query = query.filter(Maintenance.status == status)
    
    maintenance_records = query.all()
    
    # Estadísticas
    total_records = len(maintenance_records)
    
    # Agrupar por estado
    by_status = {}
    for mnt_status in MaintenanceStatus:
        count = sum(1 for m in maintenance_records if m.status == mnt_status)
        by_status[mnt_status.value] = count
    
    # Costos
    total_estimated_cost = sum(m.estimated_cost or 0 for m in maintenance_records)
    total_actual_cost = sum(m.actual_cost or 0 for m in maintenance_records if m.actual_cost)
    
    # Tiempo promedio de resolución (para completadas)
    completed = [m for m in maintenance_records if m.status == MaintenanceStatus.COMPLETED and m.started_at and m.completed_at]
    if completed:
        avg_resolution_time = sum((m.completed_at - m.started_at).total_seconds() / 3600 for m in completed) / len(completed)
    else:
        avg_resolution_time = 0
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        },
        "summary": {
            "total_records": total_records,
            "by_status": by_status,
            "total_estimated_cost": round(total_estimated_cost, 2),
            "total_actual_cost": round(total_actual_cost, 2),
            "avg_resolution_time_hours": round(avg_resolution_time, 2)
        },
        "records": [
            {
                "id": m.id,
                "maintenance_code": m.maintenance_code,
                "room_id": m.room_id,
                "title": m.title,
                "status": m.status.value,
                "priority": m.priority.value,
                "estimated_cost": m.estimated_cost,
                "actual_cost": m.actual_cost,
                "created_at": m.created_at.isoformat()
            }
            for m in maintenance_records
        ]
    }


@router.get("/inventory")
def generate_inventory_report(
    category: Optional[InventoryCategory] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Genera un reporte de inventario
    """
    query = db.query(Inventory).filter(Inventory.is_active == True)
    
    if category:
        query = query.filter(Inventory.category == category)
    
    items = query.all()
    
    # Estadísticas
    total_items = len(items)
    low_stock_items = sum(1 for item in items if item.needs_restock)
    total_value_ves = sum(item.total_value for item in items if item.currency == "VES")
    total_value_usd = sum(item.total_value for item in items if item.currency == "USD")
    
    # Agrupar por categoría
    by_category = {}
    for cat in InventoryCategory:
        category_items = [item for item in items if item.category == cat]
        if category_items:
            by_category[cat.value] = {
                "count": len(category_items),
                "total_value_ves": round(sum(i.total_value for i in category_items if i.currency == "VES"), 2),
                "total_value_usd": round(sum(i.total_value for i in category_items if i.currency == "USD"), 2)
            }
    
    return {
        "summary": {
            "total_items": total_items,
            "low_stock_items": low_stock_items,
            "total_value_ves": round(total_value_ves, 2),
            "total_value_usd": round(total_value_usd, 2)
        },
        "by_category": by_category,
        "items": [
            {
                "id": item.id,
                "item_code": item.item_code,
                "name": item.name,
                "category": item.category.value,
                "current_quantity": item.current_quantity,
                "minimum_quantity": item.minimum_quantity,
                "needs_restock": item.needs_restock,
                "unit_cost": item.unit_cost,
                "total_value": item.total_value,
                "currency": item.currency
            }
            for item in items
        ]
    }


@router.get("/guests")
def generate_guests_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Genera un reporte de huéspedes
    """
    guests = db.query(Guest).all()
    
    # Estadísticas
    total_guests = len(guests)
    
    # Agrupar por país
    by_country = {}
    for guest in guests:
        country = guest.country or "Unknown"
        by_country[country] = by_country.get(country, 0) + 1
    
    # Top huéspedes por número de reservas
    top_guests = db.query(
        Guest,
        func.count(Reservation.id).label('reservation_count')
    ).join(
        Reservation, Reservation.guest_id == Guest.id
    ).group_by(
        Guest.id
    ).order_by(
        func.count(Reservation.id).desc()
    ).limit(10).all()
    
    return {
        "summary": {
            "total_guests": total_guests,
            "by_country": by_country
        },
        "top_guests": [
            {
                "id": guest.id,
                "full_name": guest.full_name,
                "id_number": guest.id_number,
                "reservation_count": count
            }
            for guest, count in top_guests
        ]
    }