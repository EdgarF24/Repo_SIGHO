"""
Componente Sidebar (Menú lateral)
"""
import customtkinter as ctk
from config.theme import FONTS, SIZES, get_theme_colors
from config.settings import APP_NAME
from app.services.auth_service import auth_service


class Sidebar(ctk.CTkFrame):
    """Sidebar con menú de navegación"""
    
    def __init__(self, parent, on_menu_select):
        super().__init__(
            parent,
            width=SIZES["sidebar_width"],
            corner_radius=0
        )
        
        self.on_menu_select = on_menu_select
        self.current_button = None
        self.menu_buttons = {}
        
        # No permitir que se redimensione
        self.grid_propagate(False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Logo/Título
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=20)
        
        ctk.CTkLabel(
            title_frame,
            text="🏨 SIGHO",
            font=("Segoe UI", 20, "bold")
        ).pack()
        
        ctk.CTkLabel(
            title_frame,
            text="Gestión Hotelera",
            font=FONTS["small"]
        ).pack()
        
        # Separador
        ctk.CTkFrame(self, height=2).pack(fill="x", padx=15, pady=10)
        
        # Información del usuario
        user = auth_service.get_user()
        if user:
            user_frame = ctk.CTkFrame(self, fg_color="transparent")
            user_frame.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkLabel(
                user_frame,
                text=f"👤 {user['full_name']}",
                font=FONTS["body_bold"]
            ).pack(anchor="w")
            
            role_text = self.get_role_display(user['role'])
            ctk.CTkLabel(
                user_frame,
                text=role_text,
                font=FONTS["small"]
            ).pack(anchor="w")
        
        # Separador
        ctk.CTkFrame(self, height=2).pack(fill="x", padx=15, pady=10)
        
        # Menú de navegación
        self.create_menu()
    
    def get_role_display(self, role: str) -> str:
        """Obtiene el texto a mostrar para el rol"""
        roles = {
            "admin": "🔑 Administrador",
            "manager": "👔 Gerente",
            "receptionist": "📋 Recepcionista",
            "maintenance": "🔧 Mantenimiento",
            "inventory": "📦 Inventario",
            "viewer": "👁️ Visualizador"
        }
        return roles.get(role, role)
    
    def create_menu(self):
        """Crea el menú de navegación"""
        # Obtener permisos del usuario
        user = auth_service.get_user()
        role = user.get('role') if user else None
        is_superuser = user.get('is_superuser', False) if user else False
        
        # Menú principal (siempre visible)
        menu_items = [
            ("📊 Dashboard", "dashboard", True),
        ]
        
        # Módulos de recepción (admin, manager, receptionist)
        if role in ['admin', 'manager', 'receptionist'] or is_superuser:
            menu_items.extend([
                ("🛏️ Habitaciones", "rooms", True),
                ("📅 Reservas", "reservations", True),
                ("👥 Huéspedes", "guests", True),
                ("💳 Pagos", "payments", True),
            ])
        
        # Mantenimiento (admin, manager, maintenance)
        if role in ['admin', 'manager', 'maintenance'] or is_superuser:
            menu_items.append(("🔧 Mantenimiento", "maintenance", True))
        
        # Inventario (admin, manager, inventory)
        if role in ['admin', 'manager', 'inventory'] or is_superuser:
            menu_items.append(("📦 Inventario", "inventory", True))
        
        # Reportes (admin, manager)
        if role in ['admin', 'manager'] or is_superuser:
            menu_items.append(("📈 Reportes", "reports", True))
        
        # Usuarios (solo admin)
        if role == 'admin' or is_superuser:
            menu_items.append(("👤 Usuarios", "users", True))
        
        # Configuración (todos)
        menu_items.append(("⚙️ Configuración", "settings", True))
        
        # Crear botones
        for text, key, enabled in menu_items:
            btn = self.create_menu_button(text, key, enabled)
            self.menu_buttons[key] = btn
        
        # Espaciador
        ctk.CTkFrame(self, fg_color="transparent").pack(expand=True)
        
        # Botón de cerrar sesión
        logout_btn = ctk.CTkButton(
            self,
            text="🚪 Cerrar Sesión",
            command=lambda: self.on_menu_select("logout"),
            font=FONTS["body"],
            height=SIZES["button_height"],
            fg_color="transparent",
            hover_color=("#e74c3c", "#c0392b"),
            anchor="w"
        )
        logout_btn.pack(fill="x", padx=10, pady=(10, 20))
    
    def create_menu_button(self, text: str, key: str, enabled: bool = True):
        """Crea un botón de menú"""
        btn = ctk.CTkButton(
            self,
            text=text,
            command=lambda: self.handle_menu_click(key),
            font=FONTS["body"],
            height=SIZES["button_height"],
            fg_color="transparent",
            hover_color=("#1f6aa5", "#2980b9"),
            anchor="w"
        )
        btn.pack(fill="x", padx=10, pady=2)
        
        if not enabled:
            btn.configure(state="disabled")
        
        return btn
    
    def handle_menu_click(self, key: str):
        """Maneja el clic en un botón del menú"""
        # Actualizar botón actual
        if self.current_button:
            self.current_button.configure(fg_color="transparent")
        
        if key in self.menu_buttons:
            self.menu_buttons[key].configure(fg_color=("#1f6aa5", "#2980b9"))
            self.current_button = self.menu_buttons[key]
        
        # Llamar callback
        self.on_menu_select(key)
    
    def set_active_menu(self, key: str):
        """Establece el menú activo"""
        if self.current_button:
            self.current_button.configure(fg_color="transparent")
        
        if key in self.menu_buttons:
            self.menu_buttons[key].configure(fg_color=("#1f6aa5", "#2980b9"))
            self.current_button = self.menu_buttons[key]