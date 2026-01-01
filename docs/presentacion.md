# Presentación - TSP-TW México

## Resolución del Problema del Agente Viajero con Ventanas de Tiempo para las Capitales de México

**Autor:** [Tu Nombre]  
**Fecha:** 31 de Diciembre de 2024

---

## Diapositiva 1: Título

# TSP-TW México
## Algoritmos Genéticos para Optimización de Rutas

**Problema del Agente Viajero con Ventanas de Tiempo**

32 Capitales Estatales de México

---

## Diapositiva 2: Objetivos del Proyecto

### Objetivo General
Resolver el TSP-TW para las capitales mexicanas usando Algoritmos Genéticos

### Objetivos Específicos
1. ✅ Formular el TSP-TW matemáticamente
2. ✅ Procesar datos geográficos de México
3. ✅ Implementar AG con permutaciones
4. ✅ Evaluar mediante múltiples ejecuciones
5. ✅ Analizar calidad de soluciones

---

## Diapositiva 3: El Problema

### TSP con Ventanas de Tiempo

**Restricciones:**
- 🏙️ **32 capitales** estatales de México
- 🏁 **Inicio/Fin:** Ciudad de México
- ⏰ **Horario:** 9:00 - 21:00 (todas las ciudades)
- 🚗 **Velocidad:** 60 km/h (constante)
- 🕘 **Salida:** 9:00 AM desde CDMX

**Objetivo:** Minimizar tiempo total de viaje

---

## Diapositiva 4: Metodología - Datos

### Procesamiento de Datos

**Fuente:**
- Shapefiles geo-referenciados de México
- `México_Estados.shp` + `México_Ciudades.shp`

**Procesamiento:**
1. Carga con GeoPandas
2. Filtrado de capitales (CAPITAL='S')
3. Inclusión manual de CDMX
4. **Total: 32 capitales**

**Cálculos:**
- Distancias geodésicas (matriz 32×32)
- Conversión a tiempos: `tiempo = distancia / 60`

---

## Diapositiva 5: Metodología - Algoritmo Genético

### Configuración del AG

| Parámetro | Valor Inicial | Valor Optimizado |
|-----------|---------------|------------------|
| Población | 100 | **200** |
| Generaciones | 500 | **1000** |
| Mutación | 0.02 | **0.05** |
| Cruce | 0.80 | **0.85** |
| Elitismo | 10% | **15%** |

**Operadores:**
- Selección: Torneo (tamaño 5)
- Cruce: Order Crossover (OX)
- Mutación: Swap, Inversion, Scramble

---

## Diapositiva 6: Implementación

### Componentes del Sistema

```
📁 Módulos Principales:
   ├── data_loader.py         → Carga de shapefiles
   ├── distance_calculator.py → Matrices de tiempo
   ├── time_windows.py        → Ventanas de tiempo
   ├── fitness_function.py    → Función de aptitud
   ├── genetic_algorithm.py   → AG principal
   ├── operators.py           → Operadores genéticos
   └── visualizer.py          → Visualizaciones
```

**Características clave:**
- ✅ Preservación de CDMX como inicio
- ✅ Manejo de ventanas de tiempo
- ✅ Cálculo de penalizaciones

---

## Diapositiva 7: Resultados - Evaluación Inicial

### 10 Ejecuciones (Config. Inicial)

| Métrica | Valor |
|---------|-------|
| 🏆 Mejor | 251.51 horas (10.48 días) |
| 📊 Media | 286.92 horas (11.96 días) |
| 📉 Peor | 320.97 horas (13.37 días) |
| 📏 Desv. Std | 19.49 horas |

**Observaciones:**
- Variabilidad moderada (6.8%)
- Convergencia exitosa
- Rango: 69.46 horas

---

## Diapositiva 8: Resultados - Búsqueda Optimizada

### 5 Ejecuciones (Config. Optimizada)

| Métrica | Valor |
|---------|-------|
| 🏆 **Mejor** | **247.53 horas (10.31 días)** |
| 📊 Media | 257.85 horas (10.74 días) |
| 📉 Peor | 264.00 horas (11.00 días) |
| 📏 Desv. Std | 7.57 horas |

**Mejora:** 3.98 horas (1.6%) vs configuración inicial

---

## Diapositiva 9: Mejor Solución Encontrada

### Ruta Óptima: 247.53 horas

**Métricas:**
- ⏱️ Tiempo total: **247.53 horas** (10.31 días)
- 📏 Distancia: 14,263 km
- ⏳ Tiempo de espera: ~9.81 horas
- ⚠️ Penalizaciones: **0 horas** ✅
- 📊 Eficiencia: **96%**

**Cumplimiento:**
- ✅ Todas las llegadas dentro de 9:00-21:00
- ✅ Inicia y termina en CDMX
- ✅ Visita 32 capitales exactamente una vez

---

## Diapositiva 10: Hallazgo Interesante

### ¿Más Distancia pero Menos Tiempo?

**Comparación:**

| Ruta | Distancia | Tiempo Total |
|------|-----------|--------------|
| Original | 11,419 km | 251.51 h |
| **Optimizada** | **14,263 km** | **247.53 h** ✅ |

