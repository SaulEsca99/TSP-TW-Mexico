#!/usr/bin/env python3
"""
Script para generar datos procesados del TSP-TW
Extrae coordenadas de capitales y genera matrices de distancias y tiempos
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loader import DataLoader
from distance_calculator import DistanceCalculator


def main():
    print("="*60)
    print("GENERACIÓN DE DATOS PROCESADOS - TSP-TW MÉXICO")
    print("="*60)
    
    # 1. Cargar shapefiles
    print("\n1. Cargando shapefiles...")
    loader = DataLoader()
    
    try:
        estados_gdf = loader.load_shapefile('México_Estados.shp')
        ciudades_gdf = loader.load_shapefile('México_Ciudades.shp')
        print(f"   ✓ {len(estados_gdf)} estados cargados")
        print(f"   ✓ {len(ciudades_gdf)} ciudades cargadas")
    except Exception as e:
        print(f"   ✗ Error al cargar shapefiles: {e}")
        return 1
    
    # 2. Extraer capitales
    print("\n2. Extrayendo capitales estatales...")
    try:
        capitales_df = loader.extract_capitals(estados_gdf, ciudades_gdf)
        print(f"   Capitales encontradas:")
        print(capitales_df[['CIUDAD', 'ESTADO']].to_string(index=False))
    except Exception as e:
        print(f"   ✗ Error al extraer capitales: {e}")
        return 1
    
    # 3. Guardar coordenadas
    print("\n3. Guardando coordenadas de capitales...")
    try:
        loader.save_coordinates(capitales_df)
    except Exception as e:
        print(f"   ✗ Error al guardar coordenadas: {e}")
        return 1
    
    # 4. Calcular matriz de distancias
    print("\n4. Calculando matriz de distancias geodésicas...")
    try:
        calc = DistanceCalculator(capitales_df)
        distance_matrix = calc.build_distance_matrix()
        print(f"   ✓ Matriz de distancias: {distance_matrix.shape}")
        print(f"   ✓ Distancia promedio: {distance_matrix[distance_matrix > 0].mean():.2f} km")
        print(f"   ✓ Distancia máxima: {distance_matrix.max():.2f} km")
    except Exception as e:
        print(f"   ✗ Error al calcular distancias: {e}")
        return 1
    
    # 5. Guardar matriz de distancias
    print("\n5. Guardando matriz de distancias...")
    try:
        calc.save_distance_matrix()
    except Exception as e:
        print(f"   ✗ Error al guardar matriz de distancias: {e}")
        return 1
    
    # 6. Generar matriz de tiempos (60 km/h)
    print("\n6. Generando matriz de tiempos (60 km/h)...")
    try:
        time_matrix = calc.build_time_matrix(avg_speed_kmh=60)
        print(f"   ✓ Matriz de tiempos: {time_matrix.shape}")
        print(f"   ✓ Tiempo promedio: {time_matrix[time_matrix > 0].mean():.2f} horas")
        print(f"   ✓ Tiempo máximo: {time_matrix.max():.2f} horas")
    except Exception as e:
        print(f"   ✗ Error al generar matriz de tiempos: {e}")
        return 1
    
    # 7. Guardar matriz de tiempos
    print("\n7. Guardando matriz de tiempos...")
    try:
        calc.save_time_matrix(time_matrix)
    except Exception as e:
        print(f"   ✗ Error al guardar matriz de tiempos: {e}")
        return 1
    
    # 8. Identificar CDMX
    print("\n8. Identificando Ciudad de México (CDMX)...")
    try:
        cdmx_index = capitales_df[capitales_df['CIUDAD'] == 'Ciudad de México'].index[0]
        print(f"   ✓ CDMX encontrada en índice: {cdmx_index}")
        print(f"   ✓ Coordenadas: {capitales_df.iloc[cdmx_index]['lat']:.4f}, {capitales_df.iloc[cdmx_index]['lon']:.4f}")
    except Exception as e:
        print(f"   ✗ Error al identificar CDMX: {e}")
        print("   ℹ Ciudades disponibles:")
        print(capitales_df['CIUDAD'].tolist())
        return 1
    
    print("\n" + "="*60)
    print("✓ DATOS PROCESADOS GENERADOS EXITOSAMENTE")
    print("="*60)
    print(f"\nArchivos generados:")
    print(f"  - data/processed/coordenadas_capitales.csv")
    print(f"  - data/processed/matriz_distancias.csv")
    print(f"  - data/processed/matriz_tiempos.csv")
    print(f"\nTotal de capitales: {len(capitales_df)}")
    print(f"Ciudad de inicio: Ciudad de México (índice {cdmx_index})")
    print(f"Velocidad de traslado: 60 km/h")
    print(f"Ventanas de tiempo: 9:00 - 21:00")
    
    return 0


if __name__ == "__main__":
    exit(main())
