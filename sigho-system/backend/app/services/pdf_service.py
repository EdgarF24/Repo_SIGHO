"""
Servicio de Generación de PDFs para Facturas y Recibos
"""
from io import BytesIO
from datetime import datetime
from typing import Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


class PDFService:
    """Servicio para generar PDFs de facturas y recibos"""
    
    # Información del hotel (puede ser configurada)
    HOTEL_NAME = "SIGHO Hotel"
    HOTEL_ADDRESS = "Dirección del Hotel"
    HOTEL_PHONE = "+58 XXX XXX XXXX"
    HOTEL_EMAIL = "info@sighohotel.com"
    HOTEL_RIF = "J-XXXXXXXX-X"
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#7f8c8d')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.HexColor('#34495e')
        ))
        
        self.styles.add(ParagraphStyle(
            name='RightAlign',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT
        ))
        
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#95a5a6')
        ))
    
    def generate_invoice_pdf(self, invoice_data: dict) -> BytesIO:
        """
        Genera PDF de una factura
        
        Args:
            invoice_data: Diccionario con datos de la factura
                - invoice_number: str
                - issue_date: datetime
                - due_date: date (opcional)
                - guest_name: str
                - guest_document_type: str
                - guest_document_number: str
                - guest_address: str (opcional)
                - guest_phone: str (opcional)
                - guest_email: str (opcional)
                - currency: str
                - items: List[dict] con description, quantity, unit_price, subtotal
                - subtotal: float
                - tax_percentage: float
                - tax_amount: float
                - total_amount: float
                - paid_amount: float
                - balance: float
                - status: str
                - notes: str (opcional)
        
        Returns:
            BytesIO: Buffer con el PDF generado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        elements = []
        
        # Encabezado del hotel
        elements.append(Paragraph(self.HOTEL_NAME, self.styles['CustomTitle']))
        elements.append(Paragraph(
            f"{self.HOTEL_ADDRESS}<br/>{self.HOTEL_PHONE} | {self.HOTEL_EMAIL}<br/>RIF: {self.HOTEL_RIF}",
            self.styles['CustomSubtitle']
        ))
        elements.append(Spacer(1, 20))
        
        # Título de la factura
        status_text = self._get_status_text(invoice_data.get('status', 'draft'))
        elements.append(Paragraph(
            f"<b>FACTURA {invoice_data.get('invoice_number', 'N/A')}</b>",
            self.styles['CustomTitle']
        ))
        elements.append(Paragraph(f"Estado: {status_text}", self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))
        
        # Información del cliente y factura
        issue_date = invoice_data.get('issue_date')
        if isinstance(issue_date, datetime):
            issue_date = issue_date.strftime('%d/%m/%Y %H:%M')
        elif issue_date:
            issue_date = str(issue_date)[:19]
        else:
            issue_date = 'Pendiente'
        
        due_date = invoice_data.get('due_date')
        if due_date:
            due_date = str(due_date)[:10]
        else:
            due_date = 'N/A'
        
        info_data = [
            ['DATOS DEL CLIENTE', '', 'DATOS DE LA FACTURA', ''],
            [
                'Nombre:',
                invoice_data.get('guest_name', 'N/A'),
                'Número:',
                invoice_data.get('invoice_number', 'N/A')
            ],
            [
                'Documento:',
                f"{invoice_data.get('guest_document_type', 'V')}-{invoice_data.get('guest_document_number', 'N/A')}",
                'Fecha emisión:',
                issue_date
            ],
            [
                'Dirección:',
                invoice_data.get('guest_address', 'N/A') or 'N/A',
                'Fecha vencimiento:',
                due_date
            ],
            [
                'Teléfono:',
                invoice_data.get('guest_phone', 'N/A') or 'N/A',
                'Moneda:',
                invoice_data.get('currency', 'USD')
            ],
            [
                'Email:',
                invoice_data.get('guest_email', 'N/A') or 'N/A',
                '',
                ''
            ],
        ]
        
        info_table = Table(info_data, colWidths=[80, 150, 100, 150])
        info_table.setStyle(TableStyle([
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (2, 0), (3, 0)),
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#3498db')),
            ('BACKGROUND', (2, 0), (3, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (3, 0), colors.white),
            ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (3, 0), 10),
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        # Tabla de items
        elements.append(Paragraph("DETALLE DE LA FACTURA", self.styles['SectionTitle']))
        
        currency = invoice_data.get('currency', 'USD')
        currency_symbol = self._get_currency_symbol(currency)
        
        items_header = ['#', 'Descripción', 'Cantidad', 'Precio Unit.', 'Subtotal']
        items_data = [items_header]
        
        items = invoice_data.get('items', [])
        for idx, item in enumerate(items, 1):
            items_data.append([
                str(idx),
                item.get('description', ''),
                f"{item.get('quantity', 1):.2f}",
                f"{currency_symbol}{item.get('unit_price', 0):,.2f}",
                f"{currency_symbol}{item.get('subtotal', 0):,.2f}"
            ])
        
        # Si no hay items, agregar fila vacía
        if not items:
            items_data.append(['', 'Sin items', '', '', ''])
        
        items_table = Table(items_data, colWidths=[30, 230, 70, 90, 90])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 20))
        
        # Totales
        subtotal = invoice_data.get('subtotal', 0)
        tax_percentage = invoice_data.get('tax_percentage', 16)
        tax_amount = invoice_data.get('tax_amount', 0)
        total_amount = invoice_data.get('total_amount', 0)
        paid_amount = invoice_data.get('paid_amount', 0)
        balance = invoice_data.get('balance', 0)
        
        totals_data = [
            ['', '', '', 'Subtotal:', f"{currency_symbol}{subtotal:,.2f}"],
            ['', '', '', f'IVA ({tax_percentage}%):', f"{currency_symbol}{tax_amount:,.2f}"],
            ['', '', '', 'TOTAL:', f"{currency_symbol}{total_amount:,.2f}"],
            ['', '', '', 'Pagado:', f"{currency_symbol}{paid_amount:,.2f}"],
            ['', '', '', 'BALANCE:', f"{currency_symbol}{balance:,.2f}"],
        ]
        
        totals_table = Table(totals_data, colWidths=[100, 100, 110, 100, 100])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
            ('FONTNAME', (3, 0), (4, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (3, 2), (4, 2), 12),
            ('FONTSIZE', (3, 4), (4, 4), 12),
            ('TEXTCOLOR', (3, 2), (4, 2), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (3, 4), (4, 4), colors.HexColor('#e74c3c') if balance > 0 else colors.HexColor('#27ae60')),
            ('LINEABOVE', (3, 2), (4, 2), 1, colors.HexColor('#34495e')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(totals_table)
        
        # Notas
        notes = invoice_data.get('notes')
        if notes:
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("NOTAS", self.styles['SectionTitle']))
            elements.append(Paragraph(notes, self.styles['Normal']))
        
        # Pie de página
        elements.append(Spacer(1, 40))
        elements.append(Paragraph(
            f"Este documento fue generado electrónicamente por {self.HOTEL_NAME}.<br/>"
            f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            self.styles['Footer']
        ))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def generate_receipt_pdf(self, payment_data: dict, invoice_data: Optional[dict] = None) -> BytesIO:
        """
        Genera PDF de un recibo de pago
        
        Args:
            payment_data: Diccionario con datos del pago
                - payment_code: str
                - amount: float
                - currency: str
                - payment_method: str
                - payment_date: datetime
                - reference_number: str (opcional)
                - notes: str (opcional)
            invoice_data: Datos de la factura asociada (opcional)
        
        Returns:
            BytesIO: Buffer con el PDF generado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        elements = []
        
        # Encabezado del hotel
        elements.append(Paragraph(self.HOTEL_NAME, self.styles['CustomTitle']))
        elements.append(Paragraph(
            f"{self.HOTEL_ADDRESS}<br/>{self.HOTEL_PHONE} | {self.HOTEL_EMAIL}",
            self.styles['CustomSubtitle']
        ))
        elements.append(Spacer(1, 30))
        
        # Título del recibo
        elements.append(Paragraph(
            "<b>RECIBO DE PAGO</b>",
            self.styles['CustomTitle']
        ))
        elements.append(Spacer(1, 20))
        
        # Datos del recibo
        payment_date = payment_data.get('payment_date')
        if isinstance(payment_date, datetime):
            payment_date = payment_date.strftime('%d/%m/%Y %H:%M')
        elif payment_date:
            payment_date = str(payment_date)[:19]
        else:
            payment_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        currency = payment_data.get('currency', 'USD')
        currency_symbol = self._get_currency_symbol(currency)
        amount = payment_data.get('amount', 0)
        
        receipt_data = [
            ['Número de Recibo:', payment_data.get('payment_code', 'N/A')],
            ['Fecha de Pago:', payment_date],
            ['Método de Pago:', self._get_payment_method_text(payment_data.get('payment_method', ''))],
            ['Referencia:', payment_data.get('reference_number', 'N/A') or 'N/A'],
        ]
        
        if invoice_data:
            receipt_data.extend([
                ['', ''],
                ['FACTURA ASOCIADA', ''],
                ['Número de Factura:', invoice_data.get('invoice_number', 'N/A')],
                ['Cliente:', invoice_data.get('guest_name', 'N/A')],
                ['Documento:', f"{invoice_data.get('guest_document_type', 'V')}-{invoice_data.get('guest_document_number', 'N/A')}"],
            ])
        
        receipt_table = Table(receipt_data, colWidths=[150, 300])
        receipt_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('SPAN', (0, 5), (1, 5)) if invoice_data else (),
            ('BACKGROUND', (0, 5), (1, 5), colors.HexColor('#ecf0f1')) if invoice_data else (),
        ]))
        elements.append(receipt_table)
        elements.append(Spacer(1, 30))
        
        # Monto pagado (destacado)
        amount_data = [
            ['MONTO RECIBIDO'],
            [f"{currency_symbol}{amount:,.2f} {currency}"],
        ]
        
        amount_table = Table(amount_data, colWidths=[300])
        amount_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 14),
            ('FONTSIZE', (0, 1), (0, 1), 24),
            ('TEXTCOLOR', (0, 1), (0, 1), colors.HexColor('#27ae60')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#27ae60')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        # Centrar la tabla
        elements.append(Table([[amount_table]], colWidths=[510]))
        
        # Notas
        notes = payment_data.get('notes')
        if notes:
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("NOTAS", self.styles['SectionTitle']))
            elements.append(Paragraph(notes, self.styles['Normal']))
        
        # Pie de página
        elements.append(Spacer(1, 50))
        elements.append(Paragraph(
            "Este recibo es un comprobante de pago válido.<br/>"
            f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            self.styles['Footer']
        ))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def _get_status_text(self, status: str) -> str:
        """Obtiene el texto del estado"""
        status_map = {
            'draft': 'Borrador',
            'issued': 'Emitida',
            'paid': 'Pagada',
            'cancelled': 'Cancelada',
            'void': 'Anulada'
        }
        return status_map.get(status, status)
    
    def _get_currency_symbol(self, currency: str) -> str:
        """Obtiene el símbolo de la moneda"""
        symbols = {
            'VES': 'Bs.',
            'USD': '$',
            'EUR': '€'
        }
        return symbols.get(currency, '')
    
    def _get_payment_method_text(self, method: str) -> str:
        """Obtiene el texto del método de pago"""
        method_map = {
            'cash_ves': 'Efectivo (Bolívares)',
            'cash_usd': 'Efectivo (Dólares)',
            'cash_eur': 'Efectivo (Euros)',
            'transfer': 'Transferencia Bancaria',
            'mobile_payment': 'Pago Móvil',
            'credit_card': 'Tarjeta de Crédito',
            'debit_card': 'Tarjeta de Débito',
            'other': 'Otro'
        }
        return method_map.get(method, method)


# Instancia global
pdf_service = PDFService()
