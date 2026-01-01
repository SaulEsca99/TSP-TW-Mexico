# PROYECTO FINAL: TSP CON VENTANAS DE TIEMPO - CAPITALES DE MÉXICO
## Algoritmo Genético Híbrido (HGA)

**Autor:** Escamilla Lazcano Saúl  
**Grupo:** 5BV1  
**Materia:** Algoritmos Bioinspirados  
**Institución:** ESCOM - Instituto Politécnico Nacional

---

## 📋 DESCRIPCIÓN DEL PROYECTO

Implementación del **Algoritmo Genético Híbrido (HGA)** para resolver el **Problema del Agente Viajero con Ventanas de Tiempo (TSP-TW)** para las 32 capitales de los estados de México.

### Características Principales:
- ✅ Representación por permutaciones
- ✅ Cycle Crossover (CX) según pseudocódigo del curso
- ✅ Heurística de Remoción de Abruptos
- ✅ Manejo de ventanas de tiempo (9:00 - 21:00)
- ✅ Cálculo de distancias reales con fórmula de Haversine
- ✅ Conversión a tiempos con velocidad de 60 km/h
- ✅ Penalización por violación de ventanas
- ✅ 10 ejecuciones independientes con análisis estadístico

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
├── TSP_TW_Mexico_HGA.py        # Programa principal completo
├── demo_tsp_tw.py              # Versión demo (rápida)
├── README.md                   # Este archivo
└── resultados_demo/            # Resultados de la demostración
    ├── convergencia_hga.png    # Gráfica de convergencia
    ├── mapa_mejor_ruta.png     # Mapa con la ruta óptima
    ├── analisis_estadistico.png # Boxplot y histograma
    └── resultados.csv          # Tabla de resultados
```

---

## 🚀 INSTALACIÓN Y USO

### Requisitos:
```bash
pip install numpy matplotlib pandas
```

### Ejecución Rápida (DEMO):
```bash
python3 demo_tsp_tw.py
```
- 3 ejecuciones
- 200 generaciones
- ~2-3 minutos

### Ejecución Completa (PROYECTO FINAL):
```bash
python3 TSP_TW_Mexico_HGA.py
```
- 10 ejecuciones
- 1000 generaciones
- ~20-30 minutos
- Resultados en carpeta `resultados/`

---

## 🎯 RESULTADOS DE LA DEMO

### Estadísticas (3 ejecuciones):
- **Mejor fitness:** 152.53 horas
- **Fitness promedio:** 160.03 horas
- **Desviación estándar:** 5.68 horas
- **Penalizaciones:** 0.00 (todas las rutas respetan ventanas)

### Mejor Ruta Encontrada:
```
CDMX → Cuernavaca → Chilpancingo → Colima → Tepic → 
Guadalajara → Aguascalientes → Zacatecas → Durango → 
Culiacán → La Paz → Mexicali → Hermosillo → Chihuahua → 
Saltillo → Monterrey → Ciudad Victoria → San Luis Potosí → 
Guanajuato → Querétaro → Morelia → Oaxaca → Tuxtla Gutiérrez → 
Villahermosa → Chetumal → Mérida → Campeche → Xalapa → 
Puebla → Tlaxcala → Pachuca → Toluca → CDMX
```

**Tiempo total:** 152.53 horas (≈ 6.4 días)

---

## 🔧 PARÁMETROS DEL ALGORITMO

### Parámetros Principales:
```python
tam_poblacion = 100          # Tamaño de la población
num_generaciones = 1000      # Número de generaciones
prob_mutacion = 0.1          # Probabilidad de mutación (10%)
m_remocion = 5              # Ciudades cercanas en remoción de abruptos
```

### Parámetros del Problema:
```python
VELOCIDAD_KMH = 60.0        # Velocidad de desplazamiento
HORA_APERTURA = 9.0         # Ventanas abren a las 9:00 AM
HORA_CIERRE = 21.0          # Ventanas cierran a las 9:00 PM
```

---

## 📊 INTERPRETACIÓN DE RESULTADOS

### 1. Gráfica de Convergencia
Muestra la evolución del mejor fitness en cada generación para todas las ejecuciones.
- **Eje X:** Generación
- **Eje Y:** Fitness (horas)
- Líneas muestran la convergencia hacia soluciones óptimas

### 2. Mapa de Ruta
Visualización geográfica de la mejor ruta encontrada:
- 🔴 Estrella roja: CDMX (inicio/fin)
- 🔵 Puntos azules: Capitales estatales
- ➡️ Flechas rojas: Secuencia del recorrido

### 3. Análisis Estadístico
- **Boxplot:** Distribución de fitness entre ejecuciones
- **Histograma:** Frecuencia de valores de fitness
- Línea roja punteada: Media

### 4. Tabla CSV
Contiene para cada ejecución:
- Número de ejecución
- Fitness total
- Tiempo de viaje
- Penalizaciones

---

## 🧮 ALGORITMO IMPLEMENTADO

### Pseudocódigo del HGA (según curso):

```
Paso 1: Inicializar población con permutaciones aleatorias

