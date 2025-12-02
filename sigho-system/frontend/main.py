"""
SIGHO - Sistema Integrado de Gestión Hotelera
Aplicación Principal - Frontend CustomTkinter
"""
import customtkinter as ctk
from tkinter import messagebox
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import (
    APP_NAME, 
    WINDOW_WIDTH, 
    WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT
)
from config.theme import apply_theme
from app.services.auth_service import auth_service
from app.views.login_view import LoginView
from app.views.main_window import MainWindow


class SIGHOApp(ctk.CTk):
    """Aplicación principal del sistema SIGHO"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Aplicar tema
        apply_theme("dark")
        
        # Centrar ventana
        self.center_window()
        
        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Manejar cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Verificar si hay sesión activa
        if auth_service.is_authenticated():
            self.show_main_window()
        else:
            self.show_login()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_login(self):
        """Muestra la vista de login"""
        # Limpiar ventana
        for widget in self.winfo_children():
            widget.destroy()
        
        # Crear vista de login
        login_view = LoginView(self, on_login_success=self.show_main_window)
        login_view.grid(row=0, column=0, sticky="nsew")
    
    def show_main_window(self):
        """Muestra la ventana principal"""
        # Limpiar ventana
        for widget in self.winfo_children():
            widget.destroy()
        
        # Crear ventana principal
        main_window = MainWindow(self, on_logout=self.handle_logout)
        main_window.grid(row=0, column=0, sticky="nsew")
    
    def handle_logout(self):
        """Maneja el cierre de sesión"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            auth_service.logout()
            self.show_login()
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir?"):
            self.destroy()


def main():
    """Función principal"""
    try:
        app = SIGHOApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()