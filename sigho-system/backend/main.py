"""
Sistema Integrado de Gestión Hotelera (SIGHO)
Backend FastAPI + SQLite3
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base
from app.database.init_db import init_db
from app.database.session import SessionLocal

# Importar routers
from app.api.endpoints import (
    auth,
    users,
    rooms,
    room_types,
    amenities,
    reservations,
    guests,
    payments,
    maintenance,
    inventory,
    reports,
    dashboard
)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API REST para el Sistema Integrado de Gestión Hotelera",
    debug=settings.DEBUG
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    print(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    # Inicializar datos de prueba
    db = SessionLocal()
    try:
        init_db(db)
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        db.close()
    
    print(f"✅ Servidor iniciado en http://{settings.HOST}:{settings.PORT}")
    print(f"📚 Documentación API: http://{settings.HOST}:{settings.PORT}/docs")


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Verificación de salud del sistema"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(users.router, prefix="/api/users", tags=["Usuarios"])
app.include_router(amenities.router, prefix="/api/amenities", tags=["Amenidades"])
app.include_router(room_types.router, prefix="/api/room-types", tags=["Tipos de Habitación"])
app.include_router(rooms.router, prefix="/api/rooms", tags=["Habitaciones"])
app.include_router(reservations.router, prefix="/api/reservations", tags=["Reservas"])
app.include_router(guests.router, prefix="/api/guests", tags=["Huéspedes"])
app.include_router(payments.router, prefix="/api/payments", tags=["Pagos"])
app.include_router(maintenance.router, prefix="/api/maintenance", tags=["Mantenimiento"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventario"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reportes"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )