# 📁 ESTRUCTURA DEL PROYECTO - GUÍA DE INSTALACIÓN

## 🎯 OBJETIVO
Configurar correctamente todos los archivos para que el proyecto funcione con TU dataset real del profesor.

---

## 📦 PASO 1: DESCOMPRIMIR TU DATASET

Según tus imágenes, tienes un archivo RAR. Descomprímelo:

```
📁 Tu carpeta descargada/
├── Ciudades_México_Efrain...s.rar          ← DESCOMPRIME ESTE
└── otros archivos...
```

Después de descomprimir tendrás algo como:

```
📁 datos_extraidos/
├── México_Ciudades.shp
├── México_Ciudades.dbf
├── México_Ciudades.prj
├── México_Ciudades.shx
├── México_Ciudades.sbn
├── México_Ciudades.sbx
├── México_Ciudades.shp.xml
├── México_Estados.shp
├── México_Estados.dbf
├── México_Estados.prj
├── México_Estados.shx
├── México_Estados.sbn
├── México_Estados.sbx
├── México_Estados.shp.xml
└── mexico_boundary/
    └── (archivos de límites)
```

---

## 📁 PASO 2: CREAR ESTRUCTURA DEL PROYECTO

Crea una carpeta para tu proyecto final con esta estructura EXACTA:

```
📁 ProyectoFinal_TSP_TW/
│
├── 📁 datos/                              ← CREA ESTA CARPETA
│   ├── México_Ciudades.shp               ← COPIA AQUÍ (del RAR)
│   ├── México_Ciudades.dbf               ← COPIA AQUÍ
│   ├── México_Ciudades.prj               ← COPIA AQUÍ
│   ├── México_Ciudades.shx               ← COPIA AQUÍ
│   ├── México_Ciudades.sbn               ← COPIA AQUÍ
│   ├── México_Ciudades.sbx               ← COPIA AQUÍ
│   ├── México_Ciudades.shp.xml           ← COPIA AQUÍ
│   ├── México_Estados.shp                ← COPIA AQUÍ (opcional)
│   ├── México_Estados.dbf                ← COPIA AQUÍ (opcional)
│   ├── México_Estados.prj                ← COPIA AQUÍ (opcional)
│   ├── México_Estados.shx                ← COPIA AQUÍ (opcional)
│   ├── México_Estados.sbn               ← COPIA AQUÍ (opcional)
│   ├── México_Estados.sbx               ← COPIA AQUÍ (opcional)
│   └── México_Estados.shp.xml           ← COPIA AQUÍ (opcional)
│
├── 📁 codigo/                            ← CREA ESTA CARPETA
│   ├── TSP_TW_Mexico_HGA.py             ← DESCARGA que te di
│   ├── demo_tsp_tw.py                   ← DESCARGA que te di
│   ├── extraer_coordenadas.py           ← NUEVO (te lo daré)
│   └── config.py                        ← NUEVO (te lo daré)
│
├── 📁 resultados/                        ← CREA ESTA CARPETA (vacía por ahora)
│
├── 📁 documentacion/                     ← CREA ESTA CARPETA
│   ├── README.md                        ← DESCARGA que te di
│   ├── Propuesta_de_Proyecto_Final_Agente_viajero.pdf
│   └── referencias/
│       ├── Clase_1418__Algoritmo_genético_híbrido.pdf
│       └── otros PDFs del curso...
│
└── 📁 presentacion/                      ← CREA ESTA CARPETA (para después)
    └── (slides, imágenes, etc.)
```

---

## 🔧 PASO 3: ARCHIVOS QUE DEBES COPIAR

### 3.1 Del RAR del profesor → carpeta `datos/`
Copia TODOS los archivos del shapefile de ciudades:
- ✅ México_Ciudades.shp (geometría)
- ✅ México_Ciudades.dbf (atributos - aquí están los nombres)
- ✅ México_Ciudades.prj (proyección)
- ✅ México_Ciudades.shx (índice)
- ✅ México_Ciudades.sbn (índice espacial)
- ✅ México_Ciudades.sbx (índice espacial)
- ✅ México_Ciudades.shp.xml (metadatos)

**IMPORTANTE:** Todos estos archivos deben tener el MISMO nombre base (México_Ciudades) 
pero diferentes extensiones. Son necesarios para que funcione el shapefile.

### 3.2 Archivos de código que te di → carpeta `codigo/`
- ✅ TSP_TW_Mexico_HGA.py
- ✅ demo_tsp_tw.py
- ✅ README.md

---

## 🐍 PASO 4: INSTALAR LIBRERÍAS NECESARIAS

Abre una terminal/CMD y ejecuta:

```bash
pip install numpy matplotlib pandas geopandas shapely
```

