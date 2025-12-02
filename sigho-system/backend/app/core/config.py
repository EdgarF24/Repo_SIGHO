"""
Configuración del Sistema SIGHO
FastAPI + SQLite3
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Información de la aplicación
    APP_NAME: str = "SIGHO - Sistema Integrado de Gestión Hotelera"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Base de datos SQLite3
    DATABASE_URL: str = "sqlite:///./sigho.db"
    
    # Seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:*,http://127.0.0.1:*"
    
    # Información del hotel
    HOTEL_NAME: str = "Hotel SIGHO"
    HOTEL_ADDRESS: str = "Nueva Esparta, Venezuela"
    HOTEL_PHONE: str = "+58 424 1234567"
    HOTEL_EMAIL: str = "info@hotelsigho.com"
    
    # Monedas
    CURRENCIES: str = "VES,USD,EUR"
    
    # Zona horaria
    TIMEZONE: str = "America/Caracas"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convierte la cadena de orígenes permitidos en una lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def currencies_list(self) -> List[str]:
        """Convierte la cadena de monedas en una lista"""
        return [currency.strip() for currency in self.CURRENCIES.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()