"""
Visualizer Module - Actualizado para TSP-TW
Visualización de rutas y resultados con tiempos y ventanas
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Optional
import json


class TSPTWVisualizer:
    """Clase para visualizar rutas y resultados del TSP-TW"""
    
    def __init__(self, coordinates_df: pd.DataFrame, output_dir: str = "results/graficas"):
        """
        Inicializar visualizador
        
        Args:
            coordinates_df: DataFrame con coordenadas de ciudades
            output_dir: Directorio para guardar gráficas
        """
        self.coordinates = coordinates_df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_route(self, route: np.ndarray, title: str = "Ruta TSP-TW", 
                   filename: Optional[str] = None, time_hours: Optional[float] = None):
        """
        Visualizar una ruta en el mapa
        
        Args:
            route: Array con el orden de ciudades
            title: Título de la gráfica
            filename: Nombre del archivo para guardar
            time_hours: Tiempo total de la ruta en horas
        """
        plt.figure(figsize=(14, 10))
        
        # Obtener coordenadas de la ruta
        lats = [self.coordinates.iloc[city]['lat'] for city in route]
        lons = [self.coordinates.iloc[city]['lon'] for city in route]
        
        # Cerrar el ciclo
        lats.append(lats[0])
        lons.append(lons[0])
        
        # Plotear ruta
        plt.plot(lons, lats, 'b-', linewidth=2, alpha=0.6, label='Ruta')
        plt.plot(lons, lats, 'ro', markersize=6)
        
        # Marcar ciudad inicial (CDMX)
        plt.plot(lons[0], lats[0], 'g*', markersize=20, label='CDMX (Inicio/Fin)', 
                markeredgecolor='black', markeredgewidth=1.5)
        
        # Añadir números de orden
        for i, city in enumerate(route[:10]):  # Primeras 10 para no saturar
            plt.annotate(str(i+1), (lons[i], lats[i]), 
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle='circle', facecolor='white', alpha=0.7))
        
        plt.xlabel('Longitud', fontsize=12)
        plt.ylabel('Latitud', fontsize=12)
        
        if time_hours is not None:
            days = time_hours / 24
            title += f"\nTiempo total: {time_hours:.2f} horas ({days:.2f} días)"
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if filename:
            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfica guardada en: {output_path}")
            plt.close()
        else:
            plt.show()
    
    def plot_convergence(self, fitness_history: List[float], 
                        title: str = "Convergencia del Algoritmo Genético TSP-TW",
                        filename: Optional[str] = None):
        """
        Visualizar convergencia del algoritmo
        
        Args:
            fitness_history: Lista con historial de fitness (tiempos)
            title: Título de la gráfica
            filename: Nombre del archivo para guardar
        """
        plt.figure(figsize=(12, 7))
        
        generations = range(1, len(fitness_history) + 1)
        plt.plot(generations, fitness_history, 'b-', linewidth=2)
        plt.xlabel('Generación', fontsize=12)
        plt.ylabel('Mejor Tiempo (horas)', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if filename:
            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfica guardada en: {output_path}")
            plt.close()
        else:
            plt.show()
    
    def plot_multiple_runs(self, all_fitness_histories: List[List[float]],
                          title: str = "Comparación de 10 Ejecuciones - TSP-TW",
                          filename: Optional[str] = None):
        """
        Visualizar múltiples ejecuciones del algoritmo
        
        Args:
            all_fitness_histories: Lista de historiales de fitness
            title: Título de la gráfica
            filename: Nombre del archivo para guardar
        """
        plt.figure(figsize=(14, 8))
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(all_fitness_histories)))
        
        for i, history in enumerate(all_fitness_histories):
            generations = range(1, len(history) + 1)
            plt.plot(generations, history, alpha=0.4, linewidth=1.5, 
                    color=colors[i], label=f'Run {i+1}')
        
        # Calcular y plotear promedio
        max_len = max(len(h) for h in all_fitness_histories)
        avg_history = []
        
        for gen in range(max_len):
            values = [h[gen] for h in all_fitness_histories if gen < len(h)]
            avg_history.append(np.mean(values))
        
        generations = range(1, len(avg_history) + 1)
        plt.plot(generations, avg_history, 'r-', linewidth=3, label='Promedio', zorder=10)
        
        plt.xlabel('Generación', fontsize=12)
        plt.ylabel('Mejor Tiempo (horas)', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=9, ncol=2)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if filename:
            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfica guardada en: {output_path}")
            plt.close()
        else:
            plt.show()
    
    def plot_statistics_boxplot(self, all_fitness_values: List[float],
                                title: str = "Distribución de Resultados (10 Runs)",
                                filename: Optional[str] = None):
        """
        Crear boxplot de los resultados de las 10 ejecuciones
        
        Args:
            all_fitness_values: Lista con los mejores fitness de cada run
            title: Título de la gráfica
            filename: Nombre del archivo para guardar
        """
        plt.figure(figsize=(10, 7))
        
        bp = plt.boxplot([all_fitness_values], vert=True, patch_artist=True,
                         labels=['TSP-TW'])
        
        # Personalizar colores
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
        
        # Añadir puntos individuales
        y = all_fitness_values
        x = np.random.normal(1, 0.04, size=len(y))
        plt.plot(x, y, 'ro', alpha=0.6, markersize=8)
        
        # Añadir estadísticas
        mean_val = np.mean(all_fitness_values)
        median_val = np.median(all_fitness_values)
        plt.axhline(y=mean_val, color='g', linestyle='--', linewidth=2, label=f'Media: {mean_val:.2f}h')
        plt.axhline(y=median_val, color='b', linestyle='--', linewidth=2, label=f'Mediana: {median_val:.2f}h')
        
        plt.ylabel('Tiempo Total (horas)', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        if filename:
            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfica guardada en: {output_path}")
            plt.close()
        else:
            plt.show()
    
    def create_summary_report(self, results_dir: Path):
        """
        Crear reporte visual completo de los resultados
        
        Args:
            results_dir: Directorio con los resultados
        """
        print(f"\n{'='*60}")
        print("GENERANDO VISUALIZACIONES")
        print(f"{'='*60}\n")
        
        # Cargar datos
        stats_file = results_dir / "estadisticas.json"
        convergence_file = results_dir / "convergencias.csv"
        route_file = results_dir / "mejor_ruta.csv"
        
        with open(stats_file, 'r') as f:
            data = json.load(f)
        
        stats = data['statistics']
        all_values = data['all_fitness_values']
        
        convergence_df = pd.read_csv(convergence_file)
        route_df = pd.read_csv(route_file)
        
        # 1. Gráfica de convergencia de la mejor ejecución
        best_run = stats['best_run']
        best_convergence = convergence_df[convergence_df['run'] == best_run]['best_fitness'].tolist()
        self.plot_convergence(
            best_convergence,
            title=f"Convergencia - Mejor Ejecución (Run {best_run})",
            filename="convergencia_mejor_run.png"
        )
        
        # 2. Comparación de todas las ejecuciones
        all_histories = []
        for run in range(1, 11):
            history = convergence_df[convergence_df['run'] == run]['best_fitness'].tolist()
            all_histories.append(history)
        
        self.plot_multiple_runs(
            all_histories,
            title="Comparación de 10 Ejecuciones Independientes",
            filename="comparacion_10_runs.png"
        )
        
        # 3. Boxplot de resultados
        self.plot_statistics_boxplot(
            all_values,
            title=f"Distribución de Resultados\n(Media: {stats['mean']:.2f}h, Std: {stats['std']:.2f}h)",
            filename="distribucion_resultados.png"
        )
        
        # 4. Mapa de la mejor ruta
        best_route = route_df['ciudad_index'].values
        self.plot_route(
            best_route,
            title=f"Mejor Ruta Encontrada (Run {best_run})",
            time_hours=stats['best'],
            filename="mejor_ruta_mapa.png"
        )
        
        print(f"\n✓ Todas las visualizaciones generadas en: {self.output_dir}")
