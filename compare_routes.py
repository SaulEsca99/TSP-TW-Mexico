#!/usr/bin/env python3
"""
Análisis comparativo de la ruta optimizada
"""

import pandas as pd
import numpy as np
from pathlib import Path

def compare_routes():
    print("="*70)
    print("COMPARACIÓN: RUTA ORIGINAL vs RUTA OPTIMIZADA")
    print("="*70)
    
    # Cargar ambas rutas
    original = pd.read_csv('results/run_20251231_210451/mejor_ruta.csv')
    optimized = pd.read_csv('results/optimized_20251231_211719/mejor_ruta_optimizada.csv')
    coords = pd.read_csv('data/processed/coordenadas_capitales.csv')
    time_matrix = pd.read_csv('data/processed/matriz_tiempos.csv', index_col=0).values
    
    print("\n📍 RUTA ORIGINAL (251.51 horas):")
    print("-" * 70)
    for i in range(min(15, len(original))):
        ciudad = original.iloc[i]['ciudad']
        print(f"  {i+1:2d}. {ciudad}")
    print(f"  ... ({len(original)-15} más)")
    
    print("\n📍 RUTA OPTIMIZADA (247.53 horas):")
    print("-" * 70)
    for i in range(min(15, len(optimized))):
        ciudad = optimized.iloc[i]['ciudad']
        print(f"  {i+1:2d}. {ciudad}")
    print(f"  ... ({len(optimized)-15} más)")
    
    # Calcular distancias
    def calc_distance(route_df):
        route = route_df['ciudad_index'].values
        total = 0
        for i in range(len(route)):
            from_idx = route[i]
            to_idx = route[(i + 1) % len(route)]
            total += time_matrix[from_idx, to_idx] * 60  # km
        return total
    
    orig_dist = calc_distance(original)
    opt_dist = calc_distance(optimized)
    
    print(f"\n📏 COMPARACIÓN DE DISTANCIAS:")
    print("-" * 70)
    print(f"  Original:   {orig_dist:,.2f} km")
    print(f"  Optimizada: {opt_dist:,.2f} km")
    print(f"  Diferencia: {orig_dist - opt_dist:,.2f} km ({((orig_dist - opt_dist)/orig_dist)*100:.1f}%)")
    
    print(f"\n⏱️  COMPARACIÓN DE TIEMPOS:")
    print("-" * 70)
    print(f"  Original:   251.51 horas (10.48 días)")
    print(f"  Optimizada: 247.53 horas (10.31 días)")
    print(f"  Mejora:     3.98 horas (1.6%)")
    
    # Encontrar diferencias en la secuencia
    orig_cities = original['ciudad'].tolist()
    opt_cities = optimized['ciudad'].tolist()
    
    differences = 0
    for i in range(len(orig_cities)):
        if orig_cities[i] != opt_cities[i]:
            differences += 1
    
    print(f"\n🔄 DIFERENCIAS EN LA SECUENCIA:")
    print("-" * 70)
    print(f"  Ciudades en diferente posición: {differences}/{len(orig_cities)}")
    print(f"  Similitud: {((32-differences)/32)*100:.1f}%")

if __name__ == "__main__":
    compare_routes()
