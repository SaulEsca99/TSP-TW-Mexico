#!/usr/bin/env python3
"""
Script para generar visualizaciones de los resultados
"""

import sys
import pandas as pd
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from visualizer import TSPTWVisualizer


def main():
    if len(sys.argv) < 2:
        print("Uso: python visualize_results.py <directorio_resultados>")
        print("\nEjemplo:")
        print("  python visualize_results.py results/run_20250101_120000")
        return 1
    
    results_dir = Path(sys.argv[1])
    
    if not results_dir.exists():
        print(f"✗ Error: El directorio {results_dir} no existe")
        return 1
    
    print("="*60)
    print("GENERACIÓN DE VISUALIZACIONES - TSP-TW")
    print("="*60)
    print(f"\nDirectorio de resultados: {results_dir}")
    
    # Cargar coordenadas
    coords_df = pd.read_csv('data/processed/coordenadas_capitales.csv')
    
    # Crear visualizador
    viz = TSPTWVisualizer(coords_df, output_dir=results_dir / "graficas")
    
    # Generar todas las visualizaciones
    viz.create_summary_report(results_dir)
    
    print("\n" + "="*60)
    print("✓ VISUALIZACIONES COMPLETADAS")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    exit(main())
