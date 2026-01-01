"""
Main execution file for TSP Mexico project
Archivo principal para ejecutar el algoritmo genético
"""

import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

from src.data_loader import DataLoader
from src.distance_calculator import DistanceCalculator
from src.genetic_algorithm import GeneticAlgorithm
from src.local_search import LocalSearch
from src.visualizer import Visualizer
from config import (GA_CONFIG, EXPERIMENT_CONFIG, LOCAL_SEARCH_CONFIG, 
                   PATHS, PLOT_CONFIG)


def run_single_experiment(distance_matrix, coordinates_df, run_number):
    """
    Ejecutar una sola ejecución del algoritmo genético
    
    Args:
        distance_matrix: Matriz de distancias
        coordinates_df: DataFrame con coordenadas
        run_number: Número de ejecución
        
    Returns:
        Diccionario con resultados
    """
    print(f"\n{'='*60}")
    print(f"Ejecución {run_number}/{EXPERIMENT_CONFIG['num_runs']}")
    print(f"{'='*60}")
    
    # Crear algoritmo genético
    ga = GeneticAlgorithm(
        distance_matrix=distance_matrix,
        population_size=GA_CONFIG['population_size'],
        generations=GA_CONFIG['generations'],
        mutation_rate=GA_CONFIG['mutation_rate'],
        crossover_rate=GA_CONFIG['crossover_rate'],
        elitism_rate=GA_CONFIG['elitism_rate']
    )
    
    # Ejecutar algoritmo
    best_route, best_fitness, fitness_history = ga.evolve()
    
    # Aplicar búsqueda local 2-opt si está habilitada
    if LOCAL_SEARCH_CONFIG['apply_2opt']:
        print("\nAplicando optimización 2-opt...")
        local_search = LocalSearch(distance_matrix)
        optimized_route, optimized_distance = local_search.optimize(
            best_route, 
            max_iterations=LOCAL_SEARCH_CONFIG['max_iterations']
        )
        
        print(f"Distancia antes de 2-opt: {best_fitness:.2f} km")
        print(f"Distancia después de 2-opt: {optimized_distance:.2f} km")
        print(f"Mejora: {best_fitness - optimized_distance:.2f} km "
              f"({((best_fitness - optimized_distance) / best_fitness * 100):.2f}%)")
        
        best_route = optimized_route
        best_fitness = optimized_distance
    
    return {
        'run_number': run_number,
        'best_route': best_route.tolist(),
        'best_fitness': best_fitness,
        'fitness_history': fitness_history
    }


def run_experiments():
    """Ejecutar múltiples experimentos y analizar resultados"""
    
    print("="*60)
    print("TSP MÉXICO - ALGORITMO GENÉTICO")
    print("="*60)
    
    # 1. Cargar datos
    print("\n1. Cargando datos...")
    
    # Por ahora, crear datos de ejemplo
    # TODO: Reemplazar con carga real de shapefiles
    coordinates_df = pd.DataFrame({
        'ciudad': ['CDMX', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana',
                  'León', 'Juárez', 'Torreón', 'Querétaro', 'Mérida'],
        'lat': [19.4326, 20.6597, 25.6866, 19.0414, 32.5149,
               21.1212, 31.6904, 25.5428, 20.5888, 20.9674],
        'lon': [-99.1332, -103.3496, -100.3161, -98.2063, -117.0382,
               -101.6806, -106.4245, -103.4068, -100.3899, -89.5926]
    })
    
    print(f"Ciudades cargadas: {len(coordinates_df)}")
    
    # 2. Calcular matriz de distancias
    print("\n2. Calculando matriz de distancias...")
    calculator = DistanceCalculator(coordinates_df)
    distance_matrix = calculator.build_distance_matrix()
    calculator.save_distance_matrix()
    
    # 3. Ejecutar múltiples experimentos
    print(f"\n3. Ejecutando {EXPERIMENT_CONFIG['num_runs']} experimentos...")
    
    all_results = []
    all_fitness_histories = []
    
    for i in range(EXPERIMENT_CONFIG['num_runs']):
        result = run_single_experiment(distance_matrix, coordinates_df, i + 1)
        all_results.append(result)
        all_fitness_histories.append(result['fitness_history'])
    
    # 4. Analizar resultados
    print("\n" + "="*60)
    print("ANÁLISIS DE RESULTADOS")
    print("="*60)
    
    fitness_values = [r['best_fitness'] for r in all_results]
    
    stats = {
        'mean': np.mean(fitness_values),
        'std': np.std(fitness_values),
        'min': np.min(fitness_values),
        'max': np.max(fitness_values),
        'median': np.median(fitness_values)
    }
    
    print(f"\nEstadísticas de {EXPERIMENT_CONFIG['num_runs']} ejecuciones:")
    print(f"  Media: {stats['mean']:.2f} km")
    print(f"  Desviación estándar: {stats['std']:.2f} km")
    print(f"  Mínimo: {stats['min']:.2f} km")
    print(f"  Máximo: {stats['max']:.2f} km")
    print(f"  Mediana: {stats['median']:.2f} km")
    
    # 5. Guardar resultados
    print("\n4. Guardando resultados...")
    
    # Guardar estadísticas
    stats_dir = Path(PATHS['results_stats'])
    stats_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(stats_dir / f'estadisticas_{timestamp}.json', 'w') as f:
        json.dump({
            'statistics': stats,
            'all_results': all_results,
            'config': GA_CONFIG
        }, f, indent=2)
    
    # 6. Visualizar resultados
    print("\n5. Generando visualizaciones...")
    
    visualizer = Visualizer(coordinates_df)
    
    # Encontrar mejor resultado
    best_result = min(all_results, key=lambda x: x['best_fitness'])
    best_route = np.array(best_result['best_route'])
    
    # Plotear mejor ruta
    visualizer.plot_route(
        best_route,
        title="Mejor Ruta Encontrada",
        filename=f"mejor_ruta_{timestamp}.png",
        distance=best_result['best_fitness']
    )
    
    # Plotear convergencia de todas las ejecuciones
    visualizer.plot_multiple_runs(
        all_fitness_histories,
        title=f"Convergencia de {EXPERIMENT_CONFIG['num_runs']} Ejecuciones",
        filename=f"convergencia_{timestamp}.png"
    )
    
    # Guardar mejor ruta en archivo de texto
    visualizer.save_route_to_file(
        best_route,
        best_result['best_fitness'],
        filename=f"mejor_ruta_{timestamp}.txt"
    )
    
    print("\n" + "="*60)
    print("PROCESO COMPLETADO")
    print("="*60)
    print(f"\nMejor distancia encontrada: {best_result['best_fitness']:.2f} km")
    print(f"Resultados guardados en: {PATHS['results_stats']}")
    print(f"Gráficas guardadas en: {PATHS['results_plots']}")


if __name__ == "__main__":
    run_experiments()
