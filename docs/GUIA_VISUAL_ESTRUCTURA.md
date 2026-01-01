# 🗂️ GUÍA VISUAL DE ESTRUCTURA Y FLUJO DE TRABAJO

## 📊 DIAGRAMA DE FLUJO DEL PROCESO

```
┌─────────────────────────────────────────────────────────────┐
│  PASO 1: OBTENER DATOS DEL PROFESOR                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Descargar RAR  │
        │ del profesor   │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Descomprimir   │
        │     RAR        │
        └────────┬───────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│  ARCHIVOS OBTENIDOS:                                       │
│  ✓ México_Ciudades.shp                                     │
│  ✓ México_Ciudades.dbf                                     │
│  ✓ México_Ciudades.shx                                     │
│  ✓ México_Ciudades.prj                                     │
│  ✓ México_Ciudades.sbn/sbx/xml (opcionales)              │
└────────────────┬───────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 2: CREAR ESTRUCTURA DE CARPETAS                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│  ProyectoFinal_TSP_TW/                                     │
│  ├── datos/          ← COPIAR shapefiles AQUÍ             │
│  ├── codigo/         ← COPIAR scripts AQUÍ                │
│  ├── resultados/     ← Se llenará automáticamente         │
│  └── documentacion/  ← PDFs y documentos                  │
└────────────────┬───────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 3: INSTALAR DEPENDENCIAS                             │
│  $ pip install geopandas numpy matplotlib pandas           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 4: EXTRAER COORDENADAS                               │
│  $ python extraer_coordenadas.py                           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Lee shapefile  │
        │ México_Ciudades│
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Extrae lat/lon │
        │ de cada ciudad │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Reorganiza con │
        │ CDMX en idx 0  │
        └────────┬───────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│  ARCHIVO GENERADO:                                         │
│  datos/coordenadas_capitales.json                         │
│                                                            │
│  {                                                         │
│    "0": {"nombre": "Ciudad de México", ...},              │
│    "1": {"nombre": "Aguascalientes", ...},                │
│    ...                                                     │
│  }                                                         │
└────────────────┬───────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 5: MODIFICAR CÓDIGO PRINCIPAL                        │
│  Reemplazar diccionario hardcoded con carga desde JSON    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 6: EJECUTAR DEMO                                     │
│  $ python demo_tsp_tw.py                                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Carga JSON     │
        │ coordenadas    │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Calcula matriz │
        │ de distancias  │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Convierte a    │
        │ tiempos (60km/h│
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Ejecuta HGA    │
        │ 3 veces        │
        └────────┬───────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│  ARCHIVOS GENERADOS EN resultados_demo/:                  │
│  ✓ convergencia_hga.png                                   │
│  ✓ mapa_mejor_ruta.png                                    │
│  ✓ analisis_estadistico.png                               │
│  ✓ resultados.csv                                         │
└────────────────┬───────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ ¿Funciona?     │
        └────────┬───────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
      [SÍ]              [NO]
        │                 │
        │                 └──► Revisar ESTRUCTURA_PROYECTO.md
        │                      y solución de problemas
        ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 7: EJECUTAR VERSIÓN COMPLETA                         │
│  $ python TSP_TW_Mexico_HGA.py                             │
│  (10 ejecuciones, 1000 generaciones, ~30 min)             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│  RESULTADOS FINALES EN resultados/:                       │
│  ✓ 10 ejecuciones completas                               │
│  ✓ Análisis estadístico                                   │
│  ✓ Mejor ruta encontrada                                  │
│  ✓ Todas las visualizaciones                              │
└────────────────┬───────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 8: CREAR INFORME LATEX                               │
│  Usar resultados y gráficas generadas                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 9: PREPARAR PRESENTACIÓN                             │
│  Slides con mapa, convergencia, análisis                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ ¡PROYECTO      │
        │  COMPLETO!     │
        └────────────────┘
```

## 📁 ESTRUCTURA DE CARPETAS DETALLADA

