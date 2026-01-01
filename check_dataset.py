#!/usr/bin/env python3
"""
Script temporal para verificar el contenido de los shapefiles
"""

try:
    import geopandas as gpd
    print("✓ GeoPandas está instalado")
except ImportError:
    print("✗ GeoPandas NO está instalado")
    print("\nPara instalar las dependencias, ejecuta:")
    print("  pip install -r requirements.txt")
    exit(1)

print("\n" + "="*60)
print("VERIFICACIÓN DEL DATASET DE MÉXICO")
print("="*60)

# Cargar shapefiles
try:
    ciudades = gpd.read_file('data/raw/México_Ciudades.shp')
    estados = gpd.read_file('data/raw/México_Estados.shp')
    
    print("\n📍 SHAPEFILE DE CIUDADES")
    print(f"   Total de ciudades: {len(ciudades)}")
    print(f"   Columnas: {list(ciudades.columns)}")
    print(f"   Sistema de coordenadas: {ciudades.crs}")
    print("\n   Primeras ciudades:")
    print(ciudades.head(10))
    
    print("\n\n🗺️  SHAPEFILE DE ESTADOS")
    print(f"   Total de estados: {len(estados)}")
    print(f"   Columnas: {list(estados.columns)}")
    print(f"   Sistema de coordenadas: {estados.crs}")
    print("\n   Estados:")
    print(estados)
    
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print(f"✓ Shapefiles cargados correctamente")
    print(f"✓ {len(estados)} estados encontrados")
    print(f"✓ {len(ciudades)} ciudades encontradas")
    
    if len(estados) == 32:
        print("✓ Número correcto de estados (32)")
    else:
        print(f"⚠ Se esperaban 32 estados, se encontraron {len(estados)}")
    
    print("\n💡 NOTA: Necesitas identificar cuáles de estas ciudades")
    print("   son las CAPITALES de cada estado para el TSP.")
    
except Exception as e:
    print(f"\n✗ Error al cargar shapefiles: {e}")
    exit(1)
