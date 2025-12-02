"""
Servicio de autenticación
"""
import json
from typing import Optional, Dict, Any
from pathlib import Path
from app.services.api_client import api_client
from config.settings import SESSION_FILE, TOKEN_KEY, USER_KEY


class AuthService:
    """Servicio de autenticación y gestión de sesión"""
    
    def __init__(self):
        self.current_user: Optional[Dict[str, Any]] = None
        self.token: Optional[str] = None
        self._load_session()
    
    def _load_session(self):
        """Carga la sesión desde el archivo"""
        try:
            if SESSION_FILE.exists():
                with open(SESSION_FILE, 'r') as f:
                    session_data = json.load(f)
                    self.token = session_data.get(TOKEN_KEY)
                    self.current_user = session_data.get(USER_KEY)
                    
                    if self.token:
                        api_client.set_token(self.token)
                        # Verificar que el token sea válido
                        try:
                            user = api_client.get_current_user()
                            self.current_user = user
                        except:
                            # Token inválido, limpiar sesión
                            self._clear_session()
        except Exception as e:
            print(f"Error cargando sesión: {e}")
            self._clear_session()
    
    def _save_session(self):
        """Guarda la sesión en el archivo"""
        try:
            session_data = {
                TOKEN_KEY: self.token,
                USER_KEY: self.current_user
            }
            with open(SESSION_FILE, 'w') as f:
                json.dump(session_data, f)
        except Exception as e:
            print(f"Error guardando sesión: {e}")
    
    def _clear_session(self):
        """Limpia la sesión"""
        self.token = None
        self.current_user = None
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()
        api_client.clear_token()
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Inicia sesión
        
        Returns:
            Dict con el resultado del login
        """
        try:
            response = api_client.login(username, password)
            
            if response.get("access_token"):
                self.token = response["access_token"]
                
                # Obtener información del usuario
                self.current_user = api_client.get_current_user()
                
                # Guardar sesión
                self._save_session()
                
                return {
                    "success": True,
                    "user": self.current_user
                }
            else:
                return {
                    "success": False,
                    "error": "No se recibió token de acceso"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def logout(self):
        """Cierra sesión"""
        try:
            api_client.logout()
        finally:
            self._clear_session()
    
    def is_authenticated(self) -> bool:
        """Verifica si el usuario está autenticado"""
        return self.token is not None and self.current_user is not None
    
    def get_user(self) -> Optional[Dict[str, Any]]:
        """Obtiene el usuario actual"""
        return self.current_user
    
    def get_user_role(self) -> Optional[str]:
        """Obtiene el rol del usuario actual"""
        if self.current_user:
            return self.current_user.get("role")
        return None
    
    def has_role(self, *roles: str) -> bool:
        """Verifica si el usuario tiene alguno de los roles especificados"""
        user_role = self.get_user_role()
        if not user_role:
            return False
        return user_role in roles or self.current_user.get("is_superuser", False)
    
    def can_access_admin(self) -> bool:
        """Verifica si puede acceder a funciones de administrador"""
        return self.has_role("admin") or self.current_user.get("is_superuser", False)
    
    def can_access_management(self) -> bool:
        """Verifica si puede acceder a funciones de gestión"""
        return self.has_role("admin", "manager")
    
    def can_access_reception(self) -> bool:
        """Verifica si puede acceder a funciones de recepción"""
        return self.has_role("admin", "manager", "receptionist")
    
    def can_access_maintenance(self) -> bool:
        """Verifica si puede acceder a funciones de mantenimiento"""
        return self.has_role("admin", "manager", "maintenance")
    
    def can_access_inventory(self) -> bool:
        """Verifica si puede acceder a funciones de inventario"""
        return self.has_role("admin", "manager", "inventory")


# Instancia global del servicio
auth_service = AuthService()