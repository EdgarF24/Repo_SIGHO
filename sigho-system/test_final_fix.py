"""
Prueba final corregida con datos correctos
"""
import requests
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"

def main():
    # Get token
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("="*70)
    print("PRUEBA FINAL DE ENDPOINTS CORREGIDOS")
    print("="*70)
    
    # Test 1: POST /inventory (con datos correctos)
    print("\n[1/3] POST /api/inventory")
    data = {
        "item_code": "TEST-001",
        "name": "Item de Prueba Test",
        "category": "amenities",
        "unit_of_measure": "unidad",
        "current_quantity": 10,
        "minimum_quantity": 5
    }
    r = requests.post(f"{BASE_URL}/api/inventory", headers=headers, json=data)
    if r.status_code in [200, 201]:
        print(f"  ✅ SUCCESS: {r.status_code} - Item creado: {r.json().get('name')}")
    else:
        print(f"  ❌ FAILED: {r.status_code}")
        print(f"     {r.text[:150]}")
    
    # Test 2: GET /reports/occupancy (con parámetros de query)
    print("\n[2/3] GET /api/reports/occupancy")
    start = (date.today() - timedelta(days=7)).isoformat()
    end = date.today().isoformat()
    r = requests.get(f"{BASE_URL}/api/reports/reservations?start_date={start}&end_date={end}", headers=headers)
    if r.status_code == 200:
        print(f"  ✅ SUCCESS: {r.status_code} - Reporte generado")
    else:
        print(f"  ❌ FAILED: {r.status_code}")
        print(f"     {r.text[:150]}")
    
    # Test 3: GET /reports/revenue (con parámetros de query)
    print("\n[3/3] GET /api/reports/revenue")
    r = requests.get(f"{BASE_URL}/api/reports/revenue?start_date={start}&end_date={end}&currency=USD", headers=headers)
    if r.status_code == 200:
        print(f"  ✅ SUCCESS: {r.status_code} - Reporte generado")
    else:
        print(f"  ❌ FAILED: {r.status_code}")
        print(f"     {r.text[:150]}")
    
    print("\n" + "="*70)
    print("PRUEBA COMPLETA")
    print("="*70)

if __name__ == "__main__":
    main()
