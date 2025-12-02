"""
Servicio de Inventario
"""
from typing import List, Dict, Any, Optional
from app.services.api_client import api_client


class InventoryService:
    """Servicio para gestionar inventario"""
    
    def get_all(self, skip: int = 0, limit: int = 100,
                category: Optional[str] = None,
                is_active: Optional[bool] = None,
                needs_restock: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Obtiene todos los items de inventario"""
        params = {"skip": skip, "limit": limit}
        if category:
            params["category"] = category
        if is_active is not None:
            params["is_active"] = is_active
        if needs_restock is not None:
            params["needs_restock"] = needs_restock
        return api_client.get("/api/inventory/", params=params)
    
    def get_by_id(self, item_id: int) -> Dict[str, Any]:
        """Obtiene un item de inventario por ID"""
        return api_client.get(f"/api/inventory/{item_id}")
    
    def get_low_stock(self) -> List[Dict[str, Any]]:
        """Obtiene items con stock bajo"""
        return api_client.get("/api/inventory/low-stock")
    
    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Obtiene items por categoría"""
        return api_client.get(f"/api/inventory/by-category/{category}")
    
    def create(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo item de inventario"""
        return api_client.post("/api/inventory/", json_data=item_data)
    
    def update(self, item_id: int, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un item de inventario"""
        return api_client.put(f"/api/inventory/{item_id}", json_data=item_data)
    
    def adjust(self, item_id: int, new_quantity: int, reason: str, 
               notes: Optional[str] = None) -> Dict[str, Any]:
        """Ajusta la cantidad de un item"""
        data = {
            "new_quantity": new_quantity,
            "reason": reason,
            "notes": notes
        }
        return api_client.post(f"/api/inventory/{item_id}/adjust", json_data=data)
    
    def delete(self, item_id: int) -> Dict[str, Any]:
        """Elimina un item de inventario"""
        return api_client.delete(f"/api/inventory/{item_id}")
    
    # Movimientos
    def get_movements(self, skip: int = 0, limit: int = 100,
                     inventory_id: Optional[int] = None,
                     movement_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene movimientos de inventario"""
        params = {"skip": skip, "limit": limit}
        if inventory_id:
            params["inventory_id"] = inventory_id
        if movement_type:
            params["movement_type"] = movement_type
        return api_client.get("/api/inventory/movements/", params=params)
    
    def get_item_history(self, item_id: int) -> List[Dict[str, Any]]:
        """Obtiene el historial de movimientos de un item"""
        return api_client.get(f"/api/inventory/movements/{item_id}/history")
    
    def create_movement(self, movement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un movimiento de inventario (entrada o salida)"""
        return api_client.post("/api/inventory/movements/", json_data=movement_data)


# Instancia global
inventory_service = InventoryService()
