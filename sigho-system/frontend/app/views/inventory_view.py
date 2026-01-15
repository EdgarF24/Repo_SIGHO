"""
Vista Completa de Gestión de Inventario
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any
from config.theme import FONTS, SIZES
from app.components.data_table import DataTable
from app.components.form_dialog import FormDialog
from app.services.inventory_service import inventory_service


class InventoryView(ctk.CTkFrame):
    """Vista completa de gestión de inventario"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_item = None
        self.setup_ui()
        self.load_items()
    
    def setup_ui(self):
        """Configura la interfaz"""
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Toolbar
        toolbar = ctk.CTkFrame(self, height=60)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        toolbar.grid_columnconfigure(1, weight=1)
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.grid(row=0, column=0, padx=5, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text=" Nuevo Item",
            command=self.create_item,
            width=130,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Editar",
            command=self.edit_item,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Movimiento",
            command=self.create_movement,
            width=130,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Ajustar",
            command=self.adjust_quantity,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Stock Bajo",
            command=self.show_low_stock,
            width=120,
            height=SIZES["button_height"],
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="Eliminar",
            command=self.delete_item,
            width=100,
            height=SIZES["button_height"],
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text=" Actualizar",
            command=self.load_items,
            width=100,
            height=SIZES["button_height"]
        ).pack(side="left", padx=2)
        
        # Filtros y búsqueda
        filter_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        filter_frame.grid(row=0, column=1, padx=5, pady=10, sticky="e")
        
        ctk.CTkLabel(filter_frame, text="Categoría:", font=FONTS["body"]).pack(side="left", padx=5)
        
        self.category_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Todas", "cleaning", "maintenance", "bedding", "bathroom", "kitchen", "electronics", "furniture", "food_beverage", "other"],
            command=self.filter_by_category,
            width=150
        )
        self.category_filter.set("Todas")
        self.category_filter.pack(side="left", padx=5)
        
        # Estadísticas
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.total_items_label = ctk.CTkLabel(
            stats_frame,
            text="Total items: 0",
            font=FONTS["body_bold"]
        )
        self.total_items_label.grid(row=0, column=0, pady=10, padx=20)
        
        self.low_stock_label = ctk.CTkLabel(
            stats_frame,
            text="Stock bajo: 0",
            font=FONTS["body_bold"],
            text_color="#e67e22"
        )
        self.low_stock_label.grid(row=0, column=1, pady=10, padx=20)
        
        self.total_value_label = ctk.CTkLabel(
            stats_frame,
            text="Valor total: $0",
            font=FONTS["body_bold"]
        )
        self.total_value_label.grid(row=0, column=2, pady=10, padx=20)
        
        # Tabla
        columns = [
            {"key": "id", "label": "ID", "width": 50},
            {"key": "item_code", "label": "Código", "width": 100},
            {"key": "name", "label": "Nombre", "width": 200},
            {"key": "category", "label": "Categoría", "width": 120},
            {"key": "current_quantity", "label": "Cantidad", "width": 80},
            {"key": "minimum_quantity", "label": "Mínimo", "width": 80},
            {"key": "unit", "label": "Unidad", "width": 80},
            {"key": "unit_price", "label": "Precio Unit.", "width": 100},
            {"key": "status_display", "label": "Estado", "width": 120}
        ]
        
        self.table = DataTable(
            self,
            columns=columns,
            on_double_click=self.view_item_details,
            on_select=self.on_item_select
        )
        self.table.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def load_items(self):
        """Carga los items de inventario"""
        try:
            items = inventory_service.get_all(limit=500)
            
            # Agregar indicador de estado
            low_stock_count = 0
            total_value = 0.0
            
            for item in items:
                qty = item.get('current_quantity', 0)
                min_qty = item.get('minimum_quantity', 0)
                price = item.get('unit_price', 0)
                
                if qty <= min_qty:
                    item['status_display'] = "Stock Bajo"
                    low_stock_count += 1
                elif qty <= min_qty * 1.5:
                    item['status_display'] = " Alerta"
                else:
                    item['status_display'] = "Normal"
                
                total_value += qty * price
            
            self.table.load_data(items)
            self.total_items_label.configure(text=f"Total items: {len(items)}")
            self.low_stock_label.configure(text=f"Stock bajo: {low_stock_count}")
            self.total_value_label.configure(text=f"Valor total: ${total_value:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar inventario:\n{str(e)}")
    
    def filter_by_category(self, category: str):
        """Filtra items por categoría"""
        try:
            if category == "Todas":
                self.load_items()
            else:
                items = inventory_service.get_by_category(category)
                
                for item in items:
                    qty = item.get('current_quantity', 0)
                    min_qty = item.get('minimum_quantity', 0)
                    if qty <= min_qty:
                        item['status_display'] = "Stock Bajo"
                    elif qty <= min_qty * 1.5:
                        item['status_display'] = " Alerta"
                    else:
                        item['status_display'] = "Normal"
                
                self.table.load_data(items)
                self.total_items_label.configure(text=f"Items en {category}: {len(items)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar:\n{str(e)}")
    
    def show_low_stock(self):
        """Muestra items con stock bajo"""
        try:
            items = inventory_service.get_low_stock()
            
            for item in items:
                item['status_display'] = "Stock Bajo"
            
            self.table.load_data(items)
            self.total_items_label.configure(text=f"Items con stock bajo: {len(items)}")
            
            if len(items) == 0:
                messagebox.showinfo("Información", "No hay items con stock bajo")
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener stock bajo:\n{str(e)}")
    
    def on_item_select(self, item: Dict[str, Any]):
        """Callback cuando se selecciona un item"""
        self.selected_item = item
    
    def view_item_details(self, item: Dict[str, Any]):
        """Muestra los detalles de un item"""
        details = f"""
Información del Item

Código: {item['item_code']}
Nombre: {item['name']}
Categoría: {item.get('category', 'N/A')}

Stock:
Cantidad Actual: {item['current_quantity']} {item.get('unit', 'unidades')}
Cantidad Mínima: {item['minimum_quantity']} {item.get('unit', 'unidades')}
Último Reabastecimiento: {item.get('last_restock_date', 'N/A')}

Precio:
Precio Unitario: ${item.get('unit_price', 0):.2f}
Valor Total: ${item.get('current_quantity', 0) * item.get('unit_price', 0):.2f}

Estado: {'Activo' if item.get('is_active') else 'Inactivo'}

Descripción:
{item.get('description', 'Sin descripción')}
        """
        
        messagebox.showinfo("Detalles del Item", details)
    
    def create_item(self):
        """Crea un nuevo item"""
        fields = [
            {"name": "item_code", "label": "Código del Item", "type": "entry", "required": True},
            {"name": "name", "label": "Nombre", "type": "entry", "required": True},
            {"name": "category", "label": "Categoría", "type": "combobox", 
             "values": ["cleaning", "maintenance", "bedding", "bathroom", "kitchen", "electronics", "furniture", "food_beverage", "other"], "required": True},
            {"name": "description", "label": "Descripción", "type": "textarea", "height": 80},
            {"name": "current_quantity", "label": "Cantidad Inicial", "type": "entry", "validate": "number", "default": "0"},
            {"name": "minimum_quantity", "label": "Cantidad Mínima", "type": "entry", "validate": "number", "required": True},
            {"name": "unit", "label": "Unidad de Medida", "type": "entry", "default": "unidades", "required": True},
            {"name": "unit_price", "label": "Precio Unitario", "type": "entry", "validate": "number", "default": "0.00"},
            {"name": "supplier", "label": "Proveedor", "type": "entry"},
            {"name": "location", "label": "Ubicación", "type": "entry"},
            {"name": "is_active", "label": "Activo", "type": "checkbox", "default": True}
        ]
        
        def on_submit(values):
            try:
                # Convertir valores numéricos
                values['current_quantity'] = int(values.get('current_quantity', 0))
                values['minimum_quantity'] = int(values.get('minimum_quantity', 0))
                values['unit_price'] = float(values.get('unit_price', 0))
                
                inventory_service.create(values)
                messagebox.showinfo("Éx ito", "Item creado correctamente")
                self.load_items()
                return True
            except Exception as e:
                raise Exception(f"Error al crear item: {str(e)}")
        
        FormDialog(
            self,
            title="Nuevo Item de Inventario",
            fields=fields,
            on_submit=on_submit,
            height=700
        )
    
    def edit_item(self):
        """Edita un item"""
        if not self.selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un item")
            return
        
        fields = [
            {"name": "name", "label": "Nombre", "type": "entry", "required": True},
            {"name": "category", "label": "Categoría", "type": "combobox", 
             "values": ["cleaning", "maintenance", "bedding", "bathroom", "kitchen", "electronics", "furniture", "food_beverage", "other"], "required": True},
            {"name": "description", "label": "Descripción", "type": "textarea", "height": 80},
            {"name": "minimum_quantity", "label": "Cantidad Mínima", "type": "entry", "validate": "number", "required": True},
            {"name": "unit", "label": "Unidad de Medida", "type": "entry", "required": True},
            {"name": "unit_price", "label": "Precio Unitario", "type": "entry", "validate": "number"},
            {"name": "supplier", "label": "Proveedor", "type": "entry"},
            {"name": "location", "label": "Ubicación", "type": "entry"},
            {"name": "is_active", "label": "Activo", "type": "checkbox"}
        ]
        
        def on_submit(values):
            try:
                # Convertir valores numéricos
                if 'minimum_quantity' in values:
                    values['minimum_quantity'] = int(values['minimum_quantity'])
                if 'unit_price' in values:
                    values['unit_price'] = float(values['unit_price'])
                
                inventory_service.update(self.selected_item['id'], values)
                messagebox.showinfo("Éxito", "Item actualizado correctamente")
                self.load_items()
                return True
            except Exception as e:
                raise Exception(f"Error al actualizar item: {str(e)}")
        
        FormDialog(
            self,
            title="Editar Item de Inventario",
            fields=fields,
            on_submit=on_submit,
            initial_values=self.selected_item,
            height=650
        )
    
    def create_movement(self):
        """Crea un movimiento de inventario"""
        if not self.selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un item")
            return
        
        fields = [
            {"name": "movement_type", "label": "Tipo de Movimiento", "type": "combobox",
             "values": ["IN", "OUT"], "required": True},
            {"name": "quantity", "label": "Cantidad", "type": "entry", "validate": "number", "required": True},
            {"name": "reason", "label": "Razón", "type": "entry", "required": True},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 80},
            {"name": "reference_document", "label": "Documento de Referencia", "type": "entry"}
        ]
        
        def on_submit(values):
            try:
                values['inventory_id'] = self.selected_item['id']
                values['quantity'] = int(values['quantity'])
                
                inventory_service.create_movement(values)
                messagebox.showinfo("Éxito", "Movimiento registrado correctamente")
                self.load_items()
                return True
            except Exception as e:
                raise Exception(f"Error al registrar movimiento: {str(e)}")
        
        FormDialog(
            self,
            title=f"Registrar Movimiento - {self.selected_item['name']}",
            fields=fields,
            on_submit=on_submit,
            height=500
        )
    
    def adjust_quantity(self):
        """Ajusta la cantidad de un item"""
        if not self.selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un item")
            return
        
        fields = [
            {"name": "new_quantity", "label": "Nueva Cantidad", "type": "entry", "validate": "number", "required": True},
            {"name": "reason", "label": "Razón del Ajuste", "type": "entry", "required": True},
            {"name": "notes", "label": "Notas", "type": "textarea", "height": 80}
        ]
        
        def on_submit(values):
            try:
                new_qty = int(values['new_quantity'])
                inventory_service.adjust(
                    self.selected_item['id'],
                    new_qty,
                    values['reason'],
                    values.get('notes')
                )
                messagebox.showinfo("Éxito", "Cantidad ajustada correctamente")
                self.load_items()
                return True
            except Exception as e:
                raise Exception(f"Error al ajustar cantidad: {str(e)}")
        
        initial_values = {
            "new_quantity": str(self.selected_item.get('current_quantity', 0))
        }
        
        FormDialog(
            self,
            title=f"Ajustar Cantidad - {self.selected_item['name']}",
            fields=fields,
            on_submit=on_submit,
            initial_values=initial_values,
            height=400
        )
    
    def delete_item(self):
        """Elimina un item"""
        if not self.selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un item")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar el item?\\n\\n"
            f"{self.selected_item['name']}\\n"
            f"Código: {self.selected_item['item_code']}\\n\\n"
            f"Esta acción no se puede deshacer."
        )
        
        if confirm:
            try:
                inventory_service.delete(self.selected_item['id'])
                messagebox.showinfo("Éxito", "Item eliminado correctamente")
                self.selected_item = None
                self.load_items()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar item:\\n{str(e)}")
