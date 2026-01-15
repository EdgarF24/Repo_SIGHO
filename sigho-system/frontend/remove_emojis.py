"""
Script para eliminar emojis de archivos Python del frontend
"""
import os
import re
from pathlib import Path

# Mapeo de emojis a texto
EMOJI_MAP = {
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
}

def remove_emojis_from_file(file_path):
    """Elimina emojis de un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Reemplazar emojis conocidos
        for emoji, replacement in EMOJI_MAP.items():
            content = content.replace(emoji, replacement)
        
        # Remover cualquier otro emoji usando regex
        # Rango Unicode de emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticonos
            "\U0001F300-\U0001F5FF"  # símbolos & pictogramas
            "\U0001F680-\U0001F6FF"  # transporte & símbolos de mapa
            "\U0001F1E0-\U0001F1FF"  # banderas
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        content = emoji_pattern.sub('', content)
        
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
    
    python_files = list(frontend_dir.rglob("*.py"))
    
    modified_count = 0
    for file_path in python_files:
        if remove_emojis_from_file(file_path):
            print(f"Limpiado: {file_path.name}")
            modified_count += 1
    
    print(f"\n[COMPLETE] {modified_count} archivos modificados de {len(python_files)} totales")

if __name__ == "__main__":
    main()
