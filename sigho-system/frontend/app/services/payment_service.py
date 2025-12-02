# ========== frontend/app/services/payment_service.py ==========
from typing import List, Dict, Any, Optional
from app.services.api_client import api_client


class PaymentService:
    """Servicio para gestionar pagos"""
    
    def get_all(self, skip: int = 0, limit: int = 100,
                reservation_id: Optional[int] = None,
                status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene todos los pagos"""
        params = {"skip": skip, "limit": limit}
        if reservation_id:
            params["reservation_id"] = reservation_id
        if status:
            params["status"] = status
        return api_client.get("/api/payments/", params=params)
    
    def get_by_reservation(self, reservation_id: int) -> List[Dict[str, Any]]:
        """Obtiene pagos de una reserva"""
        return api_client.get(f"/api/payments/reservation/{reservation_id}")
    
    def get_by_id(self, payment_id: int) -> Dict[str, Any]:
        """Obtiene un pago por ID"""
        return api_client.get(f"/api/payments/{payment_id}")
    
    def create(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo pago"""
        return api_client.post("/api/payments/", json_data=payment_data)
    
    def update(self, payment_id: int, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un pago"""
        return api_client.put(f"/api/payments/{payment_id}", json_data=payment_data)
    
    def refund(self, payment_id: int) -> Dict[str, Any]:
        """Reembolsa un pago"""
        return api_client.post(f"/api/payments/{payment_id}/refund")
    
    def delete(self, payment_id: int) -> Dict[str, Any]:
        """Elimina un pago"""
        return api_client.delete(f"/api/payments/{payment_id}")


# Instancia global
payment_service = PaymentService()
