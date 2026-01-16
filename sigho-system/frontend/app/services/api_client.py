"""
Cliente HTTP para comunicación con el backend FastAPI
"""
import requests
import json
from typing import Dict, Any, Optional, List
from config.settings import API_BASE_URL, API_TIMEOUT


class APIClient:
    """Cliente HTTP para el backend"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    def set_token(self, token: str):
        """Establece el token de autenticación"""
        self.token = token
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
    
    def clear_token(self):
        """Limpia el token de autenticación"""
        self.token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Maneja la respuesta HTTP"""
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return {"success": True}
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_detail = "Error desconocido"
            try:
                error_data = response.json()
                error_detail = error_data.get("detail", str(e))
            except:
                error_detail = str(e)
            
            raise Exception(f"Error HTTP {response.status_code}: {error_detail}")
        except requests.exceptions.ConnectionError:
            raise Exception("No se pudo conectar con el servidor. Verifique que el backend esté ejecutándose.")
        except requests.exceptions.Timeout:
            raise Exception("La solicitud tardó demasiado tiempo.")
        except Exception as e:
            raise Exception(f"Error en la solicitud: {str(e)}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Petición GET"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, timeout=API_TIMEOUT)
        return self._handle_response(response)
    
    def get_raw(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """Petición GET que retorna la respuesta sin procesar (para archivos binarios)"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Petición POST"""
        url = f"{self.base_url}{endpoint}"
        if json_data:
            response = self.session.post(url, json=json_data, timeout=API_TIMEOUT)
        else:
            response = self.session.post(url, data=data, timeout=API_TIMEOUT)
        return self._handle_response(response)
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Petición PUT"""
        url = f"{self.base_url}{endpoint}"
        if json_data:
            response = self.session.put(url, json=json_data, timeout=API_TIMEOUT)
        else:
            response = self.session.put(url, data=data, timeout=API_TIMEOUT)
        return self._handle_response(response)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Petición DELETE"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, timeout=API_TIMEOUT)
        return self._handle_response(response)
    
    # Métodos de autenticación
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login de usuario"""
        data = {"username": username, "password": password}
        response = self.post("/api/auth/login", json_data=data)
        if response.get("access_token"):
            self.set_token(response["access_token"])
        return response
    
    def logout(self):
        """Logout de usuario"""
        self.clear_token()
        return {"success": True}
    
    def get_current_user(self) -> Dict[str, Any]:
        """Obtiene el usuario actual"""
        return self.get("/api/auth/me")


# Instancia global del cliente
api_client = APIClient()