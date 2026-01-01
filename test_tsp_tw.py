#!/usr/bin/env python3
"""
Script de prueba rápida del TSP-TW
Prueba el algoritmo genético con los datos generados
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from genetic_algorithm import GeneticAlgorithm


def main():
    print("="*60)
    print("PRUEBA RÁPIDA - TSP-TW MÉXICO")
    print("="*60)
    
    # 1. Cargar datos procesados
    print("\n1. Cargando datos procesados...")
    try:
        coords_df = pd.read_csv('data/processed/coordenadas_capitales.csv')
        time_matrix = pd.read_csv('data/processed/matriz_tiempos.csv', index_col=0).values
        
        print(f"   ✓ {len(coords_df)} capitales cargadas")
        print(f"   ✓ Matriz de tiempos: {time_matrix.shape}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print("   ℹ Ejecuta primero: python generate_data.py")
        return 1
    
    # 2. Identificar CDMX
    print("\n2. Identificando Ciudad de México...")
    try:
        cdmx_index = coords_df[coords_df['CIUDAD'] == 'Ciudad de México'].index[0]
        print(f"   ✓ CDMX en índice: {cdmx_index}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return 1
    
    # 3. Configurar y ejecutar AG
    print("\n3. Ejecutando Algoritmo Genético (prueba rápida)...")
    print("   Configuración:")
    print("   - Población: 50")
    print("   - Generaciones: 100")
    print("   - Tasa de mutación: 0.02")
    print("   - Tasa de cruce: 0.8")
    
    try:
        ga = GeneticAlgorithm(
            time_matrix=time_matrix,
            start_city_index=cdmx_index,
            population_size=50,
            generations=100,
            mutation_rate=0.02,
            crossover_rate=0.8,
            elitism_rate=0.1,
            start_time=9.0,
            penalty_weight=100.0
        )
        
        best_route, best_fitness, history = ga.evolve(verbose=True)
        
    except Exception as e:
        print(f"\n   ✗ Error durante ejecución: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 4. Mostrar resultados
    print("\n" + "="*60)
    print("RESULTADOS")
    print("="*60)
    print(f"\nMejor tiempo total: {best_fitness:.2f} horas ({best_fitness/24:.2f} días)")
    print(f"\nRuta encontrada ({len(best_route)} ciudades):")
    
    for i, city_idx in enumerate(best_route[:10]):  # Mostrar primeras 10
        city_name = coords_df.iloc[city_idx]['CIUDAD']
        print(f"   {i+1}. {city_name}")
    
    if len(best_route) > 10:
        print(f"   ... ({len(best_route)-10} ciudades más)")
    
    print(f"\n✓ Prueba completada exitosamente")
    
    return 0


if __name__ == "__main__":
    exit(main())
