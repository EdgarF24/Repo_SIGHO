"""
Vista Completa de Reportes y Estadísticas
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json
from config.theme import FONTS, SIZES
from app.components.data_table import DataTable
from app.services.report_service import report_service


class ReportsView(ctk.CTkFrame):
    """Vista completa de reportes"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.current_report_data = []
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        title_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text="📈 Reportes y Estadísticas",
            font=("Segoe UI", 28, "bold")
        ).pack(side="left")
        
        # Grid de reportes
        reports_frame = ctk.CTkFrame(self)
        reports_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        reports_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        reports = [
            ("📊 Ocupación", self.occupancy_report, "#3498db"),
            ("💰 Ingresos", self.revenue_report, "#27ae60"),
            ("📅 Reservas", self.reservations_report, "#9b59b6"),
            ("🔧 Mantenimiento", self.maintenance_report, "#e67e22"),
            ("📦 Inventario", self.inventory_report, "#f39c12"),
            ("👥 Huéspedes", self.guests_report, "#1abc9c")
        ]
        
        row = 0
        col = 0
        for text, command, color in reports:
            btn = ctk.CTkButton(
                reports_frame,
                text=text,
                command=command,
                height=70,
                font=("Segoe UI", 16, "bold"),
                fg_color=color,
                hover_color=self._darken_color(color)
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Área de resultados
        results_frame = ctk.CTkFrame(self)
        results_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        results_frame.grid_rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Toolbar de resultados
        results_toolbar = ctk.CTkFrame(results_frame, height=50)
        results_toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        results_toolbar.grid_columnconfigure(1, weight=1)
        
        self.results_title = ctk.CTkLabel(
            results_toolbar,
            text="Seleccione un tipo de reporte",
            font=FONTS["heading"]
        )
        self.results_title.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        export_btn = ctk.CTkButton(
            results_toolbar,
            text="💾 Exportar",
            command=self.export_report,
            width=120,
            height=35
        )
        export_btn.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        
        # Tabla de resultados
        columns = [
            {"key": "col1", "label": "Columna 1", "width": 150},
            {"key": "col2", "label": "Columna 2", "width": 150},
            {"key": "col3", "label": "Columna 3", "width": 150},
            {"key": "col4", "label": "Columna 4", "width": 150}
        ]
        
        self.results_table = DataTable(
            results_frame,
            columns=columns
        )
        self.results_table.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    
    def _darken_color(self, hex_color: str) -> str:
        """Oscurece un color hex para el efecto hover"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = max(0, r-30), max(0, g-30), max(0, b-30)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def occupancy_report(self):
        """Genera reporte de ocupación"""
        try:
            # Solicitar rango de fechas
            dialog = DateRangeDialog(self, "Reporte de Ocupación")
            
            if dialog.result:
                start_date, end_date = dialog.result
                data = report_service.get_occupancy(start_date, end_date)
                
                # Formatear datos para la tabla
                if isinstance(data, dict):
                    # Convertir dict a lista de registros
                    table_data = [{
                        "col1": "Fecha",
                        "col2": "Habitaciones Ocupadas",
                        "col3": "Habitaciones Disponibles",
                        "col4": "Tasa de Ocupación"
                    }]
                    
                    for key, value in data.items():
                        if isinstance(value, dict):
                            table_data.append({
                                "col1": key,
                                "col2": str(value.get('occupied', 0)),
                                "col3": str(value.get('available', 0)),
                                "col4": f"{value.get('rate', 0):.1f}%"
                            })
                else:
                    table_data = [{"col1": "Sin datos", "col2": "-", "col3": "-", "col4": "-"}]
                
                # Actualizar columnas
                columns = [
                    {"key": "col1", "label": "Fecha", "width": 150},
                    {"key": "col2", "label": "Ocupadas", "width": 150},
                    {"key": "col3", "label": "Disponibles", "width": 150},
                    {"key": "col4", "label": "Tasa", "width": 150}
                ]
                self.results_table.update_columns(columns)
                self.results_table.load_data(table_data)
                self.current_report_data = table_data
                self.results_title.configure(text="📊 Reporte de Ocupación")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")
    
    def revenue_report(self):
        """Genera reporte de ingresos"""
        try:
            dialog = DateRangeDialog(self, "Reporte de Ingresos")
            
            if dialog.result:
                start_date, end_date = dialog.result
                data = report_service.get_revenue(start_date, end_date)
                
                # Formatear datos
                table_data = []
                if isinstance(data, dict):
                    for key, value in data.items():
                        table_data.append({
                            "col1": key,
                            "col2": f"${value.get('VES', 0):,.2f}",
                            "col3": f"${value.get('USD', 0):,.2f}",
                            "col4": f"€{value.get('EUR', 0):,.2f}"
                        })
                
                if not table_data:
                    table_data = [{"col1": "Sin datos", "col2": "-", "col3": "-", "col4": "-"}]
                
                columns = [
                    {"key": "col1", "label": "Período", "width": 150},
                    {"key": "col2", "label": "VES", "width": 150},
                    {"key": "col3", "label": "USD", "width": 150},
                    {"key": "col4", "label": "EUR", "width": 150}
                ]
                self.results_table.update_columns(columns)
                self.results_table.load_data(table_data)
                self.current_report_data = table_data
                self.results_title.configure(text="💰 Reporte de Ingresos")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")
    
    def reservations_report(self):
        """Genera reporte de reservas"""
        try:
            dialog = DateRangeDialog(self, "Reporte de Reservas")
            
            if dialog.result:
                start_date, end_date = dialog.result
                data = report_service.get_reservations(start_date, end_date)
                
                table_data = []
                if isinstance(data, list):
                    for item in data:
                        table_data.append({
                            "col1": item.get('confirmation_code', 'N/A'),
                            "col2": item.get('guest_name', 'N/A'),
                            "col3": item.get('check_in_date', 'N/A'),
                            "col4": item.get('status', 'N/A')
                        })
                
                if not table_data:
                    table_data = [{"col1": "Sin datos", "col2": "-", "col3": "-", "col4": "-"}]
                
                columns = [
                    {"key": "col1", "label": "Código", "width": 120},
                    {"key": "col2", "label": "Huésped", "width": 200},
                    {"key": "col3", "label": "Check-in", "width": 120},
                    {"key": "col4", "label": "Estado", "width": 120}
                ]
                self.results_table.update_columns(columns)
                self.results_table.load_data(table_data)
                self.current_report_data = table_data
                self.results_title.configure(text="📅 Reporte de Reservas")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")
    
    def maintenance_report(self):
        """Genera reporte de mantenimiento"""
        try:
            data = report_service.get_maintenance()
            
            table_data = []
            if isinstance(data, dict):
                # Estadísticas por estado
                for status, count in data.items():
                    table_data.append({
                        "col1": status,
                        "col2": str(count),
                        "col3": "-",
                        "col4": "-"
                    })
            
            if not table_data:
                table_data = [{"col1": "Sin datos", "col2": "-", "col3": "-", "col4": "-"}]
            
            columns = [
                {"key": "col1", "label": "Estado", "width": 200},
                {"key": "col2", "label": "Cantidad", "width": 150},
                {"key": "col3", "label": "-", "width": 150},
                {"key": "col4", "label": "-", "width": 150}
            ]
            self.results_table.update_columns(columns)
            self.results_table.load_data(table_data)
            self.current_report_data = table_data
            self.results_title.configure(text="🔧 Reporte de Mantenimiento")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")
    
    def inventory_report(self):
        """Genera reporte de inventario"""
        try:
            data = report_service.get_inventory()
            
            table_data = []
            if isinstance(data, list):
                for item in data:
                    table_data.append({
                        "col1": item.get('name', 'N/A'),
                        "col2": str(item.get('current_quantity', 0)),
                        "col3": str(item.get('minimum_quantity', 0)),
                        "col4": item.get('category', 'N/A')
                    })
            
            if not table_data:
                table_data = [{"col1": "Sin datos", "col2": "-", "col3": "-", "col4": "-"}]
            
            columns = [
                {"key": "col1", "label": "Item", "width": 200},
                {"key": "col2", "label": "Cantidad Actual", "width": 120},
                {"key": "col3", "label": "Cantidad Mínima", "width": 120},
                {"key": "col4", "label": "Categoría", "width": 120}
            ]
            self.results_table.update_columns(columns)
            self.results_table.load_data(table_data)
            self.current_report_data = table_data
            self.results_title.configure(text="📦 Reporte de Inventario")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")
    
    def guests_report(self):
        """Genera reporte de huéspedes"""
        try:
            data = report_service.get_guests()
            
            table_data = []
            if isinstance(data, list):
                for guest in data:
                    table_data.append({
                        "col1": f"{guest.get('first_name', '')} {guest.get('last_name', '')}",
                        "col2": guest.get('email', 'N/A'),
                        "col3": guest.get('country', 'N/A'),
                        "col4": str(guest.get('reservations_count', 0))
                    })
            
            if not table_data:
                table_data = [{"col1": "Sin datos", "col2": "-", "col3": "-", "col4": "-"}]
            
            columns = [
                {"key": "col1", "label": "Nombre", "width": 200},
                {"key": "col2", "label": "Email", "width": 200},
                {"key": "col3", "label": "País", "width": 120},
                {"key": "col4", "label": "Reservas", "width": 80}
            ]
            self.results_table.update_columns(columns)
            self.results_table.load_data(table_data)
            self.current_report_data = table_data
            self.results_title.configure(text="👥 Reporte de Huéspedes")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")
    
    def export_report(self):
        """Exporta el reporte actual"""
        if not self.current_report_data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        # Solicitar nombre de archivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.current_report_data, f, indent=2, ensure_ascii=False)
                elif filename.endswith('.csv'):
                    import csv
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        if self.current_report_data:
                            writer = csv.DictWriter(f, fieldnames=self.current_report_data[0].keys())
                            writer.writeheader()
                            writer.writerows(self.current_report_data)
                
                messagebox.showinfo("Éxito", f"Reporte exportado a:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")


class DateRangeDialog(ctk.CTkToplevel):
    """Diálogo para seleccionar rango de fechas"""
    
    def __init__(self, parent, title="Seleccionar Rango de Fechas"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x250")
        self.resizable(False, False)
        
        self.result = None
        
        # Contenido
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Fecha inicio
        ctk.CTkLabel(main_frame, text="Fecha Inicio:", font=FONTS["body"]).grid(row=0, column=0, sticky="w", pady=10)
        self.start_entry = ctk.CTkEntry(main_frame, placeholder_text="YYYY-MM-DD")
        self.start_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        
        # Fecha fin
        ctk.CTkLabel(main_frame, text="Fecha Fin:", font=FONTS["body"]).grid(row=1, column=0, sticky="w", pady=10)
        self.end_entry = ctk.CTkEntry(main_frame, placeholder_text="YYYY-MM-DD")
        self.end_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        
        # Atajos
        shortcuts_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        shortcuts_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ctk.CTkButton(shortcuts_frame, text="Hoy", command=lambda: self.set_range(0), width=80).pack(side="left", padx=3)
        ctk.CTkButton(shortcuts_frame, text="Última Semana", command=lambda: self.set_range(7), width=120).pack(side="left", padx=3)
        ctk.CTkButton(shortcuts_frame, text="Último Mes", command=lambda: self.set_range(30), width=100).pack(side="left", padx=3)
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ctk.CTkButton(btn_frame, text="Cancelar", command=self.cancel, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Aceptar", command=self.accept, width=100).pack(side="left", padx=5)
        
        # Establecer valores por defecto (último mes)
        self.set_range(30)
        
        # Modal
        self.transient(parent)
        self.grab_set()
        self.wait_window()
    
    def set_range(self, days: int):
        """Establece un rango de días"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        self.start_entry.delete(0, 'end')
        self.start_entry.insert(0, start_date.strftime("%Y-%m-%d"))
        
        self.end_entry.delete(0, 'end')
        self.end_entry.insert(0, end_date.strftime("%Y-%m-%d"))
    
    def accept(self):
        """Acepta el diálogo"""
        start = self.start_entry.get()
        end = self.end_entry.get()
        
        if not start or not end:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambas fechas")
            return
        
        self.result = (start, end)
        self.destroy()
    
    def cancel(self):
        """Cancela el diálogo"""
        self.destroy()
