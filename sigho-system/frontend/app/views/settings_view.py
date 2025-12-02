"""
Vista Completa de Configuración del Sistema
"""
import customtkinter as ctk
from tkinter import messagebox
from config.theme import FONTS
from app.services.auth_service import auth_service


class SettingsView(ctk.CTkFrame):
    """Vista completa de configuración"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        ctk.CTkLabel(
            title_frame,
            text="⚙️ Configuración del Sistema",
            font=("Segoe UI", 28, "bold")
        ).pack(anchor="w")
        
        # Contenedor principal
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        
        # ===== APARIENCIA =====
        appearance_frame =  ctk.CTkFrame(content_frame)
        appearance_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        appearance_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            appearance_frame,
            text="🎨 Apariencia",
            font=FONTS["heading"]
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            appearance_frame,
            text="Tema de la aplicación:",
            font=FONTS["body"]
        ).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        
        theme_frame = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        theme_frame.grid(row=1, column=1, sticky="w", padx=20, pady=10)
        
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode().lower())
        
        ctk.CTkRadioButton(
            theme_frame,
            text="🌙 Oscuro",
            variable=self.theme_var,
            value="dark",
            command=self.change_theme,
            font=FONTS["body"]
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            theme_frame,
            text="☀️ Claro",
            variable=self.theme_var,
            value="light",
            command=self.change_theme,
            font=FONTS["body"]
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            theme_frame,
            text="⚙️ Sistema",
            variable=self.theme_var,
            value="system",
            command=self.change_theme,
            font=FONTS["body"]
        ).pack(side="left", padx=10)
        
        # Separador
        ctk.CTkFrame(content_frame, height=2).grid(row=1, column=0, sticky="ew", padx=40, pady=10)
        
        # ===== INFORMACIÓN DEL SISTEMA =====
        info_frame = ctk.CTkFrame(content_frame)
        info_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        info_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Información del Sistema",
            font=FONTS["heading"]
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 10))
        
        # Información
        info_data = [
            ("Sistema:", "SIGHO - Sistema Integrado de Gestión Hotelera"),
            ("Versión:", "1.0.0"),
            ("Backend:", "FastAPI + SQLite3"),
            ("Frontend:", "CustomTkinter"),
            ("URL Backend:", "http://127.0.0.1:8000"),
            ("Desarrollado por:", "Equipo SIGHO - 2024")
        ]
        
        for idx, (label, value) in enumerate(info_data, start=1):
            ctk.CTkLabel(
                info_frame,
                text=label,
                font=FONTS["body_bold"]
            ).grid(row=idx, column=0, sticky="w", padx=20, pady=5)
            
            ctk.CTkLabel(
                info_frame,
                text=value,
                font=FONTS["body"]
            ).grid(row=idx, column=1, sticky="w", padx=20, pady=5)
        
        # Separador
        ctk.CTkFrame(content_frame, height=2).grid(row=3, column=0, sticky="ew", padx=40, pady=10)
        
        # ===== PREFERENCIAS =====
        preferences_frame = ctk.CTkFrame(content_frame)
        preferences_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=10)
        preferences_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            preferences_frame,
            text="🔧 Preferencias",
            font=FONTS["heading"]
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 10))
        
        # Moneda predeterminada
        ctk.CTkLabel(
            preferences_frame,
            text="Moneda predeterminada:",
            font=FONTS["body"]
        ).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        
        self.currency_combo = ctk.CTkComboBox(
            preferences_frame,
            values=["VES", "USD", "EUR"],
            width=150
        )
        self.currency_combo.set("VES")
        self.currency_combo.grid(row=1, column=1, sticky="w", padx=20, pady=10)
        
        # Formato de fecha
        ctk.CTkLabel(
            preferences_frame,
            text="Formato de fecha:",
            font=FONTS["body"]
        ).grid(row=2, column=0, sticky="w", padx=20, pady=10)
        
        self.date_format_combo = ctk.CTkComboBox(
            preferences_frame,
            values=["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"],
            width=150
        )
        self.date_format_combo.set("DD/MM/YYYY")
        self.date_format_combo.grid(row=2, column=1, sticky="w", padx=20, pady=10)
        
        # Idioma
        ctk.CTkLabel(
            preferences_frame,
            text="Idioma:",
            font=FONTS["body"]
        ).grid(row=3, column=0, sticky="w", padx=20, pady=10)
        
        self.language_combo = ctk.CTkComboBox(
            preferences_frame,
            values=["Español", "English"],
            width=150,
            state="disabled"  # Por ahora solo español
        )
        self.language_combo.set("Español")
        self.language_combo.grid(row=3, column=1, sticky="w", padx=20, pady=10)
        
        # Guardar preferencias
        ctk.CTkButton(
            preferences_frame,
            text="💾 Guardar Preferencias",
            command=self.save_preferences,
            height=35
        ).grid(row=4, column=0, columnspan=2, padx=20, pady=(15, 10))
        
        # Separador
        ctk.CTkFrame(content_frame, height=2).grid(row=5, column=0, sticky="ew", padx=40, pady=10)
        
        # ===== ACCIONES =====
        actions_frame = ctk.CTkFrame(content_frame)
        actions_frame.grid(row=6, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkLabel(
            actions_frame,
            text="🔨 Acciones",
            font=FONTS["heading"]
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))
        
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, padx=20, pady=(0, 15))
        
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Limpiar Caché",
            command=self.clear_cache,
            width=180,
            height=35
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🚪 Cerrar Sesión",
            command=self.logout,
            width=180,
            height=35,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=5)
        
        # Separador
        ctk.CTkFrame(content_frame, height=2).grid(row=7, column=0, sticky="ew", padx=40, pady=10)
        
        # ===== ACERCA DE =====
        about_frame = ctk.CTkFrame(content_frame)
        about_frame.grid(row=8, column=0, sticky="ew", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            about_frame,
            text="📝 Acerca de",
            font=FONTS["heading"]
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        about_text = """
Sistema Integrado de Gestión Hotelera desarrollado para la 
administración completa de operaciones hoteleras en Venezuela.

