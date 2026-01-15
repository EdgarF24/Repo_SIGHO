"""
Script para verificar sistemáticamente todos los endpoints del backend
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def get_token():
    """Obtener token de admin"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]

def test_module(module_name, endpoints):
    """Prueba un módulo completo"""
    print(f"\n{'='*60}")
    print(f"TESTING: {module_name}")
    print(f"{'='*60}")
    
    results = []
    for endpoint in endpoints:
        try:
            result = endpoint['test']()
            status = "✅" if result['success'] else "❌"
            print(f"{status} {endpoint['name']}: {result['message']}")
            results.append(result)
        except Exception as e:
            print(f"❌ {endpoint['name']}: ERROR - {str(e)}")
            results.append({"success": False, "error": str(e)})
    
    success_count = sum(1 for r in results if r.get('success'))
    print(f"\nResultado: {success_count}/{len(endpoints)} pruebas exitosas")
    return results

def main():
    print("="*60)
    print("SIGHO - Verificación Exhaustiva de Endpoints")
    print("="*60)
    
    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        print("[OK] Token obtenido exitosamente")
    except Exception as e:
        print(f"[ERROR] No se pudo obtener token: {e}")
        return
    
    # MÓDULO 1: USUARIOS
    user_tests = [
        {
            "name": "Listar usuarios",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/users", headers=headers).status_code == 200,
                "message": "GET /api/users"
            }
        },
        {
            "name": "Obtener usuario por ID",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/users/1", headers=headers).status_code == 200,
                "message": "GET /api/users/1"
            }
        }
    ]
    
    # MÓDULO 2: TIPOS DE HABITACIÓN
    room_type_tests = [
        {
            "name": "Listar tipos de habitación",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/room-types", headers=headers).status_code == 200,
                "message": "GET /api/room-types"
            }
        }
    ]
    
    # MÓDULO 3: HABITACIONES
    room_tests = [
        {
            "name": "Listar habitaciones",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/rooms", headers=headers).status_code == 200,
                "message": "GET /api/rooms"
            }
        }
    ]
    
    # MÓDULO 4: HUÉSPEDES
    guest_tests = [
        {
            "name": "Listar huéspedes",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/guests", headers=headers).status_code == 200,
                "message": "GET /api/guests"
            }
        }
    ]
    
    # MÓDULO 5: RESERVAS
    reservation_tests = [
        {
            "name": "Listar reservas",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/reservations", headers=headers).status_code == 200,
                "message": "GET /api/reservations"
            }
        }
    ]
    
    # MÓDULO 6: PAGOS
    payment_tests = [
        {
            "name": "Listar pagos",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/payments", headers=headers).status_code == 200,
                "message": "GET /api/payments"
            }
        }
    ]
    
    # MÓDULO 7: MANTENIMIENTO
    maintenance_tests = [
        {
            "name": "Listar mantenimientos",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/maintenance", headers=headers).status_code == 200,
                "message": "GET /api/maintenance"
            }
        }
    ]
    
    # MÓDULO 8: INVENTARIO
    inventory_tests = [
        {
            "name": "Listar inventario",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/inventory", headers=headers).status_code == 200,
                "message": "GET /api/inventory"
            }
        }
    ]
    
    # MÓDULO 9: DASHBOARD
    dashboard_tests = [
        {
            "name": "Obtener estadísticas",
            "test": lambda: {
                "success": requests.get(f"{BASE_URL}/api/dashboard/stats", headers=headers).status_code == 200,
                "message": "GET /api/dashboard/stats"
            }
        }
    ]
    
    # Ejecutar todas las pruebas
    all_results = {}
    all_results["Usuarios"] = test_module("USUARIOS", user_tests)
    all_results["Tipos Habitación"] = test_module("TIPOS DE HABITACIÓN", room_type_tests)
    all_results["Habitaciones"] = test_module("HABITACIONES", room_tests)
    all_results["Huéspedes"] = test_module("HUÉSPEDES", guest_tests)
    all_results["Reservas"] = test_module("RESERVAS", reservation_tests)
    all_results["Pagos"] = test_module("PAGOS", payment_tests)
    all_results["Mantenimiento"] = test_module("MANTENIMIENTO", maintenance_tests)
    all_results["Inventario"] = test_module("INVENTARIO", inventory_tests)
    all_results["Dashboard"] = test_module("DASHBOARD", dashboard_tests)
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    total_tests = sum(len(results) for results in all_results.values())
    total_success = sum(sum(1 for r in results if r.get('success')) for results in all_results.values())
    print(f"Total: {total_success}/{total_tests} pruebas exitosas")
    print(f"Porcentaje de éxito: {(total_success/total_tests)*100:.1f}%")

if __name__ == "__main__":
    main()
