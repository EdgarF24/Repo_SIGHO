"""
Script para inicializar la base de datos con usuario admin
"""
from app.database.session import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.database.session import engine
from app.database.base import Base

def init_database():
    print("[INFO] Creando tablas...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar si ya existe admin
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print("[INFO] Usuario admin ya existe")
            return
        
        print("[INFO] Creando usuario admin...")
        admin = User(
            username="admin",
            email="admin@hotelsigho.com",
            full_name="Administrador del Sistema",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True
        )
        db.add(admin)
        db.commit()
        
        print("[OK] Usuario admin creado exitosamente!")
        print("")
        print("Credenciales:")
        print("  Usuario: admin")
        print("  Contrasena: admin123")
        print("")
        print("[SUCCESS] Base de datos inicializada correctamente!")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
