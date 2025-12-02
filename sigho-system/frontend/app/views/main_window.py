"""
Ventana Principal del Sistema
"""
import customtkinter as ctk
from app.components.sidebar import Sidebar
from app.components.topbar import Topbar
from app.views.dashboard_view import DashboardView
from app.views.reservations_view import ReservationsView
from app.views.rooms_view import RoomsView
from app.views.guests_view import GuestsView
from app.views.payments_view import PaymentsView
from app.views.maintenance_view import MaintenanceView
from app.views.inventory_view import InventoryView
from app.views.reports_view import ReportsView
from app.views.users_view import UsersView
from app.views.settings_view import SettingsView


class MainWindow(ctk.CTkFrame):
    """Ventana principal con sidebar, topbar y área de contenido"""
    
    def __init__(self, parent, on_logout):
        super().__init__(parent)
        
        self.parent = parent
        self.on_logout = on_logout
        self.current_view = None
        
        self.setup_ui()
        
        # Mostrar dashboard por defecto
        self.show_view("dashboard")
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Configurar grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.sidebar = Sidebar(self, on_menu_select=self.handle_menu_selection)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsw")
        
        # Topbar
        self.topbar = Topbar(self)
        self.topbar.grid(row=0, column=1, sticky="ew")
        
        # Área de contenido
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def handle_menu_selection(self, menu_key: str):
        """Maneja la selección de menú"""
        if menu_key == "logout":
            self.on_logout()
        else:
            self.show_view(menu_key)
    
    def show_view(self, view_key: str):
        """Muestra una vista específica"""
        # Limpiar contenido actual
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
        
        # Mapeo de vistas
        views = {
            "dashboard": (DashboardView, "Dashboard"),
            "reservations": (ReservationsView, "Gestión de Reservas"),
            "rooms": (RoomsView, "Gestión de Habitaciones"),
            "guests": (GuestsView, "Gestión de Huéspedes"),
            "payments": (PaymentsView, "Gestión de Pagos"),
            "maintenance": (MaintenanceView, "Gestión de Mantenimiento"),
            "inventory": (InventoryView, "Gestión de Inventario"),
            "reports": (ReportsView, "Reportes"),
            "users": (UsersView, "Gestión de Usuarios"),
            "settings": (SettingsView, "Configuración")
        }
        
        if view_key in views:
            view_class, title = views[view_key]
            
            # Actualizar título
            self.topbar.set_title(title)
            
            # Crear nueva vista
            try:
                self.current_view = view_class(self.content_frame)
                self.current_view.grid(row=0, column=0, sticky="nsew")
            except Exception as e:
                # Si hay error, mostrar mensaje
                error_label = ctk.CTkLabel(
                    self.content_frame,
                    text=f"Error al cargar la vista:\n{str(e)}",
                    font=("Segoe UI", 14)
                )
                error_label.grid(row=0, column=0)
                self.current_view = error_label
            
            # Actualizar sidebar
            self.sidebar.set_active_menu(view_key)