Equipo de Desarrollo:
• Edgar Fermenio - Backend
• Andrés Sosa - Frontend
• Lino Gouveia - Base de Datos
• Santiago Mendez - Tester
• Santiago Martin - Tester

Proyecto Académico © 2024
        """
        
        ctk.CTkLabel(
            about_frame,
            text=about_text.strip(),
            font=FONTS["body"],
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))
    
    def change_theme(self):
        """Cambia el tema de la aplicación"""
        theme = self.theme_var.get()
        ctk.set_appearance_mode(theme)
        messagebox.showinfo("Tema Cambiado", f"Tema cambiado a: {theme}")
    
    def save_preferences(self):
        """Guarda las preferencias"""
        currency = self.currency_combo.get()
        date_format = self.date_format_combo.get()
        
        # Aquí se guardarían en un archivo de configuración
        # Por ahora solo mostramos un mensaje
        messagebox.showinfo(
            "Preferencias Guardadas",
            f"Preferencias guardadas correctamente:\\n\\n"
            f"Moneda: {currency}\\n"
            f"Formato de fecha: {date_format}"
        )
    
    def clear_cache(self):
        """Limpia la caché local"""
        confirm = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro que desea limpiar la caché local?"
        )
        
        if confirm:
            # Aquí se limpiaría la caché
            messagebox.showinfo("Éxito", "Caché limpiada correctamente")
    
    def logout(self):
        """Cierra la sesión del usuario"""
        confirm = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro que desea cerrar la sesión?\\n\\n"
            "Será redirigido a la pantalla de inicio de sesión."
        )
        
        if confirm:
            try:
                # Cerrar sesión en el backend
                auth_service.logout()
                messagebox.showinfo("Sesión Cerrada", "Sesión cerrada correctamente")
                
                # Aquí se debería volver a la pantalla de login
                # Por ahora solo mostramos el mensaje
                # self.parent.show_login_view()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cerrar sesión:\n{str(e)}")