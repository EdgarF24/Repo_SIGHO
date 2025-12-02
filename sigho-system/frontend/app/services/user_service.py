"""
Servicio de Usuarios
"""
from typing import List, Dict, Any, Optional
from app.services.api_client import api_client


class UserService:
    """Servicio para gestionar usuarios del sistema"""
    
    def get_all(self, skip: int = 0, limit: int = 100, 
                role: Optional[str] = None, 
                is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Obtiene todos los usuarios"""
        params = {"skip": skip, "limit": limit}
        if role:
            params["role"] = role
        if is_active is not None:
            params["is_active"] = is_active
        return api_client.get("/api/users/", params=params)
    
    def get_by_id(self, user_id: int) -> Dict[str, Any]:
        """Obtiene un usuario por ID"""
        return api_client.get(f"/api/users/{user_id}")
    
    def get_by_username(self, username: str) -> Dict[str, Any]:
        """Obtiene un usuario por username"""
        return api_client.get(f"/api/users/by-username/{username}")
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Busca usuarios"""
        return api_client.get("/api/users/search", params={"query": query})
    
    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo usuario"""
        return api_client.post("/api/users/", json_data=user_data)
    
    def update(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un usuario"""
        return api_client.put(f"/api/users/{user_id}", json_data=user_data)
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> Dict[str, Any]:
        """Cambia la contraseña de un usuario"""
        data = {
            "current_password": current_password,
            "new_password": new_password
        }
        return api_client.post(f"/api/users/{user_id}/change-password", json_data=data)
    
    def activate(self, user_id: int) -> Dict[str, Any]:
        """Activa un usuario"""
        return api_client.post(f"/api/users/{user_id}/activate")
    
    def deactivate(self, user_id: int) -> Dict[str, Any]:
        """Desactiva un usuario"""
        return api_client.post(f"/api/users/{user_id}/deactivate")
    
    def delete(self, user_id: int) -> Dict[str, Any]:
        """Elimina un usuario"""
        return api_client.delete(f"/api/users/{user_id}")


# Instancia global
user_service = UserService()
