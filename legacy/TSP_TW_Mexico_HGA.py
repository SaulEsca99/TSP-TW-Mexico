"""
================================================================================
PROBLEMA DEL AGENTE VIAJERO CON VENTANAS DE TIEMPO (TSP-TW)
Capitales de los Estados de México

Algoritmo Genético Híbrido (HGA)
- Representación por permutaciones
- Cycle Crossover (CX)
- Heurística de Remoción de Abruptos

Autor: Escamilla Lazcano Saúl
Grupo: 5BV1
Instituto Politécnico Nacional - ESCOM
Materia: Algoritmos Bioinspirados
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd
from datetime import datetime, timedelta
import os

# ============================================================================
# DATOS DE LAS 32 CAPITALES DE MÉXICO
# ============================================================================

# Coordenadas geográficas (lat, lon) de las 32 capitales estatales
CAPITALES_MEXICO = {
    0: {'nombre': 'Ciudad de México', 'estado': 'CDMX', 'lat': 19.4326, 'lon': -99.1332},
    1: {'nombre': 'Aguascalientes', 'estado': 'Aguascalientes', 'lat': 21.8853, 'lon': -102.2916},
    2: {'nombre': 'Mexicali', 'estado': 'Baja California', 'lat': 32.6245, 'lon': -115.4523},
    3: {'nombre': 'La Paz', 'estado': 'Baja California Sur', 'lat': 24.1426, 'lon': -110.3128},
    4: {'nombre': 'Campeche', 'estado': 'Campeche', 'lat': 19.8301, 'lon': -90.5349},
    5: {'nombre': 'Tuxtla Gutiérrez', 'estado': 'Chiapas', 'lat': 16.7516, 'lon': -93.1029},
    6: {'nombre': 'Chihuahua', 'estado': 'Chihuahua', 'lat': 28.6353, 'lon': -106.0889},
    7: {'nombre': 'Saltillo', 'estado': 'Coahuila', 'lat': 25.4260, 'lon': -100.9737},
    8: {'nombre': 'Colima', 'estado': 'Colima', 'lat': 19.2452, 'lon': -103.7241},
    9: {'nombre': 'Durango', 'estado': 'Durango', 'lat': 24.0277, 'lon': -104.6532},
    10: {'nombre': 'Guanajuato', 'estado': 'Guanajuato', 'lat': 21.0190, 'lon': -101.2574},
    11: {'nombre': 'Chilpancingo', 'estado': 'Guerrero', 'lat': 17.5506, 'lon': -99.5005},
    12: {'nombre': 'Pachuca', 'estado': 'Hidalgo', 'lat': 20.1011, 'lon': -98.7591},
    13: {'nombre': 'Guadalajara', 'estado': 'Jalisco', 'lat': 20.6597, 'lon': -103.3496},
    14: {'nombre': 'Toluca', 'estado': 'México', 'lat': 19.2827, 'lon': -99.6557},
    15: {'nombre': 'Morelia', 'estado': 'Michoacán', 'lat': 19.7060, 'lon': -101.1949},
    16: {'nombre': 'Cuernavaca', 'estado': 'Morelos', 'lat': 18.9211, 'lon': -99.2344},
    17: {'nombre': 'Tepic', 'estado': 'Nayarit', 'lat': 21.5041, 'lon': -104.8942},
    18: {'nombre': 'Monterrey', 'estado': 'Nuevo León', 'lat': 25.6866, 'lon': -100.3161},
    19: {'nombre': 'Oaxaca', 'estado': 'Oaxaca', 'lat': 17.0732, 'lon': -96.7266},
    20: {'nombre': 'Puebla', 'estado': 'Puebla', 'lat': 19.0414, 'lon': -98.2063},
    21: {'nombre': 'Querétaro', 'estado': 'Querétaro', 'lat': 20.5888, 'lon': -100.3899},
    22: {'nombre': 'Chetumal', 'estado': 'Quintana Roo', 'lat': 18.5001, 'lon': -88.2960},
    23: {'nombre': 'San Luis Potosí', 'estado': 'San Luis Potosí', 'lat': 22.1565, 'lon': -100.9855},
    24: {'nombre': 'Culiacán', 'estado': 'Sinaloa', 'lat': 24.8091, 'lon': -107.3940},
    25: {'nombre': 'Hermosillo', 'estado': 'Sonora', 'lat': 29.0729, 'lon': -110.9559},
    26: {'nombre': 'Villahermosa', 'estado': 'Tabasco', 'lat': 17.9892, 'lon': -92.9475},
    27: {'nombre': 'Ciudad Victoria', 'estado': 'Tamaulipas', 'lat': 23.7369, 'lon': -99.1411},
    28: {'nombre': 'Tlaxcala', 'estado': 'Tlaxcala', 'lat': 19.3139, 'lon': -98.2404},
    29: {'nombre': 'Xalapa', 'estado': 'Veracruz', 'lat': 19.5438, 'lon': -96.9102},
    30: {'nombre': 'Mérida', 'estado': 'Yucatán', 'lat': 20.9674, 'lon': -89.5926},
    31: {'nombre': 'Zacatecas', 'estado': 'Zacatecas', 'lat': 22.7709, 'lon': -102.5832}
}

N_CIUDADES = len(CAPITALES_MEXICO)
VELOCIDAD_KMH = 60.0  # Velocidad de desplazamiento en km/h
HORA_APERTURA = 9.0   # 9:00 AM
HORA_CIERRE = 21.0    # 9:00 PM
HORA_INICIO = 9.0     # Salida de CDMX a las 9:00 AM

# ============================================================================
# FUNCIÓN 1: CÁLCULO DE DISTANCIAS (HAVERSINE)
# ============================================================================

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos en la Tierra usando la fórmula de Haversine.
    
    Parámetros:
        lat1, lon1: Latitud y longitud del punto 1 (grados)
        lat2, lon2: Latitud y longitud del punto 2 (grados)
    
    Retorna:
        Distancia en kilómetros
    """
    R = 6371.0  # Radio de la Tierra en kilómetros
    
    # Convertir grados a radianes
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    # Diferencias
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Fórmula de Haversine
    a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distancia = R * c
    
    return distancia

