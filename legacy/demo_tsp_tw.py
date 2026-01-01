"""
VERSIÓN DEMO - TSP-TW México con HGA
(Configuración rápida para demostración)
"""

# Importar el módulo principal
import sys
sys.path.insert(0, '/home/claude')
from TSP_TW_Mexico_HGA import *

if __name__ == "__main__":
    print(f"\n{'#'*80}")
    print(f"# DEMO - TSP-TW México con Algoritmo Genético Híbrido")
    print(f"# (Versión rápida: 3 ejecuciones, 200 generaciones)")
    print(f"{'#'*80}\n")
    
    # Crear matrices
    print("Calculando matriz de distancias...")
    matriz_distancias, matriz_tiempos = crear_matriz_distancias()
    print(f"✓ Matriz creada: {N_CIUDADES}x{N_CIUDADES} ciudades\n")
    
    # Realizar 3 ejecuciones rápidas
    resultados = realizar_experimentos(
        matriz_tiempos,
        num_ejecuciones=3,
        tam_poblacion=50,
        num_generaciones=200
    )
    
    # Analizar resultados
    df_resultados, mejor_idx = analizar_resultados(resultados)
    
    # Guardar resultados
    os.makedirs('resultados_demo', exist_ok=True)
    df_resultados.to_csv('resultados_demo/resultados.csv', index=False)
    print(f"✓ Guardado: resultados_demo/resultados.csv\n")
    
    # Visualizar
    print("Generando visualizaciones...")
    visualizar_resultados(resultados, matriz_distancias, output_dir='resultados_demo')
    
    # Detalles de mejor ruta
    print(f"\n{'='*80}")
    print("EVALUACIÓN DETALLADA DE LA MEJOR RUTA ENCONTRADA")
    print(f"{'='*80}")
    mejor_ruta = resultados[mejor_idx]['ruta']
    evaluar_ruta_con_ventanas(mejor_ruta, matriz_tiempos, verbose=True)
    
    print(f"\n{'#'*80}")
    print(f"# DEMO COMPLETADA")
    print(f"# Resultados en carpeta 'resultados_demo/'")
    print(f"{'#'*80}\n")
