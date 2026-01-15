"""
Inicializar la base de datos con datos de prueba
"""
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.room_type import RoomType
from app.models.room import Room, RoomStatus
from app.database.session import engine
from app.database.base import Base
import random


def init_db(db: Session) -> None:
    """
    Inicializa la base de datos con datos de prueba
    """
    
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Verificar si ya existen usuarios
    existing_user = db.query(User).first()
    if existing_user:
        print("[INFO] La base de datos ya contiene datos. Omitiendo inicializacion.")
        return
    
    print("[INFO] Creando datos iniciales...")
    
    # ========== USUARIOS ==========
    users_data = [
        {
            "username": "admin",
            "email": "admin@hotelsigho.com",
            "full_name": "Administrador del Sistema",
            "password": "admin123",
            "role": UserRole.ADMIN,
            "is_superuser": True
        },
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
    
    for user_data in users_data:
        password = user_data.pop("password")
        user = User(**user_data, hashed_password=get_password_hash(password))
        db.add(user)
    
    db.commit()
    print("[OK] Usuarios creados")
    
    # ========== TIPOS DE HABITACION ==========
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
    print("[OK] Tipos de habitacion creados")
    
    # ========== HABITACIONES ==========
    floors = [1, 2, 3, 4, 5]
    room_number = 101
    
    for floor in floors:
        # 4 individuales por piso
        for _ in range(4):
            room = Room(
                room_number=str(room_number),
                floor=floor,
                room_type_id=room_types[0].id,  # Individual
                status=RoomStatus.AVAILABLE
            )
            db.add(room)
            room_number += 1
        
        # 6 dobles por piso
        for _ in range(6):
            room = Room(
                room_number=str(room_number),
                floor=floor,
                room_type_id=room_types[1].id,  # Doble
                status=RoomStatus.AVAILABLE
            )
            db.add(room)
            room_number += 1
        
        # 3 triples por piso
        for _ in range(3):
            room = Room(
                room_number=str(room_number),
                floor=floor,
                room_type_id=room_types[2].id,  # Triple
                status=RoomStatus.AVAILABLE
            )
            db.add(room)
            room_number += 1
        
        # 1 suite junior por piso
        room = Room(
            room_number=str(room_number),
            floor=floor,
            room_type_id=room_types[3].id,  # Suite Junior
            status=RoomStatus.AVAILABLE
        )
        db.add(room)
        room_number += 1
        
        # Pasar al siguiente piso
        room_number = (floor + 1) * 100 + 1
    
    # 2 suites presidenciales en el piso 5
    for i in range(2):
        room = Room(
            room_number=f"50{i+1}",
            floor=5,
            room_type_id=room_types[4].id,  # Suite Presidencial
            status=RoomStatus.AVAILABLE
        )
        db.add(room)
    
    db.commit()
    print("[OK] Habitaciones creadas")
    
    print("[SUCCESS] Base de datos inicializada correctamente!")
    print("\n[INFO] Credenciales de acceso:")
    print("   Admin: admin / admin123")
    print("   Gerente: gerente / gerente123")
    print("   Recepcion: recepcion / recepcion123")
    print("   Mantenimiento: mantenimiento / manten123")
    print("   Inventario: inventario / inventario123")