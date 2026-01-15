"""
Vista Completa de Gestión de Huéspedes
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any
from config.theme import FONTS, SIZES
from app.components.data_table import DataTable
from app.components.form_dialog import FormDialog
from app.services.guest_service import guest_service


class GuestsView(ctk.CTkFrame):
    """Vista completa de gestión de huéspedes"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_guest = None
        self.setup_ui()
        self.load_guests()
    
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
            text=" Nuevo Huésped",
            command=self.create_guest,
            width=150,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Editar",
            command=self.edit_guest,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Eliminar",
            command=self.delete_guest,
            width=100,
            height=SIZES["button_height"],
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Actualizar",
            command=self.load_guests,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Búsqueda
        search_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_frame.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por nombre, documento, email o teléfono...",
            width=350
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_guests())
        
        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search_guests,
            width=80,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Estadísticas
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Total de huéspedes: 0",
            font=FONTS["body_bold"]
        )
        self.stats_label.pack(pady=10, padx=20)
        
        # Tabla
        columns = [
            {"key": "id", "label": "ID", "width": 50},
            {"key": "full_name", "label": "Nombre Completo", "width": 200},
            {"key": "id_type", "label": "Tipo Doc", "width": 80},
            {"key": "id_number", "label": "Documento", "width": 120},
            {"key": "email", "label": "Email", "width": 180},
            {"key": "phone", "label": "Teléfono", "width": 120},
            {"key": "country", "label": "País", "width": 120}
        ]
        
        self.table = DataTable(
            self,
            columns=columns,
            on_double_click=self.view_guest_details,
            on_select=self.on_guest_select
        )
        self.table.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def load_guests(self):
        """Carga los huéspedes"""
        try:
            guests = guest_service.get_all(limit=500)
            
            # Agregar nombre completo
            for guest in guests:
                guest['full_name'] = f"{guest['first_name']} {guest['last_name']}"
            
            self.table.load_data(guests)
            self.stats_label.configure(text=f"Total de huéspedes: {len(guests)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar huéspedes:\n{str(e)}")
    
    def search_guests(self):
        """Busca huéspedes"""
        query = self.search_entry.get().strip()
        if not query:
            self.load_guests()
            return
        
        try:
            guests = guest_service.search(query)
            
            for guest in guests:
                guest['full_name'] = f"{guest['first_name']} {guest['last_name']}"
            
            self.table.load_data(guests)
            self.stats_label.configure(text=f"Resultados encontrados: {len(guests)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda:\n{str(e)}")
    
    def on_guest_select(self, guest: Dict[str, Any]):
        """Callback cuando se selecciona un huésped"""
        self.selected_guest = guest
    
    def view_guest_details(self, guest: Dict[str, Any]):
        """Muestra los detalles de un huésped"""
        details = f"""
Información del Huésped

Nombre: {guest['first_name']} {guest['last_name']}
Documento: {guest['id_type']} {guest['id_number']}

Contacto:
Email: {guest.get('email', 'N/A')}
Teléfono: {guest['phone']}
Teléfono Alt: {guest.get('phone_alternative', 'N/A')}

Ubicación:
Dirección: {guest.get('address', 'N/A')}
Ciudad: {guest.get('city', 'N/A')}
Estado: {guest.get('state', 'N/A')}
País: {guest['country']}

Otros:
Nacionalidad: {guest.get('nationality', 'N/A')}
Fecha de Nacimiento: {guest.get('date_of_birth', 'N/A')}

Notas:
{guest.get('notes', 'Ninguna')}
        """
        
        messagebox.showinfo("Detalles del Huésped", details)
    
    def create_guest(self):
        """Crea un nuevo huésped"""
        fields = [
            {"name": "first_name", "label": "Nombre", "type": "entry", "required": True},
            {"name": "last_name", "label": "Apellido", "type": "entry", "required": True},
            {"name": "id_type", "label": "Tipo de Documento", "type": "combobox", 
             "values": ["CI", "Pasaporte", "RIF", "DNI"], "required": True},
            {"name": "id_number", "label": "Número de Documento", "type": "entry", "required": True},
            {"name": "email", "label": "Email", "type": "entry", "validate": "email"},
            {"name": "phone", "label": "Teléfono", "type": "entry", "required": True},
            {"name": "phone_alternative", "label": "Teléfono Alternativo", "type": "entry"},
            {"name": "address", "label": "Dirección", "type": "textarea", "height": 80},
            {"name": "city", "label": "Ciudad", "type": "entry"},
            {"name": "state", "label": "Estado/Provincia", "type": "entry"},
            {"name": "country", "label": "País", "type": "entry", "default": "Venezuela", "required": True},
            {"name": "nationality", "label": "Nacionalidad", "type": "entry"},
            {"name": "date_of_birth", "label": "Fecha de Nacimiento", "type": "date"},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 80}
        ]
        
        def on_submit(values):
            try:
                guest_service.create(values)
                messagebox.showinfo("Éxito", "Huésped creado correctamente")
                self.load_guests()
                return True
            except Exception as e:
                raise Exception(f"Error al crear huésped: {str(e)}")
        
        FormDialog(
            self,
            title="Nuevo Huésped",
            fields=fields,
            on_submit=on_submit,
            height=700
        )
    
    def edit_guest(self):
        """Edita un huésped"""
        if not self.selected_guest:
            messagebox.showwarning("Advertencia", "Por favor seleccione un huésped")
            return
        
        fields = [
            {"name": "first_name", "label": "Nombre", "type": "entry", "required": True},
            {"name": "last_name", "label": "Apellido", "type": "entry", "required": True},
            {"name": "email", "label": "Email", "type": "entry", "validate": "email"},
            {"name": "phone", "label": "Teléfono", "type": "entry", "required": True},
            {"name": "phone_alternative", "label": "Teléfono Alternativo", "type": "entry"},
            {"name": "address", "label": "Dirección", "type": "textarea", "height": 80},
            {"name": "city", "label": "Ciudad", "type": "entry"},
            {"name": "state", "label": "Estado/Provincia", "type": "entry"},
            {"name": "country", "label": "País", "type": "entry", "required": True},
            {"name": "nationality", "label": "Nacionalidad", "type": "entry"},
            {"name": "date_of_birth", "label": "Fecha de Nacimiento", "type": "date"},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 80}
        ]
        
        def on_submit(values):
            try:
                guest_service.update(self.selected_guest['id'], values)
                messagebox.showinfo("Éxito", "Huésped actualizado correctamente")
                self.load_guests()
                return True
            except Exception as e:
                raise Exception(f"Error al actualizar huésped: {str(e)}")
        
        FormDialog(
            self,
            title="Editar Huésped",
            fields=fields,
            on_submit=on_submit,
            initial_values=self.selected_guest,
            height=700
        )
    
    def delete_guest(self):
        """Elimina un huésped"""
        if not self.selected_guest:
            messagebox.showwarning("Advertencia", "Por favor seleccione un huésped")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar al huésped?\n\n"
            f"{self.selected_guest['first_name']} {self.selected_guest['last_name']}\n"
            f"Documento: {self.selected_guest['id_number']}\n\n"
            f"Esta acción no se puede deshacer."
        )
        
        if confirm:
            try:
                guest_service.delete(self.selected_guest['id'])
                messagebox.showinfo("Éxito", "Huésped eliminado correctamente")
                self.selected_guest = None
                self.load_guests()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar huésped:\n{str(e)}")