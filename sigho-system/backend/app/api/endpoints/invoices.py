"""
Endpoints de Facturación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, date, timedelta

from app.database.session import get_db
from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceResponse,
    InvoiceListResponse,
    InvoiceGenerateRequest,
    InvoiceAddItemRequest,
    InvoicePaymentRequest
)
from app.models.invoice import Invoice, InvoiceItem, InvoiceStatus, DocumentType
from app.models.reservation import Reservation
from app.models.guest import Guest
from app.models.payment import Payment, PaymentStatus
from app.models.user import User, UserRole
from app.api.dependencies.auth import get_current_active_user, require_role
from app.services.pdf_service import pdf_service

router = APIRouter()


def generate_invoice_number(db: Session) -> str:
    """Genera un número de factura único"""
    today = datetime.now()
    prefix = f"FAC-{today.strftime('%Y%m%d')}"
    
    # Buscar el último número del día
    last_invoice = db.query(Invoice).filter(
        Invoice.invoice_number.like(f"{prefix}%")
    ).order_by(desc(Invoice.id)).first()
    
    if last_invoice:
        # Extraer el número y aumentar
        try:
            last_num = int(last_invoice.invoice_number.split('-')[-1])
            new_num = last_num + 1
        except:
            new_num = 1
    else:
        new_num = 1
    
    return f"{prefix}-{new_num:04d}"


@router.get("/", response_model=List[InvoiceListResponse])
def get_invoices(
    skip: int = 0,
    limit: int = 100,
    status: Optional[InvoiceStatus] = None,
    guest_id: Optional[int] = None,
    currency: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene la lista de facturas con filtros opcionales
    """
    query = db.query(Invoice)
    
    if status:
        query = query.filter(Invoice.status == status)
    
    if guest_id:
        query = query.filter(Invoice.guest_id == guest_id)
    
    if currency:
        query = query.filter(Invoice.currency == currency)
    
    if from_date:
        query = query.filter(Invoice.created_at >= datetime.combine(from_date, datetime.min.time()))
    
    if to_date:
        query = query.filter(Invoice.created_at <= datetime.combine(to_date, datetime.max.time()))
    
    invoices = query.order_by(desc(Invoice.created_at)).offset(skip).limit(limit).all()
    return invoices


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtiene una factura por ID con sus items
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    return invoice


@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(
    invoice_in: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Crea una nueva factura
    """
    # Verificar que el huésped existe
    guest = db.query(Guest).filter(Guest.id == invoice_in.guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Huésped no encontrado"
        )
    
    # Verificar reserva si se especifica
    if invoice_in.reservation_id:
        reservation = db.query(Reservation).filter(Reservation.id == invoice_in.reservation_id).first()
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
    
    # Crear factura
    invoice = Invoice(
        invoice_number=generate_invoice_number(db),
        reservation_id=invoice_in.reservation_id,
        guest_id=invoice_in.guest_id,
        created_by=current_user.id,
        guest_document_type=invoice_in.guest_document_type,
        guest_document_number=invoice_in.guest_document_number,
        guest_name=invoice_in.guest_name,
        guest_address=invoice_in.guest_address,
        guest_phone=invoice_in.guest_phone,
        guest_email=invoice_in.guest_email,
        currency=invoice_in.currency,
        tax_percentage=invoice_in.tax_percentage,
        notes=invoice_in.notes,
        due_date=invoice_in.due_date,
        status=InvoiceStatus.DRAFT
    )
    
    db.add(invoice)
    db.flush()  # Para obtener el ID
    
    # Agregar items
    for item_data in invoice_in.items:
        subtotal = item_data.quantity * item_data.unit_price
        item = InvoiceItem(
            invoice_id=invoice.id,
            description=item_data.description,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            subtotal=subtotal
        )
        db.add(item)
    
    db.flush()
    
    # Calcular totales
    invoice.calculate_totals()
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


@router.post("/generate", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def generate_invoice_from_reservation(
    request: InvoiceGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Genera una factura a partir de una reserva existente
    """
    # Obtener reserva con relaciones
    reservation = db.query(Reservation).filter(Reservation.id == request.reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    # Obtener huésped
    guest = db.query(Guest).filter(Guest.id == reservation.guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Huésped de la reserva no encontrado"
        )
    
    # Usar datos del huésped o los proporcionados
    doc_type = request.guest_document_type or DocumentType.V
    doc_number = request.guest_document_number or guest.document_number or "N/A"
    
    # Crear factura
    invoice = Invoice(
        invoice_number=generate_invoice_number(db),
        reservation_id=reservation.id,
        guest_id=guest.id,
        created_by=current_user.id,
        guest_document_type=doc_type,
        guest_document_number=doc_number,
        guest_name=f"{guest.first_name} {guest.last_name}",
        guest_address=request.guest_address or guest.address,
        guest_phone=guest.phone,
        guest_email=guest.email,
        currency=reservation.currency,
        tax_percentage=reservation.tax_percentage,
        notes=request.notes,
        due_date=date.today() + timedelta(days=30),
        status=InvoiceStatus.DRAFT
    )
    
    db.add(invoice)
    db.flush()
    
    # Crear item de la reserva
    room = reservation.room
    room_type_name = room.room_type.name if room and room.room_type else "Habitación"
    
    item = InvoiceItem(
        invoice_id=invoice.id,
        description=f"Hospedaje - {room_type_name} (Hab. {room.room_number if room else 'N/A'}) - "
                    f"{reservation.total_nights} noche(s) ({reservation.check_in_date} al {reservation.check_out_date})",
        quantity=reservation.total_nights,
        unit_price=reservation.price_per_night,
        subtotal=reservation.subtotal
    )
    db.add(item)
    
    db.flush()
    
    # Calcular totales
    invoice.calculate_totals()
    
    # Si incluir pagos, registrar los pagos existentes
    if request.include_payments:
        payments = db.query(Payment).filter(
            Payment.reservation_id == reservation.id,
            Payment.status == PaymentStatus.COMPLETED
        ).all()
        
        paid_total = sum(p.amount for p in payments if p.currency == reservation.currency)
        invoice.paid_amount = paid_total
        invoice.balance = invoice.total_amount - paid_total
        
        if invoice.balance <= 0:
            invoice.status = InvoiceStatus.PAID
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: int,
    invoice_in: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Actualiza una factura (solo si está en estado borrador)
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if invoice.status != InvoiceStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden editar facturas en estado borrador"
        )
    
    update_data = invoice_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(invoice, field, value)
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


@router.post("/{invoice_id}/items", response_model=InvoiceResponse)
def add_invoice_item(
    invoice_id: int,
    item_in: InvoiceAddItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Agrega un item a una factura existente
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if invoice.status != InvoiceStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden agregar items a facturas en estado borrador"
        )
    
    subtotal = item_in.quantity * item_in.unit_price
    item = InvoiceItem(
        invoice_id=invoice.id,
        description=item_in.description,
        quantity=item_in.quantity,
        unit_price=item_in.unit_price,
        subtotal=subtotal
    )
    db.add(item)
    db.flush()
    
    # Recalcular totales
    invoice.calculate_totals()
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


@router.delete("/{invoice_id}/items/{item_id}", response_model=InvoiceResponse)
def remove_invoice_item(
    invoice_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Elimina un item de una factura
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if invoice.status != InvoiceStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden eliminar items de facturas en estado borrador"
        )
    
    item = db.query(InvoiceItem).filter(
        InvoiceItem.id == item_id,
        InvoiceItem.invoice_id == invoice_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    
    db.delete(item)
    db.flush()
    
    # Recalcular totales
    invoice.calculate_totals()
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


@router.put("/{invoice_id}/issue", response_model=InvoiceResponse)
def issue_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Emite una factura (cambia de borrador a emitida)
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if invoice.status != InvoiceStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden emitir facturas en estado borrador"
        )
    
    if not invoice.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La factura debe tener al menos un item"
        )
    
    invoice.status = InvoiceStatus.ISSUED
    invoice.issue_date = datetime.now()
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


