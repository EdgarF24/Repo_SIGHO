"""
Servicio de Reportes
"""
from typing import Dict, Any, Optional
from datetime import date
from app.services.api_client import api_client


class ReportService:
    """Servicio para generar reportes"""
    
    def get_occupancy(self, start_date: Optional[str] = None, 
                     end_date: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene reporte de ocupación"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return api_client.get("/api/reports/occupancy", params=params)
    
    def get_revenue(self, start_date: Optional[str] = None,
                   end_date: Optional[str] = None,
                   currency: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene reporte de ingresos"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if currency:
            params["currency"] = currency
        return api_client.get("/api/reports/revenue", params=params)
    
    def get_reservations(self, start_date: Optional[str] = None,
                        end_date: Optional[str] = None,
                        status: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene reporte de reservas"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if status:
            params["status"] = status
        return api_client.get("/api/reports/reservations", params=params)
    
    def get_maintenance(self, start_date: Optional[str] = None,
                       end_date: Optional[str] = None,
                       status: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene reporte de mantenimiento"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if status:
            params["status"] = status
        return api_client.get("/api/reports/maintenance", params=params)
    
    def get_inventory(self, category: Optional[str] = None,
                     low_stock_only: bool = False) -> Dict[str, Any]:
        """Obtiene reporte de inventario"""
        params = {}
        if category:
            params["category"] = category
        if low_stock_only:
            params["low_stock_only"] = low_stock_only
        return api_client.get("/api/reports/inventory", params=params)
    
    def get_guests(self, country: Optional[str] = None,
                  frequent_only: bool = False) -> Dict[str, Any]:
        """Obtiene reporte de huéspedes"""
        params = {}
        if country:
            params["country"] = country
        if frequent_only:
            params["frequent_only"] = frequent_only
        return api_client.get("/api/reports/guests", params=params)
    
    def get_payments(self, start_date: Optional[str] = None,
                    end_date: Optional[str] = None,
                    currency: Optional[str] = None,
                    payment_method: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene reporte de pagos"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if currency:
            params["currency"] = currency
        if payment_method:
            params["payment_method"] = payment_method
        return api_client.get("/api/reports/payments", params=params)


# Instancia global
report_service = ReportService()
