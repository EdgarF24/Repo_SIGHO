"""
Configuración de tema visual
"""
import customtkinter as ctk

# Colores del tema oscuro
DARK_THEME = {
    "bg_color": "#1a1a1a",
    "fg_color": "#2b2b2b",
    "hover_color": "#343638",
    "text_color": "#dce4ee",
    "text_color_disabled": "#6c6c6c",
    "button_color": "#1f6aa5",
    "button_hover_color": "#2980b9",
    "border_color": "#3f3f3f",
    "sidebar_color": "#212121",
    "topbar_color": "#2b2b2b",
    "success_color": "#27ae60",
    "error_color": "#e74c3c",
    "warning_color": "#f39c12",
    "info_color": "#3498db"
}

# Colores del tema claro
LIGHT_THEME = {
    "bg_color": "#f0f0f0",
    "fg_color": "#ffffff",
    "hover_color": "#e5e5e5",
    "text_color": "#333333",
    "text_color_disabled": "#999999",
    "button_color": "#1f6aa5",
    "button_hover_color": "#2980b9",
    "border_color": "#cccccc",
    "sidebar_color": "#f8f8f8",
    "topbar_color": "#ffffff",
    "success_color": "#27ae60",
    "error_color": "#e74c3c",
    "warning_color": "#f39c12",
    "info_color": "#3498db"
}

def apply_theme(theme_name: str = "dark"):
    """Aplica el tema a la aplicación"""
    ctk.set_appearance_mode(theme_name)
    ctk.set_default_color_theme("blue")

def get_theme_colors(theme_name: str = "dark") -> dict:
    """Obtiene los colores del tema"""
    return DARK_THEME if theme_name == "dark" else LIGHT_THEME

# Estilos de fuentes
FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "heading": ("Segoe UI", 18, "bold"),
    "subheading": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 12),
    "body_bold": ("Segoe UI", 12, "bold"),
    "small": ("Segoe UI", 10),
    "button": ("Segoe UI", 12, "bold"),
    "input": ("Segoe UI", 11)
}

# Tamaños de componentes
SIZES = {
    "button_height": 36,
    "input_height": 36,
    "sidebar_width": 250,
    "topbar_height": 60,
    "corner_radius": 8,
    "border_width": 2,
    "padding": 10,
    "margin": 15
}