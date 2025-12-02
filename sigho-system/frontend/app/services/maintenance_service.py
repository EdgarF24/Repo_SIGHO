#========== frontend/app/services/maintenance_service.py ==========
from typing import List, Dict, Any, Optional
from app.services.api_client import api_client


class MaintenanceService:
    """Servicio para gestionar mantenimiento"""
    
    def get_all(self, skip: int = 0, limit: int = 100,
                status: Optional[str] = None,
                priority: Optional[str] = None,
                room_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtiene todos los registros de mantenimiento"""
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if room_id:
            params["room_id"] = room_id
        return api_client.get("/api/maintenance/", params=params)
    
    def get_pending(self) -> List[Dict[str, Any]]:
        """Obtiene mantenimientos pendientes"""
        return api_client.get("/api/maintenance/pending")
    
    def get_in_progress(self) -> List[Dict[str, Any]]:
        """Obtiene mantenimientos en progreso"""
        return api_client.get("/api/maintenance/in-progress")
    
    def get_by_id(self, maintenance_id: int) -> Dict[str, Any]:
        """Obtiene un mantenimiento por ID"""
        return api_client.get(f"/api/maintenance/{maintenance_id}")
    
    def create(self, maintenance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo registro de mantenimiento"""
        return api_client.post("/api/maintenance/", json_data=maintenance_data)
    
    def update(self, maintenance_id: int, maintenance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un mantenimiento"""
        return api_client.put(f"/api/maintenance/{maintenance_id}", json_data=maintenance_data)
    
    def assign(self, maintenance_id: int, user_id: int) -> Dict[str, Any]:
        """Asigna un mantenimiento a un usuario"""
        return api_client.post(f"/api/maintenance/{maintenance_id}/assign", 
                              json_data={"assigned_to": user_id})
    
    def start(self, maintenance_id: int) -> Dict[str, Any]:
        """Inicia un mantenimiento"""
        return api_client.post(f"/api/maintenance/{maintenance_id}/start")
    
    def complete(self, maintenance_id: int, actual_cost: float, 
                resolution_notes: str, materials_used: Optional[str] = None) -> Dict[str, Any]:
        """Completa un mantenimiento"""
        data = {
            "actual_cost": actual_cost,
            "resolution_notes": resolution_notes,
            "materials_used": materials_used
        }
        return api_client.post(f"/api/maintenance/{maintenance_id}/complete", json_data=data)
    
    def cancel(self, maintenance_id: int) -> Dict[str, Any]:
        """Cancela un mantenimiento"""
        return api_client.post(f"/api/maintenance/{maintenance_id}/cancel")
    
    def delete(self, maintenance_id: int) -> Dict[str, Any]:
        """Elimina un mantenimiento"""
        return api_client.delete(f"/api/maintenance/{maintenance_id}")


# Instancia global
maintenance_service = MaintenanceService()