"""
Componente de Tabla de Datos
"""
import customtkinter as ctk
from tkinter import ttk
from typing import List, Dict, Any, Callable, Optional
from config.theme import FONTS


class DataTable(ctk.CTkFrame):
    """Tabla de datos reutilizable con funcionalidad de selección"""
    
    def __init__(self, parent, columns: List[Dict[str, Any]], 
                 on_double_click: Optional[Callable] = None,
                 on_select: Optional[Callable] = None):
        """
        Args:
            parent: Widget padre
            columns: Lista de diccionarios con configuración de columnas
                    [{"key": "id", "label": "ID", "width": 50}, ...]
            on_double_click: Callback cuando se hace doble clic en una fila
            on_select: Callback cuando se selecciona una fila
        """
        super().__init__(parent)
        
        self.columns = columns
        self.on_double_click = on_double_click
        self.on_select = on_select
        self.data = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Crear Treeview
        style = ttk.Style()
        style.theme_use("default")
        
        # Configurar estilo
        style.configure(
            "Custom.Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0,
            font=FONTS["body"]
        )
        style.configure(
            "Custom.Treeview.Heading",
            background="#1f6aa5",
            foreground="white",
            font=FONTS["body_bold"]
        )
        style.map("Custom.Treeview",
                 background=[("selected", "#1f6aa5")])
        
        # Frame para la tabla y scrollbar
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        
        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Crear treeview
        column_ids = [col["key"] for col in self.columns]
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=column_ids,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            selectmode="browse"
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Configurar columnas
        for col in self.columns:
            self.tree.heading(col["key"], text=col["label"])
            width = col.get("width", 100)
            self.tree.column(col["key"], width=width, anchor=col.get("anchor", "w"))
        
        # Bind eventos
        if self.on_double_click:
            self.tree.bind("<Double-1>", self._handle_double_click)
        
        if self.on_select:
            self.tree.bind("<<TreeviewSelect>>", self._handle_select)
    
    def _handle_double_click(self, event):
        """Maneja el doble clic"""
        selection = self.tree.selection()
        if selection and self.on_double_click:
            item_id = selection[0]
            values = self.tree.item(item_id, "values")
            
            # Encontrar el item en los datos
            for item in self.data:
                if str(item.get(self.columns[0]["key"])) == values[0]:
                    self.on_double_click(item)
                    break
    
    def _handle_select(self, event):
        """Maneja la selección"""
        selection = self.tree.selection()
        if selection and self.on_select:
            item_id = selection[0]
            values = self.tree.item(item_id, "values")
            
            # Encontrar el item en los datos
            for item in self.data:
                if str(item.get(self.columns[0]["key"])) == values[0]:
                    self.on_select(item)
                    break
    
    def load_data(self, data: List[Dict[str, Any]]):
        """Carga datos en la tabla"""
        # Guardar datos
        self.data = data
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar nuevos datos
        for item in data:
            values = []
            for col in self.columns:
                value = item.get(col["key"], "")
                
                # Formatear valor si hay formatter
                if "formatter" in col:
                    value = col["formatter"](value)
                
                values.append(value)
            
            self.tree.insert("", "end", values=values)
    
    def get_selected_item(self) -> Optional[Dict[str, Any]]:
        """Obtiene el item seleccionado"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item_id = selection[0]
        values = self.tree.item(item_id, "values")
        
        # Encontrar el item en los datos
        for item in self.data:
            if str(item.get(self.columns[0]["key"])) == values[0]:
                return item
        
        return None
    
    def clear(self):
        """Limpia la tabla"""
        self.data = []
        for item in self.tree.get_children():
            self.tree.delete(item)