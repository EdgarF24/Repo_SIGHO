"""
Vista de Gestión de Reservas
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from typing import Optional, Dict, Any
from config.theme import FONTS, SIZES
from app.components.data_table import DataTable
from app.services.reservation_service import reservation_service
from app.services.room_service import room_service
from app.services.api_client import api_client


class ReservationsView(ctk.CTkFrame):
    """Vista de gestión de reservas"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.selected_reservation = None
        self.setup_ui()
        self.load_reservations()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Configurar grid
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
            text="➕ Nueva Reserva",
            command=self.create_reservation,
            width=140,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="✏️ Editar",
            command=self.edit_reservation,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="📥 Check-in",
            command=self.checkin_reservation,
            width=100,
            height=SIZES["button_height"],
            fg_color="#27ae60"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="📤 Check-out",
            command=self.checkout_reservation,
            width=100,
            height=SIZES["button_height"],
            fg_color="#e67e22"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=self.cancel_reservation,
            width=100,
            height=SIZES["button_height"],
            fg_color="#e74c3c"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Actualizar",
            command=self.load_reservations,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Búsqueda
        search_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_frame.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar por código, huésped o habitación...",
            width=300
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_reservations())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_reservations,
            width=80,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Filtros
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(filter_frame, text="Estado:", font=FONTS["body_bold"]).pack(side="left", padx=5)
        
        self.status_var = ctk.StringVar(value="all")
        statuses = [
            ("Todas", "all"),
            ("Pendientes", "pending"),
            ("Confirmadas", "confirmed"),
            ("Check-in", "checked_in"),
            ("Check-out", "checked_out"),
            ("Canceladas", "cancelled")
        ]
        
        for label, value in statuses:
            ctk.CTkRadioButton(
                filter_frame,
                text=label,
                variable=self.status_var,
                value=value,
                command=self.load_reservations
            ).pack(side="left", padx=5)
        
        # Tabla de reservas
        columns = [
            {"key": "id", "label": "ID", "width": 50},
            {"key": "confirmation_code", "label": "Código", "width": 100},
            {"key": "guest_name", "label": "Huésped", "width": 200},
            {"key": "room_number", "label": "Habitación", "width": 100},
            {"key": "check_in_date", "label": "Check-in", "width": 100},
            {"key": "check_out_date", "label": "Check-out", "width": 100},
            {"key": "total_nights", "label": "Noches", "width": 70},
            {"key": "status", "label": "Estado", "width": 120, "formatter": self.format_status},
            {"key": "total_amount", "label": "Total", "width": 100, "formatter": lambda v: f"${v:,.2f}"},
            {"key": "balance", "label": "Balance", "width": 100, "formatter": lambda v: f"${v:,.2f}"}
        ]
        
        self.table = DataTable(
            self,
            columns=columns,
            on_double_click=self.view_reservation_details,
            on_select=self.on_reservation_select
        )
        self.table.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def format_status(self, status: str) -> str:
        """Formatea el estado de la reserva"""
        status_map = {
            "pending": "⏳ Pendiente",
            "confirmed": "✅ Confirmada",
            "checked_in": "🏨 Check-in",
            "checked_out": "📤 Check-out",
            "cancelled": "❌ Cancelada",
            "no_show": "⚠️ No Show"
        }
        return status_map.get(status, status)
    
    def load_reservations(self):
        """Carga las reservas"""
        try:
            status_filter = self.status_var.get()
            status = None if status_filter == "all" else status_filter
            
            reservations = reservation_service.get_all(status=status, limit=500)
            
            # Enriquecer datos
            enriched_data = []
            for res in reservations:
                # Obtener huésped
                try:
                    guest = api_client.get(f"/api/guests/{res['guest_id']}")
                    res['guest_name'] = f"{guest['first_name']} {guest['last_name']}"
                except:
                    res['guest_name'] = "N/A"
                
                # Obtener habitación
                try:
                    room = api_client.get(f"/api/rooms/{res['room_id']}")
                    res['room_number'] = room['room_number']
                except:
                    res['room_number'] = "N/A"
                
                enriched_data.append(res)
            
            self.table.load_data(enriched_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar reservas:\n{str(e)}")
    
    def search_reservations(self):
        """Busca reservas"""
        query = self.search_entry.get().strip()
        if not query:
            self.load_reservations()
            return
        
        try:
            reservations = reservation_service.search(query)
            
            # Enriquecer datos
            enriched_data = []
            for res in reservations:
                try:
                    guest = api_client.get(f"/api/guests/{res['guest_id']}")
                    res['guest_name'] = f"{guest['first_name']} {guest['last_name']}"
                except:
                    res['guest_name'] = "N/A"
                
                try:
                    room = api_client.get(f"/api/rooms/{res['room_id']}")
                    res['room_number'] = room['room_number']
                except:
                    res['room_number'] = "N/A"
                
                enriched_data.append(res)
            
            self.table.load_data(enriched_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda:\n{str(e)}")
    
    def on_reservation_select(self, reservation: Dict[str, Any]):
        """Callback cuando se selecciona una reserva"""
        self.selected_reservation = reservation
    
    def view_reservation_details(self, reservation: Dict[str, Any]):
        """Muestra los detalles de una reserva"""
        details = f"""
Código de Confirmación: {reservation['confirmation_code']}
Huésped: {reservation['guest_name']}
Habitación: {reservation['room_number']}

Check-in: {reservation['check_in_date']}
Check-out: {reservation['check_out_date']}
Noches: {reservation['total_nights']}

Adultos: {reservation['num_adults']}
Niños: {reservation['num_children']}

Estado: {self.format_status(reservation['status'])}

Subtotal: ${reservation['subtotal']:,.2f} {reservation['currency']}
Impuestos: ${reservation['tax_amount']:,.2f}
Total: ${reservation['total_amount']:,.2f}
Pagado: ${reservation['paid_amount']:,.2f}
Balance: ${reservation['balance']:,.2f}

Solicitudes Especiales:
{reservation.get('special_requests', 'Ninguna')}
        """
        
        messagebox.showinfo("Detalles de la Reserva", details)
    
    def create_reservation(self):
        """Crea una nueva reserva"""
        from app.components.form_dialog import FormDialog
        from app.services.guest_service import guest_service
        
        #Cargar datos necesarios
        try:
            rooms = room_service.get_all(status="available", limit=500)
            guests = guest_service.get_all(limit=500)
        except:
            rooms = []
            guests = []
        
        # Preparar opciones
        room_options = [f"Hab. {r.get('room_number', '')} - {r.get('room_type', {}).get('name', '')}" 
                       for r in rooms] if rooms else ["101"]
        guest_options = [f"{g.get('first_name', '')} {g.get('last_name', '')} - {g.get('id_number', '')}" 
                        for g in guests] if guests else ["Nuevo Huésped"]
        
        fields = [
            {"name": "guest", "label": "Huésped", "type": "combobox",
             "values": guest_options, "required": True},
            {"name": "room", "label": "Habitación", "type": "combobox",
             "values": room_options, "required": True},
            {"name": "check_in_date", "label": "Fecha Check-in (YYYY-MM-DD)", "type": "entry", "required": True},
            {"name": "check_out_date", "label": "Fecha Check-out (YYYY-MM-DD)", "type": "entry", "required": True},
            {"name": "num_adults", "label": "Número de Adultos", "type": "entry", "validate": "number", "default": "1", "required": True},
            {"name": "num_children", "label": "Número de Niños", "type": "entry", "validate": "number", "default": "0"},
            {"name": "currency", "label": "Moneda", "type": "combobox",
             "values": ["VES", "USD", "EUR"], "default": "VES", "required": True},
            {"name": "special_requests", "label": "Solicitudes Especiales", "type": "textarea", "height": 80},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 60}
        ]
        
        def on_submit(values):
            try:
                # Extraer IDs
                if guests:
                    guest_text = values['guest']
                    guest_id = next((g['id'] for g in guests if g.get('id_number', '') in guest_text), None)
                    if guest_id:
                        values['guest_id'] = guest_id
                else:
                    values['guest_id'] = 1
                
                if rooms:
                    room_text = values['room']
                    room_id = next((r['id'] for r in rooms if f"Hab. {r.get('room_number', '')}" in room_text), None)
                    if room_id:
                        values['room_id'] = room_id
                else:
                    values['room_id'] = 1
                
                # Limpiar campos temporales
                values.pop('guest', None)
                values.pop('room', None)
                
                # Convertir números
                values['num_adults'] = int(values.get('num_adults', 1))
                values['num_children'] = int(values.get('num_children', 0))
                
                # Crear reserva
                reservation_service.create(values)
                messagebox.showinfo("Éxito", "Reserva creada correctamente")
                self.load_reservations()
                return True
            except Exception as e:
                raise Exception(f"Error al crear reserva: {str(e)}")
        
        FormDialog(
            self,
            title="Nueva Reserva",
            fields=fields,
            on_submit=on_submit,
            height=650
        )
    
    def edit_reservation(self):
        """Edita una reserva"""
        if not self.selected_reservation:
            messagebox.showwarning("Advertencia", "Por favor seleccione una reserva")
            return
        
        if self.selected_reservation.get('status') in ['checked_out', 'cancelled']:
            messagebox.showwarning("Advertencia", "No se pueden editar reservas completadas o canceladas")
            return
        
        from app.components.form_dialog import FormDialog
        
        fields = [
            {"name": "check_in_date", "label": "Fecha Check-in (YYYY-MM-DD)", "type": "entry", "required": True},
            {"name": "check_out_date", "label": "Fecha Check-out (YYYY-MM-DD)", "type": "entry", "required": True},
            {"name": "num_adults", "label": "Número de Adultos", "type": "entry", "validate": "number", "required": True},
            {"name": "num_children", "label": "Número de Niños", "type": "entry", "validate": "number"},
            {"name": "special_requests", "label": "Solicitudes Especiales", "type": "textarea", "height": 80},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 60}
        ]
        
        def on_submit(values):
            try:
                # Convertir números
                if 'num_adults' in values:
                    values['num_adults'] = int(values['num_adults'])
                if 'num_children' in values:
                    values['num_children'] = int(values['num_children'])
                
                # Actualizar reserva
                reservation_service.update(self.selected_reservation['id'], values)
                messagebox.showinfo("Éxito", "Reserva actualizada correctamente")
                self.load_reservations()
                return True
            except Exception as e:
                raise Exception(f"Error al actualizar reserva: {str(e)}")
        
        FormDialog(
            self,
            title=f"Editar Reserva - {self.selected_reservation.get('confirmation_code', '')}",
            fields=fields,
            on_submit=on_submit,
            initial_values=self.selected_reservation,
            height=550
        )

    
    def checkin_reservation(self):
        """Realiza check-in"""
        if not self.selected_reservation:
            messagebox.showwarning("Advertencia", "Por favor seleccione una reserva")
            return
        
        if self.selected_reservation['status'] != 'confirmed':
            messagebox.showerror("Error", "Solo se puede hacer check-in de reservas confirmadas")
            return
        
        if messagebox.askyesno("Check-in", "¿Confirmar check-in?"):
            try:
                reservation_service.check_in(self.selected_reservation['id'])
                messagebox.showinfo("Éxito", "Check-in realizado correctamente")
                self.load_reservations()
            except Exception as e:
                messagebox.showerror("Error", f"Error al hacer check-in:\n{str(e)}")
    
    def checkout_reservation(self):
        """Realiza check-out"""
        if not self.selected_reservation:
            messagebox.showwarning("Advertencia", "Por favor seleccione una reserva")
            return
        
        if self.selected_reservation['status'] != 'checked_in':
            messagebox.showerror("Error", "Solo se puede hacer check-out de reservas con check-in")
            return
        
        if self.selected_reservation['balance'] > 0:
            messagebox.showerror("Error", "Debe completar el pago antes del check-out")
            return
        
        if messagebox.askyesno("Check-out", "¿Confirmar check-out?"):
            try:
                reservation_service.check_out(self.selected_reservation['id'])
                messagebox.showinfo("Éxito", "Check-out realizado correctamente")
                self.load_reservations()
            except Exception as e:
                messagebox.showerror("Error", f"Error al hacer check-out:\n{str(e)}")
    
    def cancel_reservation(self):
        """Cancela una reserva"""
        if not self.selected_reservation:
            messagebox.showwarning("Advertencia", "Por favor seleccione una reserva")
            return
        
        if self.selected_reservation['status'] == 'cancelled':
            messagebox.showerror("Error", "La reserva ya está cancelada")
            return
        
        reason = ctk.CTkInputDialog(
            text="Motivo de cancelación:",
            title="Cancelar Reserva"
        ).get_input()
        
        if reason:
            try:
                reservation_service.cancel(self.selected_reservation['id'], reason)
                messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
                self.load_reservations()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cancelar:\n{str(e)}")