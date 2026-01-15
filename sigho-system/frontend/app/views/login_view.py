"""
Vista de Login
"""
import customtkinter as ctk
from tkinter import messagebox
from app.services.auth_service import auth_service
from config.theme import FONTS, SIZES
from config.settings import APP_NAME


class LoginView(ctk.CTkFrame):
    """Vista de inicio de sesión"""
    
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Centrar el contenido
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Container principal
        container = ctk.CTkFrame(self, corner_radius=20)
        container.grid(row=0, column=0, sticky="", padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1)
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            container,
            text="" + APP_NAME,
            font=FONTS["title"]
        )
        title_label.grid(row=0, column=0, pady=(30, 10), padx=40)
        
        subtitle_label = ctk.CTkLabel(
            container,
            text="Sistema de Gestión Hotelera",
            font=FONTS["body"]
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30), padx=40)
        
        # Frame de login
        login_frame = ctk.CTkFrame(container, corner_radius=10)
        login_frame.grid(row=2, column=0, pady=20, padx=40, sticky="ew")
        login_frame.grid_columnconfigure(0, weight=1)
        
        # Usuario
        ctk.CTkLabel(
            login_frame,
            text="Usuario:",
            font=FONTS["body_bold"],
            anchor="w"
        ).grid(row=0, column=0, pady=(20, 5), padx=20, sticky="w")
        
        self.username_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Ingrese su usuario",
            font=FONTS["input"],
            height=SIZES["input_height"]
        )
        self.username_entry.grid(row=1, column=0, pady=(0, 15), padx=20, sticky="ew")
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Contraseña
        ctk.CTkLabel(
            login_frame,
            text="Contraseña:",
            font=FONTS["body_bold"],
            anchor="w"
        ).grid(row=2, column=0, pady=(0, 5), padx=20, sticky="w")
        
        self.password_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Ingrese su contraseña",
            show="•",
            font=FONTS["input"],
            height=SIZES["input_height"]
        )
        self.password_entry.grid(row=3, column=0, pady=(0, 20), padx=20, sticky="ew")
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Botón de login
        self.login_button = ctk.CTkButton(
            login_frame,
            text="Iniciar Sesión",
            command=self.handle_login,
            font=FONTS["button"],
            height=SIZES["button_height"],
            corner_radius=SIZES["corner_radius"]
        )
        self.login_button.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="ew")
        
        # Información de credenciales por defecto
        info_frame = ctk.CTkFrame(container, fg_color="transparent")
        info_frame.grid(row=3, column=0, pady=(10, 30), padx=40)
        
        ctk.CTkLabel(
            info_frame,
            text="Credenciales de prueba:",
            font=FONTS["small"]
        ).pack()
        
        ctk.CTkLabel(
            info_frame,
            text="admin / admin123",
            font=("Segoe UI", 10, "bold")
        ).pack()
        
        # Enfocar el campo de usuario
        self.username_entry.focus()
    
    def handle_login(self):
        """Maneja el evento de login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validación
        if not username:
            messagebox.showerror("Error", "Por favor ingrese su usuario")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Error", "Por favor ingrese su contraseña")
            self.password_entry.focus()
            return
        
        # Deshabilitar botón
        self.login_button.configure(state="disabled", text="Iniciando sesión...")
        self.update()
        
        try:
            # Intentar login
            result = auth_service.login(username, password)
            
            if result["success"]:
                # Login exitoso
                user = result["user"]
                messagebox.showinfo(
                    "Login Exitoso",
                    f"Bienvenido/a {user['full_name']}"
                )
                self.on_login_success()
            else:
                # Login fallido
                messagebox.showerror("Error de Login", result.get("error", "Credenciales inválidas"))
                self.password_entry.delete(0, "end")
                self.password_entry.focus()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión:\n{str(e)}")
            self.password_entry.delete(0, "end")
            self.password_entry.focus()
        
        finally:
            # Rehabilitar botón
            self.login_button.configure(state="normal", text="Iniciar Sesión")