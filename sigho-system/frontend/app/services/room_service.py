"""
Servicio de Habitaciones
"""
from typing import List, Dict, Any, Optional
from app.services.api_client import api_client


class RoomService:
    """Servicio para gestionar habitaciones"""
    
    # ========== ROOM TYPES ==========
    def get_room_types(self, skip: int = 0, limit: int = 100, 
                       is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Obtiene tipos de habitación"""
        params = {"skip": skip, "limit": limit}
        if is_active is not None:
            params["is_active"] = is_active
        return api_client.get("/api/rooms/types", params=params)
    
    def get_room_type(self, room_type_id: int) -> Dict[str, Any]:
        """Obtiene un tipo de habitación por ID"""
        return api_client.get(f"/api/rooms/types/{room_type_id}")
    
    def create_room_type(self, room_type_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un tipo de habitación"""
        return api_client.post("/api/rooms/types", json_data=room_type_data)
    
    def update_room_type(self, room_type_id: int, room_type_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un tipo de habitación"""
        return api_client.put(f"/api/rooms/types/{room_type_id}", json_data=room_type_data)
    
    def delete_room_type(self, room_type_id: int) -> Dict[str, Any]:
        """Elimina un tipo de habitación"""
        return api_client.delete(f"/api/rooms/types/{room_type_id}")
    
    # ========== ROOMS ==========
    def get_all(self, skip: int = 0, limit: int = 100,
                floor: Optional[int] = None,
                status: Optional[str] = None,
                room_type_id: Optional[int] = None,
                is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Obtiene todas las habitaciones"""
        params = {"skip": skip, "limit": limit}
        if floor is not None:
            params["floor"] = floor
        if status:
            params["status"] = status
        if room_type_id:
            params["room_type_id"] = room_type_id
        if is_active is not None:
            params["is_active"] = is_active
        
        return api_client.get("/api/rooms/", params=params)
    
    def get_available(self, check_in: str, check_out: str) -> List[Dict[str, Any]]:
        """Obtiene habitaciones disponibles"""
        params = {"check_in": check_in, "check_out": check_out}
        return api_client.get("/api/rooms/available", params=params)
    
    def check_availability(self, check_in_date: str, check_out_date: str,
                          num_adults: int = 1, num_children: int = 0) -> List[Dict[str, Any]]:
        """Verifica disponibilidad y precios"""
        data = {
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "num_adults": num_adults,
            "num_children": num_children
        }
        return api_client.post("/api/rooms/check-availability", json_data=data)
    
    def get_by_id(self, room_id: int) -> Dict[str, Any]:
        """Obtiene una habitación por ID"""
        return api_client.get(f"/api/rooms/{room_id}")
    
    def create(self, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una habitación"""
        return api_client.post("/api/rooms/", json_data=room_data)
    
    def update(self, room_id: int, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza una habitación"""
        return api_client.put(f"/api/rooms/{room_id}", json_data=room_data)
    
    def change_status(self, room_id: int, status: str) -> Dict[str, Any]:
        """Cambia el estado de una habitación"""
        data = {"status": status}
        return api_client.put(f"/api/rooms/{room_id}/status", json_data=data)
    
    def delete(self, room_id: int) -> Dict[str, Any]:
        """Elimina una habitación"""
        return api_client.delete(f"/api/rooms/{room_id}")


# Instancia global
room_service = RoomService()