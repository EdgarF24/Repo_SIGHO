"""
Vista Completa de Gestión de Habitaciones
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any
from config.theme import FONTS, SIZES
from app.components.data_table import DataTable
from app.components.form_dialog import FormDialog
from app.services.room_service import room_service


class RoomsView(ctk.CTkFrame):
    """Vista completa de gestión de habitaciones"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_room = None
        self.room_types = []
        self.setup_ui()
        self.load_rooms()
    
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
            text=" Nueva Habitación",
            command=self.create_room,
            width=150,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Editar",
            command=self.edit_room,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Cambiar Estado",
            command=self.change_status,
            width=140,
            height=SIZES["button_height"],
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Eliminar",
            command=self.delete_room,
            width=100,
            height=SIZES["button_height"],
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Actualizar",
            command=self.load_rooms,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Filtros
        filter_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        filter_frame.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        
        ctk.CTkLabel(filter_frame, text="Estado:", font=FONTS["body"]).pack(side="left", padx=5)
        
        self.status_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Todos", "available", "occupied", "cleaning", "maintenance"],
            command=self.filter_by_status,
            width=150
        )
        self.status_filter.set("Todos")
        self.status_filter.pack(side="left", padx=5)
        
        # Estadísticas
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.total_rooms_label = ctk.CTkLabel(stats_frame, text="Total: 0", font=FONTS["body_bold"])
        self.total_rooms_label.grid(row=0, column=0, pady=10, padx=10)
        
        self.available_label = ctk.CTkLabel(stats_frame, text="Disponibles: 0", font=FONTS["body_bold"], text_color="#27ae60")
        self.available_label.grid(row=0, column=1, pady=10, padx=10)
        
        self.occupied_label = ctk.CTkLabel(stats_frame, text="Ocupadas: 0", font=FONTS["body_bold"], text_color="#e74c3c")
        self.occupied_label.grid(row=0, column=2, pady=10, padx=10)
        
        self.maintenance_label = ctk.CTkLabel(stats_frame, text="Mantenimiento: 0", font=FONTS["body_bold"], text_color="#f39c12")
        self.maintenance_label.grid(row=0, column=3, pady=10, padx=10)
        
        # Tabla
        columns = [
            {"key": "id", "label": "ID", "width": 50},
            {"key": "room_number", "label": "Número", "width": 100},
            {"key": "floor", "label": "Piso", "width": 70},
            {"key": "room_type_name", "label": "Tipo", "width": 150},
            {"key": "status_display", "label": "Estado", "width": 150},
            {"key": "is_active_display", "label": "Activa", "width": 80}
        ]
        
        self.table = DataTable(
            self,
            columns=columns,
            on_double_click=self.view_room_details,
            on_select=self.on_room_select
        )
        self.table.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def load_rooms(self):
        """Carga las habitaciones"""
        try:
            rooms = room_service.get_all(limit=500)
            
            # Cargar tipos de habitación para los diálogos
            try:
                self.room_types = room_service.get_room_types()
            except:
                self.room_types = []
            
            # Formatear datos y contar
            counts = {"available": 0, "occupied": 0, "maintenance": 0, "cleaning": 0}
            
            for room in rooms:
                room['room_type_name'] = room.get('room_type', {}).get('name', 'N/A')
                
                # Estado con emoji
                status = room.get('status', 'available')
                status_map = {
                    "available": "Disponible",
                    "occupied": "Ocupada",
                    "cleaning": "Limpieza",
                    "maintenance": "Mantenimiento",
                    "out_of_service": "Fuera de servicio"
                }
                room['status_display'] = status_map.get(status, status)
                
                # Activa
                room['is_active_display'] = "Sí" if room.get('is_active', True) else "No"
                
                # Contar
                if status in counts:
                    counts[status] += 1
            
            self.table.load_data(rooms)
            self.total_rooms_label.configure(text=f"Total: {len(rooms)}")
            self.available_label.configure(text=f"Disponibles: {counts['available']}")
            self.occupied_label.configure(text=f"Ocupadas: {counts['occupied']}")
            self.maintenance_label.configure(text=f"Mantenimiento: {counts['maintenance']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar habitaciones:\n{str(e)}")
    
    def filter_by_status(self, status: str):
        """Filtra por estado"""
        try:
            if status == "Todos":
                self.load_rooms()
            else:
                rooms = room_service.get_all(status=status, limit=500)
                self._format_and_load(rooms)
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def _format_and_load(self, rooms):
        """Formatea y carga datos"""
        for room in rooms:
            room['room_type_name'] = room.get('room_type', {}).get('name', 'N/A')
            status_map = {"available": "Disponible", "occupied": "Ocupada", "cleaning": "Limpieza", "maintenance": "Mantenimiento", "out_of_service": "Fuera de servicio"}
            room['status_display'] = status_map.get(room.get('status', 'available'), 'N/A')
            room['is_active_display'] = "Sí" if room.get('is_active', True) else "No"
        
        self.table.load_data(rooms)
        self.total_rooms_label.configure(text=f"Resultados: {len(rooms)}")
    
    def on_room_select(self, room: Dict[str, Any]):
        """Callback cuando se selecciona una habitación"""
        self.selected_room = room
    
    def view_room_details(self, room: Dict[str, Any]):
        """Muestra los detalles de una habitación"""
        room_type = room.get('room_type', {})
        details = f"""
Información de la Habitación

Número: {room.get('room_number', 'N/A')}
Piso: {room.get('floor', 'N/A')}
Tipo: {room_type.get('name', 'N/A')}
Descripción: {room_type.get('description', 'N/A')}

Capacidad: {room_type.get('max_occupancy', 0)} personas
Precio por noche: ${room_type.get('base_price', 0):,.2f}

Estado: {room.get('status_display', 'N/A')}
Activa: {room.get('is_active_display', 'N/A')}

Notas:
{room.get('notes', 'Ninguna')}
        """
        
        messagebox.showinfo("Detalles de la Habitación", details)
    
    def create_room(self):
        """Crea una nueva habitación"""
        # Preparar tipos de habitación
        room_type_options = [f"{rt.get('name', '')} - ${rt.get('base_price', 0):,.2f}/noche" 
                            for rt in self.room_types] if self.room_types else ["Estándar"]
        
        fields = [
            {"name": "room_number", "label": "Número de Habitación", "type": "entry", "required": True},
            {"name": "floor", "label": "Piso", "type": "entry", "validate": "number", "required": True},
            {"name": "room_type", "label": "Tipo de Habitación", "type": "combobox",
             "values": room_type_options, "required": True},
            {"name": "status", "label": "Estado", "type": "combobox",
             "values": ["available", "occupied", "cleaning", "maintenance", "out_of_service"], 
             "default": "available", "required": True},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 80},
            {"name": "is_active", "label": "Activa", "type": "checkbox", "default": True}
        ]
        
        def on_submit(values):
            try:
                # Extraer el ID del tipo de habitación
                if self.room_types:
                    rt_text = values['room_type']
                    rt_id = next((rt['id'] for rt in self.room_types if rt.get('name', '') in rt_text), None)
                    if rt_id:
                        values['room_type_id'] = rt_id
                else:
                    values['room_type_id'] = 1  # Default
                
                values.pop('room_type', None)  # Remover campo temporal
                values['floor'] = int(values['floor'])
                
                room_service.create(values)
                messagebox.showinfo("Éxito", "Habitación creada correctamente")
                self.load_rooms()
                return True
            except Exception as e:
                raise Exception(f"Error al crear habitación: {str(e)}")
        
        FormDialog(
            self,
            title="Nueva Habitación",
            fields=fields,
            on_submit=on_submit,
            height=500
        )
    
    def edit_room(self):
        """Edita una habitación"""
        if not self.selected_room:
            messagebox.showwarning("Advertencia", "Por favor seleccione una habitación")
            return
        
        # Preparar tipos de habitación
        room_type_options = [f"{rt.get('name', '')} - ${rt.get('base_price', 0):,.2f}/noche" 
                            for rt in self.room_types] if self.room_types else ["Estándar"]
        
        fields = [
            {"name": "room_number", "label": "Número de Habitación", "type": "entry", "required": True},
            {"name": "floor", "label": "Piso", "type": "entry", "validate": "number", "required": True},
            {"name": "room_type", "label": "Tipo de Habitación", "type": "combobox",
             "values": room_type_options},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 80},
            {"name": "is_active", "label": "Activa", "type": "checkbox"}
        ]
        
        def on_submit(values):
            try:
                # Extraer el ID del tipo de habitación si se cambió
                if 'room_type' in values and self.room_types:
                    rt_text = values['room_type']
                    rt_id = next((rt['id'] for rt in self.room_types if rt.get('name', '') in rt_text), None)
                    if rt_id:
                        values['room_type_id'] = rt_id
                    values.pop('room_type', None)
                
                if 'floor' in values:
                    values['floor'] = int(values['floor'])
                
                room_service.update(self.selected_room['id'], values)
                messagebox.showinfo("Éxito", "Habitación actualizada correctamente")
                self.load_rooms()
                return True
            except Exception as e:
                raise Exception(f"Error al actualizar habitación: {str(e)}")
        
        # Preparar valores iniciales
        initial_values = self.selected_room.copy()
        if self.room_types and 'room_type' in self.selected_room:
            rt = self.selected_room.get('room_type', {})
            initial_values['room_type'] = f"{rt.get('name', '')} - ${rt.get('base_price', 0):,.2f}/noche"
        
        FormDialog(
            self,
            title="Editar Habitación",
            fields=fields,
            on_submit=on_submit,
            initial_values=initial_values,
            height=500
        )
    
    def change_status(self):
        """Cambia el estado de una habitación"""
        if not self.selected_room:
            messagebox.showwarning("Advertencia", "Por favor seleccione una habitación")
            return
        
        fields = [
            {"name": "status", "label": "Nuevo Estado", "type": "combobox",
             "values": ["available", "occupied", "cleaning", "maintenance", "out_of_service"], 
             "required": True}
        ]
        
        def on_submit(values):
            try:
                room_service.change_status(self.selected_room['id'], values['status'])
                messagebox.showinfo("Éxito", "Estado actualizado correctamente")
                self.load_rooms()
                return True
            except Exception as e:
                raise Exception(f"Error al cambiar estado: {str(e)}")
        
        initial_values = {"status": self.selected_room.get('status', 'available')}
        
        FormDialog(
            self,
            title=f"Cambiar Estado - Habitación {self.selected_room.get('room_number', '')}",
            fields=fields,
            on_submit=on_submit,
            initial_values=initial_values,
            height=250
        )
    
    def delete_room(self):
        """Elimina una habitación"""
        if not self.selected_room:
            messagebox.showwarning("Advertencia", "Por favor seleccione una habitación")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar la habitación?\\n\\n"
            f"Número: {self.selected_room.get('room_number', '')}\\n"
            f"Tipo: {self.selected_room.get('room_type_name', '')}\\n\\n"
            f"Esta acción no se puede deshacer."
        )
        
        if confirm:
            try:
                room_service.delete(self.selected_room['id'])
                messagebox.showinfo("Éxito", "Habitación eliminada correctamente")
                self.selected_room = None
                self.load_rooms()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar habitación:\n{str(e)}")