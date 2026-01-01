"""
Distance Calculator Module
Calcular distancias y tiempos de viaje entre ciudades
"""

import numpy as np
import pandas as pd
from geopy.distance import geodesic
from typing import Tuple, List


class DistanceCalculator:
    """Clase para calcular distancias entre ciudades"""
    
    def __init__(self, coordinates_df: pd.DataFrame):
        """
        Inicializar calculador de distancias
        
        Args:
            coordinates_df: DataFrame con coordenadas de ciudades
        """
        self.coordinates = coordinates_df
        self.distance_matrix = None
        
    def calculate_distance(self, city1: Tuple[float, float], 
                          city2: Tuple[float, float]) -> float:
        """
        Calcular distancia geodésica entre dos ciudades
        
        Args:
            city1: Tupla (latitud, longitud) de la primera ciudad
            city2: Tupla (latitud, longitud) de la segunda ciudad
            
        Returns:
            Distancia en kilómetros
        """
        return geodesic(city1, city2).kilometers
    
    def build_distance_matrix(self) -> np.ndarray:
        """
        Construir matriz de distancias entre todas las ciudades
        
        Returns:
            Matriz numpy con distancias
        """
        n_cities = len(self.coordinates)
        matrix = np.zeros((n_cities, n_cities))
        
        for i in range(n_cities):
            for j in range(i + 1, n_cities):
                city1 = (self.coordinates.iloc[i]['lat'], 
                        self.coordinates.iloc[i]['lon'])
                city2 = (self.coordinates.iloc[j]['lat'], 
                        self.coordinates.iloc[j]['lon'])
                
                distance = self.calculate_distance(city1, city2)
                matrix[i, j] = distance
                matrix[j, i] = distance
                
        self.distance_matrix = matrix
        return matrix
    
    def estimate_travel_time(self, distance_km: float, 
                           avg_speed_kmh: float = 60) -> float:
        """
        Estimar tiempo de viaje basado en distancia
        
        Args:
            distance_km: Distancia en kilómetros
            avg_speed_kmh: Velocidad promedio en km/h (default: 60 km/h según especificaciones)
            
        Returns:
            Tiempo estimado en horas
        """
        return distance_km / avg_speed_kmh
    
    def build_time_matrix(self, avg_speed_kmh: float = 60) -> np.ndarray:
        """
        Construir matriz de tiempos de viaje entre todas las ciudades
        Convierte distancias a tiempos usando velocidad especificada
        
        Args:
            avg_speed_kmh: Velocidad promedio en km/h (default: 60 km/h)
            
        Returns:
            Matriz numpy con tiempos en horas
        """
        if self.distance_matrix is None:
            self.build_distance_matrix()
        
        # Convertir distancias a tiempos (distancia / velocidad)
        time_matrix = self.distance_matrix / avg_speed_kmh
        
        print(f"✓ Matriz de tiempos generada (velocidad: {avg_speed_kmh} km/h)")
        return time_matrix
    
    def save_distance_matrix(self, filename: str = "data/processed/matriz_distancias.csv"):
        """
        Guardar matriz de distancias en archivo CSV
        
        Args:
            filename: Ruta del archivo de salida
        """
        if self.distance_matrix is not None:
            df = pd.DataFrame(self.distance_matrix, 
                            columns=self.coordinates['CIUDAD'],
                            index=self.coordinates['CIUDAD'])
            df.to_csv(filename)
            print(f"✓ Matriz de distancias guardada en: {filename}")
    
    def save_time_matrix(self, time_matrix: np.ndarray, 
                        filename: str = "data/processed/matriz_tiempos.csv"):
        """
        Guardar matriz de tiempos en archivo CSV
        
        Args:
            time_matrix: Matriz de tiempos
            filename: Ruta del archivo de salida
        """
        df = pd.DataFrame(time_matrix,
                         columns=self.coordinates['CIUDAD'],
                         index=self.coordinates['CIUDAD'])
        df.to_csv(filename)
        print(f"✓ Matriz de tiempos guardada en: {filename}")
