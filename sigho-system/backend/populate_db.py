"""
Script para poblar la base de datos con datos de prueba
"""
from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.models.user import User, UserRole
from app.models.room_type import RoomType
from app.models.room import Room, RoomStatus
import bcrypt

def populate_database():
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("[INFO] Poblando base de datos...")
        
        # ========== VERIFICAR SI YA HAY DATOS ==========
        existing_room_types = db.query(RoomType).count()
        if existing_room_types > 0:
            print("[INFO] La base de datos ya tiene datos. Omitiendo...")
            return
        
        # ========== TIPOS DE HABITACION ==========
        print("[INFO] Creando tipos de habitacion...")
        room_types_data = [
            {
                "name": "Individual",
                "description": "Habitacion individual con cama sencilla",
                "capacity": 1,
                "base_price_ves": 50000.0,
                "base_price_usd": 25.0,
                "base_price_eur": 23.0,
                "has_wifi": True,
                "has_tv": True,
                "has_ac": True,
                "has_minibar": False,
                "has_balcony": False
            },
            {
                "name": "Doble",
                "description": "Habitacion doble con cama matrimonial",
                "capacity": 2,
                "base_price_ves": 80000.0,
                "base_price_usd": 40.0,
                "base_price_eur": 37.0,
                "has_wifi": True,
                "has_tv": True,
                "has_ac": True,
                "has_minibar": False,
                "has_balcony": True
            },
            {
                "name": "Triple",
                "description": "Habitacion triple con tres camas",
                "capacity": 3,
                "base_price_ves": 120000.0,
                "base_price_usd": 60.0,
                "base_price_eur": 55.0,
                "has_wifi": True,
                "has_tv": True,
                "has_ac": True,
                "has_minibar": True,
                "has_balcony": True
            },
            {
                "name": "Suite Junior",
                "description": "Suite junior con sala de estar",
                "capacity": 2,
                "base_price_ves": 150000.0,
                "base_price_usd": 75.0,
                "base_price_eur": 70.0,
                "has_wifi": True,
                "has_tv": True,
                "has_ac": True,
                "has_minibar": True,
                "has_balcony": True,
                "has_kitchen": False
            },
            {
                "name": "Suite Presidencial",
                "description": "Suite presidencial de lujo con todas las comodidades",
                "capacity": 4,
                "base_price_ves": 300000.0,
                "base_price_usd": 150.0,
                "base_price_eur": 140.0,
                "has_wifi": True,
                "has_tv": True,
                "has_ac": True,
                "has_minibar": True,
                "has_balcony": True,
                "has_kitchen": True
            }
        ]
        
        room_types = []
        for rt_data in room_types_data:
            rt = RoomType(**rt_data)
            db.add(rt)
            room_types.append(rt)
        
        db.commit()
        db.refresh(room_types[0])
        print(f"[OK] {len(room_types)} tipos de habitacion creados")
        
        # ========== HABITACIONES ==========
        print("[INFO] Creando habitaciones...")
        floors = [1, 2, 3, 4, 5]
        room_count = 0
        
        for floor in floors:
            room_number = floor * 100 + 1
            
            # 4 individuales por piso
            for _ in range(4):
                room = Room(
                    room_number=str(room_number),
                    floor=floor,
                    room_type_id=room_types[0].id,
                    status=RoomStatus.AVAILABLE
                )
                db.add(room)
                room_number += 1
                room_count += 1
            
            # 6 dobles por piso
            for _ in range(6):
                room = Room(
                    room_number=str(room_number),
                    floor=floor,
                    room_type_id=room_types[1].id,
                    status=RoomStatus.AVAILABLE
                )
                db.add(room)
                room_number += 1
                room_count += 1
            
            # 3 triples por piso
            for _ in range(3):
                room = Room(
                    room_number=str(room_number),
                    floor=floor,
                    room_type_id=room_types[2].id,
                    status=RoomStatus.AVAILABLE
                )
                db.add(room)
                room_number += 1
                room_count += 1
            
            # 1 suite junior por piso
            room = Room(
                room_number=str(room_number),
                floor=floor,
                room_type_id=room_types[3].id,
                status=RoomStatus.AVAILABLE
            )
            db.add(room)
            room_count += 1
        
        # 2 suites presidenciales en el piso 5
        for i in range(2):
            room = Room(
                room_number=f"50{i+1}",
                floor=5,
                room_type_id=room_types[4].id,
                status=RoomStatus.AVAILABLE
            )
            db.add(room)
            room_count += 1
        
        db.commit()
        print(f"[OK] {room_count} habitaciones creadas")
        
        # ========== USUARIOS ADICIONALES ==========
        print("[INFO] Creando usuarios adicionales...")
        additional_users = [
            {
                "username": "gerente",
                "email": "gerente@hotelsigho.com",
                "full_name": "Gerente General",
                "password": "gerente123",
                "role": UserRole.MANAGER
            },
            {
                "username": "recepcion",
                "email": "recepcion@hotelsigho.com",
                "full_name": "Maria Recepcion",
                "password": "recepcion123",
                "role": UserRole.RECEPTIONIST
            },
            {
                "username": "mantenimiento",
                "email": "mantenimiento@hotelsigho.com",
                "full_name": "Carlos Mantenimiento",
                "password": "manten123",
                "role": UserRole.MAINTENANCE
            },
            {
                "username": "inventario",
                "email": "inventario@hotelsigho.com",
                "full_name": "Ana Inventario",
                "password": "inventario123",
                "role": UserRole.INVENTORY
            }
        ]
        
        user_count = 0
        for user_data in additional_users:
            # Verificar si ya existe
            existing = db.query(User).filter(User.username == user_data["username"]).first()
            if not existing:
                password = user_data.pop("password")
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user = User(
                    **user_data,
                    hashed_password=hashed.decode('utf-8'),
                    is_active=True,
                    is_superuser=False
                )
                db.add(user)
                user_count += 1
        
        db.commit()
        print(f"[OK] {user_count} usuarios adicionales creados")
        
        print("")
        print("[SUCCESS] Base de datos poblada exitosamente!")
        print("")
        print("Resumen:")
        print(f"  - {len(room_types)} tipos de habitacion")
        print(f"  - {room_count} habitaciones")
        print(f"  - {user_count + 1} usuarios (incluyendo admin)")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()