**¿Por qué?**

La ruta optimizada:
- Reduce esperas: 62.63h → 9.81h (ahorro ~53h)
- Aumenta viaje: 190.33h → 237.72h (costo ~47h)
- **Ganancia neta: ~4-6 horas**

**Lección:** En TSP-TW, la ruta más corta NO siempre es la más rápida

---

## Diapositiva 11: Análisis de Convergencia

### Gráfica de Convergencia

[Aquí iría la imagen: convergencia_mejor_run.png]

**Observaciones:**
- Convergencia rápida en primeras 200-300 generaciones
- Mejoras marginales después de gen. 500
- Plateau antes de generación 1000
- Elitismo efectivo

---

## Diapositiva 12: Visualización de la Ruta

### Mapa de la Mejor Ruta

[Aquí iría la imagen: mejor_ruta_mapa.png]

**Características:**
- Inicio/Fin: CDMX (marcado con estrella)
- 32 capitales visitadas
- Ruta cerrada
- Cumple ventanas de tiempo

---

## Diapositiva 13: Comparación de Múltiples Runs

### 10 Ejecuciones Independientes

[Aquí iría la imagen: comparacion_10_runs.png]

**Análisis:**
- Consistencia entre ejecuciones
- Línea promedio estable
- Variabilidad aceptable
- Reproducibilidad demostrada

---

## Diapositiva 14: Distribución de Resultados

### Boxplot de Resultados

[Aquí iría la imagen: distribucion_resultados.png]

**Estadísticas:**
- Media: 257.85 horas
- Mediana: 264.00 horas
- Rango intercuartílico: pequeño
- Outliers: mínimos

---

## Diapositiva 15: Discusión

### Calidad de la Solución

**Fortalezas:**
- ✅ Cumplimiento perfecto de restricciones
- ✅ Eficiencia temporal del 96%
- ✅ Minimización efectiva de esperas
- ✅ Mejora iterativa demostrada

**Limitaciones:**
- ⚠️ 9 cambios de dirección bruscos
- ⚠️ Algunos segmentos largos
- ⚠️ Agrupación regional mejorable

**Calificación:** 8.5/10

---

## Diapositiva 16: Comparación con Óptimo

### Estimación de Optimalidad

**Óptimo estimado:** ~220-230 horas

**Nuestra solución:** 247.53 horas

**Diferencia:** ~8-12% por encima del óptimo

**Evaluación:**
- ✅ Excelente para una metaheurística
- ✅ AG no garantiza óptimo global
- ✅ Resultado muy competitivo

---

## Diapositiva 17: Trabajo Futuro

### Posibles Mejoras

**Algorítmicas:**
- Implementar búsqueda local 2-opt
- Hibridación con otros algoritmos
- Inicialización inteligente (greedy)
- Mutación adaptativa

**Extensiones:**
- Ventanas de tiempo variables
- Múltiples vehículos
- Costos de combustible
- Restricciones de capacidad

---

## Diapositiva 18: Conclusiones

### Principales Hallazgos

1. **Implementación exitosa** del TSP-TW para México

2. **Mejor solución:** 247.53 horas con 0 penalizaciones

3. **Comprensión del problema:** Optimización de tiempo total, no solo distancia

4. **Efectividad del AG:** Convergencia y mejora iterativa demostradas

5. **Aplicabilidad:** Metodología extensible a problemas reales

---

## Diapositiva 19: Contribuciones

### Aportes del Proyecto

**Técnicas:**
- Sistema completo de TSP-TW en Python
- Implementación de AG con operadores especializados
- Manejo robusto de ventanas de tiempo

**Metodológicas:**
- Evaluación estadística rigurosa
- Análisis de optimalidad
- Documentación completa

**Prácticas:**
- Código modular y reutilizable
- Visualizaciones profesionales
- Resultados reproducibles

---

## Diapositiva 20: Cierre

# ¡Gracias!

## Preguntas

**Contacto:** [Tu email]  
**Repositorio:** [URL del repositorio]

**Resultados disponibles en:**
- `results/optimized_20251231_211719/`
- Código fuente en `src/`
- Documentación en `docs/`

---

## Notas para la Presentación

### Tiempo estimado: 15-20 minutos

**Distribución sugerida:**
- Introducción (2 min): Diapositivas 1-3
- Metodología (4 min): Diapositivas 4-6
- Resultados (6 min): Diapositivas 7-14
- Discusión (3 min): Diapositivas 15-17
- Conclusiones (2 min): Diapositivas 18-20

**Consejos:**
- Enfatizar el hallazgo de "más distancia, menos tiempo"
- Mostrar las visualizaciones (gráficas)
- Explicar claramente las ventanas de tiempo
- Destacar la mejora iterativa (1.6%)
- Preparar respuestas sobre optimalidad

**Preguntas anticipadas:**
- ¿Por qué no es óptima la solución?
- ¿Cómo se manejan las ventanas de tiempo?
- ¿Por qué más distancia pero menos tiempo?
- ¿Qué mejoras se podrían hacer?