```
ProyectoFinal_TSP_TW/
│
├── 📁 datos/
│   │
│   ├── 📄 México_Ciudades.shp           ← [COPIAR del RAR]
│   ├── 📄 México_Ciudades.dbf           ← [COPIAR del RAR]
│   ├── 📄 México_Ciudades.shx           ← [COPIAR del RAR]
│   ├── 📄 México_Ciudades.prj           ← [COPIAR del RAR]
│   ├── 📄 México_Ciudades.sbn           ← [COPIAR del RAR] (opcional)
│   ├── 📄 México_Ciudades.sbx           ← [COPIAR del RAR] (opcional)
│   ├── 📄 México_Ciudades.shp.xml       ← [COPIAR del RAR] (opcional)
│   │
│   ├── 📄 México_Estados.shp            ← [COPIAR del RAR] (opcional)
│   ├── 📄 México_Estados.dbf            ← [COPIAR del RAR] (opcional)
│   ├── 📄 México_Estados.shx            ← [COPIAR del RAR] (opcional)
│   ├── 📄 México_Estados.prj            ← [COPIAR del RAR] (opcional)
│   │
│   └── 📄 coordenadas_capitales.json    ← [AUTO-GENERADO]
│       └─► Creado por extraer_coordenadas.py
│
├── 📁 codigo/
│   │
│   ├── 📄 extraer_coordenadas.py        ← [DESCARGAR de outputs]
│   │   └─► Lee shapefile → Genera JSON
│   │
│   ├── 📄 TSP_TW_Mexico_HGA.py          ← [DESCARGAR y MODIFICAR]
│   │   └─► Programa principal completo
│   │
│   └── 📄 demo_tsp_tw.py                ← [DESCARGAR de outputs]
│       └─► Versión rápida de prueba
│
├── 📁 resultados/
│   │
│   ├── 📊 convergencia_hga.png          ← [AUTO-GENERADO]
│   ├── 🗺️  mapa_mejor_ruta.png          ← [AUTO-GENERADO]
│   ├── 📈 analisis_estadistico.png      ← [AUTO-GENERADO]
│   ├── 📄 resultados_experimentos.csv   ← [AUTO-GENERADO]
│   │
│   └── 📄 mejor_ruta_detalle.txt        ← [AUTO-GENERADO]
│       └─► Evaluación paso a paso
│
├── 📁 documentacion/
│   │
│   ├── 📄 README.md                     ← [DESCARGAR de outputs]
│   ├── 📄 ESTRUCTURA_PROYECTO.md        ← [DESCARGAR de outputs]
│   ├── 📄 MODIFICACIONES_CODIGO.txt     ← [DESCARGAR de outputs]
│   │
│   ├── 📁 propuesta/
│   │   └── 📄 Propuesta_Proyecto_Final.pdf
│   │
│   └── 📁 referencias/
│       ├── 📄 Clase_1418_HGA.pdf
│       ├── 📄 Clase_8_Cruzamientos.pdf
│       └── 📄 otros_PDFs_curso.pdf
│
└── 📁 presentacion/
    │
    ├── 📄 slides.pptx
    ├── 📄 poster.pdf
    │
    └── 📁 imagenes/
        ├── mapa_ruta.png
        ├── convergencia.png
        └── analisis.png
```

## 🔄 FLUJO DE ARCHIVOS

