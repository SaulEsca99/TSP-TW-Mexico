"""
Genetic Operators Module
Operadores genéticos: cruce y mutación
"""

import numpy as np
from typing import Tuple


class GeneticOperators:
    """Operadores genéticos para el algoritmo TSP-TW"""
    
    def __init__(self, mutation_rate: float = 0.01, crossover_rate: float = 0.8, 
                 start_city_index: int = 0):
        """
        Inicializar operadores genéticos
        
        Args:
            mutation_rate: Tasa de mutación
            crossover_rate: Tasa de cruce
            start_city_index: Índice de la ciudad de inicio (no debe moverse)
        """
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.start_city_index = start_city_index
    
    def crossover(self, parent1: np.ndarray, parent2: np.ndarray, 
                  method: str = 'order') -> np.ndarray:
        """
        Realizar cruce entre dos padres
        
        Args:
            parent1: Primera ruta padre
            parent2: Segunda ruta padre
            method: Método de cruce ('order', 'pmx', 'cycle')
            
        Returns:
            Ruta hijo resultante
        """
        if method == 'order':
            return self._order_crossover(parent1, parent2)
        elif method == 'pmx':
            return self._pmx_crossover(parent1, parent2)
        else:
            return self._order_crossover(parent1, parent2)
    
    def _order_crossover(self, parent1: np.ndarray, 
                        parent2: np.ndarray) -> np.ndarray:
        """
        Order Crossover (OX) - Preserva la ciudad de inicio en posición 0
        
        Args:
            parent1: Primera ruta padre
            parent2: Segunda ruta padre
            
        Returns:
            Ruta hijo
        """
        size = len(parent1)
        
        # Si la ruta tiene la ciudad de inicio, trabajar solo con el resto
        if parent1[0] == self.start_city_index:
            # Trabajar solo con las ciudades después de la primera
            p1_subset = parent1[1:]
            p2_subset = parent2[1:]
            subset_size = len(p1_subset)
            
            if subset_size <= 1:
                return parent1.copy()
            
            start, end = sorted(np.random.choice(range(subset_size), 2, replace=False))
            
            # Copiar segmento del padre 1
            offspring_subset = np.full(subset_size, -1)
            offspring_subset[start:end] = p1_subset[start:end]
            
            # Llenar el resto con genes del padre 2 en orden
            current_pos = end
            for gene in np.concatenate([p2_subset[end:], p2_subset[:end]]):
                if gene not in offspring_subset:
                    if current_pos >= subset_size:
                        current_pos = 0
                    offspring_subset[current_pos] = gene
                    current_pos += 1
            
            # Reconstruir ruta completa con ciudad de inicio
            offspring = np.concatenate([[self.start_city_index], offspring_subset])
        else:
            # Crossover normal si no hay ciudad de inicio fija
            start, end = sorted(np.random.choice(range(size), 2, replace=False))
            offspring = np.full(size, -1)
            offspring[start:end] = parent1[start:end]
            
            current_pos = end
            for gene in np.concatenate([parent2[end:], parent2[:end]]):
                if gene not in offspring:
                    if current_pos >= size:
                        current_pos = 0
                    offspring[current_pos] = gene
                    current_pos += 1
        
        return offspring
    
    def _pmx_crossover(self, parent1: np.ndarray, 
                      parent2: np.ndarray) -> np.ndarray:
        """
        Partially Mapped Crossover (PMX)
        
        Args:
            parent1: Primera ruta padre
            parent2: Segunda ruta padre
            
        Returns:
            Ruta hijo
        """
        size = len(parent1)
        start, end = sorted(np.random.choice(range(size), 2, replace=False))
        
        offspring = parent1.copy()
        
        # Mapeo de genes
        for i in range(start, end):
            if parent2[i] not in offspring[start:end]:
                # Encontrar posición para intercambiar
                j = i
                while start <= j < end:
                    j = np.where(parent1 == parent2[j])[0][0]
                offspring[j] = parent2[i]
        
        offspring[start:end] = parent2[start:end]
        return offspring
    
    def mutate(self, route: np.ndarray, method: str = 'swap') -> np.ndarray:
        """
        Aplicar mutación a una ruta
        
        Args:
            route: Ruta a mutar
            method: Método de mutación ('swap', 'inversion', 'scramble')
            
        Returns:
            Ruta mutada
        """
        if np.random.random() > self.mutation_rate:
            return route
        
        if method == 'swap':
            return self._swap_mutation(route)
        elif method == 'inversion':
            return self._inversion_mutation(route)
        elif method == 'scramble':
            return self._scramble_mutation(route)
        else:
            return self._swap_mutation(route)
    
    def _swap_mutation(self, route: np.ndarray) -> np.ndarray:
        """
        Swap Mutation: intercambiar dos ciudades (preserva ciudad de inicio)
        
        Args:
            route: Ruta a mutar
            
        Returns:
            Ruta mutada
        """
        mutated = route.copy()
        
        # Si la primera ciudad es la ciudad de inicio, no la incluir en la mutación
        if len(route) > 1 and route[0] == self.start_city_index:
            # Seleccionar dos índices del resto de la ruta (excluyendo posición 0)
            idx1, idx2 = np.random.choice(range(1, len(route)), 2, replace=False)
        else:
            # Mutación normal
            idx1, idx2 = np.random.choice(len(route), 2, replace=False)
        
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
        return mutated
    
    def _inversion_mutation(self, route: np.ndarray) -> np.ndarray:
        """
        Inversion Mutation: invertir un segmento de la ruta (preserva ciudad de inicio)
        
        Args:
            route: Ruta a mutar
            
        Returns:
            Ruta mutada
        """
        mutated = route.copy()
        
        # Si la primera ciudad es la ciudad de inicio, no la incluir en la mutación
        if len(route) > 2 and route[0] == self.start_city_index:
            start, end = sorted(np.random.choice(range(1, len(route)), 2, replace=False))
        else:
            start, end = sorted(np.random.choice(len(route), 2, replace=False))
        
        mutated[start:end] = mutated[start:end][::-1]
        return mutated
    
    def _scramble_mutation(self, route: np.ndarray) -> np.ndarray:
        """
        Scramble Mutation: mezclar aleatoriamente un segmento
        
        Args:
            route: Ruta a mutar
            
        Returns:
            Ruta mutada
        """
        mutated = route.copy()
        start, end = sorted(np.random.choice(len(route), 2, replace=False))
        segment = mutated[start:end].copy()
        np.random.shuffle(segment)
        mutated[start:end] = segment
        return mutated
