"""
Data Loader Module
Cargar y procesar shapefiles de México (estados y ciudades)
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path


class DataLoader:
    """Clase para cargar y procesar datos geográficos de México"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
    def load_shapefile(self, filename: str) -> gpd.GeoDataFrame:
        """
        Cargar un shapefile desde el directorio raw
        
        Args:
            filename: Nombre del archivo shapefile
            
        Returns:
            GeoDataFrame con los datos cargados
        """
        filepath = self.raw_dir / filename
        return gpd.read_file(filepath)
    
    def extract_capitals(self, states_gdf: gpd.GeoDataFrame, 
                        cities_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
        """
        Extraer coordenadas de las capitales estatales
        
        Args:
            states_gdf: GeoDataFrame con estados (no usado actualmente)
            cities_gdf: GeoDataFrame con ciudades
            
        Returns:
            DataFrame con coordenadas de capitales (CIUDAD, ESTADO, lat, lon)
        """
        # Filtrar solo las capitales (CAPITAL == 'S')
        capitales = cities_gdf[cities_gdf['CAPITAL'] == 'S'].copy()
        
        # IMPORTANTE: Agregar Ciudad de México manualmente
        # CDMX no está marcada como capital en el shapefile porque Toluca es la capital del Estado de México
        # Pero CDMX es el punto de inicio requerido para el TSP-TW
        cdmx = cities_gdf[cities_gdf['CIUDAD'] == 'Ciudad de México'].copy()
        if not cdmx.empty:
            capitales = pd.concat([capitales, cdmx], ignore_index=True)
            print(f"   ℹ Ciudad de México agregada manualmente (punto de inicio del TSP-TW)")
        
        # Extraer coordenadas de la geometría
        capitales['lat'] = capitales.geometry.y
        capitales['lon'] = capitales.geometry.x
        
        # Crear DataFrame limpio con las columnas necesarias
        df = capitales[['CIUDAD', 'ESTADO', 'lat', 'lon']].reset_index(drop=True)
        
        # Ordenar por nombre de ciudad para consistencia
        df = df.sort_values('CIUDAD').reset_index(drop=True)
        
        print(f"✓ Extraídas {len(df)} capitales estatales (incluyendo CDMX)")
        
        return df
    
    def save_coordinates(self, df: pd.DataFrame, filename: str = "coordenadas_capitales.csv"):
        """
        Guardar coordenadas procesadas
        
        Args:
            df: DataFrame con coordenadas
            filename: Nombre del archivo de salida
        """
        output_path = self.processed_dir / filename
        df.to_csv(output_path, index=False)
        print(f"Coordenadas guardadas en: {output_path}")
