"""
Vista de Dashboard (Panel Principal)
"""
import customtkinter as ctk
from tkinter import messagebox
from config.theme import FONTS, SIZES
from app.services.api_client import api_client


class DashboardView(ctk.CTkScrollableFrame):
    """Vista principal con estadísticas del hotel"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.dashboard_data = None
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Configurar grid
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Título de bienvenida
        welcome_label = ctk.CTkLabel(
            self,
            text="Bienvenido al Sistema de Gestión Hotelera",
            font=FONTS["heading"]
        )
        welcome_label.grid(row=0, column=0, columnspan=4, pady=20, padx=20, sticky="w")
        
        # Botón de actualizar
        refresh_btn = ctk.CTkButton(
            self,
            text="🔄 Actualizar",
            command=self.load_data,
            width=120,
            height=32
        )
        refresh_btn.grid(row=0, column=3, pady=20, padx=20, sticky="e")
        
        # Tarjetas de estadísticas - Habitaciones
        self.create_section_label("🏨 Estado de Habitaciones", 1)
        
        self.total_rooms_card = self.create_stat_card("Total", "0", "#3498db", 2, 0)
        self.available_rooms_card = self.create_stat_card("Disponibles", "0", "#2ecc71", 2, 1)
        self.occupied_rooms_card = self.create_stat_card("Ocupadas", "0", "#e74c3c", 2, 2)
        self.cleaning_rooms_card = self.create_stat_card("En Limpieza", "0", "#f39c12", 2, 3)
        
        self.occupancy_rate_card = self.create_stat_card("Tasa de Ocupación", "0%", "#9b59b6", 3, 0)
        self.maintenance_rooms_card = self.create_stat_card("En Mantenimiento", "0", "#95a5a6", 3, 1)
        
        # Tarjetas de estadísticas - Reservas
        self.create_section_label("📅 Reservas", 4)
        
        self.today_checkins_card = self.create_stat_card("Check-ins Hoy", "0", "#3498db", 5, 0)
        self.today_checkouts_card = self.create_stat_card("Check-outs Hoy", "0", "#e74c3c", 5, 1)
        self.active_reservations_card = self.create_stat_card("Reservas Activas", "0", "#2ecc71", 5, 2)
        self.pending_reservations_card = self.create_stat_card("Pendientes", "0", "#f39c12", 5, 3)
        
        # Tarjetas de estadísticas - Ingresos
        self.create_section_label("💰 Ingresos", 6)
        
        self.today_revenue_card = self.create_stat_card("Hoy (USD)", "$0.00", "#27ae60", 7, 0)
        self.monthly_revenue_card = self.create_stat_card("Este Mes (USD)", "$0.00", "#16a085", 7, 1)
        
        # Otras estadísticas
        self.create_section_label("🔧 Operaciones", 6)
        
        self.pending_maintenance_card = self.create_stat_card("Mantenimiento Pendiente", "0", "#e67e22", 7, 2)
        self.low_stock_card = self.create_stat_card("Items Bajo Stock", "0", "#c0392b", 7, 3)
    
    def create_section_label(self, text: str, row: int):
        """Crea una etiqueta de sección"""
        label = ctk.CTkLabel(
            self,
            text=text,
            font=FONTS["subheading"],
            anchor="w"
        )
        label.grid(row=row, column=0, columnspan=4, pady=(20, 10), padx=20, sticky="w")
    
    def create_stat_card(self, title: str, value: str, color: str, row: int, col: int):
        """Crea una tarjeta de estadística"""
        card = ctk.CTkFrame(self, corner_radius=10, fg_color=color)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Título
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=FONTS["body"],
            text_color="white"
        )
        title_label.pack(pady=(15, 5), padx=15)
        
        # Valor
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        )
        value_label.pack(pady=(0, 15), padx=15)
        
        return {"card": card, "title": title_label, "value": value_label}
    
    def load_data(self):
        """Carga los datos del dashboard"""
        try:
            # Obtener datos del dashboard
            self.dashboard_data = api_client.get("/api/dashboard/overview")
            
            # Actualizar tarjetas
            self.update_cards()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos del dashboard:\n{str(e)}")
    
    def update_cards(self):
        """Actualiza las tarjetas con los datos"""
        if not self.dashboard_data:
            return
        
        # Habitaciones
        rooms = self.dashboard_data.get("rooms", {})
        self.total_rooms_card["value"].configure(text=str(rooms.get("total", 0)))
        self.available_rooms_card["value"].configure(text=str(rooms.get("available", 0)))
        self.occupied_rooms_card["value"].configure(text=str(rooms.get("occupied", 0)))
        self.cleaning_rooms_card["value"].configure(text=str(rooms.get("cleaning", 0)))
        self.occupancy_rate_card["value"].configure(text=f"{rooms.get('occupancy_rate', 0)}%")
        self.maintenance_rooms_card["value"].configure(text=str(rooms.get("maintenance", 0)))
        
        # Reservas
        reservations = self.dashboard_data.get("reservations", {})
        self.today_checkins_card["value"].configure(text=str(reservations.get("today_checkins", 0)))
        self.today_checkouts_card["value"].configure(text=str(reservations.get("today_checkouts", 0)))
        self.active_reservations_card["value"].configure(text=str(reservations.get("active", 0)))
        self.pending_reservations_card["value"].configure(text=str(reservations.get("pending", 0)))
        
        # Ingresos
        revenue = self.dashboard_data.get("revenue", {})
        self.today_revenue_card["value"].configure(text=f"${revenue.get('today', 0):,.2f}")
        self.monthly_revenue_card["value"].configure(text=f"${revenue.get('monthly', 0):,.2f}")
        
        # Mantenimiento
        maintenance = self.dashboard_data.get("maintenance", {})
        self.pending_maintenance_card["value"].configure(text=str(maintenance.get("pending", 0)))
        
        # Inventario
        inventory = self.dashboard_data.get("inventory", {})
        self.low_stock_card["value"].configure(text=str(inventory.get("low_stock_items", 0)))