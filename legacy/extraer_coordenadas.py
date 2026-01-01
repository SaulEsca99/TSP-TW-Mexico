"""
================================================================================
EXTRACTOR DE COORDENADAS DESDE SHAPEFILE
Proyecto: TSP-TW Capitales de México

Este script lee el shapefile proporcionado por el profesor y extrae:
- Coordenadas geográficas (latitud, longitud) de cada capital
- Nombres de las ciudades
- Estados correspondientes

Autor: Escamilla Lazcano Saúl
Grupo: 5BV1 - ESCOM - IPN
================================================================================
"""

import geopandas as gpd
import json
import os
import sys

def extraer_coordenadas_shapefile(ruta_shapefile, mostrar_detalles=True):
    """
    Extrae coordenadas de las capitales desde el shapefile.
    
    Args:
        ruta_shapefile (str): Ruta al archivo .shp
        mostrar_detalles (bool): Si True, muestra información detallada
    
    Returns:
        dict: Diccionario con coordenadas de cada capital
    """
    print(f"\n{'='*80}")
    print(f"EXTRAYENDO COORDENADAS DEL SHAPEFILE")
    print(f"{'='*80}\n")
    
    # Verificar que el archivo existe
    if not os.path.exists(ruta_shapefile):
        print(f"❌ ERROR: No se encontró el archivo: {ruta_shapefile}")
        print(f"\nVerifica que:")
        print(f"  1. Descomprimiste el RAR del profesor")
        print(f"  2. Copiaste México_Ciudades.shp (y archivos .dbf, .shx, .prj) a la carpeta datos/")
        print(f"  3. La ruta es correcta\n")
        sys.exit(1)
    
    print(f"📂 Leyendo shapefile: {ruta_shapefile}")
    
    try:
        # Leer shapefile
        gdf = gpd.read_file(ruta_shapefile)
        print(f"✓ Shapefile cargado exitosamente!\n")
        
    except Exception as e:
        print(f"❌ ERROR al leer shapefile: {e}")
        print(f"\nVerifica que todos los archivos asociados estén presentes:")
        print(f"  - México_Ciudades.shp")
        print(f"  - México_Ciudades.dbf")
        print(f"  - México_Ciudades.shx")
        print(f"  - México_Ciudades.prj")
        sys.exit(1)
    
    # Información básica
    print(f"📊 INFORMACIÓN DEL SHAPEFILE:")
    print(f"  - Número de ciudades: {len(gdf)}")
    print(f"  - Sistema de coordenadas: {gdf.crs}")
    print(f"  - Tipo de geometría: {gdf.geometry.type.unique()[0]}")
    print(f"  - Columnas disponibles: {list(gdf.columns)}\n")
    
    if mostrar_detalles:
        print(f"{'='*80}")
        print(f"PRIMERAS 5 CIUDADES EN EL SHAPEFILE:")
        print(f"{'='*80}")
        print(gdf.head().to_string())
        print()
    
    # IMPORTANTE: Detectar automáticamente los nombres de columnas
    # El shapefile puede tener diferentes nombres
    posibles_nombres_ciudad = ['NOMBRE', 'Ciudad', 'CITY_NAME', 'NOM_LOC', 'NOMGEO', 'Name']
    posibles_nombres_estado = ['ESTADO', 'Estado', 'STATE_NAME', 'NOM_ENT', 'CVE_ENT', 'State']
    
    columna_nombre = None
    columna_estado = None
    
    # Detectar columna de nombres
    for col in posibles_nombres_ciudad:
        if col in gdf.columns:
            columna_nombre = col
            break
    
    # Detectar columna de estados
    for col in posibles_nombres_estado:
        if col in gdf.columns:
            columna_estado = col
            break
    
    if not columna_nombre:
        print(f"⚠️  ADVERTENCIA: No se detectó columna de nombres automáticamente")
        print(f"   Columnas disponibles: {list(gdf.columns)}")
        print(f"   Por favor, modifica manualmente el script para especificar la columna correcta\n")
        columna_nombre = gdf.columns[0]  # Usar primera columna por defecto
    
    print(f"🔍 COLUMNAS DETECTADAS:")
    print(f"  - Nombres de ciudades: {columna_nombre}")
    print(f"  - Nombres de estados: {columna_estado if columna_estado else 'No detectada'}\n")
    
    # Extraer coordenadas
    capitales = {}
    cdmx_idx = None
    
    for idx, row in gdf.iterrows():
        # Obtener geometría (punto)
        punto = row.geometry
        
        # Extraer nombre y estado
        nombre = str(row[columna_nombre]) if columna_nombre else f'Ciudad_{idx}'
        estado = str(row[columna_estado]) if columna_estado else ''
        
        # Detectar CDMX para asignarle índice 0
        nombre_lower = nombre.lower()
        if 'méxico' in nombre_lower and 'ciudad' in nombre_lower or nombre_lower == 'cdmx':
            cdmx_idx = idx
        
        capitales[idx] = {
            'nombre': nombre,
            'estado': estado,
            'lat': float(punto.y),  # Latitud
            'lon': float(punto.x)   # Longitud
        }
    
    # Reorganizar para que CDMX sea índice 0
    if cdmx_idx is not None and cdmx_idx != 0:
        print(f"⚙️  Reorganizando: CDMX encontrada en índice {cdmx_idx}, moviéndola a índice 0\n")
        
        # Crear nuevo diccionario con CDMX en índice 0
        capitales_reordenadas = {}
        capitales_reordenadas[0] = capitales[cdmx_idx]
        
        nuevo_idx = 1
        for idx in range(len(capitales)):
            if idx != cdmx_idx:
                capitales_reordenadas[nuevo_idx] = capitales[idx]
                nuevo_idx += 1
        
        capitales = capitales_reordenadas
    
    return capitales

