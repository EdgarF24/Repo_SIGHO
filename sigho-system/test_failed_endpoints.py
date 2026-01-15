"""
Prueba específica de los 4 endpoints que fallaron
"""
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"

def get_token():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "admin123"})
    return response.json()["access_token"]

def test_failed_endpoints():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    print("="*70)
    print("PRUEBA DE ENDPOINTS FALLIDOS")
    print("="*70)
    
    # Test 1: POST /maintenance
    print("\n[1/4] POST /api/maintenance")
    print("-"*70)
    try:
        data = {
            "room_id": 1,
            "title": "Prueba de mantenimiento",  # min 5 caracteres
            "description": "Esta es una descripción de prueba mayor a 10 caracteres",  # min 10 caracteres
            "maintenance_type": "corrective",
            "priority": "medium",
            "currency": "VES"
        }
        r = requests.post(f"{BASE_URL}/api/maintenance", headers=headers, json=data)
        if r.status_code in [200, 201]:
            print(f"✅ SUCCESS: {r.status_code}")
            print(f"   Mantenimiento creado: {r.json().get('maintenance_code')}")
        else:
            print(f"❌ FAILED: {r.status_code}")
            print(f"   Error: {r.text[:200]}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:100]}")
    
    # Test 2: POST /inventory
    print("\n[2/4] POST /api/inventory")
    print("-"*70)
    try:
        data = {
            "name": "Item de Prueba",
            "category": "amenities",
            "current_stock": 10,
            "min_stock": 5,
            "unit": "unidad"
        }
        r = requests.post(f"{BASE_URL}/api/inventory", headers=headers, json=data)
        if r.status_code in [200, 201]:
            print(f"✅ SUCCESS: {r.status_code}")
            print(f"   Item creado: {r.json().get('name')}")
        else:
            print(f"❌ FAILED: {r.status_code}")
            print(f"   Error: {r.text[:200]}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:100]}")
    
    # Test 3: POST /reports/occupancy
    print("\n[3/4] POST /api/reports/occupancy")
    print("-"*70)
    try:
        start_date = (date.today() - timedelta(days=7)).isoformat()
        end_date = date.today().isoformat()
        data = {
            "start_date": start_date,
            "end_date": end_date
        }
        r = requests.post(f"{BASE_URL}/api/reports/occupancy", headers=headers, json=data)
        if r.status_code == 200:
            print(f"✅ SUCCESS: {r.status_code}")
            result = r.json()
            print(f"   Reporte generado: {len(result.get('daily_data', []))} días")
        else:
            print(f"❌ FAILED: {r.status_code}")
            print(f"   Error: {r.text[:200]}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:100]}")
    
    # Test 4: POST /reports/revenue
    print("\n[4/4] POST /api/reports/revenue")
    print("-"*70)
    try:
        start_date = (date.today() - timedelta(days=7)).isoformat()
        end_date = date.today().isoformat()
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "currency": "USD"
        }
        r = requests.post(f"{BASE_URL}/api/reports/revenue", headers=headers, json=data)
        if r.status_code == 200:
            print(f"✅ SUCCESS: {r.status_code}")
            result = r.json()
            print(f"   Total ingresos: ${result.get('total_revenue', 0)}")
        else:
            print(f"❌ FAILED: {r.status_code}")
            print(f"   Error: {r.text[:200]}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:100]}")
    
    print("\n" + "="*70)
    print("PRUEBA COMPLETA")
    print("="*70)

if __name__ == "__main__":
    test_failed_endpoints()
