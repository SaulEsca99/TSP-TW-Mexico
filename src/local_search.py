"""
Local Search Module
Heurística 2-opt para mejora local de rutas
"""

import numpy as np
from typing import Tuple


class LocalSearch:
    """Búsqueda local 2-opt para optimización de rutas"""
    
    def __init__(self, distance_matrix: np.ndarray):
        """
        Inicializar búsqueda local
        
        Args:
            distance_matrix: Matriz de distancias entre ciudades
        """
        self.distance_matrix = distance_matrix
    
    def calculate_route_distance(self, route: np.ndarray) -> float:
        """
        Calcular distancia total de una ruta
        
        Args:
            route: Array con el orden de ciudades
            
        Returns:
            Distancia total
        """
        total_distance = 0
        for i in range(len(route)):
            from_city = route[i]
            to_city = route[(i + 1) % len(route)]
            total_distance += self.distance_matrix[from_city, to_city]
        return total_distance
    
    def two_opt_swap(self, route: np.ndarray, i: int, j: int) -> np.ndarray:
        """
        Realizar intercambio 2-opt
        
        Args:
            route: Ruta actual
            i: Índice inicial
            j: Índice final
            
        Returns:
            Nueva ruta con segmento invertido
        """
        new_route = route.copy()
        new_route[i:j+1] = route[i:j+1][::-1]
        return new_route
    
    def optimize(self, route: np.ndarray, max_iterations: int = 1000) -> Tuple[np.ndarray, float]:
        """
        Optimizar ruta usando 2-opt
        
        Args:
            route: Ruta inicial
            max_iterations: Número máximo de iteraciones
            
        Returns:
            Tupla con (mejor_ruta, mejor_distancia)
        """
        best_route = route.copy()
        best_distance = self.calculate_route_distance(best_route)
        improved = True
        iteration = 0
        
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            
            for i in range(1, len(route) - 1):
                for j in range(i + 1, len(route)):
                    # Probar intercambio 2-opt
                    new_route = self.two_opt_swap(best_route, i, j)
                    new_distance = self.calculate_route_distance(new_route)
                    
                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True
                        break
                
                if improved:
                    break
        
        return best_route, best_distance
    
    def optimize_greedy(self, route: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Optimización 2-opt greedy (primera mejora encontrada)
        
        Args:
            route: Ruta inicial
            
        Returns:
            Tupla con (mejor_ruta, mejor_distancia)
        """
        best_route = route.copy()
        best_distance = self.calculate_route_distance(best_route)
        improved = True
        
        while improved:
            improved = False
            
            for i in range(1, len(route) - 1):
                if improved:
                    break
                    
                for j in range(i + 1, len(route)):
                    new_route = self.two_opt_swap(best_route, i, j)
                    new_distance = self.calculate_route_distance(new_route)
                    
                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True
                        break
        
        return best_route, best_distance
