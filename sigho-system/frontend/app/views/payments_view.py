"""
Vista Completa de Gestión de Pagos
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any
from config.theme import FONTS, SIZES
from app.components.data_table import DataTable
from app.components.form_dialog import FormDialog
from app.services.payment_service import payment_service
from app.services.reservation_service import reservation_service


class PaymentsView(ctk.CTkFrame):
    """Vista completa de gestión de pagos"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_payment = None
        self.reservations = []
        self.setup_ui()
        self.load_payments()
    
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
            text=" Registrar Pago",
            command=self.create_payment,
            width=140,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Ver Detalles",
            command=self.view_payment_details,
            width=130,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Balance Reserva",
            command=self.check_reservation_balance,
            width=150,
            height=SIZES["button_height"],
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Actualizar",
            command=self.load_payments,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Filtros
        filter_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        filter_frame.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        
        ctk.CTkLabel(filter_frame, text="Moneda:", font=FONTS["body"]).pack(side="left", padx=5)
        
        self.currency_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Todas", "VES", "USD", "EUR"],
            command=self.filter_by_currency,
            width=120
        )
        self.currency_filter.set("Todas")
        self.currency_filter.pack(side="left", padx=5)
        
        ctk.CTkLabel(filter_frame, text="Método:", font=FONTS["body"]).pack(side="left", padx=5)
        
        self.method_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Todos", "cash", "card", "transfer", "mobile"],
            command=self.filter_by_method,
            width=130
        )
        self.method_filter.set("Todos")
        self.method_filter.pack(side="left", padx=5)
        
        # Estadísticas
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.total_payments_label = ctk.CTkLabel(
            stats_frame,
            text="Total pagos: 0",
            font=FONTS["body_bold"]
        )
        self.total_payments_label.grid(row=0, column=0, pady=10, padx=10)
        
        self.ves_total_label = ctk.CTkLabel(
            stats_frame,
            text="VES: Bs. 0.00",
            font=FONTS["body_bold"],
            text_color="#27ae60"
        )
        self.ves_total_label.grid(row=0, column=1, pady=10, padx=10)
        
        self.usd_total_label = ctk.CTkLabel(
            stats_frame,
            text="USD: $0.00",
            font=FONTS["body_bold"],
            text_color="#2ecc71"
        )
        self.usd_total_label.grid(row=0, column=2, pady=10, padx=10)
        
        self.eur_total_label = ctk.CTkLabel(
            stats_frame,
            text="EUR: €0.00",
            font=FONTS["body_bold"],
            text_color="#16a085"
        )
        self.eur_total_label.grid(row=0, column=3, pady=10, padx=10)
        
        # Tabla
        columns = [
            {"key": "id", "label": "ID", "width": 50},
            {"key": "reservation_code", "label": "Reserva", "width": 120},
            {"key": "amount_display", "label": "Monto", "width": 120},
            {"key": "currency", "label": "Moneda", "width": 80},
            {"key": "payment_method_display", "label": "Método", "width": 120},
            {"key": "payment_date", "label": "Fecha", "width": 150},
            {"key": "status_display", "label": "Estado", "width": 100},
            {"key": "reference", "label": "Referencia", "width": 150}
        ]
        
        self.table = DataTable(
            self,
            columns=columns,
            on_double_click=self.view_payment_details_callback,
            on_select=self.on_payment_select
        )
        self.table.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def load_payments(self):
        """Carga los pagos"""
        try:
            payments = payment_service.get_all(limit=500)
            
            # Cargar reservas para los diálogos
            try:
                self.reservations = reservation_service.get_all(limit=500)
            except:
                pass
            
            # Agregar información formateada y calcular totales
            totals = {"VES": 0.0, "USD": 0.0, "EUR": 0.0}
            
            for payment in payments:
                # Código de reserva
                payment['reservation_code'] = payment.get('reservation_code', f"RES-{payment.get('reservation_id', 'N/A')}")
                
                # Monto formateado
                amount = payment.get('amount', 0)
                currency = payment.get('currency', 'VES')
                payment['amount_display'] = self._format_amount(amount, currency)
                
                # Método de pago con icono
                method = payment.get('payment_method', 'cash')
                method_map = {
                    "cash_ves": "Efectivo VES",
                    "cash_usd": "Efectivo USD",
                    "cash_eur": "Efectivo EUR",
                    "transfer": "Transferencia",
                    "mobile_payment": "Pago Móvil",
                    "credit_card": "Tarjeta Crédito",
                    "debit_card": "Tarjeta Débito",
                    "other": "Otro"
                }
                payment['payment_method_display'] = method_map.get(method, method)
                
                # Estado con icono
                status = payment.get('status', 'completed')
                status_map = {
                    "completed": "Completado",
                    "pending": "Pendiente",
                    "cancelled": "Cancelado",
                    "refunded": "Reembolsado"
                }
                payment['status_display'] = status_map.get(status, status)
                
                # Formatear fecha
                payment_date = payment.get('payment_date', '')
                if payment_date and len(payment_date) > 10:
                    payment['payment_date'] = payment_date[:19]
                
                # Acumular totales
                if currency in totals and status == 'completed':
                    totals[currency] += amount
            
            self.table.load_data(payments)
            self.total_payments_label.configure(text=f"Total pagos: {len(payments)}")
            self.ves_total_label.configure(text=f"VES: Bs. {totals['VES']:,.2f}")
            self.usd_total_label.configure(text=f"USD: ${totals['USD']:,.2f}")
            self.eur_total_label.configure(text=f"EUR: €{totals['EUR']:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pagos:\n{str(e)}")
    
    def _format_amount(self, amount: float, currency: str) -> str:
        """Formatea un monto según la moneda"""
        symbols = {"VES": "Bs.", "USD": "$", "EUR": "€"}
        symbol = symbols.get(currency, "")
        return f"{symbol} {amount:,.2f}"
    
    def filter_by_currency(self, currency: str):
        """Filtra pagos por moneda"""
        try:
            if currency == "Todas":
                self.load_payments()
            else:
                payments = payment_service.get_all(currency=currency, limit=500)
                self._format_and_load(payments)
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def filter_by_method(self, method: str):
        """Filtra pagos por método"""
        try:
            if method == "Todos":
                self.load_payments()
            else:
                payments = payment_service.get_all(payment_method=method, limit=500)
                self._format_and_load(payments)
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def _format_and_load(self, payments):
        """Formatea y carga los datos"""
        for payment in payments:
            payment['reservation_code'] = payment.get('reservation_code', f"RES-{payment.get('reservation_id', 'N/A')}")
            amount = payment.get('amount', 0)
            currency = payment.get('currency', 'VES')
            payment['amount_display'] = self._format_amount(amount, currency)
            method_map = {"cash_ves": "Efectivo VES", "cash_usd": "Efectivo USD", "cash_eur": "Efectivo EUR", "transfer": "Transferencia", "mobile_payment": "Pago Móvil", "credit_card": "Tarjeta Crédito", "debit_card": "Tarjeta Débito", "other": "Otro"}
            payment['payment_method_display'] = method_map.get(payment.get('payment_method', 'cash'), 'N/A')
            status_map = {"completed": "Completado", "pending": "Pendiente", "cancelled": "Cancelado", "refunded": "Reembolsado"}
            payment['status_display'] = status_map.get(payment.get('status', 'completed'), 'N/A')
            payment_date = payment.get('payment_date', '')
            if payment_date and len(payment_date) > 10:
                payment['payment_date'] = payment_date[:19]
        
        self.table.load_data(payments)
        self.total_payments_label.configure(text=f"Resultados: {len(payments)}")
    
    def on_payment_select(self, payment: Dict[str, Any]):
        """Callback cuando se selecciona un pago"""
        self.selected_payment = payment
    
    def view_payment_details_callback(self, payment: Dict[str, Any]):
        """Callback para doble clic"""
        self.selected_payment = payment
        self.view_payment_details()
    
    def view_payment_details(self):
        """Muestra los detalles de un pago"""
        if not self.selected_payment:
            messagebox.showwarning("Advertencia", "Por favor seleccione un pago")
            return
        
        details = f"""
Detalles del Pago

ID: {self.selected_payment.get('id')}
Reserva: {self.selected_payment.get('reservation_code', 'N/A')}

Monto: {self.selected_payment.get('amount_display', 'N/A')}
Moneda: {self.selected_payment.get('currency', 'N/A')}
Método: {self.selected_payment.get('payment_method_display', 'N/A')}

Estado: {self.selected_payment.get('status_display', 'N/A')}
Fecha: {self.selected_payment.get('payment_date', 'N/A')}
Referencia: {self.selected_payment.get('reference', 'N/A')}

Notas:
{self.selected_payment.get('notes', 'Ninguna')}
        """
        
        messagebox.showinfo("Detalles del Pago", details)
    
    def create_payment(self):
        """Registra un nuevo pago"""
        # Preparar lista de reservas
        reservation_options = [f"{r.get('confirmation_code', '')} - {r.get('guest_name', '')}" 
                              for r in self.reservations] if self.reservations else ["RES-001"]
        
        fields = [
            {"name": "reservation", "label": "Reserva", "type": "combobox",
             "values": reservation_options, "required": True},
            {"name": "amount", "label": "Monto", "type": "entry", "validate": "number", "required": True},
            {"name": "currency", "label": "Moneda", "type": "combobox",
             "values": ["VES", "USD", "EUR"], "required": True, "default": "VES"},
            {"name": "payment_method", "label": "Método de Pago", "type": "combobox",
             "values": ["cash_ves", "cash_usd", "cash_eur", "transfer", "mobile_payment", "credit_card", "debit_card", "other"], "required": True},
            {"name": "reference", "label": "Referencia/Comprobante", "type": "entry"},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 80}
        ]
        
        def on_submit(values):
            try:
                # Extraer el ID de la reserva
                if self.reservations:
                    res_text = values['reservation']
                    res_id = next((r['id'] for r in self.reservations 
                                 if r.get('confirmation_code', '') in res_text), None)
                    if res_id:
                        values['reservation_id'] = res_id
                else:
                    values['reservation_id'] = 1  # Default
                
                values.pop('reservation', None)  # Remover el campo temporal
                values['amount'] = float(values['amount'])
                
                payment_service.create(values)
                messagebox.showinfo("Éxito", "Pago registrado correctamente")
                self.load_payments()
                return True
            except Exception as e:
                raise Exception(f"Error al registrar pago: {str(e)}")
        
        FormDialog(
            self,
            title="Registrar Nuevo Pago",
            fields=fields,
            on_submit=on_submit,
            height=550
        )
    
    def check_reservation_balance(self):
        """Verifica el balance de una reserva"""
        if not self.reservations:
            messagebox.showwarning("Advertencia", "No hay reservas disponibles")
            return
        
        # Diálogo para seleccionar reserva
        reservation_options = [f"{r.get('confirmation_code', '')} - {r.get('guest_name', '')}" 
                              for r in self.reservations]
        
        fields = [
            {"name": "reservation", "label": "Seleccione Reserva", "type": "combobox",
             "values": reservation_options, "required": True}
        ]
        
        def on_submit(values):
            try:
                res_text = values['reservation']
                reservation = next((r for r in self.reservations 
                                  if r.get('confirmation_code', '') in res_text), None)
                
                if reservation:
                    total = reservation.get('total_price', 0)
                    paid = reservation.get('paid_amount', 0)
                    balance = total - paid
                    
                    status = "Pagado" if balance <= 0 else "Pendiente"
                    
                    details = f"""
Balance de Reserva

Código: {reservation.get('confirmation_code', 'N/A')}
Huésped: {reservation.get('guest_name', 'N/A')}

Monto Total: ${total:,.2f}
Monto Pagado: ${paid:,.2f}
Balance Pendiente: ${balance:,.2f}

Estado: {status}
                    """
                    
                    messagebox.showinfo("Balance de Reserva", details)
                    return True
                
                raise Exception("Reserva no encontrada")
            except Exception as e:
                raise Exception(f"Error al consultar balance: {str(e)}")
        
        FormDialog(
            self,
            title="Consultar Balance de Reserva",
            fields=fields,
            on_submit=on_submit,
            height=250
        )
