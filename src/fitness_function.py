"""
Fitness Function Module
Función de aptitud con ventanas de tiempo para TSP-TW
Optimiza TIEMPO en lugar de distancia, con penalizaciones por violación de ventanas
"""

import numpy as np
from typing import List, Optional
from time_windows import RouteTimeCalculator, TimeWindow


class FitnessFunction:
    """Función de aptitud para evaluar rutas del TSP-TW"""
    
    def __init__(self, 
                 time_matrix: np.ndarray,
                 start_city_index: int = 0,
                 start_time: float = 9.0,
                 penalty_weight: float = 100.0):
        """
        Inicializar función de aptitud para TSP-TW
        
        Args:
            time_matrix: Matriz de tiempos de viaje entre ciudades (en horas)
            start_city_index: Índice de la ciudad de inicio (CDMX)
            start_time: Hora de inicio del viaje (default: 9:00 AM)
            penalty_weight: Peso de la penalización por violar ventanas
        """
        self.time_matrix = time_matrix
        self.start_city_index = start_city_index
        self.start_time = start_time
        self.penalty_weight = penalty_weight
        self.route_calculator = RouteTimeCalculator(time_matrix, start_time)
        
    def calculate_route_time(self, route: np.ndarray) -> float:
        """
        Calcular tiempo total de una ruta (solo tiempo de viaje, sin penalizaciones)
        
        Args:
            route: Array con el orden de ciudades a visitar
            
        Returns:
            Tiempo total de viaje en horas
        """
        total_time = 0
        for i in range(len(route)):
            from_city = route[i]
            to_city = route[(i + 1) % len(route)]  # Volver al inicio
            total_time += self.time_matrix[from_city, to_city]
        return total_time
    
    def calculate_fitness(self, route: np.ndarray, 
                         include_waiting: bool = True,
                         include_penalties: bool = True) -> float:
        """
        Calcular fitness total de una ruta con ventanas de tiempo
        
        Args:
            route: Array con el orden de ciudades a visitar
            include_waiting: Si incluir tiempos de espera
            include_penalties: Si incluir penalizaciones
            
        Returns:
            Valor de fitness (menor es mejor) - tiempo total + penalizaciones
        """
        # Asegurar que la ruta empieza y termina en la ciudad de inicio (CDMX)
        full_route = self._ensure_start_end_city(route)
        
        # Calcular tiempo total, tiempo de espera y penalizaciones
        total_time, waiting_time, penalty = self.route_calculator.calculate_route_time(
            full_route.tolist(),
            include_waiting=include_waiting,
            include_penalties=include_penalties
        )
        
        return total_time
    
    def calculate_detailed_fitness(self, route: np.ndarray) -> dict:
        """
        Calcular fitness detallado con todos los componentes
        
        Args:
            route: Array con el orden de ciudades a visitar
            
        Returns:
            Diccionario con componentes del fitness
        """
        full_route = self._ensure_start_end_city(route)
        
        # Calcular componentes
        total_time, waiting_time, penalty = self.route_calculator.calculate_route_time(
            full_route.tolist(),
            include_waiting=True,
            include_penalties=True
        )
        
        # Tiempo puro de viaje (sin esperas ni penalizaciones)
        travel_time = self.calculate_route_time(full_route)
        
        return {
            'total_time': total_time,
            'travel_time': travel_time,
            'waiting_time': waiting_time,
            'penalty': penalty,
            'fitness': total_time
        }
    
    def get_arrival_times(self, route: np.ndarray) -> List[float]:
        """
        Obtener tiempos de llegada a cada ciudad
        
        Args:
            route: Array con el orden de ciudades a visitar
            
        Returns:
            Lista de tiempos de llegada
        """
        full_route = self._ensure_start_end_city(route)
        return self.route_calculator.get_arrival_times(full_route.tolist())
    
    def _ensure_start_end_city(self, route: np.ndarray) -> np.ndarray:
        """
        Asegurar que la ruta empieza y termina en la ciudad de inicio
        
        Args:
            route: Ruta original
            
        Returns:
            Ruta que empieza y termina en start_city_index
        """
        # Si la ruta ya incluye la ciudad de inicio al principio, usarla tal cual
        if route[0] == self.start_city_index:
            return route
        
        # Si no, asegurar que empieza con la ciudad de inicio
        # Remover la ciudad de inicio si está en otro lugar
        route_without_start = route[route != self.start_city_index]
        
        # Agregar ciudad de inicio al principio
        full_route = np.concatenate([[self.start_city_index], route_without_start])
        
        return full_route
    
    def is_valid_route(self, route: np.ndarray) -> bool:
        """
        Verificar si una ruta es válida
        
        Args:
            route: Array con el orden de ciudades a visitar
            
        Returns:
            True si la ruta es válida
        """
        n_cities = len(self.time_matrix)
        
        # Verificar que todas las ciudades estén presentes exactamente una vez
        # (excepto la ciudad de inicio que puede estar al principio y al final)
        unique_cities = set(route)
        
        # Debe tener todas las ciudades
        if len(unique_cities) != n_cities:
            return False
        
        # Todas las ciudades deben estar en el rango válido
        if not all(0 <= city < n_cities for city in route):
            return False
        
        return True


class FitnessFunctionLegacy:
    """Función de aptitud original basada en distancias (para compatibilidad)"""
    
    def __init__(self, 
                 distance_matrix: np.ndarray,
                 time_windows: Optional[List[tuple]] = None,
                 penalty_weight: float = 1000):
        """
        Inicializar función de aptitud legacy
        
        Args:
            distance_matrix: Matriz de distancias entre ciudades
            time_windows: Lista de tuplas (inicio, fin) para ventanas de tiempo
            penalty_weight: Peso de la penalización por violar ventanas
        """
        self.distance_matrix = distance_matrix
        self.time_windows = time_windows
        self.penalty_weight = penalty_weight
        
    def calculate_route_distance(self, route: np.ndarray) -> float:
        """Calcular distancia total de una ruta"""
        total_distance = 0
        for i in range(len(route)):
            from_city = route[i]
            to_city = route[(i + 1) % len(route)]
            total_distance += self.distance_matrix[from_city, to_city]
        return total_distance
    
    def calculate_fitness(self, route: np.ndarray) -> float:
        """Calcular fitness basado en distancia"""
        return self.calculate_route_distance(route)