def crear_matriz_distancias():
    """
    Crea la matriz de distancias entre todas las capitales.
    
    Retorna:
        matriz_distancias: Matriz NxN con distancias en km
        matriz_tiempos: Matriz NxN con tiempos en horas
    """
    n = N_CIUDADES
    matriz_distancias = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                dist = haversine(
                    CAPITALES_MEXICO[i]['lat'], CAPITALES_MEXICO[i]['lon'],
                    CAPITALES_MEXICO[j]['lat'], CAPITALES_MEXICO[j]['lon']
                )
                matriz_distancias[i, j] = dist
    
    # Convertir a matriz de tiempos (horas)
    matriz_tiempos = matriz_distancias / VELOCIDAD_KMH
    
    return matriz_distancias, matriz_tiempos

# ============================================================================
# FUNCIÓN 2: EVALUACIÓN DE RUTA CON VENTANAS DE TIEMPO
# ============================================================================

def evaluar_ruta_con_ventanas(ruta, matriz_tiempos, verbose=False):
    """
    Evalúa una ruta considerando ventanas de tiempo.
    
    Parámetros:
        ruta: Lista de ciudades a visitar (sin incluir CDMX al inicio/fin)
        matriz_tiempos: Matriz de tiempos entre ciudades
        verbose: Si True, imprime detalles del recorrido
    
    Retorna:
        fitness: Valor de aptitud (tiempo total + penalizaciones)
        tiempo_total: Tiempo real de viaje
        penalizacion_total: Suma de penalizaciones
    """
    # Ruta completa: CDMX -> ciudades -> CDMX
    ruta_completa = [0] + list(ruta) + [0]
    
    tiempo_total = 0.0
    penalizacion_total = 0.0
    hora_actual = HORA_INICIO
    dia_actual = 0
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"EVALUACIÓN DE RUTA")
        print(f"{'='*80}")
        print(f"Ruta: {[CAPITALES_MEXICO[c]['nombre'] for c in ruta_completa]}")
        print(f"\n{'Desde':<20} {'Hasta':<20} {'Tiempo':<10} {'Llega':<15} {'Estado':<20}")
        print(f"{'-'*80}")
    
    for i in range(len(ruta_completa) - 1):
        ciudad_desde = ruta_completa[i]
        ciudad_hasta = ruta_completa[i + 1]
        
        # Tiempo de viaje
        tiempo_viaje = matriz_tiempos[ciudad_desde, ciudad_hasta]
        tiempo_total += tiempo_viaje
        
        # Calcular hora de llegada
        hora_llegada = hora_actual + tiempo_viaje
        
        # Manejo de cambio de día
        while hora_llegada >= 24.0:
            hora_llegada -= 24.0
            dia_actual += 1
        
        estado_ventana = ""
        
        # Verificar ventana de tiempo (solo para ciudades diferentes de CDMX)
        if ciudad_hasta != 0:  # No aplicar ventanas a CDMX
            if hora_llegada < HORA_APERTURA:
                # Llega antes de que abra: ESPERA
                tiempo_espera = HORA_APERTURA - hora_llegada
                hora_actual = HORA_APERTURA
                estado_ventana = f"ESPERA {tiempo_espera:.2f}h"
                
            elif hora_llegada > HORA_CIERRE:
                # Llega después de cerrar: PENALIZACIÓN FUERTE
                exceso = hora_llegada - HORA_CIERRE
                penalizacion = 1000.0 * exceso  # Penalización muy fuerte
                penalizacion_total += penalizacion
                
                # Debe esperar al siguiente día
                hora_actual = HORA_APERTURA
                dia_actual += 1
                estado_ventana = f"CERRADO! +{exceso:.2f}h (Penalización: {penalizacion:.0f})"
                
            else:
                # Llega dentro de la ventana
                hora_actual = hora_llegada
                estado_ventana = "OK"
        else:
            # Regreso a CDMX, no hay restricción
            hora_actual = hora_llegada
            estado_ventana = "LLEGADA FINAL"
        
        if verbose:
            nombre_desde = CAPITALES_MEXICO[ciudad_desde]['nombre']
            nombre_hasta = CAPITALES_MEXICO[ciudad_hasta]['nombre']
            hora_str = f"Día {dia_actual}, {hora_llegada:.2f}h"
            print(f"{nombre_desde:<20} {nombre_hasta:<20} {tiempo_viaje:.2f}h    {hora_str:<15} {estado_ventana:<20}")
    
    # Fitness = tiempo total + penalizaciones
    fitness = tiempo_total + penalizacion_total
    
    if verbose:
        print(f"{'-'*80}")
        print(f"Tiempo total de viaje: {tiempo_total:.2f} horas")
        print(f"Penalizaciones totales: {penalizacion_total:.2f}")
        print(f"FITNESS TOTAL: {fitness:.2f}")
        print(f"{'='*80}\n")
    
    return fitness, tiempo_total, penalizacion_total

