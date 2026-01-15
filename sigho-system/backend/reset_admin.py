"""
Script para resetear la contraseña del usuario admin
"""
from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def reset_admin_password():
    db = SessionLocal()
    try:
        # Buscar usuario admin
        admin = db.query(User).filter(User.username == "admin").first()
        
        if admin:
            # Resetear contraseña a admin123
            admin.hashed_password = get_password_hash("admin123")
            db.commit()
            print("[OK] Contrasena del usuario 'admin' reseteada a 'admin123'")
            print("[INFO] Puedes hacer login con:")
            print("       Usuario: admin")
            print("       Contrasena: admin123")
        else:
            print("[ERROR] Usuario 'admin' no encontrado en la base de datos")
            print("[INFO] Usuarios existentes:")
            users = db.query(User).all()
            for user in users:
                print(f"  - Username: {user.username}, Email: {user.email}")
    
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin_password()