def guardar_coordenadas(capitales, ruta_salida):
    """
    Guarda las coordenadas en formato JSON.
    
    Args:
        capitales (dict): Diccionario con coordenadas
        ruta_salida (str): Ruta donde guardar el JSON
    """
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(capitales, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Coordenadas guardadas en: {ruta_salida}\n")

def mostrar_resumen(capitales):
    """
    Muestra un resumen de las coordenadas extraídas.
    
    Args:
        capitales (dict): Diccionario con coordenadas
    """
    print(f"{'='*80}")
    print(f"RESUMEN DE EXTRACCIÓN")
    print(f"{'='*80}")
    print(f"Total de capitales: {len(capitales)}\n")
    
    print(f"{'Idx':<5} {'Ciudad':<25} {'Estado':<20} {'Latitud':<12} {'Longitud':<12}")
    print(f"{'-'*80}")
    
    for i in range(min(10, len(capitales))):  # Mostrar primeras 10
        cap = capitales[i]
        print(f"{i:<5} {cap['nombre']:<25} {cap['estado']:<20} "
              f"{cap['lat']:>10.4f}  {cap['lon']:>10.4f}")
    
    if len(capitales) > 10:
        print(f"... y {len(capitales) - 10} ciudades más")
    
    print(f"{'='*80}\n")
    
    # Verificar que CDMX sea índice 0
    if 'méxico' in capitales[0]['nombre'].lower() or 'cdmx' in capitales[0]['nombre'].lower():
        print(f"✓ VERIFICACIÓN: CDMX correctamente asignada al índice 0")
    else:
        print(f"⚠️  ADVERTENCIA: La ciudad en índice 0 no parece ser CDMX")
        print(f"   Ciudad en índice 0: {capitales[0]['nombre']}")
    
    print()

def main():
    """
    Función principal del script.
    """
    print(f"\n{'#'*80}")
    print(f"# EXTRACTOR DE COORDENADAS - TSP-TW CAPITALES DE MÉXICO")
    print(f"# Autor: Escamilla Lazcano Saúl - 5BV1")
    print(f"{'#'*80}")
    
    # CONFIGURACIÓN - AJUSTA ESTAS RUTAS SEGÚN TU ESTRUCTURA
    RUTA_SHAPEFILE = "../datos/México_Ciudades.shp"
    RUTA_SALIDA_JSON = "../datos/coordenadas_capitales.json"
    
    # Permitir pasar ruta como argumento
    if len(sys.argv) > 1:
        RUTA_SHAPEFILE = sys.argv[1]
    
    if len(sys.argv) > 2:
        RUTA_SALIDA_JSON = sys.argv[2]
    
    print(f"\n📋 CONFIGURACIÓN:")
    print(f"  - Shapefile entrada: {RUTA_SHAPEFILE}")
    print(f"  - JSON salida: {RUTA_SALIDA_JSON}")
    
    # Extraer coordenadas
    capitales = extraer_coordenadas_shapefile(RUTA_SHAPEFILE, mostrar_detalles=True)
    
    # Guardar a JSON
    guardar_coordenadas(capitales, RUTA_SALIDA_JSON)
    
    # Mostrar resumen
    mostrar_resumen(capitales)
    
    print(f"{'#'*80}")
    print(f"# EXTRACCIÓN COMPLETADA EXITOSAMENTE")
    print(f"# Puedes ahora ejecutar el algoritmo principal")
    print(f"{'#'*80}\n")

if __name__ == "__main__":
    main()
