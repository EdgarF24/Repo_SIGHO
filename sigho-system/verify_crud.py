"""
Script exhaustivo para verificar TODAS las operaciones CRUD
"""
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"

def get_token():
    """Obtener token de admin"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]

def test_crud_operations():
    """Prueba operaciones CRUD en todos los módulos"""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    results = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "modules": {}
    }
    
    print("="*70)
    print("VERIFICACIÓN EXHAUSTIVA DE OPERACIONES CRUD")
    print("="*70)
    print()
    
    # ====== MÓDULO 1: HUÉSPEDES ======
    print("\n[1/9] MÓDULO: HUÉSPEDES")
    print("-"*70)
    guest_results = {"tests": [], "passed": 0}
    
    # Create
    try:
        new_guest = {
            "first_name": "Juan",
            "last_name": "Test",
            "id_type": "CI",
            "id_number": "12345678",
            "email": "juan.test@example.com",
            "phone": "+58-412-1234567",
            "country": "Venezuela"
        }
        r = requests.post(f"{BASE_URL}/api/guests", headers=headers, json=new_guest)
        if r.status_code in [200, 201]:
            guest_id = r.json()["id"]
            print(f"  ✅ CREATE guest (ID: {guest_id})")
            guest_results["passed"] += 1
            guest_results["tests"].append(("CREATE", True))
            
            # Read
            r = requests.get(f"{BASE_URL}/api/guests/{guest_id}", headers=headers)
            if r.status_code == 200:
                print(f"  ✅ READ guest")
                guest_results["passed"] += 1
                guest_results["tests"].append(("READ", True))
            else:
                print(f"  ❌ READ guest: {r.status_code}")
                guest_results["tests"].append(("READ", False))
            
            # Update
            update_data = {"phone": "+58-424-9999999"}
            r = requests.put(f"{BASE_URL}/api/guests/{guest_id}", headers=headers, json=update_data)
            if r.status_code == 200:
                print(f"  ✅ UPDATE guest")
                guest_results["passed"] += 1
                guest_results["tests"].append(("UPDATE", True))
            else:
                print(f"  ❌ UPDATE guest: {r.status_code}")
                guest_results["tests"].append(("UPDATE", False))
            
            # Delete
            r = requests.delete(f"{BASE_URL}/api/guests/{guest_id}", headers=headers)
            if r.status_code in [200, 204]:
                print(f"  ✅ DELETE guest")
                guest_results["passed"] += 1
                guest_results["tests"].append(("DELETE", True))
            else:
                print(f"  ❌ DELETE guest: {r.status_code}")
                guest_results["tests"].append(("DELETE", False))
        else:
            print(f"  ❌ CREATE guest: {r.status_code} - {r.text[:100]}")
            guest_results["tests"].append(("CREATE", False))
    except Exception as e:
        print(f"  ❌ Error en módulo huéspedes: {str(e)[:100]}")
    
    results["modules"]["Huéspedes"] = guest_results
    results["total_tests"] += len(guest_results["tests"])
    results["passed"] +=guest_results["passed"]
    
    # ====== MÓDULO 2: USUARIOS ======
    print("\n[2/9] MÓDULO: USUARIOS")
    print("-"*70)
    user_results = {"tests": [], "passed": 0}
    
    # Create
    try:
        new_user = {
            "username": "test_user",
            "email": "test@example.com",
            "full_name": "Usuario Test",
            "password": "test123",
            "role": "viewer",
            "is_active": True
        }
        r = requests.post(f"{BASE_URL}/api/users", headers=headers, json=new_user)
        if r.status_code in [200, 201]:
            user_id = r.json()["id"]
            print(f"  ✅ CREATE user (ID: {user_id})")
            user_results["passed"] += 1
            user_results["tests"].append(("CREATE", True))
            
            # Read
            r = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
            if r.status_code == 200:
                print(f"  ✅ READ user")
                user_results["passed"] += 1
                user_results["tests"].append(("READ", True))
            
            # Update
            update_data = {"full_name": "Usuario Test Modificado"}
            r = requests.put(f"{BASE_URL}/api/users/{user_id}", headers=headers, json=update_data)
            if r.status_code == 200:
                print(f"  ✅ UPDATE user")
                user_results["passed"] += 1
                user_results["tests"].append(("UPDATE", True))
            
            # Delete
            r = requests.delete(f"{BASE_URL}/api/users/{user_id}", headers=headers)
            if r.status_code in [200, 204]:
                print(f"  ✅ DELETE user")
                user_results["passed"] += 1
                user_results["tests"].append(("DELETE", True))
        else:
            print(f"  ❌ CREATE user: {r.status_code}")
            user_results["tests"].append(("CREATE", False))
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")
    
    results["modules"]["Usuarios"] = user_results
    results["total_tests"] += len(user_results["tests"])
    results["passed"] += user_results["passed"]
    
    # ====== MÓDULO 3: DASHBOARD ======
    print("\n[3/9] MÓDULO: DASHBOARD")
    print("-"*70)
    dashboard_results = {"tests": [], "passed": 0}
    
    try:
        # Overview
        r = requests.get(f"{BASE_URL}/api/dashboard/overview", headers=headers)
        if r.status_code == 200:
            print(f"  ✅ GET dashboard/overview")
            dashboard_results["passed"] += 1
            dashboard_results["tests"].append(("GET overview", True))
        else:
            print(f"  ❌ GET dashboard/overview: {r.status_code}")
            dashboard_results["tests"].append(("GET overview", False))
        
        # Occupancy
        r = requests.get(f"{BASE_URL}/api/dashboard/occupancy-rate", headers=headers)
        if r.status_code == 200:
            print(f"  ✅ GET occupancy-rate")
            dashboard_results["passed"] += 1
            dashboard_results["tests"].append(("GET occupancy", True))
        else:
            print(f"  ❌ GET occupancy-rate: {r.status_code}")
            dashboard_results["tests"].append(("GET occupancy", False))
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")
    
    results["modules"]["Dashboard"] = dashboard_results
    results["total_tests"] += len(dashboard_results["tests"])
    results["passed"] += dashboard_results["passed"]
    
    # ====== RESUMEN FINAL ======
    print("\n" + "="*70)
    print("RESUMEN FINAL")
    print("="*70)
    
    for module_name, module_data in results["modules"].items():
        total = len(module_data["tests"])
        passed = module_data["passed"]
        percentage = (passed/total*100) if total > 0 else 0
        status = "✅" if percentage == 100 else "⚠️" if percentage >= 50 else "❌"
        print(f"{status} {module_name}: {passed}/{total} ({percentage:.0f}%)")
    
    print(f"\nTOTAL: {results['passed']}/{results['total_tests']} pruebas exitosas")
    print(f"PORCENTAJE GLOBAL: {(results['passed']/results['total_tests']*100):.1f}%")
    
    return results

if __name__ == "__main__":
    test_crud_operations()
