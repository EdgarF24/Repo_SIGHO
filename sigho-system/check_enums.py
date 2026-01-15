"""
Script para verificar coincidencia de enums entre Frontend y Backend
"""
import re
from pathlib import Path

# Definir todos los enums del backend con sus valores correctos
BACKEND_ENUMS = {
    "PaymentMethod": ["cash_ves", "cash_usd", "cash_eur", "transfer", "mobile_payment", "credit_card", "debit_card", "other"],
    "PaymentStatus": ["pending", "completed", "failed", "refunded"],
    "UserRole": ["admin", "manager", "receptionist", "maintenance", "inventory", "viewer"],
    "RoomStatus": ["available", "occupied", "cleaning", "maintenance", "out_of_service"],
    "ReservationStatus": ["pending", "confirmed", "checked_in", "checked_out", "cancelled", "no_show"],
    "MaintenanceType": ["preventive", "corrective", "emergency"],
    "MaintenancePriority": ["low", "medium", "high", "critical"],
    "MaintenanceStatus": ["pending", "assigned", "in_progress", "completed", "cancelled"],
    "MovementType": ["entry", "exit", "adjustment", "loss"],
    "InventoryCategory": ["amenities", "cleaning", "food_beverage", "maintenance", "office"]
}

def check_frontend_views():
    """Verifica todos los archivos de vistas del frontend"""
    frontend_dir = Path(__file__).parent / "frontend" / "app" / "views"
    issues = []
    
    for view_file in frontend_dir.glob("*.py"):
        with open(view_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar definiciones de combobox con valores
        pattern = r'"values":\s*\[([^\]]+)\]'
        matches = re.findall(pattern, content)
        
        for match in matches:
            # Limpiar y obtener valores
            values = [v.strip().strip('"').strip("'") for v in match.split(',')]
            
            # Verificar contra enums conocidos
            for enum_name, enum_values in BACKEND_ENUMS.items():
                # Si hay coincidencia parcial, verificar si falta alguno
                intersection = set(values) & set(enum_values)
                if intersection and len(intersection) < len(set(values)):
                    # Hay valores que no están en el enum del backend
                    invalid = set(values) - set(enum_values)
                    if invalid and len(values) > 2:  # Ignorar casos simples como ["Todas"]
                        issues.append({
                            "file": view_file.name,
                            "enum": enum_name,
                            "found": values,
                            "expected": enum_values,
                            "invalid": list(invalid)
                        })
    
    return issues

def main():
    print("="*60)
    print("VERIFICADOR DE ENUMS FRONTEND-BACKEND")
    print("="*60)
    print()
    
    issues = check_frontend_views()
    
    if not issues:
        print("[OK] No se encontraron problemas de enums!")
    else:
        print(f"[ADVERTENCIA] Se encontraron {len(issues)} posibles problemas:\n")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue['file']}")
            print(f"   Enum probable: {issue['enum']}")
            print(f"   Valores encontrados: {issue['found']}")
            print(f"   Valores esperados: {issue['expected']}")
            print(f"   Valores inválidos: {issue['invalid']}")
            print()

if __name__ == "__main__":
    main()
