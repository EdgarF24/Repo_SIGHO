"""
Script para poblar datos usando la API REST (evita problemas de bcrypt)
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def get_admin_token():
    """Login como admin y obtener token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error login: {response.status_code}")
        print(response.text)
        return None

def create_room_types(token):
    """Crear tipos de habitacion via API"""
    headers = {"Authorization": f"Bearer {token}"}
    
    room_types = [
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
            "description": "Habitacion triple",
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
            "description": "Suite junior con sala",
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
            "description": "Suite presidencial de lujo",
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
    
    created = []
    for rt in room_types:
        response = requests.post(
            f"{BASE_URL}/api/room-types",
            headers=headers,
            json=rt
        )
        if response.status_code in [200, 201]:
            created.append(response.json())
            print(f"[OK] Creado: {rt['name']}")
        else:
            print(f"[ERROR] {rt['name']}: {response.status_code}")
    
    return created

def create_rooms(token, room_types):
    """Crear habitaciones via API"""
    headers = {"Authorization": f"Bearer {token}"}
    
    created_count = 0
    
    for floor in [1, 2, 3, 4, 5]:
        room_num = floor * 100 + 1
        
        # 4 individuales
        for _ in range(4):
            room = {
                "room_number": str(room_num),
                "floor": floor,
                "room_type_id": room_types[0]["id"],
                "status": "available"
            }
            response = requests.post(f"{BASE_URL}/api/rooms", headers=headers, json=room)
            if response.status_code in [200, 201]:
                created_count += 1
            room_num += 1
        
        # 6 dobles
        for _ in range(6):
            room = {
                "room_number": str(room_num),
                "floor": floor,
                "room_type_id": room_types[1]["id"],
                "status": "available"
            }
            response = requests.post(f"{BASE_URL}/api/rooms", headers=headers, json=room)
            if response.status_code in [200, 201]:
                created_count += 1
            room_num += 1
        
        # 3 triples  
        for _ in range(3):
            room = {
                "room_number": str(room_num),
                "floor": floor,
                "room_type_id": room_types[2]["id"],
                "status": "available"
            }
            response = requests.post(f"{BASE_URL}/api/rooms", headers=headers, json=room)
            if response.status_code in [200, 201]:
                created_count += 1
            room_num += 1
        
        # 1 suite junior
        room = {
            "room_number": str(room_num),
            "floor": floor,
            "room_type_id": room_types[3]["id"],
            "status": "available"
        }
        response = requests.post(f"{BASE_URL}/api/rooms", headers=headers, json=room)
        if response.status_code in [200, 201]:
            created_count += 1
    
    # 2 suites presidenciales
    for i in range(2):
        room = {
            "room_number": f"50{i+1}",
            "floor": 5,
            "room_type_id": room_types[4]["id"],
            "status": "available"
        }
        response = requests.post(f"{BASE_URL}/api/rooms", headers=headers, json=room)
        if response.status_code in [200, 201]:
            created_count += 1
    
    print(f"[OK] {created_count} habitaciones creadas")
    return created_count

def create_users(token):
    """Crear usuarios adicionales via API"""
    headers = {"Authorization": f"Bearer {token}"}
    
    users = [
        {
            "username": "gerente",
            "email": "gerente@hotel.com",
            "full_name": "Gerente General",
            "password": "gerente123",
            "role": "manager",
            "is_active": True
        },
        {
            "username": "recepcion",
            "email": "recepcion@hotel.com",
            "full_name": "Maria Recepcion",
            "password": "recepcion123",
            "role": "receptionist",
            "is_active": True
        }
    ]
    
    created = 0
    for user in users:
        response = requests.post(f"{BASE_URL}/api/users", headers=headers, json=user)
        if response.status_code in [200, 201]:
            created += 1
            print(f"[OK] Usuario: {user['username']}")
        else:
            print(f"[INFO] {user['username']} ya existe o error")
    
    return created

def main():
    print("="*50)
    print("SIGHO - Poblador de Datos via API")
    print("="*50)
    print()
    
    # 1. Login
    print("[1/4] Obteniendo token de admin...")
    token = get_admin_token()
    if not token:
        print("[ERROR] No se pudo obtener token")
        return
    print("[OK] Token obtenido")
    print()
    
    # 2. Tipos de habitacion
    print("[2/4] Creando tipos de habitacion...")
    room_types = create_room_types(token)
    print(f"[OK] {len(room_types)} tipos creados")
    print()
    
    # 3. Habitaciones
    print("[3/4] Creando habitaciones...")
    rooms_count = create_rooms(token, room_types)
    print()
    
    # 4. Usuarios
    print("[4/4] Creando usuarios adicionales...")
    users_count = create_users(token)
    print()
    
    print("="*50)
    print("[SUCCESS] Sistema poblado exitosamente!")
    print("="*50)
    print()
    print("Resumen:")
    print(f"  - {len(room_types)} tipos de habitacion")
    print(f"  - {rooms_count} habitaciones")
    print(f"  - {users_count + 1} usuarios")
    print()
    print("El sistema esta listo para usarse!")

if __name__ == "__main__":
    main()
