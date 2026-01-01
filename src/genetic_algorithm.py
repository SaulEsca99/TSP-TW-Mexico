"""
Genetic Algorithm Module
Implementación del Algoritmo Genético para TSP-TW
"""

import numpy as np
from typing import List, Tuple
from fitness_function import FitnessFunction
from operators import GeneticOperators


class GeneticAlgorithm:
    """Algoritmo Genético para resolver el TSP-TW"""
    
    def __init__(self, 
                 time_matrix: np.ndarray,
                 start_city_index: int = 0,
                 population_size: int = 100,
                 generations: int = 500,
                 mutation_rate: float = 0.01,
                 crossover_rate: float = 0.8,
                 elitism_rate: float = 0.1,
                 start_time: float = 9.0,
                 penalty_weight: float = 100.0):
        """
        Inicializar Algoritmo Genético para TSP-TW
        
        Args:
            time_matrix: Matriz de tiempos de viaje entre ciudades (en horas)
            start_city_index: Índice de la ciudad de inicio (CDMX)
            population_size: Tamaño de la población
            generations: Número de generaciones
            mutation_rate: Tasa de mutación
            crossover_rate: Tasa de cruce
            elitism_rate: Porcentaje de élite a preservar
            start_time: Hora de inicio del viaje (default: 9:00 AM)
            penalty_weight: Peso de penalización por violación de ventanas
        """
        self.time_matrix = time_matrix
        self.n_cities = len(time_matrix)
        self.start_city_index = start_city_index
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        
        # Fitness function para TSP-TW
        self.fitness_func = FitnessFunction(
            time_matrix=time_matrix,
            start_city_index=start_city_index,
            start_time=start_time,
            penalty_weight=penalty_weight
        )
        
        # Operadores genéticos con preservación de ciudad de inicio
        self.operators = GeneticOperators(
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,
            start_city_index=start_city_index
        )
        
        self.population = None
        self.best_solution = None
        self.best_fitness = float('inf')
        self.fitness_history = []
        
    def initialize_population(self) -> np.ndarray:
        """
        Inicializar población con rutas aleatorias
        Todas las rutas empiezan con la ciudad de inicio (CDMX)
        
        Returns:
            Array con población inicial
        """
        population = []
        
        # Crear lista de ciudades sin la ciudad de inicio
        other_cities = [i for i in range(self.n_cities) if i != self.start_city_index]
        
        for _ in range(self.population_size):
            # Permutar las otras ciudades
            route = np.random.permutation(other_cities)
            # Agregar ciudad de inicio al principio
            route = np.concatenate([[self.start_city_index], route])
            population.append(route)
            
        return np.array(population)
    
    def select_parents(self, population: np.ndarray, 
                      fitness_scores: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Seleccionar padres usando selección por torneo
        
        Args:
            population: Población actual
            fitness_scores: Puntuaciones de fitness
            
        Returns:
            Tupla con dos padres seleccionados
        """
        tournament_size = 5
        idx1 = np.random.choice(len(population), tournament_size)
        idx2 = np.random.choice(len(population), tournament_size)
        
        parent1 = population[idx1[np.argmin(fitness_scores[idx1])]]
        parent2 = population[idx2[np.argmin(fitness_scores[idx2])]]
        
        return parent1, parent2
    
    def evolve(self, verbose: bool = True) -> Tuple[np.ndarray, float, List[float]]:
        """
        Ejecutar el algoritmo genético
        
        Args:
            verbose: Si mostrar progreso
            
        Returns:
            Tupla con (mejor_ruta, mejor_fitness, historial_fitness)
        """
        # Inicializar población
        self.population = self.initialize_population()
        
        if verbose:
            print(f"\n🧬 Iniciando Algoritmo Genético para TSP-TW")
            print(f"   Población: {self.population_size}")
            print(f"   Generaciones: {self.generations}")
            print(f"   Ciudad de inicio: índice {self.start_city_index}")
            print(f"   Ventanas de tiempo: 9:00 - 21:00\n")
        
        for generation in range(self.generations):
            # Evaluar fitness
            fitness_scores = np.array([
                self.fitness_func.calculate_fitness(route) 
                for route in self.population
            ])
            
            # Guardar mejor solución
            best_idx = np.argmin(fitness_scores)
            if fitness_scores[best_idx] < self.best_fitness:
                self.best_fitness = fitness_scores[best_idx]
                self.best_solution = self.population[best_idx].copy()
            
            self.fitness_history.append(self.best_fitness)
            
            # Crear nueva población
            new_population = []
            
            # Elitismo
            n_elite = int(self.elitism_rate * self.population_size)
            elite_indices = np.argsort(fitness_scores)[:n_elite]
            for idx in elite_indices:
                new_population.append(self.population[idx])
            
            # Generar resto de la población
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(self.population, fitness_scores)
                
                # Cruce
                if np.random.random() < self.crossover_rate:
                    offspring = self.operators.crossover(parent1, parent2)
                else:
                    offspring = parent1.copy()
                
                # Mutación
                offspring = self.operators.mutate(offspring)
                new_population.append(offspring)
            
            self.population = np.array(new_population)
            
            # Imprimir progreso
            if verbose and (generation + 1) % 50 == 0:
                print(f"   Generación {generation + 1}/{self.generations} - "
                      f"Mejor tiempo: {self.best_fitness:.2f} horas")
        
        if verbose:
            print(f"\n✓ Algoritmo completado")
            print(f"   Mejor tiempo total: {self.best_fitness:.2f} horas")
        
        return self.best_solution, self.best_fitness, self.fitness_history