# ============================================================================
# FUNCIÓN 3: INICIALIZACIÓN DE POBLACIÓN
# ============================================================================

def inicializar_poblacion(tam_poblacion, n_ciudades):
    """
    Genera población inicial con permutaciones aleatorias.
    
    Parámetros:
        tam_poblacion: Número de individuos
        n_ciudades: Número total de ciudades (incluyendo CDMX)
    
    Retorna:
        poblacion: Lista de rutas (permutaciones)
    """
    poblacion = []
    # Ciudades a visitar (sin CDMX que es índice 0)
    ciudades = list(range(1, n_ciudades))
    
    for _ in range(tam_poblacion):
        ruta = ciudades.copy()
        np.random.shuffle(ruta)
        poblacion.append(ruta)
    
    return poblacion

# ============================================================================
# FUNCIÓN 4: CYCLE CROSSOVER (CX)
# ============================================================================

def cycle_crossover(padre1, padre2):
    """
    Operador Cycle Crossover según el pseudocódigo del curso.
    
    Parámetros:
        padre1, padre2: Listas con permutaciones
    
    Retorna:
        hijo: Nueva permutación resultado del cruce
    """
    n = len(padre1)
    hijo = [-1] * n
    visitado = [False] * n
    
    # Primer ciclo: copiar del padre1
    idx = 0
    while not visitado[idx]:
        hijo[idx] = padre1[idx]
        visitado[idx] = True
        # Buscar el valor en padre2 y encontrar su posición en padre1
        valor = padre2[idx]
        idx = padre1.index(valor)
    
    # Completar posiciones restantes con padre2
    for i in range(n):
        if hijo[i] == -1:
            hijo[i] = padre2[i]
    
    return hijo

