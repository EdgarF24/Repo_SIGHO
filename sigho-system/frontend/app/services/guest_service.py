"""
Servicio de Huéspedes
"""
from typing import List, Dict, Any, Optional
from app.services.api_client import api_client


class GuestService:
    """Servicio para gestionar huéspedes"""
    
    def get_all(self, skip: int = 0, limit: int = 100, country: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene todos los huéspedes"""
        params = {"skip": skip, "limit": limit}
        if country:
            params["country"] = country
        return api_client.get("/api/guests/", params=params)
    
    def get_by_id(self, guest_id: int) -> Dict[str, Any]:
        """Obtiene un huésped por ID"""
        return api_client.get(f"/api/guests/{guest_id}")
    
    def get_by_document(self, id_number: str) -> Dict[str, Any]:
        """Obtiene un huésped por número de documento"""
        return api_client.get(f"/api/guests/by-document/{id_number}")
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Busca huéspedes"""
        return api_client.get("/api/guests/search", params={"query": query})
    
    def create(self, guest_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo huésped"""
        return api_client.post("/api/guests/", json_data=guest_data)
    
    def update(self, guest_id: int, guest_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un huésped"""
        return api_client.put(f"/api/guests/{guest_id}", json_data=guest_data)
    
    def delete(self, guest_id: int) -> Dict[str, Any]:
        """Elimina un huésped"""
        return api_client.delete(f"/api/guests/{guest_id}")


# Instancia global
guest_service = GuestService()