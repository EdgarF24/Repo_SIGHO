"""
Componente Topbar (Barra superior)
"""
import customtkinter as ctk
from datetime import datetime
from config.theme import FONTS, SIZES
from app.services.auth_service import auth_service


class Topbar(ctk.CTkFrame):
    """Barra superior con título y acciones"""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            height=SIZES["topbar_height"],
            corner_radius=0
        )
        
        # No permitir que se redimensione
        self.grid_propagate(False)
        
        self.title_text = "Dashboard"
        self.setup_ui()
        
        # Actualizar reloj cada segundo
        self.update_clock()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self,
            text=self.title_text,
            font=FONTS["heading"],
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, padx=20, sticky="w")
        
        # Espaciador
        ctk.CTkFrame(self, fg_color="transparent").grid(row=0, column=1, sticky="ew")
        
        # Fecha y hora
        self.datetime_label = ctk.CTkLabel(
            self,
            text="",
            font=FONTS["body"]
        )
        self.datetime_label.grid(row=0, column=2, padx=20, sticky="e")
        
        # Usuario
        user = auth_service.get_user()
        if user:
            user_text = f"👤 {user['username']}"
            self.user_label = ctk.CTkLabel(
                self,
                text=user_text,
                font=FONTS["body_bold"]
            )
            self.user_label.grid(row=0, column=3, padx=(0, 20), sticky="e")
    
    def update_clock(self):
        """Actualiza el reloj"""
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M:%S")
        self.datetime_label.configure(text=f"📅 {date_str}  🕐 {time_str}")
        
        # Actualizar cada segundo
        self.after(1000, self.update_clock)
    
    def set_title(self, title: str):
        """Establece el título"""
        self.title_text = title
        self.title_label.configure(text=title)