# ============================================================================
# FUNCIÓN 5: HEURÍSTICA DE REMOCIÓN DE ABRUPTOS
# ============================================================================

def remocion_abruptos(ruta, matriz_tiempos, m=5, max_iteraciones=10):
    """
    Heurística de Remoción de Abruptos según el pseudocódigo del curso.
    
    Parámetros:
        ruta: Ruta a mejorar
        matriz_tiempos: Matriz de tiempos
        m: Número de ciudades más cercanas a considerar
        max_iteraciones: Máximo número de pasadas completas
    
    Retorna:
        mejor_ruta: Ruta mejorada
    """
    mejor_ruta = ruta.copy()
    mejor_fitness, _, _ = evaluar_ruta_con_ventanas(mejor_ruta, matriz_tiempos)
    
    iteracion = 0
    mejora = True
    
    while mejora and iteracion < max_iteraciones:
        mejora = False
        iteracion += 1
        
        # Para cada ciudad en la ruta
        for i in range(len(ruta)):
            ciudad_actual = ruta[i]
            
            # PASO 1: Crear NEARLIST con m ciudades más cercanas
            distancias = []
            for j, ciudad in enumerate(ruta):
                if j != i:
                    dist = matriz_tiempos[ciudad_actual, ciudad]
                    distancias.append((dist, j, ciudad))
            
            # Ordenar por distancia y tomar las m más cercanas
            distancias.sort(key=lambda x: x[0])
            nearlist = [ciudad for _, _, ciudad in distancias[:m]]
            
            # PASO 2: Sacar ciudad actual y probar inserciones
            ruta_temp = ruta.copy()
            ruta_temp.pop(i)
            
            # Probar insertar antes y después de cada ciudad en NEARLIST
            for ciudad_cercana in nearlist:
                if ciudad_cercana not in ruta_temp:
                    continue
                    
                idx = ruta_temp.index(ciudad_cercana)
                
                # Insertar ANTES
                ruta_prueba1 = ruta_temp.copy()
                ruta_prueba1.insert(idx, ciudad_actual)
                fitness1, _, _ = evaluar_ruta_con_ventanas(ruta_prueba1, matriz_tiempos)
                
                # Insertar DESPUÉS
                ruta_prueba2 = ruta_temp.copy()
                if idx + 1 <= len(ruta_temp):
                    ruta_prueba2.insert(idx + 1, ciudad_actual)
                    fitness2, _, _ = evaluar_ruta_con_ventanas(ruta_prueba2, matriz_tiempos)
                else:
                    fitness2 = float('inf')
                
                # PASO 4: Si mejora, actualizar
                if fitness1 < mejor_fitness:
                    mejor_ruta = ruta_prueba1
                    mejor_fitness = fitness1
                    mejora = True
                
                if fitness2 < mejor_fitness:
                    mejor_ruta = ruta_prueba2
                    mejor_fitness = fitness2
                    mejora = True
            
            # Si encontramos mejora, reiniciar con la nueva ruta
            if mejora:
                ruta = mejor_ruta.copy()
                break
    
    return mejor_ruta

# ============================================================================
# FUNCIÓN 6: ALGORITMO GENÉTICO HÍBRIDO (HGA)
# ============================================================================

