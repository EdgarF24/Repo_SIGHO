#!/usr/bin/env python3
"""
Script de migración para normalizar amenidades
Crea tablas de amenidades y migra datos existentes desde campos booleanos
"""
import sys
import os

# Agregar el directorio backend al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine, Base
from app.models import RoomType, Amenity, RoomTypeAmenity


# Amenidades predefinidas
INITIAL_AMENITIES = [
    {"name": "WiFi", "description": "Internet inalámbrico de alta velocidad", "category": "básico", "icon": "wifi"},
    {"name": "TV", "description": "Televisión por cable", "category": "básico", "icon": "tv"},
    {"name": "Aire Acondicionado", "description": "Climatización", "category": "básico", "icon": "ac"},
    {"name": "Minibar", "description": "Frigobar con bebidas", "category": "premium", "icon": "minibar"},
    {"name": "Balcón", "description": "Balcón privado", "category": "premium", "icon": "balcony"},
    {"name": "Cocina", "description": "Cocineta equipada", "category": "premium", "icon": "kitchen"},
    {"name": "Caja Fuerte", "description": "Caja de seguridad", "category": "básico", "icon": "safe"},
    {"name": "Servicio de Habitación", "description": "Room service 24/7", "category": "premium", "icon": "room-service"},
    {"name": "Vista al Mar", "description": "Vista panorámica al mar", "category": "lujo", "icon": "ocean-view"},
    {"name": "Jacuzzi", "description": "Jacuzzi privado", "category": "lujo", "icon": "jacuzzi"},
]


def create_tables():
    """Crear tablas de amenidades"""
    print("📦 Creando tablas de amenidades...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas")


def insert_initial_amenities(db: Session):
    """Insertar amenidades iniciales"""
    print("\n🌟 Insertando amenidades iniciales...")
    
    amenities_dict = {}
    for amenity_data in INITIAL_AMENITIES:
        # Verificar si ya existe
        existing = db.query(Amenity).filter(Amenity.name == amenity_data["name"]).first()
        if existing:
            print(f"  ⏩ Amenidad '{amenity_data['name']}' ya existe, omitiendo...")
            amenities_dict[amenity_data["name"]] = existing
            continue
        
        amenity = Amenity(**amenity_data)
        db.add(amenity)
        amenities_dict[amenity_data["name"]] = amenity
        print(f"  ✅ Creada amenidad: {amenity_data['name']}")
    
    db.commit()
    print(f"✅ Total de amenidades en la base de datos: {db.query(Amenity).count()}")
    return amenities_dict


def migrate_room_type_amenities(db: Session, amenities_dict: dict):
    """Migrar campos booleanos de room_types a relaciones con amenities"""
    print("\n🔄 Migrando datos de tipos de habitación...")
    
    # Mapeo de campos booleanos antiguos a nombres de amenidades
    field_mapping = {
        "has_wifi": "WiFi",
        "has_tv": "TV",
        "has_ac": "Aire Acondicionado",
        "has_minibar": "Minibar",
        "has_balcony": "Balcón",
        "has_kitchen": "Cocina",
    }
    
    room_types = db.query(RoomType).all()
    if not room_types:
        print("  ⚠️  No hay tipos de habitación para migrar")
        return
    
    migrated_count = 0
    for room_type in room_types:
        print(f"\n  📝 Procesando tipo de habitación: {room_type.name}")
        amenities_to_add = []
        
        # Revisar cada campo booleano
        for field, amenity_name in field_mapping.items():
            if hasattr(room_type, field):
                value = getattr(room_type, field)
                if value is True:
                    amenity = amenities_dict.get(amenity_name)
                    if amenity:
                        amenities_to_add.append(amenity)
                        print(f"    ✅ Agregando amenidad: {amenity_name}")
        
        # Agregar amenidades al tipo de habitación
        if amenities_to_add:
            room_type.amenities = amenities_to_add
            migrated_count += 1
            print(f"    ✨ Total de amenidades agregadas: {len(amenities_to_add)}")
        else:
            print(f"    ℹ️ No hay amenidades booleanas activas en este tipo")
    
    db.commit()
    print(f"\n✅ Tipos de habitación migrados: {migrated_count}")


def verify_migration(db: Session):
    """Verificar que la migración fue exitosa"""
    print("\n🔍 Verificando migración...")
    
    room_types = db.query(RoomType).all()
    for room_type in room_types:
        amenity_names = [a.name for a in room_type.amenities]
        print(f"  📊 {room_type.name}: {len(amenity_names)} amenidades - {', '.join(amenity_names) if amenity_names else 'ninguna'}")
    
    total_associations = db.query(RoomTypeAmenity).count()
    print(f"\n✅ Total de asociaciones room_type-amenity: {total_associations}")


def remove_boolean_fields_warning():
    """Mostrar advertencia sobre eliminación de campos booleanos"""
    print("\n" + "="*70)
    print("⚠️  IMPORTANTE: SIGUIENTE PASO MANUAL")
    print("="*70)
    print("""
Los datos han sido migrados exitosamente a las nuevas tablas.

El siguiente paso es ELIMINAR las columnas booleanas antiguas de la tabla room_types:
  - has_wifi
  - has_tv
  - has_ac
  - has_minibar
  - has_balcony
  - has_kitchen

Esto requiere ejecutar comandos ALTER TABLE en SQLite3.

⚠️  ADVERTENCIA: Haz un backup de la base de datos antes de proceder.

Comandos SQL para ejecutar:
""")
    for field in ["has_wifi", "has_tv", "has_ac", "has_minibar", "has_balcony", "has_kitchen"]:
        print(f"  ALTER TABLE room_types DROP COLUMN {field};")
    
    print("\nNOTA: SQLite no soporta DROP COLUMN directamente en todas las versiones.")
    print("Si tu versión de SQLite no lo soporta, necesitarás recrear la tabla.")
    print("="*70)


def main():
    """Función principal de migración"""
    print("="*70)
    print("🚀 MIGRACIÓN DE AMENIDADES - SIGHO")
    print("="*70)
    print("\nEste script hará lo siguiente:")
    print("1. Crear tablas: amenities y room_type_amenities")
    print("2. Insertar 10 amenidades predefinidas")
    print("3. Migrar datos de campos booleanos a relaciones")
    print("4. Verificar la migración")
    print("\n⚠️  IMPORTANTE: Asegúrate de tener un backup de la base de datos\n")
    
    response = input("¿Deseas continuar? (s/n): ")
    if response.lower() != 's':
        print("❌ Migración cancelada")
        return
    
    # Crear sesión de base de datos
    db = SessionLocal()
    
    try:
        # Paso 1: Crear tablas
        create_tables()
        
        # Paso 2: Insertar amenidades iniciales
        amenities_dict = insert_initial_amenities(db)
        
        # Paso 3: Migrar datos existentes
        migrate_room_type_amenities(db, amenities_dict)
        
        # Paso 4: Verificar migración
        verify_migration(db)
        
        # Paso 5: Mostrar advertencia sobre limpieza manual
        remove_boolean_fields_warning()
        
        print("\n✅ ¡Migración completada exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
