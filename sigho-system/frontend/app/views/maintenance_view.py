"""
Vista Completa de Gestión de Mantenimiento
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any
from config.theme import FONTS, SIZES
from app.components.data_table import DataTable
from app.components.form_dialog import FormDialog
from app.services.maintenance_service import maintenance_service
from app.services.room_service import room_service
from app.services.user_service import user_service


class MaintenanceView(ctk.CTkFrame):
    """Vista completa de gestión de mantenimiento"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_maintenance = None
        self.rooms = []
        self.technicians = []
        self.setup_ui()
        self.load_maintenance()
    
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
            text=" Nueva Solicitud",
            command=self.create_maintenance,
            width=140,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Editar",
            command=self.edit_maintenance,
            width=90,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Asignar",
            command=self.assign_technician,
            width=90,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Iniciar",
            command=self.start_maintenance,
            width=90,
            height=SIZES["button_height"],
            fg_color="#27ae60",
            hover_color="#229954"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Completar",
            command=self.complete_maintenance,
            width=110,
            height=SIZES["button_height"],
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=self.cancel_maintenance,
            width=100,
            height=SIZES["button_height"],
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Actualizar",
            command=self.load_maintenance,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Filtros
        filter_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        filter_frame.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        
        ctk.CTkLabel(filter_frame, text="Estado:", font=FONTS["body"]).pack(side="left", padx=5)
        
        self.status_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Todos", "pending", "assigned", "in_progress", "completed", "cancelled"],
            command=self.filter_by_status,
            width=140
        )
        self.status_filter.set("Todos")
        self.status_filter.pack(side="left", padx=5)
        
        ctk.CTkLabel(filter_frame, text="Prioridad:", font=FONTS["body"]).pack(side="left", padx=5)
        
        self.priority_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Todas", "low", "medium", "high", "urgent"],
            command=self.filter_by_priority,
            width=120
        )
        self.priority_filter.set("Todas")
        self.priority_filter.pack(side="left", padx=5)
        
        # Estadísticas
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.total_label = ctk.CTkLabel(stats_frame, text="Total: 0", font=FONTS["body_bold"])
        self.total_label.grid(row=0, column=0, pady=10, padx=10)
        
        self.pending_label = ctk.CTkLabel(stats_frame, text="Pendientes: 0", font=FONTS["body_bold"], text_color="#f39c12")
        self.pending_label.grid(row=0, column=1, pady=10, padx=10)
        
        self.in_progress_label = ctk.CTkLabel(stats_frame, text="En progreso: 0", font=FONTS["body_bold"], text_color="#3498db")
        self.in_progress_label.grid(row=0, column=2, pady=10, padx=10)
        
        self.completed_label = ctk.CTkLabel(stats_frame, text="Completados: 0", font=FONTS["body_bold"], text_color="#27ae60")
        self.completed_label.grid(row=0, column=3, pady=10, padx=10)
        
        # Tabla
        columns = [
            {"key": "id", "label": "ID", "width": 50},
            {"key": "room_number", "label": "Habitación", "width": 100},
            {"key": "maintenance_type", "label": "Tipo", "width": 100},
            {"key": "priority_display", "label": "Prioridad", "width": 120},
            {"key": "description", "label": "Descripción", "width": 250},
            {"key": "status_display", "label": "Estado", "width": 120},
            {"key": "assigned_to_name", "label": "Asignado a", "width": 150},
            {"key": "created_at", "label": "Fecha", "width": 150}
        ]
        
        self.table = DataTable(
            self,
            columns=columns,
            on_double_click=self.view_maintenance_details,
            on_select=self.on_maintenance_select
        )
        self.table.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def load_maintenance(self):
        """Carga las solicitudes de mantenimiento"""
        try:
            maintenances = maintenance_service.get_all(limit=500)
            
            # Cargar habitaciones y técnicos para los diálogos
            try:
                self.rooms = room_service.get_all(limit=500)
            except:
                pass
            
            try:
                self.technicians = user_service.get_all(role="maintenance", limit=100)
            except:
                pass
            
            # Agregar información formateada
            counts = {"pending": 0, "in_progress": 0, "completed": 0}
            
            for maint in maintenances:
                # Número de habitación
                maint['room_number'] = f"Hab. {maint.get('room_id', 'N/A')}"
                
                # Prioridad con emoji
                priority = maint.get('priority', 'low')
                priority_map = {
                    "low": "🟢 Baja",
                    "medium": "🟡 Media",
                    "high": "🟠 Alta",
                    "urgent": " Urgente"
                }
                maint['priority_display'] = priority_map.get(priority, priority)
                
                # Estado con emoji
                status = maint.get('status', 'pending')
                status_map = {
                    "pending": "Pendiente",
                    "assigned": " Asignado",
                    "in_progress": "En Progreso",
                    "completed": "Completado",
                    "cancelled": "Cancelado"
                }
                maint['status_display'] = status_map.get(status, status)
                
                # Asignado a
                maint['assigned_to_name'] = maint.get('assigned_to_name', '-')
                
                # Contar por estado
                if status in counts:
                    counts[status] += 1
            
            self.table.load_data(maintenances)
            self.total_label.configure(text=f"Total: {len(maintenances)}")
            self.pending_label.configure(text=f"Pendientes: {counts['pending']}")
            self.in_progress_label.configure(text=f"En progreso: {counts['in_progress']}")
            self.completed_label.configure(text=f"Completados: {counts['completed']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar mantenimientos:\n{str(e)}")
    
    def filter_by_status(self, status: str):
        """Filtra por estado"""
        try:
            if status == "Todos":
                self.load_maintenance()
            else:
                maintenances = maintenance_service.get_all(status=status, limit=500)
                self._format_and_load(maintenances)
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def filter_by_priority(self, priority: str):
        """Filtra por prioridad"""
        try:
            if priority == "Todas":
                self.load_maintenance()
            else:
                maintenances = maintenance_service.get_all(priority=priority, limit=500)
                self._format_and_load(maintenances)
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def _format_and_load(self, maintenances):
        """Formatea y carga los datos"""
        for maint in maintenances:
            maint['room_number'] = f"Hab. {maint.get('room_id', 'N/A')}"
            priority_map = {"low": "🟢 Baja", "medium": "🟡 Media", "high": "🟠 Alta", "urgent": " Urgente"}
            maint['priority_display'] = priority_map.get(maint.get('priority', 'low'), 'N/A')
            status_map = {"pending": "Pendiente", "assigned": " Asignado", "in_progress": "En Progreso", "completed": "Completado", "cancelled": "Cancelado"}
            maint['status_display'] = status_map.get(maint.get('status', 'pending'), 'N/A')
            maint['assigned_to_name'] = maint.get('assigned_to_name', '-')
        
        self.table.load_data(maintenances)
        self.total_label.configure(text=f"Resultados: {len(maintenances)}")
    
    def on_maintenance_select(self, maintenance: Dict[str, Any]):
        """Callback cuando se selecciona un mantenimiento"""
        self.selected_maintenance = maintenance
    
    def view_maintenance_details(self, maintenance: Dict[str, Any]):
        """Muestra los detalles de un mantenimiento"""
        details = f"""
Detalles del Mantenimiento

ID: {maintenance.get('id')}
Habitación: {maintenance.get('room_number', 'N/A')}
Tipo: {maintenance.get('maintenance_type', 'N/A')}
Prioridad: {maintenance.get('priority_display', 'N/A')}

Descripción:
{maintenance.get('description', 'Sin descripción')}

Estado: {maintenance.get('status_display', 'N/A')}
Asignado a: {maintenance.get('assigned_to_name', '-')}

Costos:
Costo Estimado: ${maintenance.get('estimated_cost', 0):.2f}
Costo Real: ${maintenance.get('actual_cost', 0):.2f}

Fechas:
Creado: {maintenance.get('created_at', 'N/A')}
Iniciado: {maintenance.get('started_at', '-')}
Completado: {maintenance.get('completed_at', '-')}

Notas de Resolución:
{maintenance.get('resolution_notes', 'Ninguna')}
        """
        
        messagebox.showinfo("Detalles del Mantenimiento", details)
    
    def create_maintenance(self):
        """Crea una nueva solicitud de mantenimiento"""
        # Preparar lista de habitaciones
        room_options = [f"{r.get('room_number')} - {r.get('room_type_name', '')}" for r in self.rooms] if self.rooms else ["101"]
        
        fields = [
            {"name": "room_id", "label": "Habitación", "type": "combobox", 
             "values": room_options, "required": True},
            {"name": "maintenance_type", "label": "Tipo de Mantenimiento", "type": "combobox",
             "values": ["preventive", "corrective"], "required": True},
            {"name": "priority", "label": "Prioridad", "type": "combobox",
             "values": ["low", "medium", "high", "urgent"], "required": True},
            {"name": "description", "label": "Descripción", "type": "textarea", "height": 100, "required": True},
            {"name": "estimated_cost", "label": "Costo Estimado", "type": "entry", "validate": "number", "default": "0.00"}
        ]
        
        def on_submit(values):
            try:
                # Extraer el ID de la habitación
                if self.rooms:
                    room_text = values['room_id']
                    room_id = next((r['id'] for r in self.rooms if f"{r.get('room_number')}" in room_text), None)
                    if room_id:
                        values['room_id'] = room_id
                else:
                    values['room_id'] = 1  # Default
                
                values['estimated_cost'] = float(values.get('estimated_cost', 0))
                
                maintenance_service.create(values)
                messagebox.showinfo("Éxito", "Solicitud de mantenimiento creada correctamente")
                self.load_maintenance()
                return True
            except Exception as e:
                raise Exception(f"Error al crear solicitud: {str(e)}")
        
        FormDialog(
            self,
            title="Nueva Solicitud de Mantenimiento",
            fields=fields,
            on_submit=on_submit,
            height=550
        )
    
    def edit_maintenance(self):
        """Edita una solicitud de mantenimiento"""
        if not self.selected_maintenance:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud")
            return
        
        if self.selected_maintenance.get('status') in ['completed', 'cancelled']:
            messagebox.showwarning("Advertencia", "No se puede editar una solicitud completada o cancelada")
            return
        
        fields = [
            {"name": "maintenance_type", "label": "Tipo de Mantenimiento", "type": "combobox",
             "values": ["preventive", "corrective"], "required": True},
            {"name": "priority", "label": "Prioridad", "type": "combobox",
             "values": ["low", "medium", "high", "urgent"], "required": True},
            {"name": "description", "label": "Descripción", "type": "textarea", "height": 100, "required": True},
            {"name": "estimated_cost", "label": "Costo Estimado", "type": "entry", "validate": "number"}
        ]
        
        def on_submit(values):
            try:
                if 'estimated_cost' in values:
                    values['estimated_cost'] = float(values['estimated_cost'])
                
                maintenance_service.update(self.selected_maintenance['id'], values)
                messagebox.showinfo("Éxito", "Solicitud actualizada correctamente")
                self.load_maintenance()
                return True
            except Exception as e:
                raise Exception(f"Error al actualizar solicitud: {str(e)}")
        
        FormDialog(
            self,
            title="Editar Solicitud de Mantenimiento",
            fields=fields,
            on_submit=on_submit,
            initial_values=self.selected_maintenance,
            height=500
        )
    
    def assign_technician(self):
        """Asigna un técnico a la solicitud"""
        if not self.selected_maintenance:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud")
            return
        
        # Preparar lista de técnicos
        tech_options = [f"{t.get('username')} - {t.get('first_name', '')} {t.get('last_name', '')}" 
                       for t in self.technicians] if self.technicians else ["Técnico 1"]
        
        fields = [
            {"name": "technician", "label": "Asignar a", "type": "combobox",
             "values": tech_options, "required": True}
        ]
        
        def on_submit(values):
            try:
                # Extraer el ID del técnico
                if self.technicians:
                    tech_text = values['technician']
                    tech_id = next((t['id'] for t in self.technicians if t.get('username') in tech_text), None)
                    if tech_id:
                        maintenance_service.assign(self.selected_maintenance['id'], tech_id)
                        messagebox.showinfo("Éxito", "Técnico asignado correctamente")
                        self.load_maintenance()
                        return True
                
                raise Exception("No se pudo asignar el técnico")
            except Exception as e:
                raise Exception(f"Error al asignar técnico: {str(e)}")
        
        FormDialog(
            self,
            title="Asignar Técnico",
            fields=fields,
            on_submit=on_submit,
            height=250
        )
    
    def start_maintenance(self):
        """Inicia un mantenimiento"""
        if not self.selected_maintenance:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud")
            return
        
        if self.selected_maintenance.get('status') not in ['pending', 'assigned']:
            messagebox.showwarning("Advertencia", "Solo se pueden iniciar solicitudes pendientes o asignadas")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar",
            f"¿Iniciar mantenimiento de la habitación {self.selected_maintenance.get('room_number')}?"
        )
        
        if confirm:
            try:
                maintenance_service.start(self.selected_maintenance['id'])
                messagebox.showinfo("Éxito", "Mantenimiento iniciado")
                self.load_maintenance()
            except Exception as e:
                messagebox.showerror("Error", f"Error al iniciar mantenimiento:\n{str(e)}")
    
    def complete_maintenance(self):
        """Completa un mantenimiento"""
        if not self.selected_maintenance:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud")
            return
        
        if self.selected_maintenance.get('status') != 'in_progress':
            messagebox.showwarning("Advertencia", "Solo se pueden completar mantenimientos en progreso")
            return
        
        fields = [
            {"name": "actual_cost", "label": "Costo Real", "type": "entry", "validate": "number", "required": True},
            {"name": "resolution_notes", "label": "Notas de Resolución", "type": "textarea", "height": 100, "required": True},
            {"name": "materials_used", "label": "Materiales Utilizados", "type": "textarea", "height": 80}
        ]
        
        def on_submit(values):
            try:
                actual_cost = float(values['actual_cost'])
                maintenance_service.complete(
                    self.selected_maintenance['id'],
                    actual_cost,
                    values['resolution_notes'],
                    values.get('materials_used')
                )
                messagebox.showinfo("Éxito", "Mantenimiento completado correctamente")
                self.load_maintenance()
                return True
            except Exception as e:
                raise Exception(f"Error al completar mantenimiento: {str(e)}")
        
        FormDialog(
            self,
            title="Completar Mantenimiento",
            fields=fields,
            on_submit=on_submit,
            height=450
        )
    
    def cancel_maintenance(self):
        """Cancela un mantenimiento"""
        if not self.selected_maintenance:
            messagebox.showwarning("Advertencia", "Por favor seleccione una solicitud")
            return
        
        if self.selected_maintenance.get('status') in ['completed', 'cancelled']:
            messagebox.showwarning("Advertencia", "No se puede cancelar una solicitud ya completada o cancelada")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar cancelación",
            f"¿Está seguro que desea cancelar esta solicitud de mantenimiento?\\n\\n"
            f"Habitación: {self.selected_maintenance.get('room_number')}\\n"
            f"Descripción: {self.selected_maintenance.get('description', '')[:50]}..."
        )
        
        if confirm:
            try:
                maintenance_service.cancel(self.selected_maintenance['id'])
                messagebox.showinfo("Éxito", "Solicitud cancelada")
                self.load_maintenance()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cancelar solicitud:\n{str(e)}")
