"""
Vista Completa de Gestión de Usuarios
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any
from config.theme import FONTS, SIZES
from app.components.data_table import DataTable
from app.components.form_dialog import FormDialog
from app.services.user_service import user_service


class UsersView(ctk.CTkFrame):
    """Vista completa de gestión de usuarios"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_user = None
        self.setup_ui()
        self.load_users()
    
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
            text=" Nuevo Usuario",
            command=self.create_user,
            width=140,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Editar",
            command=self.edit_user,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Cambiar Contraseña",
            command=self.change_password,
            width=180,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Activar/Desactivar",
            command=self.toggle_active,
            width=160,
            height=SIZES["button_height"],
            fg_color="#f39c12",
            hover_color="#e67e22"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Eliminar",
            command=self.delete_user,
            width=100,
            height=SIZES["button_height"],
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Actualizar",
            command=self.load_users,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Filtros
        filter_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        filter_frame.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        
        ctk.CTkLabel(filter_frame, text="Rol:", font=FONTS["body"]).pack(side="left", padx=5)
        
        self.role_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Todos", "admin", "manager", "receptionist", "maintenance", "inventory"],
            command=self.filter_by_role,
            width=150
        )
        self.role_filter.set("Todos")
        self.role_filter.pack(side="left", padx=5)
        
        # Estadísticas
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.total_users_label = ctk.CTkLabel(
            stats_frame,
            text="Total usuarios: 0",
            font=FONTS["body_bold"]
        )
        self.total_users_label.grid(row=0, column=0, pady=10, padx=20)
        
        self.active_users_label = ctk.CTkLabel(
            stats_frame,
            text="Activos: 0",
            font=FONTS["body_bold"],
            text_color="#27ae60"
        )
        self.active_users_label.grid(row=0, column=1, pady=10, padx=20)
        
        self.inactive_users_label = ctk.CTkLabel(
            stats_frame,
            text="Inactivos: 0",
            font=FONTS["body_bold"],
            text_color="#e74c3c"
        )
        self.inactive_users_label.grid(row=0, column=2, pady=10, padx=20)
        
        # Tabla
        columns = [
            {"key": "id", "label": "ID", "width": 50},
            {"key": "username", "label": "Usuario", "width": 120},
            {"key": "full_name", "label": "Nombre Completo", "width": 200},
            {"key": "email", "label": "Email", "width": 200},
            {"key": "role_display", "label": "Rol", "width": 150},
            {"key": "is_active_display", "label": "Estado", "width": 100},
            {"key": "last_login", "label": "Última Conexión", "width": 150}
        ]
        
        self.table = DataTable(
            self,
            columns=columns,
            on_double_click=self.view_user_details,
            on_select=self.on_user_select
        )
        self.table.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def load_users(self):
        """Carga los usuarios"""
        try:
            users = user_service.get_all(limit=500)
            
            # Agregar información formateada
            active_count = 0
            inactive_count = 0
            
            for user in users:
                user['full_name'] = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "N/A"
                
                # Rol con icono
                role = user.get('role', 'receptionist')
                role_map = {
                    "admin": "Administrador",
                    "manager": "Gerente",
                    "receptionist": "Recepcionista",
                    "maintenance": "Mantenimiento",
                    "inventory": "Inventario"
                }
                user['role_display'] = role_map.get(role, role)
                
                # Estado con icono
                is_active = user.get('is_active', True)
                user['is_active_display'] = "Activo" if is_active else "Inactivo"
                
                if is_active:
                    active_count += 1
                else:
                    inactive_count += 1
                
                # Formatear última conexión
                last_login = user.get('last_login')
                user['last_login'] = last_login if last_login else "-"
            
            self.table.load_data(users)
            self.total_users_label.configure(text=f"Total usuarios: {len(users)}")
            self.active_users_label.configure(text=f"Activos: {active_count}")
            self.inactive_users_label.configure(text=f"Inactivos: {inactive_count}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios:\n{str(e)}")
    
    def filter_by_role(self, role: str):
        """Filtra usuarios por rol"""
        try:
            if role == "Todos":
                self.load_users()
            else:
                users = user_service.get_all(role=role, limit=500)
                self._format_and_load(users)
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def _format_and_load(self, users):
        """Formatea y carga los datos"""
        for user in users:
            user['full_name'] = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "N/A"
            role_map = {"admin": "Administrador", "manager": "Gerente", "receptionist": "Recepcionista", "maintenance": "Mantenimiento", "inventory": "Inventario"}
            user['role_display'] = role_map.get(user.get('role', 'receptionist'), 'N/A')
            user['is_active_display'] = "Activo" if user.get('is_active', True) else "Inactivo"
            user['last_login'] = user.get('last_login') or "-"
        
        self.table.load_data(users)
        self.total_users_label.configure(text=f"Resultados: {len(users)}")
    
    def on_user_select(self, user: Dict[str, Any]):
        """Callback cuando se selecciona un usuario"""
        self.selected_user = user
    
    def view_user_details(self, user: Dict[str, Any]):
        """Muestra los detalles de un usuario"""
        details = f"""
Información del Usuario

ID: {user.get('id')}
Usuario: {user.get('username')}
Nombre: {user['full_name']}
Email: {user.get('email', 'N/A')}
Rol: {user.get('role_display', 'N/A')}
Estado: {user.get('is_active_display', 'N/A')}

Última Conexión: {user.get('last_login', '-')}
Fecha de Creación: {user.get('created_at', 'N/A')}
        """
        
        messagebox.showinfo("Detalles del Usuario", details)
    
    def create_user(self):
        """Crea un nuevo usuario"""
        fields = [
            {"name": "username", "label": "Nombre de Usuario", "type": "entry", "required": True},
            {"name": "email", "label": "Email", "type": "entry", "validate": "email", "required": True},
            {"name": "password", "label": "Contraseña", "type": "entry", "required": True},
            {"name": "first_name", "label": "Nombre", "type": "entry", "required": True},
            {"name": "last_name", "label": "Apellido", "type": "entry", "required": True},
            {"name": "role", "label": "Rol", "type": "combobox",
             "values": ["admin", "manager", "receptionist", "maintenance", "inventory"], "required": True},
            {"name": "is_active", "label": "Activo", "type": "checkbox", "default": True}
        ]
        
        def on_submit(values):
            try:
                user_service.create(values)
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                self.load_users()
                return True
            except Exception as e:
                raise Exception(f"Error al crear usuario: {str(e)}")
        
        FormDialog(
            self,
            title="Nuevo Usuario",
            fields=fields,
            on_submit=on_submit,
            height=550
        )
    
    def edit_user(self):
        """Edita un usuario"""
        if not self.selected_user:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return
        
        fields = [
            {"name": "email", "label": "Email", "type": "entry", "validate": "email"},
            {"name": "first_name", "label": "Nombre", "type": "entry"},
            {"name": "last_name", "label": "Apellido", "type": "entry"},
            {"name": "role", "label": "Rol", "type": "combobox",
             "values": ["admin", "manager", "receptionist", "maintenance", "inventory"]},
            {"name": "is_active", "label": "Activo", "type": "checkbox"}
        ]
        
        def on_submit(values):
            try:
                user_service.update(self.selected_user['id'], values)
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                self.load_users()
                return True
            except Exception as e:
                raise Exception(f"Error al actualizar usuario: {str(e)}")
        
        FormDialog(
            self,
            title="Editar Usuario",
            fields=fields,
            on_submit=on_submit,
            initial_values=self.selected_user,
            height=500
        )
    
    def change_password(self):
        """Cambia la contraseña de un usuario"""
        if not self.selected_user:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return
        
        fields = [
            {"name": "current_password", "label": "Contraseña Actual", "type": "entry", "required": True},
            {"name": "new_password", "label": "Nueva Contraseña", "type": "entry", "required": True},
            {"name": "confirm_password", "label": "Confirmar Contraseña", "type": "entry", "required": True}
        ]
        
        def on_submit(values):
            try:
                if values['new_password'] != values['confirm_password']:
                    raise Exception("Las contraseñas no coinciden")
                
                user_service.change_password(
                    self.selected_user['id'],
                    values['current_password'],
                    values['new_password']
                )
                messagebox.showinfo("Éxito", "Contraseña cambiada correctamente")
                return True
            except Exception as e:
                raise Exception(f"Error al cambiar contraseña: {str(e)}")
        
        FormDialog(
            self,
            title=f"Cambiar Contraseña - {self.selected_user['username']}",
            fields=fields,
            on_submit=on_submit,
            height=400
        )
    
    def toggle_active(self):
        """Activa/desactiva un usuario"""
        if not self.selected_user:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return
        
        is_active = self.selected_user.get('is_active', True)
        action = "desactivar" if is_active else "activar"
        
        confirm = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro que desea {action} el usuario {self.selected_user['username']}?"
        )
        
        if confirm:
            try:
                if is_active:
                    user_service.deactivate(self.selected_user['id'])
                else:
                    user_service.activate(self.selected_user['id'])
                
                messagebox.showinfo("Éxito", f"Usuario {action}do correctamente")
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Error al {action} usuario:\n{str(e)}")
    
    def delete_user(self):
        """Elimina un usuario"""
        if not self.selected_user:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar el usuario?\\n\\n"
            f"Usuario: {self.selected_user['username']}\\n"
            f"Nombre: {self.selected_user['full_name']}\\n\\n"
            f"Esta acción no se puede deshacer."
        )
        
        if confirm:
            try:
                user_service.delete(self.selected_user['id'])
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.selected_user = None
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar usuario:\n{str(e)}")
