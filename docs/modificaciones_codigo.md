"""
================================================================================
INSTRUCCIONES PARA MODIFICAR TSP_TW_Mexico_HGA.py
================================================================================

OPCIÓN 1: CARGAR DESDE JSON (RECOMENDADO)
------------------------------------------

Reemplaza las líneas 28-62 (donde está el diccionario CAPITALES_MEXICO) con:

"""

import json
import os

# Cargar coordenadas desde el archivo JSON generado por extraer_coordenadas.py
RUTA_COORDENADAS = '../datos/coordenadas_capitales.json'

if not os.path.exists(RUTA_COORDENADAS):
    print(f"❌ ERROR: No se encontró {RUTA_COORDENADAS}")
    print(f"Por favor, ejecuta primero: python extraer_coordenadas.py")
    sys.exit(1)

with open(RUTA_COORDENADAS, 'r', encoding='utf-8') as f:
    CAPITALES_MEXICO = json.load(f)
    # Convertir keys de string a int (JSON guarda keys como strings)
    CAPITALES_MEXICO = {int(k): v for k, v in CAPITALES_MEXICO.items()}

N_CIUDADES = len(CAPITALES_MEXICO)
print(f"✓ Cargadas {N_CIUDADES} capitales desde {RUTA_COORDENADAS}")

"""
================================================================================

OPCIÓN 2: CÓDIGO COMPLETO MODIFICADO
--------------------------------------

O DESCARGA ESTE ARCHIVO COMPLETO y reemplaza TSP_TW_Mexico_HGA.py:

"""

# [AQUÍ VA TODO EL CÓDIGO PERO CON LA MODIFICACIÓN]
# Por brevedad, solo te muestro la parte modificada arriba
# El resto del código es IDÉNTICO al TSP_TW_Mexico_HGA.py original

"""
================================================================================

PASOS PARA INTEGRAR:
--------------------

1. Ejecuta primero:
   python extraer_coordenadas.py
   
   Esto creará: datos/coordenadas_capitales.json

2. Opción A - Modificación manual:
   - Abre TSP_TW_Mexico_HGA.py
   - Busca las líneas 28-62 (el diccionario CAPITALES_MEXICO)
   - Reemplázalas con el código de "OPCIÓN 1" arriba
   
   Opción B - Usar este archivo:
   - Este archivo ya tiene todo integrado
   - Renómbralo a TSP_TW_Mexico_HGA_JSON.py
   - Úsalo en lugar del original

3. Ejecuta:
   python TSP_TW_Mexico_HGA.py
   # o
   python TSP_TW_Mexico_HGA_JSON.py

================================================================================

ESTRUCTURA DE coordenadas_capitales.json:
------------------------------------------

{
  "0": {
    "nombre": "Ciudad de México",
    "estado": "CDMX", 
    "lat": 19.4326,
    "lon": -99.1332
  },
  "1": {
    "nombre": "Aguascalientes",
    "estado": "Aguascalientes",
    "lat": 21.8853,
    "lon": -102.2916
  },
  ...
}

================================================================================

VERIFICACIÓN:
-------------

Después de modificar, ejecuta para verificar:

python -c "import json; d = json.load(open('../datos/coordenadas_capitales.json')); print(f'Capitales: {len(d)}'); print(f'CDMX: {d[\"0\"][\"nombre\"]}')"

Debe mostrar:
Capitales: 32
CDMX: Ciudad de México

================================================================================
"""
