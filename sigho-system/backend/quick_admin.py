"""
Script rapido para crear usuario admin
"""
from app.database.session import SessionLocal, engine
from app.models.user import User, UserRole
from app.database.base import Base
import bcrypt

def create_admin():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar si existe
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print("[INFO] Usuario admin ya existe")
            # Actualizar contraseña
            password = "admin123"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            existing.hashed_password = hashed.decode('utf-8')
            db.commit()
            print("[OK] Contrasena actualizada")
        else:
            # Crear nuevo
            password = "admin123"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            admin = User(
                username="admin",
                email="admin@hotel.com",
                full_name="Administrador",
                hashed_password=hashed.decode('utf-8'),
                role=UserRole.ADMIN,
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            print("[OK] Usuario admin creado")
        
        print("")
        print("LOGIN:")
        print("  Usuario: admin")
        print("  Contrasena: admin123")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
