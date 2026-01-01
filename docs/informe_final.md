# Informe Final - Proyecto TSP-TW México

## Resolución del Problema del Agente Viajero con Ventanas de Tiempo para las Capitales de los Estados de México Usando Algoritmos Genéticos

**Autor:** [Tu Nombre]  
**Fecha:** 31 de Diciembre de 2024  
**Institución:** [Tu Institución]

---

## Resumen Ejecutivo

Este proyecto aborda la resolución del Problema del Agente Viajero con Ventanas de Tiempo (TSP-TW) para las 32 capitales de los estados de México, utilizando Algoritmos Genéticos. El objetivo es encontrar la ruta óptima que minimice el tiempo total de viaje, partiendo y regresando a la Ciudad de México, respetando restricciones de horario (9:00-21:00) y una velocidad constante de 60 km/h.

**Resultados principales:**
- Mejor solución encontrada: **247.53 horas** (10.31 días)
- Distancia total: 14,263 km
- Cumplimiento perfecto de ventanas de tiempo (0 penalizaciones)
- Mejora de 1.6% respecto a configuración inicial

---

## 1. Introducción

### 1.1 Contexto del Problema

El Problema del Agente Viajero (TSP) es un problema clásico de optimización combinatoria NP-difícil. La variante con Ventanas de Tiempo (TSP-TW) añade restricciones temporales que hacen el problema aún más complejo y realista.

### 1.2 Objetivos del Proyecto

**Objetivo General:**
Resolver el TSP-TW para las capitales de los 32 estados de México utilizando Algoritmos Genéticos.

**Objetivos Específicos:**
1. Formular matemáticamente el TSP-TW para el caso de estudio
2. Extraer y procesar datos geográficos de las capitales mexicanas
3. Implementar un Algoritmo Genético con representación por permutaciones
4. Evaluar y comparar resultados mediante múltiples ejecuciones
5. Analizar la calidad de las soluciones encontradas

---

## 2. Metodología

### 2.1 Obtención y Procesamiento de Datos

**Fuente de datos:**
- Shapefiles geo-referenciados de México
- Total: 32 capitales procesadas (incluyendo CDMX)

**Procesamiento:**
1. Carga de shapefiles usando GeoPandas
2. Filtrado de capitales estatales
3. Cálculo de distancias geodésicas
4. Conversión a tiempos: tiempo = distancia / 60 km/h

### 2.2 Implementación del Algoritmo Genético

**Configuración optimizada:**
- Población: 200 individuos
- Generaciones: 1000
- Tasa de mutación: 0.05
- Tasa de cruce: 0.85
- Elitismo: 15%

**Operadores genéticos:**
- Selección: Torneo de tamaño 5
- Cruce: Order Crossover (OX)
- Mutación: Swap, Inversion, Scramble
- Preservación de CDMX como punto de inicio

---

## 3. Resultados

### 3.1 Mejor Solución Encontrada

**Tiempo total:** 247.53 horas (10.31 días)  
**Distancia total:** 14,263 km  
**Penalizaciones:** 0 horas  
**Eficiencia:** 96% (tiempo viaje / tiempo total)

### 3.2 Estadísticas (5 Runs Optimizados)

| Métrica | Valor |
|---------|-------|
| Mejor | 247.53 horas |
| Media | 257.85 horas |
| Peor | 264.00 horas |
| Desv. Std | 7.57 horas |

**Mejora:** 1.6% respecto a configuración inicial (251.51h → 247.53h)

---

## 4. Conclusiones

1. **Implementación exitosa:** Sistema completo para TSP-TW cumpliendo todos los requisitos

2. **Resultados satisfactorios:** Solución de 247.53 horas con cumplimiento perfecto de ventanas de tiempo

3. **Comprensión del problema:** El algoritmo optimiza tiempo total, no solo distancia

4. **Efectividad del AG:** Convergencia exitosa con mejora iterativa demostrada

---

**Ver documentación completa y código en el repositorio del proyecto**
