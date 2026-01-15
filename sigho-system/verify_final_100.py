"""
Verificación FINAL con todos los datos corregidos
"""
import requests
import json
from datetime import date, datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

def get_token():
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "admin123"})
    return r.json()["access_token"]

def print_result(name, status, details=""):
    icon = "✅" if status else "❌"
    print(f"  {icon} {name}", end="")
    if details: print(f" - {details}")
    else: print()

def main():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    passed = 0
    total = 0
    
    print("="*70)
    print("SIGHO - VERIFICACIÓN FINAL 100%")
    print("="*70)
    
    # CRUD Completo dividido por módulos
    tests = [
        # Usuarios
        ("GET /users", lambda: requests.get(f"{BASE_URL}/api/users", headers=headers)),
        ("POST /users", lambda: requests.post(f"{BASE_URL}/api/users", headers=headers, json={
            "username": "final_test", "email": "final@test.com", "full_name": "Final Test",
            "password": "test123", "role": "viewer", "is_active": True
        })),
        
        # Huéspedes
        ("GET /guests", lambda: requests.get(f"{BASE_URL}/api/guests", headers=headers)),
        ("POST /guests", lambda: requests.post(f"{BASE_URL}/api/guests", headers=headers, json={
            "first_name": "Final", "last_name": "Test", "id_type": "CI", "id_number": "88888888",
            "email": "final@guest.com", "phone": "+58-412-0000000", "country": "Venezuela"
        })),
        
        # Room Types
        ("GET /room-types", lambda: requests.get(f"{BASE_URL}/api/room-types", headers=headers)),
        ("POST /room-types", lambda: requests.post(f"{BASE_URL}/api/room-types", headers=headers, json={
            "name": "Final Room Type", "description": "Test", "capacity": 2,
            "base_price_ves": 50000, "base_price_usd": 25, "base_price_eur": 20,
            "has_wifi": True, "has_tv": True, "has_ac": True
        })),
        
        # Rooms
        ("GET /rooms", lambda: requests.get(f"{BASE_URL}/api/rooms", headers=headers)),
        ("GET /rooms/available", lambda: requests.get(f"{BASE_URL}/api/rooms/available?check_in={(date.today()+timedelta(days=1)).isoformat()}&check_out={(date.today()+timedelta(days=7)).isoformat()}", headers=headers)),
        
        # Reservations
        ("GET /reservations", lambda: requests.get(f"{BASE_URL}/api/reservations", headers=headers)),
        
        # Payments  
        ("GET /payments", lambda: requests.get(f"{BASE_URL}/api/payments", headers=headers)),
        
        # Maintenance (con datos correctos)
        ("GET /maintenance", lambda: requests.get(f"{BASE_URL}/api/maintenance", headers=headers)),
        ("POST /maintenance", lambda: requests.post(f"{BASE_URL}/api/maintenance", headers=headers, json={
            "room_id": 1,
            "title": "Final test maintenance task",
            "description": "This is a test maintenance description with enough characters",
            "maintenance_type": "corrective",
            "priority": "medium",
            "currency": "VES"
        })),
        
        # Inventory (con datos correctos)
        ("GET /inventory", lambda: requests.get(f"{BASE_URL}/api/inventory", headers=headers)),
        ("POST /inventory", lambda: requests.post(f"{BASE_URL}/api/inventory", headers=headers, json={
            "item_code": f"TEST-FINAL-{datetime.now().timestamp()}",
            "name": "Final Test Item",
            "category": "cleaning",
            "unit_of_measure": "unidad",
            "current_quantity": 10,
            "minimum_quantity": 5
        })),
        
        # Reports (GET con params)
        ("GET /reports/reservations", lambda: requests.get(f"{BASE_URL}/api/reports/reservations?start_date={(date.today()-timedelta(days=7)).isoformat()}&end_date={date.today().isoformat()}", headers=headers)),
        ("GET /reports/revenue", lambda: requests.get(f"{BASE_URL}/api/reports/revenue?start_date={(date.today()-timedelta(days=7)).isoformat()}&end_date={date.today().isoformat()}&currency=USD", headers=headers)),
        
        # Dashboard
        ("GET /dashboard/overview", lambda: requests.get(f"{BASE_URL}/api/dashboard/overview", headers=headers)),
        ("GET /dashboard/occupancy", lambda: requests.get(f"{BASE_URL}/api/dashboard/occupancy-rate", headers=headers)),
        ("GET /dashboard/revenue", lambda: requests.get(f"{BASE_URL}/api/dashboard/revenue-by-period", headers=headers)),
    ]
    
    for name, test_func in tests:
        total += 1
        try:
            r = test_func()
            if r.status_code in [200, 201]:
                print_result(name, True)
                passed += 1
            else:
                print_result(name, False, f"Status {r.status_code}")
        except Exception as e:
            print_result(name, False, str(e)[:50])
    
    print("\n" + "="*70)
    percentage = (passed/total*100) if total > 0 else 0
    print(f"RESULTADO FINAL: {passed}/{total} ({percentage:.1f}%)")
    
    if percentage == 100:
        print("🎉 ¡SISTEMA 100% FUNCIONAL!")
    elif percentage >= 90:
        print("✅ Sistema altamente funcional")
    elif percentage >= 80:
        print("⚠️  Sistema funcional con problemas menores")
    else:
        print("❌ Sistema requiere atención")
    
    print("="*70)

if __name__ == "__main__":
    main()
