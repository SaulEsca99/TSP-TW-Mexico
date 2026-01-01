#!/usr/bin/env python3
"""
Script para analizar la calidad de la ruta encontrada
Verifica coherencia geográfica y calcula métricas detalladas
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from time_windows import RouteTimeCalculator


def analyze_route_quality(route_file, coords_file, time_matrix_file):
    """
    Analizar la calidad y coherencia de una ruta
    """
    print("="*70)
    print("ANÁLISIS DETALLADO DE LA MEJOR RUTA")
    print("="*70)
    
    # Cargar datos
    route_df = pd.read_csv(route_file)
    coords_df = pd.read_csv(coords_file)
    time_matrix = pd.read_csv(time_matrix_file, index_col=0).values
    distance_matrix = time_matrix * 60  # Convertir de vuelta a km
    
    route = route_df['ciudad_index'].values
    
    print(f"\n📍 Ruta completa ({len(route)} ciudades):\n")
    
    # Mostrar ruta completa con coordenadas
    for i, idx in enumerate(route):
        ciudad = coords_df.iloc[idx]['CIUDAD']
        estado = coords_df.iloc[idx]['ESTADO']
        lat = coords_df.iloc[idx]['lat']
        lon = coords_df.iloc[idx]['lon']
        
        marker = "🏁" if i == 0 else f"{i:2d}."
        print(f"{marker} {ciudad:25s} ({estado:20s}) - Lat: {lat:7.4f}, Lon: {lon:8.4f}")
    
    # Calcular métricas detalladas
    print(f"\n{'='*70}")
    print("MÉTRICAS DETALLADAS")
    print(f"{'='*70}\n")
    
    total_distance = 0
    total_time = 0
    segments = []
    
    for i in range(len(route)):
        from_idx = route[i]
        to_idx = route[(i + 1) % len(route)]
        
        from_city = coords_df.iloc[from_idx]['CIUDAD']
        to_city = coords_df.iloc[to_idx]['CIUDAD']
        
        distance = distance_matrix[from_idx, to_idx]
        time = time_matrix[from_idx, to_idx]
        
        total_distance += distance
        total_time += time
        
        segments.append({
            'from': from_city,
            'to': to_city,
            'distance_km': distance,
            'time_hours': time
        })
    
    print(f"📏 Distancia total: {total_distance:.2f} km")
    print(f"⏱️  Tiempo total de viaje: {total_time:.2f} horas ({total_time/24:.2f} días)")
    print(f"🚗 Velocidad promedio: 60 km/h (constante)")
    
    # Mostrar los 10 segmentos más largos
    print(f"\n{'='*70}")
    print("10 SEGMENTOS MÁS LARGOS")
    print(f"{'='*70}\n")
    
    segments_df = pd.DataFrame(segments)
    longest = segments_df.nlargest(10, 'distance_km')
    
    for idx, row in longest.iterrows():
        print(f"{row['from']:20s} → {row['to']:20s}: {row['distance_km']:7.2f} km ({row['time_hours']:5.2f}h)")
    
    # Análisis de coherencia geográfica
    print(f"\n{'='*70}")
    print("ANÁLISIS DE COHERENCIA GEOGRÁFICA")
    print(f"{'='*70}\n")
    
    # Verificar si hay cruces obvios (backtracking)
    coords = coords_df.iloc[route][['lat', 'lon']].values
    
    # Calcular cambios de dirección bruscos
    direction_changes = []
    for i in range(1, len(coords) - 1):
        prev = coords[i-1]
        curr = coords[i]
        next_c = coords[i+1]
        
        # Vectores de dirección
        v1 = curr - prev
        v2 = next_c - curr
        
        # Ángulo entre vectores
        if np.linalg.norm(v1) > 0 and np.linalg.norm(v2) > 0:
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            angle = np.arccos(np.clip(cos_angle, -1, 1)) * 180 / np.pi
            
            if angle > 120:  # Cambio de dirección mayor a 120 grados
                direction_changes.append({
                    'position': i,
                    'city': coords_df.iloc[route[i]]['CIUDAD'],
                    'angle': angle
                })
    
    if direction_changes:
        print(f"⚠️  Se detectaron {len(direction_changes)} cambios de dirección bruscos (>120°):")
        for change in direction_changes[:5]:
            print(f"   - En {change['city']}: {change['angle']:.1f}°")
    else:
        print("✅ No se detectaron cambios de dirección bruscos significativos")
    
    # Análisis de regiones
    print(f"\n{'='*70}")
    print("ANÁLISIS POR REGIONES")
    print(f"{'='*70}\n")
    
    # Clasificar ciudades por región aproximada
    regions = {
        'Norte': ['Chihuahua', 'Hermosillo', 'Mexicali', 'Monterrey', 'Saltillo', 'Durango'],
        'Centro-Norte': ['Zacatecas', 'San Luis Potosí', 'Aguascalientes', 'Guanajuato', 'Querétaro'],
        'Centro': ['Ciudad de México', 'Toluca', 'Pachuca', 'Tlaxcala', 'Puebla', 'Cuernavaca', 'Morelia'],
        'Occidente': ['Guadalajara', 'Colima', 'Tepic'],
        'Sur': ['Chilpancingo', 'Oaxaca', 'Tuxtla Gutierrez'],
        'Golfo': ['Jalapa', 'Villahermosa', 'Campeche'],
        'Península': ['Mérida', 'Chetumal'],
        'Noroeste': ['Culiacán', 'La Paz'],
        'Noreste': ['Ciudad Victoria']
    }
    
    route_cities = [coords_df.iloc[idx]['CIUDAD'] for idx in route]
    
    for region, cities in regions.items():
        cities_in_route = [c for c in route_cities if c in cities]
        if cities_in_route:
            positions = [route_cities.index(c) for c in cities_in_route]
            print(f"{region:15s}: {len(cities_in_route)} ciudades - Posiciones: {positions}")
    
    # Calcular con ventanas de tiempo
    print(f"\n{'='*70}")
    print("ANÁLISIS CON VENTANAS DE TIEMPO")
    print(f"{'='*70}\n")
    
    calculator = RouteTimeCalculator(time_matrix, start_time=9.0)
    total_time_tw, waiting_time, penalty = calculator.calculate_route_time(
        route.tolist(),
        include_waiting=True,
        include_penalties=True
    )
    
    print(f"⏱️  Tiempo de viaje puro: {total_time:.2f} horas")
    print(f"⏳ Tiempo de espera: {waiting_time:.2f} horas")
    print(f"⚠️  Penalizaciones: {penalty:.2f} horas")
    print(f"📊 Tiempo total (con TW): {total_time_tw:.2f} horas ({total_time_tw/24:.2f} días)")
    
    # Tiempos de llegada
    arrival_times = calculator.get_arrival_times(route.tolist())
    
    print(f"\n{'='*70}")
    print("TIEMPOS DE LLEGADA (primeras 10 ciudades)")
    print(f"{'='*70}\n")
    
    for i in range(min(10, len(route))):
        ciudad = coords_df.iloc[route[i]]['CIUDAD']
        arrival = arrival_times[i]
        day = int(arrival // 24) + 1
        hour_of_day = arrival % 24
        hours = int(hour_of_day)
        minutes = int((hour_of_day - hours) * 60)
        
        status = "✅" if 9 <= hour_of_day <= 21 else "⚠️"
        print(f"{status} {ciudad:25s}: Día {day}, {hours:02d}:{minutes:02d}")
    
    return {
        'total_distance': total_distance,
        'total_time': total_time,
        'total_time_tw': total_time_tw,
        'waiting_time': waiting_time,
        'penalty': penalty,
        'num_direction_changes': len(direction_changes)
    }


if __name__ == "__main__":
    results_dir = "results/run_20251231_210451"
    
    metrics = analyze_route_quality(
        f"{results_dir}/mejor_ruta.csv",
        "data/processed/coordenadas_capitales.csv",
        "data/processed/matriz_tiempos.csv"
    )
    
    print(f"\n{'='*70}")
    print("CONCLUSIÓN")
    print(f"{'='*70}\n")
    
    if metrics['penalty'] == 0:
        print("✅ La ruta cumple perfectamente con las ventanas de tiempo")
    else:
        print(f"⚠️  La ruta tiene {metrics['penalty']:.2f} horas de penalizaciones")
    
    if metrics['num_direction_changes'] < 5:
        print("✅ La ruta tiene buena coherencia geográfica (pocos retrocesos)")
    else:
        print(f"⚠️  La ruta tiene {metrics['num_direction_changes']} cambios de dirección bruscos")
    
    print(f"\n📊 Eficiencia: {(metrics['total_time'] / metrics['total_time_tw'] * 100):.1f}%")
    print(f"   (Tiempo de viaje / Tiempo total)")
