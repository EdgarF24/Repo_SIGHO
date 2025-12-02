"""
Servicio de Reservas
"""
from typing import List, Dict, Any, Optional
from datetime import date
from app.services.api_client import api_client


class ReservationService:
    """Servicio para gestionar reservas"""
    
    def get_all(self, skip: int = 0, limit: int = 100, 
                status: Optional[str] = None,
                check_in_date_from: Optional[str] = None,
                check_in_date_to: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene todas las reservas"""
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status
        if check_in_date_from:
            params["check_in_date_from"] = check_in_date_from
        if check_in_date_to:
            params["check_in_date_to"] = check_in_date_to
        
        return api_client.get("/api/reservations/", params=params)
    
    def get_today(self) -> List[Dict[str, Any]]:
        """Obtiene reservas de hoy"""
        return api_client.get("/api/reservations/today")
    
    def get_by_id(self, reservation_id: int) -> Dict[str, Any]:
        """Obtiene una reserva por ID"""
        return api_client.get(f"/api/reservations/{reservation_id}")
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Busca reservas"""
        return api_client.get("/api/reservations/search", params={"query": query})
    
    def create(self, reservation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva reserva"""
        return api_client.post("/api/reservations/", json_data=reservation_data)
    
    def update(self, reservation_id: int, reservation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza una reserva"""
        return api_client.put(f"/api/reservations/{reservation_id}", json_data=reservation_data)
    
    def check_in(self, reservation_id: int, notes: Optional[str] = None) -> Dict[str, Any]:
        """Realiza check-in"""
        data = {"notes": notes} if notes else {}
        return api_client.post(f"/api/reservations/{reservation_id}/check-in", json_data=data)
    
    def check_out(self, reservation_id: int, notes: Optional[str] = None) -> Dict[str, Any]:
        """Realiza check-out"""
        data = {"notes": notes} if notes else {}
        return api_client.post(f"/api/reservations/{reservation_id}/check-out", json_data=data)
    
    def cancel(self, reservation_id: int, reason: str) -> Dict[str, Any]:
        """Cancela una reserva"""
        data = {"cancellation_reason": reason}
        return api_client.post(f"/api/reservations/{reservation_id}/cancel", json_data=data)
    
    def delete(self, reservation_id: int) -> Dict[str, Any]:
        """Elimina una reserva"""
        return api_client.delete(f"/api/reservations/{reservation_id}")


# Instancia global
reservation_service = ReservationService()