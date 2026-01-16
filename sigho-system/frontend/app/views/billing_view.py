"""
Vista Completa de Gestión de Facturación
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any
from config.theme import FONTS, SIZES
from app.components.data_table import DataTable
from app.components.form_dialog import FormDialog
from app.services.invoice_service import invoice_service
from app.services.reservation_service import reservation_service


class BillingView(ctk.CTkFrame):
    """Vista completa de gestión de facturación"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_invoice = None
        self.reservations = []
        self.setup_ui()
        self.load_invoices()
    
    def setup_ui(self):
        """Configura la interfaz"""
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Toolbar
        toolbar = ctk.CTkFrame(self, height=60)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        toolbar.grid_columnconfigure(1, weight=1)
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.grid(row=0, column=0, padx=5, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text=" Generar Factura",
            command=self.generate_invoice,
            width=150,
            height=SIZES["button_height"],
            fg_color="#27ae60",
            hover_color="#1e8449"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Ver Detalle",
            command=self.view_invoice_details,
            width=110,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Descargar PDF",
            command=self.download_pdf,
            width=140,
            height=SIZES["button_height"],
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Recibo",
            command=self.download_receipt,
            width=100,
            height=SIZES["button_height"],
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Emitir",
            command=self.issue_invoice,
            width=90,
            height=SIZES["button_height"],
            fg_color="#f39c12",
            hover_color="#d68910"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Anular",
            command=self.void_invoice,
            width=90,
            height=SIZES["button_height"],
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Actualizar",
            command=self.load_invoices,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Filtros
        filter_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        filter_frame.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        
        ctk.CTkLabel(filter_frame, text="Estado:", font=FONTS["body"]).pack(side="left", padx=5)
        
        self.status_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Todos", "draft", "issued", "paid", "void"],
            command=self.filter_by_status,
            width=120
        )
        self.status_filter.set("Todos")
        self.status_filter.pack(side="left", padx=5)
        
        ctk.CTkLabel(filter_frame, text="Moneda:", font=FONTS["body"]).pack(side="left", padx=5)
        
        self.currency_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Todas", "VES", "USD", "EUR"],
            command=self.filter_by_currency,
            width=100
        )
        self.currency_filter.set("Todas")
        self.currency_filter.pack(side="left", padx=5)
        
        # Estadísticas
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        stats_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.total_invoices_label = ctk.CTkLabel(
            stats_frame,
            text="Total: 0",
            font=FONTS["body_bold"]
        )
        self.total_invoices_label.grid(row=0, column=0, pady=10, padx=10)
        
        self.draft_label = ctk.CTkLabel(
            stats_frame,
            text="Borradores: 0",
            font=FONTS["body_bold"],
            text_color="#95a5a6"
        )
        self.draft_label.grid(row=0, column=1, pady=10, padx=10)
        
        self.issued_label = ctk.CTkLabel(
            stats_frame,
            text="Emitidas: 0",
            font=FONTS["body_bold"],
            text_color="#3498db"
        )
        self.issued_label.grid(row=0, column=2, pady=10, padx=10)
        
        self.paid_label = ctk.CTkLabel(
            stats_frame,
            text="Pagadas: 0",
            font=FONTS["body_bold"],
            text_color="#27ae60"
        )
        self.paid_label.grid(row=0, column=3, pady=10, padx=10)
        
        self.void_label = ctk.CTkLabel(
            stats_frame,
            text="Anuladas: 0",
            font=FONTS["body_bold"],
            text_color="#e74c3c"
        )
        self.void_label.grid(row=0, column=4, pady=10, padx=10)
        
        # Tabla
        columns = [
            {"key": "id", "label": "ID", "width": 50},
            {"key": "invoice_number", "label": "Número", "width": 150},
            {"key": "guest_name", "label": "Cliente", "width": 180},
            {"key": "total_display", "label": "Total", "width": 120},
            {"key": "balance_display", "label": "Balance", "width": 100},
            {"key": "status_display", "label": "Estado", "width": 100},
            {"key": "issue_date_display", "label": "Fecha Emisión", "width": 150}
        ]
        
        self.table = DataTable(
            self,
            columns=columns,
            on_double_click=self.view_invoice_details_callback,
            on_select=self.on_invoice_select
        )
        self.table.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def load_invoices(self):
        """Carga las facturas"""
        try:
            invoices = invoice_service.get_all(limit=500)
            
            # Cargar reservas para generar facturas
            try:
                self.reservations = reservation_service.get_all(limit=500)
            except:
                self.reservations = []
            
            # Contar por estado
            counts = {"draft": 0, "issued": 0, "paid": 0, "void": 0, "cancelled": 0}
            
            for invoice in invoices:
                # Formatear monto total
                currency = invoice.get('currency', 'USD')
                total = invoice.get('total_amount', 0)
                balance = invoice.get('balance', 0)
                invoice['total_display'] = self._format_amount(total, currency)
                invoice['balance_display'] = self._format_amount(balance, currency)
                
                # Formatear estado
                status = invoice.get('status', 'draft')
                status_map = {
                    "draft": "Borrador",
                    "issued": "Emitida",
                    "paid": "Pagada",
                    "cancelled": "Cancelada",
                    "void": "Anulada"
                }
                invoice['status_display'] = status_map.get(status, status)
                
                # Formatear fecha
                issue_date = invoice.get('issue_date', '')
                if issue_date:
                    invoice['issue_date_display'] = str(issue_date)[:19]
                else:
                    invoice['issue_date_display'] = "Pendiente"
                
                # Contar
                if status in counts:
                    counts[status] += 1
            
            self.table.load_data(invoices)
            self.total_invoices_label.configure(text=f"Total: {len(invoices)}")
            self.draft_label.configure(text=f"Borradores: {counts['draft']}")
            self.issued_label.configure(text=f"Emitidas: {counts['issued']}")
            self.paid_label.configure(text=f"Pagadas: {counts['paid']}")
            self.void_label.configure(text=f"Anuladas: {counts['void']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar facturas:\n{str(e)}")
    
    def _format_amount(self, amount: float, currency: str) -> str:
        """Formatea un monto según la moneda"""
        symbols = {"VES": "Bs.", "USD": "$", "EUR": "€"}
        symbol = symbols.get(currency, "")
        return f"{symbol}{amount:,.2f}"
    
    def filter_by_status(self, status: str):
        """Filtra facturas por estado"""
        try:
            if status == "Todos":
                self.load_invoices()
            else:
                invoices = invoice_service.get_all(status=status, limit=500)
                self._format_and_load(invoices)
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def filter_by_currency(self, currency: str):
        """Filtra facturas por moneda"""
        try:
            if currency == "Todas":
                self.load_invoices()
            else:
                invoices = invoice_service.get_all(currency=currency, limit=500)
                self._format_and_load(invoices)
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def _format_and_load(self, invoices):
        """Formatea y carga los datos"""
        for invoice in invoices:
            currency = invoice.get('currency', 'USD')
            invoice['total_display'] = self._format_amount(invoice.get('total_amount', 0), currency)
            invoice['balance_display'] = self._format_amount(invoice.get('balance', 0), currency)
            status_map = {"draft": "Borrador", "issued": "Emitida", "paid": "Pagada", "cancelled": "Cancelada", "void": "Anulada"}
            invoice['status_display'] = status_map.get(invoice.get('status', 'draft'), 'N/A')
            issue_date = invoice.get('issue_date', '')
            invoice['issue_date_display'] = str(issue_date)[:19] if issue_date else "Pendiente"
        
        self.table.load_data(invoices)
        self.total_invoices_label.configure(text=f"Resultados: {len(invoices)}")
    
    def on_invoice_select(self, invoice: Dict[str, Any]):
        """Callback cuando se selecciona una factura"""
        self.selected_invoice = invoice
    
    def view_invoice_details_callback(self, invoice: Dict[str, Any]):
        """Callback para doble clic"""
        self.selected_invoice = invoice
        self.view_invoice_details()
    
    def view_invoice_details(self):
        """Muestra los detalles de una factura"""
        if not self.selected_invoice:
            messagebox.showwarning("Advertencia", "Por favor seleccione una factura")
            return
        
        try:
            # Obtener factura completa con items
            invoice = invoice_service.get_by_id(self.selected_invoice['id'])
            
            # Formatear items
            items_text = ""
            for item in invoice.get('items', []):
                items_text += f"  - {item.get('description', '')[:50]}...\n"
                items_text += f"    Cantidad: {item.get('quantity', 1)} x ${item.get('unit_price', 0):,.2f} = ${item.get('subtotal', 0):,.2f}\n"
            
            if not items_text:
                items_text = "  Sin items\n"
            
            currency = invoice.get('currency', 'USD')
            details = f"""
FACTURA: {invoice.get('invoice_number', 'N/A')}

Cliente: {invoice.get('guest_name', 'N/A')}
Documento: {invoice.get('guest_document_type', 'V')}-{invoice.get('guest_document_number', 'N/A')}
Dirección: {invoice.get('guest_address', 'N/A') or 'N/A'}

Estado: {invoice.get('status', 'draft').upper()}
Fecha Emisión: {str(invoice.get('issue_date', 'Pendiente'))[:19]}

ITEMS:
{items_text}
Subtotal: {self._format_amount(invoice.get('subtotal', 0), currency)}
IVA ({invoice.get('tax_percentage', 16)}%): {self._format_amount(invoice.get('tax_amount', 0), currency)}
TOTAL: {self._format_amount(invoice.get('total_amount', 0), currency)}

Pagado: {self._format_amount(invoice.get('paid_amount', 0), currency)}
BALANCE: {self._format_amount(invoice.get('balance', 0), currency)}

Notas: {invoice.get('notes', 'Ninguna') or 'Ninguna'}
            """
            
            messagebox.showinfo("Detalles de la Factura", details)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener detalles:\n{str(e)}")
    
    def generate_invoice(self):
        """Genera una factura desde una reserva"""
        if not self.reservations:
            messagebox.showwarning("Advertencia", "No hay reservas disponibles")
            return
        
        # Preparar lista de reservas
        reservation_options = []
        for r in self.reservations:
            code = r.get('confirmation_code', '')
            guest_name = r.get('guest_name', '')
            if not guest_name:
                guest = r.get('guest', {})
                guest_name = f"{guest.get('first_name', '')} {guest.get('last_name', '')}".strip()
            total = r.get('total_amount', 0)
            currency = r.get('currency', 'USD')
            reservation_options.append(f"{code} - {guest_name} - ${total:,.2f} {currency}")
        
        fields = [
            {"name": "reservation", "label": "Reserva", "type": "combobox",
             "values": reservation_options, "required": True},
            {"name": "guest_document_type", "label": "Tipo Documento", "type": "combobox",
             "values": ["V", "E", "J", "G", "P"], "default": "V"},
            {"name": "guest_document_number", "label": "Número Documento", "type": "entry"},
            {"name": "guest_address", "label": "Dirección Fiscal", "type": "entry"},
            {"name": "include_payments", "label": "Incluir pagos existentes", "type": "checkbox", "default": True},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 60}
        ]
        
        def on_submit(values):
            try:
                # Extraer el ID de la reserva
                res_text = values['reservation']
                res_code = res_text.split(' - ')[0]
                reservation = next((r for r in self.reservations 
                                  if r.get('confirmation_code', '') == res_code), None)
                
                if not reservation:
                    raise Exception("Reserva no encontrada")
                
                invoice_service.generate_from_reservation(
                    reservation_id=reservation['id'],
                    include_payments=values.get('include_payments', True),
                    guest_document_type=values.get('guest_document_type'),
                    guest_document_number=values.get('guest_document_number'),
                    guest_address=values.get('guest_address'),
                    notes=values.get('notes')
                )
                
                messagebox.showinfo("Éxito", "Factura generada correctamente.\n\nRecuerde emitirla cuando esté lista.")
                self.load_invoices()
                return True
            except Exception as e:
                raise Exception(f"Error al generar factura: {str(e)}")
        
        FormDialog(
            self,
            title="Generar Factura desde Reserva",
            fields=fields,
            on_submit=on_submit,
            height=500
        )
    
    def issue_invoice(self):
        """Emite una factura"""
        if not self.selected_invoice:
            messagebox.showwarning("Advertencia", "Por favor seleccione una factura")
            return
        
        if self.selected_invoice.get('status') != 'draft':
            messagebox.showwarning("Advertencia", "Solo se pueden emitir facturas en estado borrador")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar Emisión",
            f"¿Está seguro que desea EMITIR la factura?\n\n"
            f"Número: {self.selected_invoice.get('invoice_number', 'N/A')}\n"
            f"Cliente: {self.selected_invoice.get('guest_name', 'N/A')}\n\n"
            f"Una vez emitida, no podrá editar la factura."
        )
        
        if confirm:
            try:
                invoice_service.issue(self.selected_invoice['id'])
                messagebox.showinfo("Éxito", "Factura emitida correctamente")
                self.load_invoices()
            except Exception as e:
                messagebox.showerror("Error", f"Error al emitir factura:\n{str(e)}")
    
    def void_invoice(self):
        """Anula una factura"""
        if not self.selected_invoice:
            messagebox.showwarning("Advertencia", "Por favor seleccione una factura")
            return
        
        if self.selected_invoice.get('status') == 'void':
            messagebox.showwarning("Advertencia", "La factura ya está anulada")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar Anulación",
            f"¿Está seguro que desea ANULAR la factura?\n\n"
            f"Número: {self.selected_invoice.get('invoice_number', 'N/A')}\n"
            f"Cliente: {self.selected_invoice.get('guest_name', 'N/A')}\n\n"
            f"Esta acción no se puede deshacer."
        )
        
        if confirm:
            try:
                invoice_service.void(self.selected_invoice['id'])
                messagebox.showinfo("Éxito", "Factura anulada correctamente")
                self.load_invoices()
            except Exception as e:
                messagebox.showerror("Error", f"Error al anular factura:\n{str(e)}")
    
    def download_pdf(self):
        """Descarga el PDF de una factura"""
        if not self.selected_invoice:
            messagebox.showwarning("Advertencia", "Por favor seleccione una factura")
            return
        
        try:
            filepath = invoice_service.download_pdf(self.selected_invoice['id'])
            messagebox.showinfo("Éxito", f"PDF descargado y abierto:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al descargar PDF:\n{str(e)}")
    
    def download_receipt(self):
        """Descarga el recibo de pago"""
        if not self.selected_invoice:
            messagebox.showwarning("Advertencia", "Por favor seleccione una factura")
            return
        
        if self.selected_invoice.get('paid_amount', 0) <= 0:
            messagebox.showwarning("Advertencia", "La factura no tiene pagos registrados")
            return
        
        try:
            filepath = invoice_service.download_receipt_pdf(self.selected_invoice['id'])
            messagebox.showinfo("Éxito", f"Recibo descargado y abierto:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al descargar recibo:\n{str(e)}")