**Nota:** `geopandas` es la librería para leer shapefiles en Python.

---

## 📊 PASO 5: SCRIPT PARA EXTRAER COORDENADAS DEL SHAPEFILE

Voy a crear un script que LEE tu shapefile y extrae las coordenadas reales.

**Archivo:** `codigo/extraer_coordenadas.py`

```python
import geopandas as gpd
import json

def extraer_coordenadas_shapefile(ruta_shapefile):
    """
    Extrae coordenadas de las capitales desde el shapefile.
    
    Args:
        ruta_shapefile: Ruta al archivo .shp
    
    Returns:
        dict: Diccionario con coordenadas de cada capital
    """
    print(f"Leyendo shapefile: {ruta_shapefile}")
    
    # Leer shapefile
    gdf = gpd.read_file(ruta_shapefile)
    
    print(f"\nShapefile cargado exitosamente!")
    print(f"Número de ciudades: {len(gdf)}")
    print(f"\nColumnas disponibles: {list(gdf.columns)}")
    
    # Mostrar primeras filas para ver estructura
    print("\nPrimeras 5 ciudades:")
    print(gdf.head())
    
    # Extraer coordenadas
    capitales = {}
    
    for idx, row in gdf.iterrows():
        # Obtener geometría (punto)
        punto = row.geometry
        
        # AJUSTA ESTOS NOMBRES según las columnas de tu shapefile
        # Podrían ser: 'NOMBRE', 'Ciudad', 'CITY_NAME', etc.
        nombre = row.get('NOMBRE', row.get('Ciudad', row.get('NOM_ENT', f'Ciudad_{idx}')))
        estado = row.get('ESTADO', row.get('Estado', row.get('NOM_ENT', '')))
        
        capitales[idx] = {
            'nombre': str(nombre),
            'estado': str(estado),
            'lat': punto.y,  # Latitud
            'lon': punto.x   # Longitud
        }
    
    return capitales

if __name__ == "__main__":
    # Ruta al shapefile (ajusta según tu estructura)
    RUTA_SHAPEFILE = "../datos/México_Ciudades.shp"
    
    # Extraer coordenadas
    capitales = extraer_coordenadas_shapefile(RUTA_SHAPEFILE)
    
    # Guardar a JSON
    with open('../datos/coordenadas_capitales.json', 'w', encoding='utf-8') as f:
        json.dump(capitales, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Coordenadas extraídas y guardadas en: coordenadas_capitales.json")
    print(f"\nTotal de capitales: {len(capitales)}")
    
    # Mostrar algunas capitales
    print("\nEjemplo de coordenadas extraídas:")
    for i in range(min(5, len(capitales))):
        cap = capitales[i]
        print(f"  {i}: {cap['nombre']} ({cap['estado']}) - "
              f"Lat: {cap['lat']:.4f}, Lon: {cap['lon']:.4f}")
```

---

## 🔄 PASO 6: VERIFICAR QUE EL SHAPEFILE SE LEE CORRECTAMENTE

**Comando para ejecutar:**

```bash
cd ProyectoFinal_TSP_TW/codigo
python extraer_coordenadas.py
```

**Salida esperada:**

```
Leyendo shapefile: ../datos/México_Ciudades.shp

Shapefile cargado exitosamente!
Número de ciudades: 32

Columnas disponibles: ['NOMBRE', 'ESTADO', 'geometry', ...]

Primeras 5 ciudades:
         NOMBRE              ESTADO                    geometry
0  Ciudad de México           CDMX  POINT (-99.1332 19.4326)
1  Aguascalientes    Aguascalientes  POINT (-102.2916 21.8853)
...

✓ Coordenadas extraídas y guardadas en: coordenadas_capitales.json

Total de capitales: 32
```

---

## ⚙️ PASO 7: MODIFICAR EL CÓDIGO PRINCIPAL

Una vez que tengas `coordenadas_capitales.json`, modifica `TSP_TW_Mexico_HGA.py`:

**BUSCA esta sección (líneas 28-60):**

```python
CAPITALES_MEXICO = {
    0: {'nombre': 'Ciudad de México', 'estado': 'CDMX', 'lat': 19.4326, 'lon': -99.1332},
    1: {'nombre': 'Aguascalientes', ...},
    # ... etc
}
```

**REEMPLÁZALA con:**

```python
import json

# Cargar coordenadas desde el shapefile
with open('../datos/coordenadas_capitales.json', 'r', encoding='utf-8') as f:
    CAPITALES_MEXICO = json.load(f)
    # Convertir keys de string a int
    CAPITALES_MEXICO = {int(k): v for k, v in CAPITALES_MEXICO.items()}
```

---

## 🎯 PASO 8: EJECUTAR EL PROYECTO

