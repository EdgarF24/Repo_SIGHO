"""
Verificación COMPLETA de TODOS los módulos del sistema SIGHO
"""
import requests
import json
from datetime import date, datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

def get_token():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "admin123"})
    return response.json()["access_token"]

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")

def print_test(name, status, details=""):
    icon = "✅" if status else "❌"
    print(f"  {icon} {name}", end="")
    if details:
        print(f" - {details}")
    else:
        print()

def main():
    print_header("SIGHO - VERIFICACIÓN COMPLETA DEL SISTEMA")
    
    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        print("  [OK] Token obtenido")
    except Exception as e:
        print(f"  [ERROR] No se pudo obtener token: {e}")
        return
    
    results = {"total": 0, "passed": 0, "failed": 0}
    
    # ==================== MÓDULO 1: USUARIOS ====================
    print_header("MÓDULO 1: USUARIOS")
    try:
        # List
        r = requests.get(f"{BASE_URL}/api/users", headers=headers)
        print_test("GET /users", r.status_code == 200, f"({len(r.json())} usuarios)")
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
        
        # Create
        r = requests.post(f"{BASE_URL}/api/users", headers=headers, json={
            "username": "test_verify", "email": "verify@test.com", "full_name": "Test Verify",
            "password": "test123", "role": "viewer", "is_active": True
        })
        user_id = r.json()["id"] if r.status_code in [200, 201] else None
        print_test("POST /users (create)", r.status_code in [200, 201])
        results["total"] += 1
        if r.status_code in [200, 201]: results["passed"] += 1
        
        if user_id:
            # Read
            r = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
            print_test("GET /users/{id}", r.status_code == 200)
            results["total"] += 1
            if r.status_code == 200: results["passed"] += 1
            
            # Update
            r = requests.put(f"{BASE_URL}/api/users/{user_id}", headers=headers, json={"full_name": "Modified"})
            print_test("PUT /users/{id}", r.status_code == 200)
            results["total"] += 1
            if r.status_code == 200: results["passed"] += 1
            
            # Delete
            r = requests.delete(f"{BASE_URL}/api/users/{user_id}", headers=headers)
            print_test("DELETE /users/{id}", r.status_code in [200, 204])
            results["total"] += 1
            if r.status_code in [200, 204]: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== MÓDULO 2: HUÉSPEDES ====================
    print_header("MÓDULO 2: HUÉSPEDES")
    try:
        r = requests.get(f"{BASE_URL}/api/guests", headers=headers)
        print_test("GET /guests", r.status_code == 200, f"({len(r.json())} huéspedes)")
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
        
        r = requests.post(f"{BASE_URL}/api/guests", headers=headers, json={
            "first_name": "Test", "last_name": "Guest", "id_type": "CI", "id_number": "99999999",
            "email": "test@guest.com", "phone": "+58-412-0000000", "country": "Venezuela"
        })
        guest_id = r.json()["id"] if r.status_code in [200, 201] else None
        print_test("POST /guests", r.status_code in [200, 201])
        results["total"] += 1
        if r.status_code in [200, 201]: results["passed"] += 1
        
        if guest_id:
            r = requests.get(f"{BASE_URL}/api/guests/{guest_id}", headers=headers)
            print_test("GET /guests/{id}", r.status_code == 200)
            results["total"] += 1
            if r.status_code == 200: results["passed"] += 1
            
            r = requests.put(f"{BASE_URL}/api/guests/{guest_id}", headers=headers, json={"phone": "+58-424-1111111"})
            print_test("PUT /guests/{id}", r.status_code == 200)
            results["total"] += 1
            if r.status_code == 200: results["passed"] += 1
            
            r = requests.delete(f"{BASE_URL}/api/guests/{guest_id}", headers=headers)
            print_test("DELETE /guests/{id}", r.status_code in [200, 204])
            results["total"] += 1
            if r.status_code in [200, 204]: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== MÓDULO 3: TIPOS DE HABITACIÓN ====================
    print_header("MÓDULO 3: TIPOS DE HABITACIÓN")
    try:
        r = requests.get(f"{BASE_URL}/api/room-types", headers=headers)
        print_test("GET /room-types", r.status_code == 200, f"({len(r.json())} tipos)")
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
        
        import time
        unique_name = f"TestType_{int(time.time())}"
        r = requests.post(f"{BASE_URL}/api/room-types/", headers=headers, json={
            "name": unique_name, "description": "Tipo de prueba para verificacion", "capacity": 2,
            "base_price_ves": 100000, "base_price_usd": 50, "base_price_eur": 45
        })
        rt_id = r.json()["id"] if r.status_code in [200, 201] else None
        print_test("POST /room-types", r.status_code in [200, 201])
        results["total"] += 1
        if r.status_code in [200, 201]: results["passed"] += 1
        
        if rt_id:
            r = requests.get(f"{BASE_URL}/api/room-types/{rt_id}", headers=headers)
            print_test("GET /room-types/{id}", r.status_code == 200)
            results["total"] += 1
            if r.status_code == 200: results["passed"] += 1
            
            r = requests.delete(f"{BASE_URL}/api/room-types/{rt_id}", headers=headers)
            print_test("DELETE /room-types/{id}", r.status_code in [200, 204])
            results["total"] += 1
            if r.status_code in [200, 204]: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== MÓDULO 4: HABITACIONES ====================
    print_header("MÓDULO 4: HABITACIONES")
    try:
        r = requests.get(f"{BASE_URL}/api/rooms", headers=headers)
        print_test("GET /rooms", r.status_code == 200, f"({len(r.json())} habitaciones)")
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
        
        # Get available rooms
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        next_week = (date.today() + timedelta(days=7)).isoformat()
        r = requests.get(f"{BASE_URL}/api/rooms/available?check_in={tomorrow}&check_out={next_week}", headers=headers)
        print_test("GET /rooms/available", r.status_code == 200)
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== MÓDULO 5: RESERVAS ====================
    print_header("MÓDULO 5: RESERVAS")
    try:
        r = requests.get(f"{BASE_URL}/api/reservations", headers=headers)
        print_test("GET /reservations", r.status_code == 200, f"({len(r.json())} reservas)")
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== MÓDULO 6: PAGOS ====================
    print_header("MÓDULO 6: PAGOS")
    try:
        r = requests.get(f"{BASE_URL}/api/payments", headers=headers)
        print_test("GET /payments", r.status_code == 200, f"({len(r.json())} pagos)")
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== MÓDULO 7: MANTENIMIENTO ====================
    print_header("MÓDULO 7: MANTENIMIENTO")
    try:
        r = requests.get(f"{BASE_URL}/api/maintenance", headers=headers)
        print_test("GET /maintenance", r.status_code == 200, f"({len(r.json())} reportes)")
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
        
        r = requests.post(f"{BASE_URL}/api/maintenance/", headers=headers, json={
            "room_id": 1, "maintenance_type": "corrective", "priority": "medium",
            "title": "Test Maintenance Task", "description": "This is a test maintenance description for verification purposes"
        })
        print_test("POST /maintenance", r.status_code in [200, 201])
        results["total"] += 1
        if r.status_code in [200, 201]: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== MÓDULO 8: INVENTARIO ====================
    print_header("MÓDULO 8: INVENTARIO")
    try:
        r = requests.get(f"{BASE_URL}/api/inventory", headers=headers)
        print_test("GET /inventory", r.status_code == 200, f"({len(r.json())} items)")
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
        
        unique_item_code = f"TEST{int(time.time())}"
        r = requests.post(f"{BASE_URL}/api/inventory/", headers=headers, json={
            "item_code": unique_item_code, "name": "Test Verify Item", "category": "cleaning",
            "unit_of_measure": "unidad", "current_quantity": 10, "minimum_quantity": 5
        })
        print_test("POST /inventory", r.status_code in [200, 201])
        results["total"] += 1
        if r.status_code in [200, 201]: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== MÓDULO 9: REPORTES ====================
    print_header("MÓDULO 9: REPORTES")
    try:
        start_date = (date.today() - timedelta(days=30)).isoformat()
        end_date = date.today().isoformat()
        
        r = requests.get(f"{BASE_URL}/api/reports/occupancy", headers=headers, params={
            "start_date": start_date, "end_date": end_date
        })
        print_test("GET /reports/occupancy", r.status_code == 200)
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
        
        r = requests.get(f"{BASE_URL}/api/reports/revenue", headers=headers, params={
            "start_date": start_date, "end_date": end_date, "currency": "USD"
        })
        print_test("GET /reports/revenue", r.status_code == 200)
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== MÓDULO 10: DASHBOARD ====================
    print_header("MÓDULO 10: DASHBOARD")
    try:
        r = requests.get(f"{BASE_URL}/api/dashboard/overview", headers=headers)
        print_test("GET /dashboard/overview", r.status_code == 200)
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
        
        r = requests.get(f"{BASE_URL}/api/dashboard/occupancy-rate", headers=headers)
        print_test("GET /dashboard/occupancy-rate", r.status_code == 200)
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
        
        r = requests.get(f"{BASE_URL}/api/dashboard/revenue-by-period", headers=headers)
        print_test("GET /dashboard/revenue-by-period", r.status_code == 200)
        results["total"] += 1
        if r.status_code == 200: results["passed"] += 1
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")
    
    # ==================== RESUMEN FINAL ====================
    print_header("RESUMEN FINAL")
    percentage = (results["passed"] / results["total"] * 100) if results["total"] > 0 else 0
    
    print(f"\n  Total de pruebas: {results['total']}")
    print(f"  Exitosas: {results['passed']} ✅")
    print(f"  Fallidas: {results['total'] - results['passed']} ❌")
    print(f"  Porcentaje de éxito: {percentage:.1f}%\n")
    
    if percentage >= 90:
        print("  🎉 ¡SISTEMA EN EXCELENTE ESTADO!")
    elif percentage >= 70:
        print("  ⚠️  Sistema funcional con algunos problemas menores")
    else:
        print("  ❌ Sistema requiere atención")
    
    print("="*70)

if __name__ == "__main__":
    main()
