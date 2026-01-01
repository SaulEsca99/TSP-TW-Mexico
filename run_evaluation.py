#!/usr/bin/env python3
"""
Sistema de Evaluación Multi-Run para TSP-TW
Ejecuta el algoritmo genético 10 veces y calcula estadísticas
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from genetic_algorithm import GeneticAlgorithm


def run_experiment(time_matrix, start_city_index, run_number, config):
    """
    Ejecutar una ejecución del algoritmo genético
    
    Args:
        time_matrix: Matriz de tiempos
        start_city_index: Índice de CDMX
        run_number: Número de ejecución (para seed)
        config: Configuración del AG
        
    Returns:
        Diccionario con resultados
    """
    print(f"\n{'='*60}")
    print(f"EJECUCIÓN {run_number}/10")
    print(f"{'='*60}")
    
    # Configurar seed para reproducibilidad
    np.random.seed(run_number * 42)
    
    # Crear y ejecutar AG
    ga = GeneticAlgorithm(
        time_matrix=time_matrix,
        start_city_index=start_city_index,
        population_size=config['population_size'],
        generations=config['generations'],
        mutation_rate=config['mutation_rate'],
        crossover_rate=config['crossover_rate'],
        elitism_rate=config['elitism_rate'],
        start_time=9.0,
        penalty_weight=config['penalty_weight']
    )
    
    best_route, best_fitness, history = ga.evolve(verbose=False)
    
    print(f"✓ Completado - Mejor tiempo: {best_fitness:.2f} horas ({best_fitness/24:.2f} días)")
    
    return {
        'run': run_number,
        'best_fitness': best_fitness,
        'best_route': best_route.tolist(),
        'convergence_history': history,
        'seed': run_number * 42
    }


def calculate_statistics(results):
    """
    Calcular estadísticas de las 10 ejecuciones
    
    Args:
        results: Lista de resultados
        
    Returns:
        Diccionario con estadísticas
    """
    fitness_values = [r['best_fitness'] for r in results]
    
    stats = {
        'best': min(fitness_values),
        'worst': max(fitness_values),
        'mean': np.mean(fitness_values),
        'std': np.std(fitness_values),
        'median': np.median(fitness_values),
        'best_run': np.argmin(fitness_values) + 1,
        'worst_run': np.argmax(fitness_values) + 1,
        'all_values': fitness_values
    }
    
    return stats


def save_results(results, stats, coords_df, config):
    """
    Guardar resultados en archivos
    
    Args:
        results: Lista de resultados
        stats: Estadísticas
        coords_df: DataFrame de coordenadas
        config: Configuración usada
    """
    # Crear directorio de resultados con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(f"results/run_{timestamp}")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Guardar estadísticas
    stats_file = results_dir / "estadisticas.json"
    with open(stats_file, 'w') as f:
        json.dump({
            'statistics': {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                          for k, v in stats.items() if k != 'all_values'},
            'all_fitness_values': stats['all_values'],
            'configuration': config,
            'timestamp': timestamp
        }, f, indent=2)
    print(f"\n✓ Estadísticas guardadas en: {stats_file}")
    
    # 2. Guardar mejor ruta
    best_run_idx = stats['best_run'] - 1
    best_route = results[best_run_idx]['best_route']
    
    route_file = results_dir / "mejor_ruta.csv"
    route_df = pd.DataFrame({
        'orden': range(1, len(best_route) + 1),
        'ciudad_index': best_route,
        'ciudad': [coords_df.iloc[idx]['CIUDAD'] for idx in best_route],
        'estado': [coords_df.iloc[idx]['ESTADO'] for idx in best_route]
    })
    route_df.to_csv(route_file, index=False)
    print(f"✓ Mejor ruta guardada en: {route_file}")
    
    # 3. Guardar todas las convergencias
    convergence_file = results_dir / "convergencias.csv"
    convergence_data = []
    for r in results:
        for gen, fitness in enumerate(r['convergence_history']):
            convergence_data.append({
                'run': r['run'],
                'generation': gen + 1,
                'best_fitness': fitness
            })
    pd.DataFrame(convergence_data).to_csv(convergence_file, index=False)
    print(f"✓ Convergencias guardadas en: {convergence_file}")
    
    # 4. Guardar resumen de todas las ejecuciones
    summary_file = results_dir / "resumen_ejecuciones.csv"
    summary_df = pd.DataFrame([{
        'run': r['run'],
        'best_fitness_hours': r['best_fitness'],
        'best_fitness_days': r['best_fitness'] / 24,
        'seed': r['seed']
    } for r in results])
    summary_df.to_csv(summary_file, index=False)
    print(f"✓ Resumen guardado en: {summary_file}")
    
    return results_dir


def main():
    print("="*60)
    print("SISTEMA DE EVALUACIÓN MULTI-RUN - TSP-TW MÉXICO")
    print("="*60)
    
    # Configuración del experimento
    config = {
        'population_size': 100,
        'generations': 500,
        'mutation_rate': 0.02,
        'crossover_rate': 0.8,
        'elitism_rate': 0.1,
        'penalty_weight': 100.0,
        'num_runs': 10
    }
    
    print("\nConfiguración del experimento:")
    for key, value in config.items():
        print(f"  - {key}: {value}")
    
    # Cargar datos
    print("\nCargando datos procesados...")
    try:
        coords_df = pd.read_csv('data/processed/coordenadas_capitales.csv')
        time_matrix = pd.read_csv('data/processed/matriz_tiempos.csv', index_col=0).values
        cdmx_index = coords_df[coords_df['CIUDAD'] == 'Ciudad de México'].index[0]
        
        print(f"✓ {len(coords_df)} capitales cargadas")
        print(f"✓ CDMX en índice: {cdmx_index}")
    except Exception as e:
        print(f"✗ Error al cargar datos: {e}")
        return 1
    
    # Ejecutar 10 runs
    print(f"\nEjecutando {config['num_runs']} ejecuciones independientes...")
    results = []
    
    for i in range(1, config['num_runs'] + 1):
        result = run_experiment(time_matrix, cdmx_index, i, config)
        results.append(result)
    
    # Calcular estadísticas
    print(f"\n{'='*60}")
    print("CALCULANDO ESTADÍSTICAS")
    print(f"{'='*60}")
    
    stats = calculate_statistics(results)
    
    print(f"\nEstadísticas de {config['num_runs']} ejecuciones:")
    print(f"  Mejor valor:      {stats['best']:.2f} horas ({stats['best']/24:.2f} días) - Run {stats['best_run']}")
    print(f"  Peor valor:       {stats['worst']:.2f} horas ({stats['worst']/24:.2f} días) - Run {stats['worst_run']}")
    print(f"  Valor medio:      {stats['mean']:.2f} horas ({stats['mean']/24:.2f} días)")
    print(f"  Mediana:          {stats['median']:.2f} horas ({stats['median']/24:.2f} días)")
    print(f"  Desv. estándar:   {stats['std']:.2f} horas")
    print(f"  Rango:            {stats['worst'] - stats['best']:.2f} horas")
    
    # Guardar resultados
    print(f"\n{'='*60}")
    print("GUARDANDO RESULTADOS")
    print(f"{'='*60}")
    
    results_dir = save_results(results, stats, coords_df, config)
    
    print(f"\n{'='*60}")
    print("✓ EVALUACIÓN COMPLETADA")
    print(f"{'='*60}")
    print(f"\nResultados guardados en: {results_dir}")
    print(f"\nArchivos generados:")
    print(f"  - estadisticas.json")
    print(f"  - mejor_ruta.csv")
    print(f"  - convergencias.csv")
    print(f"  - resumen_ejecuciones.csv")
    
    return 0


if __name__ == "__main__":
    exit(main())
