"""
Componente de Diálogo con Formulario
"""
import customtkinter as ctk
from typing import Dict, List, Optional, Callable, Any
from config.theme import FONTS, SIZES


class FormDialog(ctk.CTkToplevel):
    """Diálogo modal con formulario genérico"""
    
    def __init__(self, parent, title: str, fields: List[Dict[str, Any]], 
                 on_submit: Callable, initial_values: Optional[Dict] = None,
                 width: int = 500, height: int = 600):
        """
        Args:
            parent: Ventana padre
            title: Título del diálogo
            fields: Lista de campos del formulario
                   [{"name": "username", "label": "Usuario", "type": "entry", "required": True}, ...]
            on_submit: Función callback al enviar (recibe dict con valores)
            initial_values: Valores iniciales para el formulario
            width: Ancho del diálogo
            height: Alto del diálogo
        """
        super().__init__(parent)
        
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        
        # Centrar en la pantalla
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Hacer modal
        self.transient(parent)
        self.grab_set()
        
        self.fields = fields
        self.on_submit = on_submit
        self.initial_values = initial_values or {}
        self.field_widgets = {}
        self.result = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Configurar grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(self, fg_color=("gray90", "gray20"))
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        ctk.CTkLabel(
            header,
            text=self.wm_title(),
            font=FONTS["heading"]
        ).pack(pady=15, padx=20)
        
        # Scrollable frame para el formulario
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 0))
        scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Crear campos
        row = 0
        for field in self.fields:
            self.create_field(scroll_frame, field, row)
            row += 1
        
        # Botones
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        button_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.on_cancel,
            fg_color="gray",
            hover_color="darkgray",
            height=SIZES["button_height"]
        ).grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        ctk.CTkButton(
            button_frame,
            text="Guardar",
            command=self.on_save,
            height=SIZES["button_height"]
        ).grid(row=0, column=1, padx=(5, 0), sticky="ew")
    
    def create_field(self, parent, field: Dict, row: int):
        """Crea un campo del formulario"""
        field_name = field["name"]
        field_type = field.get("type", "entry")
        required = field.get("required", False)
        
        # Label
        label_text = field["label"]
        if required:
            label_text += " *"
        
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=FONTS["body_bold"],
            anchor="w"
        )
        label.grid(row=row*2, column=0, sticky="w", pady=(10, 5), padx=5)
        
        # Widget según tipo
        widget = None
        initial_value = self.initial_values.get(field_name, field.get("default", ""))
        
        if field_type == "entry":
            widget = ctk.CTkEntry(
                parent,
                placeholder_text=field.get("placeholder", ""),
                height=SIZES["input_height"]
            )
            if initial_value:
                widget.insert(0, str(initial_value))
        
        elif field_type == "password":
            widget = ctk.CTkEntry(
                parent,
                show="•",
                placeholder_text=field.get("placeholder", ""),
                height=SIZES["input_height"]
            )
        
        elif field_type == "number":
            widget = ctk.CTkEntry(
                parent,
                placeholder_text=field.get("placeholder", "0"),
                height=SIZES["input_height"]
            )
            if initial_value:
                widget.insert(0, str(initial_value))
        
        elif field_type == "textarea":
            widget = ctk.CTkTextbox(
                parent,
                height=field.get("height", 100)
            )
            if initial_value:
                widget.insert("1.0", str(initial_value))
        
        elif field_type == "combobox":
            widget = ctk.CTkComboBox(
                parent,
                values=field.get("values", []),
                height=SIZES["input_height"]
            )
            if initial_value:
                widget.set(str(initial_value))
            elif field.get("values"):
                widget.set(field["values"][0])
        
        elif field_type == "checkbox":
            widget = ctk.CTkCheckBox(
                parent,
                text=field.get("checkbox_text", "")
            )
            if initial_value:
                widget.select()
        
        elif field_type == "date":
            widget = ctk.CTkEntry(
                parent,
                placeholder_text="YYYY-MM-DD",
                height=SIZES["input_height"]
            )
            if initial_value:
                widget.insert(0, str(initial_value))
        
        if widget:
            widget.grid(row=row*2 + 1, column=0, sticky="ew", pady=(0, 5), padx=5)
            self.field_widgets[field_name] = {
                "widget": widget,
                "type": field_type,
                "required": required
            }
    
    def get_field_value(self, field_name: str) -> Any:
        """Obtiene el valor de un campo"""
        field_info = self.field_widgets.get(field_name)
        if not field_info:
            return None
        
        widget = field_info["widget"]
        field_type = field_info["type"]
        
        if field_type == "textarea":
            return widget.get("1.0", "end-1c").strip()
        elif field_type == "checkbox":
            return widget.get() == 1
        elif field_type in ["combobox"]:
            return widget.get()
        else:
            return widget.get().strip()
    
    def validate_fields(self) -> tuple[bool, str]:
        """Valida los campos del formulario"""
        for field in self.fields:
            field_name = field["name"]
            field_info = self.field_widgets.get(field_name)
            
            if not field_info:
                continue
            
            if field_info["required"]:
                value = self.get_field_value(field_name)
                if not value or (isinstance(value, str) and not value.strip()):
                    return False, f"El campo '{field['label']}' es obligatorio"
            
            # Validaciones específicas por tipo
            if field.get("type") == "number":
                value = self.get_field_value(field_name)
                if value:
                    try:
                        float(value)
                    except ValueError:
                        return False, f"El campo '{field['label']}' debe ser un número"
            
            # Validación de email
            if field.get("validate") == "email":
                value = self.get_field_value(field_name)
                if value and "@" not in value:
                    return False, f"'{field['label']}' debe ser un email válido"
        
        return True, ""
    
    def get_values(self) -> Dict[str, Any]:
        """Obtiene todos los valores del formulario"""
        values = {}
        for field_name in self.field_widgets.keys():
            values[field_name] = self.get_field_value(field_name)
        return values
    
    def on_save(self):
        """Maneja el evento de guardar"""
        # Validar
        valid, error = self.validate_fields()
        if not valid:
            from tkinter import messagebox
            messagebox.showerror("Error de validación", error)
            return
        
        # Obtener valores
        values = self.get_values()
        
        # Llamar callback
        try:
            self.result = self.on_submit(values)
            self.destroy()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")
    
    def on_cancel(self):
        """Maneja el evento de cancelar"""
        self.result = None
        self.destroy()