Paso 2: Aplicar Remoción de Abruptos a toda la población

Paso 3 (Ciclo Principal):
    Para cada pareja de padres:
        a) Seleccionar padres aleatoriamente
        b) Aplicar Cycle Crossover (CX)
        c) Evaluar descendiente
        d) Aplicar Remoción de Abruptos al descendiente

Paso 4: Selección familiar
    - Ordenar padres + descendiente por fitness
    - Los 2 mejores pasan a siguiente generación

Paso 5: Operador de mezcla
    - Con probabilidad pm, generar individuo aleatorio
    - Sustituir en población

Paso 6: Repetir Pasos 3-5 hasta completar generaciones
```

### Funciones Clave:

#### 1. **Cycle Crossover (CX)**
```python
def cycle_crossover(padre1, padre2):
    # Garantiza permutaciones válidas
    # Hereda características de ambos padres
    # Sin repeticiones ni ciudades faltantes
```

#### 2. **Remoción de Abruptos**
```python
def remocion_abruptos(ruta, matriz_tiempos, m=5):
    # Para cada ciudad:
    #   - Identificar m ciudades más cercanas (NEARLIST)
    #   - Probar reubicaciones antes/después de cada cercana
    #   - Mantener la que mejore el fitness
    # Itera hasta no encontrar mejoras
```

#### 3. **Evaluación con Ventanas**
```python
def evaluar_ruta_con_ventanas(ruta, matriz_tiempos):
    # Simula el recorrido ciudad por ciudad
    # Verifica llegadas vs ventanas de tiempo
    # Aplica esperas o penalizaciones
    # Retorna: fitness, tiempo_real, penalizaciones