def algoritmo_genetico_hibrido(matriz_tiempos, n_ciudades=32,
                                tam_poblacion=100, num_generaciones=1000,
                                prob_mutacion=0.1, m_remocion=5,
                                verbose=True):
    """
    Algoritmo Genético Híbrido según el pseudocódigo del curso.
    
    Parámetros:
        matriz_tiempos: Matriz de tiempos entre ciudades
        n_ciudades: Número total de ciudades
        tam_poblacion: Tamaño de la población
        num_generaciones: Número de generaciones
        prob_mutacion: Probabilidad de mutación/mezcla
        m_remocion: Parámetro m para remoción de abruptos
        verbose: Si True, muestra progreso
    
    Retorna:
        mejor_ruta_global: Mejor ruta encontrada
        mejor_fitness_global: Fitness de la mejor ruta
        historial: Lista con mejor fitness por generación
    """
    print(f"\n{'='*80}")
    print(f"INICIANDO ALGORITMO GENÉTICO HÍBRIDO")
    print(f"{'='*80}")
    print(f"Parámetros:")
    print(f"  - Tamaño población: {tam_poblacion}")
    print(f"  - Generaciones: {num_generaciones}")
    print(f"  - Prob. mutación: {prob_mutacion}")
    print(f"  - m (remoción): {m_remocion}")
    print(f"{'='*80}\n")
    
    # PASO 1: Inicializar población
    poblacion = inicializar_poblacion(tam_poblacion, n_ciudades)
    
    # Evaluar población inicial
    fitness = []
    for ind in poblacion:
        f, _, _ = evaluar_ruta_con_ventanas(ind, matriz_tiempos)
        fitness.append(f)
    
    # PASO 2: Aplicar Remoción de Abruptos a población inicial
    print("Aplicando Remoción de Abruptos a población inicial...")
    for i in range(tam_poblacion):
        poblacion[i] = remocion_abruptos(poblacion[i], matriz_tiempos, m_remocion)
        f, _, _ = evaluar_ruta_con_ventanas(poblacion[i], matriz_tiempos)
        fitness[i] = f
    
    # Registro de mejor solución
    mejor_idx = np.argmin(fitness)
    mejor_fitness_global = fitness[mejor_idx]
    mejor_ruta_global = poblacion[mejor_idx].copy()
    historial = [mejor_fitness_global]
    
    print(f"Fitness inicial (después de remoción): {mejor_fitness_global:.2f}\n")
    
    # CICLO PRINCIPAL (PASO 3-6)
    for gen in range(num_generaciones):
        
        # PASO 3: Selección, Cruce y Mejora
        for _ in range(tam_poblacion // 2):
            # Selección aleatoria de padres
            idx1, idx2 = np.random.choice(tam_poblacion, 2, replace=False)
            padre1 = poblacion[idx1]
            padre2 = poblacion[idx2]
            
            # Aplicar Cycle Crossover
            hijo = cycle_crossover(padre1, padre2)
            
            # Evaluar descendiente
            fitness_hijo, _, _ = evaluar_ruta_con_ventanas(hijo, matriz_tiempos)
            
            # Aplicar Remoción de Abruptos al descendiente
            hijo = remocion_abruptos(hijo, matriz_tiempos, m_remocion)
            fitness_hijo, _, _ = evaluar_ruta_con_ventanas(hijo, matriz_tiempos)
            
            # PASO 4: Selección familiar (los 2 mejores pasan)
            familia = [
                (padre1, fitness[idx1]),
                (padre2, fitness[idx2]),
                (hijo, fitness_hijo)
            ]
            familia.sort(key=lambda x: x[1])  # Ordenar por fitness (menor es mejor)
            
            # Los dos mejores reemplazan a los padres
            poblacion[idx1] = familia[0][0]
            poblacion[idx2] = familia[1][0]
            fitness[idx1] = familia[0][1]
            fitness[idx2] = familia[1][1]
        
        # PASO 5: Operador de mezcla (mutación)
        if np.random.rand() < prob_mutacion:
            idx_mutacion = np.random.randint(tam_poblacion)
            nuevo_individuo = list(range(1, n_ciudades))
            np.random.shuffle(nuevo_individuo)
            poblacion[idx_mutacion] = nuevo_individuo
            f, _, _ = evaluar_ruta_con_ventanas(nuevo_individuo, matriz_tiempos)
            fitness[idx_mutacion] = f
        
        # Actualizar mejor global
        mejor_idx = np.argmin(fitness)
        mejor_gen = fitness[mejor_idx]
        
        if mejor_gen < mejor_fitness_global:
            mejor_fitness_global = mejor_gen
            mejor_ruta_global = poblacion[mejor_idx].copy()
        
        historial.append(mejor_fitness_global)
        
        # Mostrar progreso
        if verbose and (gen % 50 == 0 or gen == num_generaciones - 1):
            print(f"Gen {gen:4d}: Mejor = {mejor_fitness_global:.2f} h | "
                  f"Prom = {np.mean(fitness):.2f} h | "
                  f"Peor = {np.max(fitness):.2f} h")
    
    print(f"\n{'='*80}")
    print(f"OPTIMIZACIÓN COMPLETADA")
    print(f"Mejor fitness encontrado: {mejor_fitness_global:.2f} horas")
    print(f"{'='*80}\n")
    
    return mejor_ruta_global, mejor_fitness_global, historial

# ============================================================================
# FUNCIÓN 7: EXPERIMENTACIÓN (10 EJECUCIONES)
# ============================================================================

def realizar_experimentos(matriz_tiempos, num_ejecuciones=10, 
                         tam_poblacion=100, num_generaciones=1000):
    """
    Realiza múltiples ejecuciones independientes del algoritmo.
    
    Retorna:
        resultados: Lista de diccionarios con resultados de cada ejecución
    """
    resultados = []
    
    for ejecucion in range(num_ejecuciones):
        print(f"\n{'#'*80}")
        print(f"# EJECUCIÓN {ejecucion + 1}/{num_ejecuciones}")
        print(f"{'#'*80}\n")
        
        # Semilla diferente para cada ejecución
        np.random.seed(ejecucion * 42)
        
        mejor_ruta, mejor_fitness, historial = algoritmo_genetico_hibrido(
            matriz_tiempos,
            n_ciudades=N_CIUDADES,
            tam_poblacion=tam_poblacion,
            num_generaciones=num_generaciones,
            prob_mutacion=0.1,
            m_remocion=5,
            verbose=True
        )
        
        # Calcular detalles de la mejor ruta
        fitness, tiempo_total, penalizacion = evaluar_ruta_con_ventanas(
            mejor_ruta, matriz_tiempos, verbose=False)
        
        resultados.append({
            'ejecucion': ejecucion + 1,
            'ruta': mejor_ruta,
            'fitness': fitness,
            'tiempo_viaje': tiempo_total,
            'penalizacion': penalizacion,
            'historial': historial
        })
    
    return resultados

# ============================================================================
# FUNCIÓN 8: ANÁLISIS ESTADÍSTICO
# ============================================================================

def analizar_resultados(resultados):
    """
    Analiza estadísticamente los resultados de las ejecuciones.
    """
    fitness_values = [r['fitness'] for r in resultados]
    tiempos = [r['tiempo_viaje'] for r in resultados]
    penalizaciones = [r['penalizacion'] for r in resultados]
    
    print(f"\n{'='*80}")
    print(f"ANÁLISIS ESTADÍSTICO ({len(resultados)} EJECUCIONES)")
    print(f"{'='*80}")
    print(f"\nFITNESS (Tiempo + Penalizaciones):")
    print(f"  Mejor valor:          {np.min(fitness_values):.4f} horas")
    print(f"  Peor valor:           {np.max(fitness_values):.4f} horas")
    print(f"  Valor medio:          {np.mean(fitness_values):.4f} horas")
    print(f"  Mediana:              {np.median(fitness_values):.4f} horas")
    print(f"  Desviación estándar:  {np.std(fitness_values):.4f} horas")
    
    print(f"\nTIEMPO DE VIAJE REAL:")
    print(f"  Mejor:                {np.min(tiempos):.4f} horas")
    print(f"  Promedio:             {np.mean(tiempos):.4f} horas")
    
    print(f"\nPENALIZACIONES:")
    print(f"  Mínima:               {np.min(penalizaciones):.4f}")
    print(f"  Máxima:               {np.max(penalizaciones):.4f}")
    print(f"  Promedio:             {np.mean(penalizaciones):.4f}")
    
    # Encontrar la mejor solución global
    mejor_idx = np.argmin(fitness_values)
    print(f"\n{'='*80}")
    print(f"MEJOR SOLUCIÓN ENCONTRADA (Ejecución #{mejor_idx + 1}):")
    print(f"{'='*80}")
    
    mejor_resultado = resultados[mejor_idx]
    print(f"Fitness total:        {mejor_resultado['fitness']:.4f} horas")
    print(f"Tiempo de viaje:      {mejor_resultado['tiempo_viaje']:.4f} horas")
    print(f"Penalización:         {mejor_resultado['penalizacion']:.4f}")
    
    print(f"\nRuta óptima:")
    ruta_completa = [0] + mejor_resultado['ruta'] + [0]
    for idx in ruta_completa:
        print(f"  -> {CAPITALES_MEXICO[idx]['nombre']} ({CAPITALES_MEXICO[idx]['estado']})")
    
    print(f"{'='*80}\n")
    
    # Crear DataFrame para exportar
    df_resultados = pd.DataFrame({
        'Ejecución': [r['ejecucion'] for r in resultados],
        'Fitness': [r['fitness'] for r in resultados],
        'Tiempo_Viaje': [r['tiempo_viaje'] for r in resultados],
        'Penalización': [r['penalizacion'] for r in resultados]
    })
    
    return df_resultados, mejor_idx

# ============================================================================
# FUNCIÓN 9: VISUALIZACIÓN
# ============================================================================

def visualizar_resultados(resultados, matriz_distancias, output_dir='resultados'):
    """
    Genera visualizaciones de los resultados.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. GRÁFICA DE CONVERGENCIA
    plt.figure(figsize=(14, 8))
    for i, resultado in enumerate(resultados):
        plt.plot(resultado['historial'], alpha=0.4, linewidth=1, 
                label=f"Ej {i+1}" if i < 3 else "")
    
    plt.xlabel('Generación', fontsize=12)
    plt.ylabel('Fitness (horas)', fontsize=12)
    plt.title('Convergencia del Algoritmo Genético Híbrido\nTSP-TW - Capitales de México', 
             fontsize=14, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/convergencia_hga.png', dpi=300, bbox_inches='tight')
    print(f"✓ Guardada: {output_dir}/convergencia_hga.png")
    
    # 2. MAPA DE LA MEJOR RUTA
    mejor_idx = np.argmin([r['fitness'] for r in resultados])
    mejor_ruta = resultados[mejor_idx]['ruta']
    mejor_fitness = resultados[mejor_idx]['fitness']
    
    ruta_completa = [0] + mejor_ruta + [0]
    
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Plot todas las ciudades
    lons = [CAPITALES_MEXICO[i]['lon'] for i in range(N_CIUDADES)]
    lats = [CAPITALES_MEXICO[i]['lat'] for i in range(N_CIUDADES)]
    
    # Ciudades normales
    ax.scatter(lons[1:], lats[1:], c='royalblue', s=100, zorder=3, 
              edgecolors='darkblue', linewidths=1.5, label='Capitales')
    
    # CDMX (inicio/fin)
    ax.scatter(lons[0], lats[0], c='red', s=300, zorder=4, marker='*', 
              edgecolors='darkred', linewidths=2, label='CDMX (inicio/fin)')
    
    # Plot la ruta
    for i in range(len(ruta_completa) - 1):
        c1_idx = ruta_completa[i]
        c2_idx = ruta_completa[i + 1]
        
        lon1 = CAPITALES_MEXICO[c1_idx]['lon']
        lat1 = CAPITALES_MEXICO[c1_idx]['lat']
        lon2 = CAPITALES_MEXICO[c2_idx]['lon']
        lat2 = CAPITALES_MEXICO[c2_idx]['lat']
        
        ax.plot([lon1, lon2], [lat1, lat2], 'r-', alpha=0.6, linewidth=2, zorder=2)
        
        # Agregar flechas
        mid_lon = (lon1 + lon2) / 2
        mid_lat = (lat1 + lat2) / 2
        dx = lon2 - lon1
        dy = lat2 - lat1
        ax.annotate('', xy=(mid_lon + dx*0.1, mid_lat + dy*0.1), 
                   xytext=(mid_lon, mid_lat),
                   arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                   zorder=2)
    
    # Etiquetas de ciudades
    for idx in range(N_CIUDADES):
        nombre = CAPITALES_MEXICO[idx]['nombre']
        lon = CAPITALES_MEXICO[idx]['lon']
        lat = CAPITALES_MEXICO[idx]['lat']
        
        # Offset para evitar superposición
        offset_x = 0.3
        offset_y = 0.2 if idx % 2 == 0 else -0.3
        
        ax.annotate(nombre, (lon, lat), xytext=(lon + offset_x, lat + offset_y),
                   fontsize=8, ha='left', 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.7))
    
    ax.set_xlabel('Longitud', fontsize=12)
    ax.set_ylabel('Latitud', fontsize=12)
    ax.set_title(f'Mejor Ruta TSP-TW - Capitales de México\n'
                f'Fitness: {mejor_fitness:.2f} horas | '
                f'Tiempo viaje: {resultados[mejor_idx]["tiempo_viaje"]:.2f} h | '
                f'Penalización: {resultados[mejor_idx]["penalizacion"]:.2f}',
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/mapa_mejor_ruta.png', dpi=300, bbox_inches='tight')
    print(f"✓ Guardada: {output_dir}/mapa_mejor_ruta.png")
    
    # 3. BOXPLOT DE RESULTADOS
    fitness_values = [r['fitness'] for r in resultados]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Boxplot de fitness
    axes[0].boxplot(fitness_values, vert=True)
    axes[0].set_ylabel('Fitness (horas)', fontsize=12)
    axes[0].set_title('Distribución de Fitness\n(10 ejecuciones)', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Histograma
    axes[1].hist(fitness_values, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
    axes[1].axvline(np.mean(fitness_values), color='red', linestyle='--', 
                   linewidth=2, label=f'Media: {np.mean(fitness_values):.2f}')
    axes[1].set_xlabel('Fitness (horas)', fontsize=12)
    axes[1].set_ylabel('Frecuencia', fontsize=12)
    axes[1].set_title('Histograma de Fitness', fontsize=12, fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/analisis_estadistico.png', dpi=300, bbox_inches='tight')
    print(f"✓ Guardada: {output_dir}/analisis_estadistico.png")
    
    plt.close('all')

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal del programa.
    """
    print(f"\n{'#'*80}")
    print(f"# PROBLEMA DEL AGENTE VIAJERO CON VENTANAS DE TIEMPO")
    print(f"# Capitales de los Estados de México")
    print(f"# Algoritmo Genético Híbrido (HGA)")
    print(f"#")
    print(f"# Autor: Escamilla Lazcano Saúl")
    print(f"# Grupo: 5BV1 - ESCOM - IPN")
    print(f"{'#'*80}\n")
    
    # Crear matrices de distancias y tiempos
    print("Calculando matriz de distancias entre capitales...")
    matriz_distancias, matriz_tiempos = crear_matriz_distancias()
    print(f"✓ Matriz creada: {N_CIUDADES}x{N_CIUDADES} ciudades")
    print(f"  Distancia máxima: {np.max(matriz_distancias):.2f} km")
    print(f"  Tiempo máximo: {np.max(matriz_tiempos):.2f} horas\n")
    
    # Realizar experimentos
    resultados = realizar_experimentos(
        matriz_tiempos,
        num_ejecuciones=10,
        tam_poblacion=100,
        num_generaciones=1000
    )
    
    # Analizar resultados
    df_resultados, mejor_idx = analizar_resultados(resultados)
    
    # Guardar resultados en CSV
    df_resultados.to_csv('resultados/resultados_experimentos.csv', index=False)
    print(f"✓ Guardado: resultados/resultados_experimentos.csv\n")
    
    # Visualizar resultados
    print("Generando visualizaciones...")
    visualizar_resultados(resultados, matriz_distancias)
    
    # Mostrar detalles de la mejor ruta
    print(f"\n{'='*80}")
    print("EVALUACIÓN DETALLADA DE LA MEJOR RUTA")
    print(f"{'='*80}")
    mejor_ruta = resultados[mejor_idx]['ruta']
    evaluar_ruta_con_ventanas(mejor_ruta, matriz_tiempos, verbose=True)
    
    print(f"\n{'#'*80}")
    print(f"# PROGRAMA FINALIZADO EXITOSAMENTE")
    print(f"# Todos los resultados guardados en la carpeta 'resultados/'")
    print(f"{'#'*80}\n")

if __name__ == "__main__":
    main()
