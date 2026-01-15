"""
Script para limpiar completamente los corchetes residuales de emojis
"""
import os
import re
from pathlib import Path

def clean_brackets(file_path):
    """Elimina los corchetes residuales como [Hotel], [OK], [Editar], etc."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Patrones específicos a eliminar
        patterns_to_remove = [
            r'\[Editar\]\s*',
            r'\[OK\]\s*',
            r'\[X\]\s*',
            r'\[Eliminar\]\s*',
            r'\[Reporte\]\s*',
            r'\[Hotel\]\s*',
            r'\[Mantenimiento\]\s*',
            r'\[Advertencia\]\s*',
            r'\[Tema\]\s*',
            r'\[Claro\]\s*',
            r'\[Config\]\s*',
            r'\[Info\]\s*',
            r'\[Nota\]\s*',
            r'\[Buscar\]\s*',
            r'\[Docs\]\s*',
            r'\[Inicio\]\s*',
            r'\[Sistema\]\s*',
            r'\[Limpieza\]\s*',
            r'\[Iniciar\]\s*',
            r'\[Pendiente\]\s*',
            r'\[Devolver\]\s*',
            r'\[Admin\]\s*',
            r'\[Inventario\]\s*',
            r'\[Idea\]\s*',
            r'\[Exito\]\s*',
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content)
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return False

def main():
    frontend_dir = Path(__file__).parent
    
    # Buscar todos archivos Python excepto este script
    python_files = [f for f in frontend_dir.rglob("*.py") if f.name != "clean_brackets.py"]
    
    modified_count = 0
    for file_path in python_files:
        if clean_brackets(file_path):
            print(f"[OK] Limpiado: {file_path.relative_to(frontend_dir)}")
            modified_count += 1
    
    print(f"\n[COMPLETE] {modified_count} archivos modificados de {len(python_files)} totales")

if __name__ == "__main__":
    main()