```

---

## 📈 ANÁLISIS DE COMPLEJIDAD

### Complejidad Temporal:
- **Inicialización:** O(tam_poblacion × n_ciudades)
- **Remoción de Abruptos:** O(n_ciudades² × m)
- **Por generación:** O(tam_poblacion × n_ciudades²)
- **Total:** O(num_generaciones × tam_poblacion × n_ciudades²)

Con los parámetros por defecto:
- O(1000 × 100 × 32²) ≈ O(10⁸) operaciones

### Espacio:
- **Población:** O(tam_poblacion × n_ciudades)
- **Matrices:** O(n_ciudades²)
- **Total:** O(100 × 32 + 32²) ≈ O(4,224)

---

## 🎓 FUNDAMENTO TEÓRICO

### Problema del Agente Viajero con Ventanas de Tiempo (TSP-TW)

**Definición Formal:**
Dado un conjunto de n ciudades y una matriz de tiempos t[i,j]:
- Minimizar: Σ t[i,j] + penalizaciones
- Sujeto a:
  - Visitar cada ciudad exactamente una vez
  - Inicio y fin en CDMX (ciudad 0)
  - Llegada a ciudad i dentro de [hora_apertura, hora_cierre]

**Variante implementada:**
- Si llega antes de apertura: espera (sin penalización)
- Si llega después de cierre: penalización fuerte (1000 × exceso)

### Ventajas del HGA sobre AG Clásico:
1. **Representación especializada:** Permutaciones vs binario
2. **Operadores específicos:** CX mantiene validez de rutas
3. **Búsqueda local:** Remoción de abruptos mejora explotación
4. **Híbrido:** Combina exploración global (AG) + local (heurística)

---

## 🔬 POSIBLES MEJORAS Y EXTENSIONES

### Mejoras al Algoritmo:
1. **Selección de padres:** Implementar torneo o ruleta
2. **Operadores adicionales:** PMX, OX, inversion mutation
3. **Búsqueda local:** 2-opt, 3-opt, Lin-Kernighan
4. **Paralelización:** Ejecutar múltiples poblaciones en paralelo
5. **Auto-ajuste:** Parámetros adaptativos

### Extensiones del Problema:
1. **Ventanas asimétricas:** Diferentes horarios por ciudad
2. **Múltiples vehículos:** Vehicle Routing Problem (VRP)
3. **Capacidades:** Considerar capacidad de carga
4. **Restricciones adicionales:** Prioridades, dependencias

---

## 📚 REFERENCIAS

1. Jayalakshmi, G. A., Sathiamoorthy, S., & Rajaram, R. (2001). 
   *A hybrid genetic algorithm—a new approach to solve traveling salesman problem.* 
   International Journal of Computational Engineering Science, 2(02), 339-355.

2. Potvin, J. Y. (1996). 
   *Genetic algorithms for the traveling salesman problem.* 
   Annals of Operations Research, 63, 337-370.

3. Clase 14-18: Algoritmo genético híbrido. 
   *Tópicos Selectos de Algoritmos Bioinspirados - ESCOM IPN*

---

## 📞 CONTACTO

**Escamilla Lazcano Saúl**  
Grupo 5BV1  
ESCOM - Instituto Politécnico Nacional  
Materia: Algoritmos Bioinspirados

---

## 📝 NOTAS PARA EL INFORME LATEX

### Secciones Sugeridas:

1. **Introducción**
   - Contexto del TSP-TW
   - Relevancia práctica
   - Objetivos del proyecto

2. **Marco Teórico**
   - Definición formal del TSP-TW
   - Algoritmos genéticos
   - Representación por permutaciones
   - Cycle Crossover
   - Heurística de Remoción de Abruptos

3. **Metodología**
   - Obtención de coordenadas
   - Cálculo de distancias (Haversine)
   - Conversión a tiempos
   - Manejo de ventanas
   - Implementación del HGA

4. **Experimentación**
   - Protocolo de 10 ejecuciones
   - Parámetros utilizados
   - Hardware/Software

5. **Resultados**
   - Tabla de resultados
   - Gráficas de convergencia
   - Mapa de mejor ruta
   - Análisis estadístico

6. **Discusión**
   - Calidad de soluciones
   - Impacto de ventanas de tiempo
   - Comparación con solución trivial/greedy
   - Fortalezas y debilidades del HGA

7. **Conclusiones**
   - Logros alcanzados
   - Aprendizajes
   - Trabajo futuro

---

## ✅ CHECKLIST PARA ENTREGA

- [ ] Código fuente completo y comentado
- [ ] 10 ejecuciones independientes realizadas
- [ ] Tabla de resultados (CSV)
- [ ] Gráficas de convergencia
- [ ] Mapa de la mejor ruta
- [ ] Análisis estadístico
- [ ] Informe en LaTeX
- [ ] Presentación para jurado
- [ ] Evaluación detallada de mejor ruta

---

**¡Éxito en el proyecto final! 🚀**
