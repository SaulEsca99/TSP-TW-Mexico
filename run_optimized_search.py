#!/usr/bin/env python3
"""
Búsqueda Optimizada - TSP-TW México
Configuración mejorada para encontrar mejores soluciones
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


def run_optimized_search():
    """
    Ejecutar búsqueda optimizada con mejores parámetros
    """
    print("="*70)
    print("BÚSQUEDA OPTIMIZADA - TSP-TW MÉXICO")
    print("="*70)
    
    # Configuración OPTIMIZADA
    config = {
        'population_size': 200,      # Duplicado (más diversidad)
        'generations': 1000,         # Duplicado (más tiempo de convergencia)
        'mutation_rate': 0.05,       # Aumentado (más exploración)
        'crossover_rate': 0.85,      # Aumentado ligeramente
        'elitism_rate': 0.15,        # Aumentado (preservar mejores)
        'penalty_weight': 100.0,
        'num_runs': 5                # 5 runs para encontrar mejor
    }
    
    print("\nConfiguración OPTIMIZADA:")
    print(f"  - Población: {config['population_size']} (↑ 100%)")
    print(f"  - Generaciones: {config['generations']} (↑ 100%)")
    print(f"  - Mutación: {config['mutation_rate']} (↑ 150%)")
    print(f"  - Cruce: {config['crossover_rate']} (↑ 6%)")
    print(f"  - Elitismo: {config['elitism_rate']} (↑ 50%)")
    print(f"  - Ejecuciones: {config['num_runs']}")
    
    # Cargar datos
    print("\nCargando datos procesados...")
    coords_df = pd.read_csv('data/processed/coordenadas_capitales.csv')
    time_matrix = pd.read_csv('data/processed/matriz_tiempos.csv', index_col=0).values
    cdmx_index = coords_df[coords_df['CIUDAD'] == 'Ciudad de México'].index[0]
    
    print(f"✓ {len(coords_df)} capitales cargadas")
    print(f"✓ CDMX en índice: {cdmx_index}")
    print(f"✓ Dataset SIN MODIFICAR (como fue entregado)")
    
    # Ejecutar búsqueda optimizada
    print(f"\n{'='*70}")
    print("EJECUTANDO BÚSQUEDA OPTIMIZADA")
    print(f"{'='*70}")
    print("\n⏱️  Tiempo estimado: ~30-40 minutos\n")
    
    results = []
    best_overall = float('inf')
    best_overall_route = None
    best_run_num = 0
    
    for i in range(1, config['num_runs'] + 1):
        print(f"\n{'='*70}")
        print(f"EJECUCIÓN OPTIMIZADA {i}/{config['num_runs']}")
        print(f"{'='*70}")
        
        # Seed diferente para cada run
        np.random.seed(i * 123)
        
        ga = GeneticAlgorithm(
            time_matrix=time_matrix,
            start_city_index=cdmx_index,
            population_size=config['population_size'],
            generations=config['generations'],
            mutation_rate=config['mutation_rate'],
            crossover_rate=config['crossover_rate'],
            elitism_rate=config['elitism_rate'],
            start_time=9.0,
            penalty_weight=config['penalty_weight']
        )
        
        best_route, best_fitness, history = ga.evolve(verbose=True)
        
        results.append({
            'run': i,
            'best_fitness': best_fitness,
            'best_route': best_route.tolist(),
            'convergence_history': history,
            'seed': i * 123
        })
        
        if best_fitness < best_overall:
            best_overall = best_fitness
            best_overall_route = best_route
            best_run_num = i
        
        print(f"\n✓ Run {i} completado: {best_fitness:.2f} horas ({best_fitness/24:.2f} días)")
        print(f"   Mejor hasta ahora: {best_overall:.2f} horas (Run {best_run_num})")
    
    # Calcular estadísticas
    print(f"\n{'='*70}")
    print("RESULTADOS DE BÚSQUEDA OPTIMIZADA")
    print(f"{'='*70}")
    
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
    
    print(f"\nEstadísticas de {config['num_runs']} ejecuciones optimizadas:")
    print(f"  🏆 MEJOR:         {stats['best']:.2f} horas ({stats['best']/24:.2f} días) - Run {stats['best_run']}")
    print(f"  📊 Promedio:      {stats['mean']:.2f} horas ({stats['mean']/24:.2f} días)")
    print(f"  📉 Peor:          {stats['worst']:.2f} horas ({stats['worst']/24:.2f} días)")
    print(f"  📏 Desv. Std:     {stats['std']:.2f} horas")
    print(f"  📐 Mediana:       {stats['median']:.2f} horas")
    
    # Comparar con resultado anterior
    previous_best = 251.51
    improvement = previous_best - stats['best']
    improvement_pct = (improvement / previous_best) * 100
    
    print(f"\n{'='*70}")
    print("COMPARACIÓN CON RESULTADO ANTERIOR")
    print(f"{'='*70}")
    print(f"  Resultado anterior:  {previous_best:.2f} horas")
    print(f"  Nuevo mejor:         {stats['best']:.2f} horas")
    print(f"  Mejora:              {improvement:.2f} horas ({improvement_pct:.1f}%)")
    
    if improvement > 0:
        print(f"\n  ✅ ¡MEJORA ENCONTRADA! {improvement:.2f} horas más rápido")
    else:
        print(f"\n  ℹ️  No se encontró mejora significativa")
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(f"results/optimized_{timestamp}")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar estadísticas
    stats_file = results_dir / "estadisticas_optimizadas.json"
    with open(stats_file, 'w') as f:
        json.dump({
            'statistics': {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                          for k, v in stats.items() if k != 'all_values'},
            'all_fitness_values': stats['all_values'],
            'configuration': config,
            'timestamp': timestamp,
            'comparison': {
                'previous_best': previous_best,
                'new_best': float(stats['best']),
                'improvement_hours': float(improvement),
                'improvement_percent': float(improvement_pct)
            }
        }, f, indent=2)
    
    # Guardar mejor ruta
    best_run_idx = stats['best_run'] - 1
    best_route = results[best_run_idx]['best_route']
    
    route_file = results_dir / "mejor_ruta_optimizada.csv"
    route_df = pd.DataFrame({
        'orden': range(1, len(best_route) + 1),
        'ciudad_index': best_route,
        'ciudad': [coords_df.iloc[idx]['CIUDAD'] for idx in best_route],
        'estado': [coords_df.iloc[idx]['ESTADO'] for idx in best_route]
    })
    route_df.to_csv(route_file, index=False)
    
    # Guardar convergencias
    convergence_file = results_dir / "convergencias_optimizadas.csv"
    convergence_data = []
    for r in results:
        for gen, fitness in enumerate(r['convergence_history']):
            convergence_data.append({
                'run': r['run'],
                'generation': gen + 1,
                'best_fitness': fitness
            })
    pd.DataFrame(convergence_data).to_csv(convergence_file, index=False)
    
    print(f"\n{'='*70}")
    print("✓ BÚSQUEDA OPTIMIZADA COMPLETADA")
    print(f"{'='*70}")
    print(f"\nResultados guardados en: {results_dir}")
    print(f"\nArchivos generados:")
    print(f"  - estadisticas_optimizadas.json")
    print(f"  - mejor_ruta_optimizada.csv")
    print(f"  - convergencias_optimizadas.csv")
    
    return results_dir, stats


if __name__ == "__main__":
    results_dir, stats = run_optimized_search()
    
    print(f"\n{'='*70}")
    print("PRÓXIMO PASO")
    print(f"{'='*70}")
    print(f"\nPara analizar la nueva ruta:")
    print(f"  python3 analyze_route.py")
    print(f"\nPara generar visualizaciones:")
    print(f"  python3 visualize_results.py {results_dir}")
