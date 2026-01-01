"""
Configuration file for TSP Mexico project
Parámetros del Algoritmo Genético y configuración general
"""

# Parámetros del Algoritmo Genético
GA_CONFIG = {
    'population_size': 100,
    'generations': 500,
    'mutation_rate': 0.01,
    'crossover_rate': 0.8,
    'elitism_rate': 0.1,
    'tournament_size': 5
}

# Parámetros de operadores genéticos
OPERATORS_CONFIG = {
    'crossover_method': 'order',  # 'order', 'pmx', 'cycle'
    'mutation_method': 'swap'     # 'swap', 'inversion', 'scramble'
}

# Parámetros de búsqueda local
LOCAL_SEARCH_CONFIG = {
    'apply_2opt': True,
    'max_iterations': 1000
}

# Parámetros de ventanas de tiempo
TIME_WINDOW_CONFIG = {
    'use_time_windows': False,
    'penalty_weight': 1000,
    'avg_speed_kmh': 80
}

# Configuración de experimentos
EXPERIMENT_CONFIG = {
    'num_runs': 10,
    'save_all_results': True,
    'save_plots': True
}

# Rutas de archivos
PATHS = {
    'data_raw': 'data/raw',
    'data_processed': 'data/processed',
    'results_routes': 'results/rutas',
    'results_plots': 'results/graficas',
    'results_stats': 'results/estadisticas'
}

# Configuración de visualización
PLOT_CONFIG = {
    'figure_size': (12, 8),
    'dpi': 300,
    'show_plots': True,
    'save_plots': True
}