```
┌──────────────────┐
│   RAR PROFESOR   │
└────────┬─────────┘
         │ [DESCOMPRIMIR]
         ▼
┌──────────────────┐
│  Shapefiles SHP  │
│  + archivos .dbf │
│  + archivos .shx │
│  + archivos .prj │
└────────┬─────────┘
         │ [COPIAR]
         ▼
┌──────────────────┐
│  datos/          │
│  México_Ciudades │
└────────┬─────────┘
         │ [EJECUTAR extraer_coordenadas.py]
         ▼
┌──────────────────┐
│ coordenadas_     │
│ capitales.json   │
└────────┬─────────┘
         │ [CARGAR EN código principal]
         ▼
┌──────────────────┐
│ TSP_TW_Mexico_   │
│ HGA.py           │
└────────┬─────────┘
         │ [EJECUTAR]
         ▼
┌──────────────────┐
│  resultados/     │
│  ├── PNG         │
│  └── CSV         │
└────────┬─────────┘
         │ [USAR PARA]
         ▼
┌──────────────────┐
│  Informe LaTeX + │
│  Presentación    │
└──────────────────┘
```

## ⚙️ COMANDOS EN ORDEN

```bash
# 1. Crear estructura
mkdir -p ProyectoFinal_TSP_TW/{datos,codigo,resultados,documentacion,presentacion}

# 2. Copiar shapefiles
cp ruta/al/RAR/extraido/México_Ciudades.* ProyectoFinal_TSP_TW/datos/

# 3. Copiar código descargado
cp TSP_TW_Mexico_HGA.py demo_tsp_tw.py extraer_coordenadas.py ProyectoFinal_TSP_TW/codigo/
cp README.md ESTRUCTURA_PROYECTO.md ProyectoFinal_TSP_TW/documentacion/

# 4. Instalar dependencias
pip install geopandas numpy matplotlib pandas

# 5. Ir a carpeta de código
cd ProyectoFinal_TSP_TW/codigo/

# 6. Extraer coordenadas
python extraer_coordenadas.py

# 7. Verificar JSON
cat ../datos/coordenadas_capitales.json | head -30

# 8. Modificar TSP_TW_Mexico_HGA.py
# (seguir instrucciones en MODIFICACIONES_CODIGO.txt)

# 9. Ejecutar demo
python demo_tsp_tw.py

# 10. Si funciona, ejecutar versión completa
python TSP_TW_Mexico_HGA.py

# 11. Revisar resultados
ls -lh ../resultados/
```

## 🎯 CHECKLIST DE VERIFICACIÓN

### Antes de ejecutar:
- [ ] Carpeta `datos/` existe
- [ ] México_Ciudades.shp está en datos/
- [ ] México_Ciudades.dbf está en datos/
- [ ] México_Ciudades.shx está en datos/
- [ ] México_Ciudades.prj está en datos/
- [ ] Instalaste geopandas: `pip list | grep geopandas`
- [ ] Carpeta `codigo/` tiene los 3 scripts Python

### Después de extraer_coordenadas.py:
- [ ] Archivo coordenadas_capitales.json existe en datos/
- [ ] JSON tiene 32 ciudades
- [ ] Índice 0 es CDMX
- [ ] Coordenadas tienen formato correcto (lat, lon)

### Después de modificar código:
- [ ] TSP_TW_Mexico_HGA.py carga desde JSON
- [ ] No hay errores de sintaxis
- [ ] Importa correctamente: `import json`

### Después de ejecutar:
- [ ] Carpeta resultados/ tiene PNG
- [ ] Carpeta resultados/ tiene CSV
- [ ] Gráficas se ven correctamente
- [ ] Mapa muestra la ruta

## ❓ ¿ALGO NO FUNCIONA?

```
¿Error al leer shapefile?
└─► Verifica que TODOS los archivos (.shp, .dbf, .shx, .prj) estén juntos

¿No encuentra coordenadas_capitales.json?
└─► Ejecutaste extraer_coordenadas.py primero?

¿Geopandas no instala?
└─► Prueba: conda install geopandas
    O: pip install --upgrade pip
       pip install geopandas

¿CDMX no es índice 0?
└─► El script lo reorganiza automáticamente
    Si falla, verifica el nombre en shapefile

¿Coordenadas incorrectas?
└─► Verifica que el shapefile use WGS84 (EPSG:4326)
    El script muestra el CRS al cargar
```

---

¡Con esta estructura tendrás TODO perfectamente organizado! 🎯