```bash
cd ProyectoFinal_TSP_TW/codigo
python demo_tsp_tw.py
```

Si todo funciona, verás:

```
Calculando matriz de distancias...
✓ Matriz creada: 32x32 ciudades

INICIANDO ALGORITMO GENÉTICO HÍBRIDO
...
```

---

## 📝 PASO 9: CHECKLIST DE VERIFICACIÓN

Antes de ejecutar, verifica:

- [ ] Carpeta `datos/` existe
- [ ] Todos los archivos .shp, .dbf, .shx están en `datos/`
- [ ] Instalaste: `pip install geopandas numpy matplotlib pandas`
- [ ] Ejecutaste `extraer_coordenadas.py` exitosamente
- [ ] Existe el archivo `coordenadas_capitales.json` en `datos/`
- [ ] Modificaste `TSP_TW_Mexico_HGA.py` para cargar el JSON

---

## ❓ SOLUCIÓN DE PROBLEMAS COMUNES

### Problema 1: "No such file or directory: México_Ciudades.shp"
**Solución:** Verifica que la ruta sea correcta. Usa rutas absolutas si es necesario:
```python
RUTA_SHAPEFILE = "C:/Users/TuUsuario/ProyectoFinal_TSP_TW/datos/México_Ciudades.shp"
```

### Problema 2: "ModuleNotFoundError: No module named 'geopandas'"
**Solución:** 
```bash
pip install geopandas
# Si falla, prueba:
conda install geopandas
```

### Problema 3: El shapefile tiene diferentes nombres de columnas
**Solución:** Ejecuta primero el script de extracción para ver qué columnas tiene:
```python
print(gdf.columns)
```
Luego ajusta los nombres en la línea:
```python
nombre = row.get('NOMBRE_CORRECTO_AQUI', ...)
```

### Problema 4: Tienes más o menos de 32 ciudades
**Solución:** El código se adapta automáticamente al número de ciudades en el shapefile.
Solo asegúrate que CDMX sea el índice 0 (ciudad de inicio).

---

## 🎓 NOTAS IMPORTANTES

1. **CDMX debe ser índice 0:** Verifica que Ciudad de México sea la primera ciudad 
   en el shapefile o ajusta el código para que tenga índice 0.

2. **Orden de ciudades:** El orden en el shapefile determinará los índices. 
   Si el profesor te dio un orden específico, ordena el shapefile antes de extraer.

3. **Proyección:** El shapefile probablemente está en WGS84 (EPSG:4326). 
   Esto es correcto para Haversine que usa lat/lon.

4. **Archivos faltantes:** Si faltan archivos .sbn o .sbx, no pasa nada. 
   Los archivos críticos son .shp, .dbf, .shx, .prj

---

## ✅ ESTRUCTURA FINAL ESPERADA

```
📁 ProyectoFinal_TSP_TW/
│
├── 📁 datos/
│   ├── México_Ciudades.shp          ← Del RAR del profesor
│   ├── México_Ciudades.dbf          ← Del RAR del profesor
│   ├── México_Ciudades.shx          ← Del RAR del profesor
│   ├── México_Ciudades.prj          ← Del RAR del profesor
│   ├── coordenadas_capitales.json   ← GENERADO por extraer_coordenadas.py
│   └── matriz_distancias.npy        ← GENERADO por el programa principal
│
├── 📁 codigo/
│   ├── TSP_TW_Mexico_HGA.py        ← Programa principal
│   ├── demo_tsp_tw.py              ← Versión demo
│   └── extraer_coordenadas.py      ← Script de extracción
│
├── 📁 resultados/
│   ├── convergencia_hga.png        ← GENERADO al ejecutar
│   ├── mapa_mejor_ruta.png         ← GENERADO al ejecutar
│   ├── analisis_estadistico.png    ← GENERADO al ejecutar
│   └── resultados_experimentos.csv ← GENERADO al ejecutar
│
└── 📁 documentacion/
    └── README.md
```

---

## 🚀 ORDEN DE EJECUCIÓN

```
1. Descomprime el RAR → obtén México_Ciudades.shp
2. Crea estructura de carpetas
3. Copia archivos del shapefile a datos/
4. pip install geopandas numpy matplotlib pandas
5. python extraer_coordenadas.py
6. Verifica que exista coordenadas_capitales.json
7. Modifica TSP_TW_Mexico_HGA.py para cargar el JSON
8. python demo_tsp_tw.py
9. Si funciona → python TSP_TW_Mexico_HGA.py (versión completa)
10. Usa los resultados para tu informe
```

---

¡Listo! Con esta estructura tendrás todo organizado profesionalmente y usando 
TUS datos reales del profesor. 🎯