@router.put("/{invoice_id}/void", response_model=InvoiceResponse)
def void_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
):
    """
    Anula una factura
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if invoice.status == InvoiceStatus.VOID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La factura ya está anulada"
        )
    
    invoice.status = InvoiceStatus.VOID
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


@router.post("/{invoice_id}/payment", response_model=InvoiceResponse)
def register_invoice_payment(
    invoice_id: int,
    payment_in: InvoicePaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.RECEPTIONIST]))
):
    """
    Registra un pago en la factura
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if invoice.status == InvoiceStatus.VOID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden registrar pagos en facturas anuladas"
        )
    
    if invoice.status == InvoiceStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Primero debe emitir la factura"
        )
    
    invoice.paid_amount += payment_in.amount
    invoice.balance = invoice.total_amount - invoice.paid_amount
    
    if invoice.balance <= 0:
        invoice.status = InvoiceStatus.PAID
    
    db.commit()
    db.refresh(invoice)
    
    return invoice


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Elimina una factura (solo si está en estado borrador)
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if invoice.status != InvoiceStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden eliminar facturas en estado borrador"
        )
    
    db.delete(invoice)
    db.commit()
    
    return None


@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Descarga el PDF de una factura
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    # Preparar datos para el PDF
    invoice_data = {
        'invoice_number': invoice.invoice_number,
        'issue_date': invoice.issue_date,
        'due_date': invoice.due_date,
        'guest_name': invoice.guest_name,
        'guest_document_type': invoice.guest_document_type.value if invoice.guest_document_type else 'V',
        'guest_document_number': invoice.guest_document_number,
        'guest_address': invoice.guest_address,
        'guest_phone': invoice.guest_phone,
        'guest_email': invoice.guest_email,
        'currency': invoice.currency,
        'items': [
            {
                'description': item.description,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'subtotal': item.subtotal
            }
            for item in invoice.items
        ],
        'subtotal': invoice.subtotal,
        'tax_percentage': invoice.tax_percentage,
        'tax_amount': invoice.tax_amount,
        'total_amount': invoice.total_amount,
        'paid_amount': invoice.paid_amount,
        'balance': invoice.balance,
        'status': invoice.status.value if invoice.status else 'draft',
        'notes': invoice.notes
    }
    
    pdf_buffer = pdf_service.generate_invoice_pdf(invoice_data)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=factura_{invoice.invoice_number}.pdf"
        }
    )


@router.get("/{invoice_id}/receipt-pdf")
def download_receipt_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Descarga el PDF de un recibo de pago para la factura
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )
    
    if invoice.paid_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La factura no tiene pagos registrados"
        )
    
    # Datos del pago
    payment_data = {
        'payment_code': f"REC-{invoice.invoice_number}",
        'amount': invoice.paid_amount,
        'currency': invoice.currency,
        'payment_method': 'other',
        'payment_date': invoice.updated_at or invoice.created_at,
        'reference_number': None,
        'notes': None
    }
    
    # Datos de la factura
    invoice_data = {
        'invoice_number': invoice.invoice_number,
        'guest_name': invoice.guest_name,
        'guest_document_type': invoice.guest_document_type.value if invoice.guest_document_type else 'V',
        'guest_document_number': invoice.guest_document_number
    }
    
    pdf_buffer = pdf_service.generate_receipt_pdf(payment_data, invoice_data)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=recibo_{invoice.invoice_number}.pdf"
        }
    )
