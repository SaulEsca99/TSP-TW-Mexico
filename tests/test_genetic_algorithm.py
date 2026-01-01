"""
Tests for genetic algorithm
"""

import unittest
import numpy as np
from src.genetic_algorithm import GeneticAlgorithm
from src.operators import GeneticOperators


class TestGeneticAlgorithm(unittest.TestCase):
    """Test cases for GeneticAlgorithm"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Crear matriz de distancias de prueba (5 ciudades)
        self.distance_matrix = np.array([
            [0, 10, 15, 20, 25],
            [10, 0, 35, 25, 30],
            [15, 35, 0, 30, 20],
            [20, 25, 30, 0, 15],
            [25, 30, 20, 15, 0]
        ])
        
        self.ga = GeneticAlgorithm(
            self.distance_matrix,
            population_size=20,
            generations=10
        )
    
    def test_initialize_population(self):
        """Test population initialization"""
        population = self.ga.initialize_population()
        
        # Verificar tamaño
        self.assertEqual(len(population), 20)
        
        # Verificar que cada individuo tenga todas las ciudades
        for individual in population:
            self.assertEqual(len(individual), 5)
            self.assertEqual(set(individual), set(range(5)))
    
    def test_evolve(self):
        """Test evolution process"""
        best_route, best_fitness, history = self.ga.evolve()
        
        # Verificar que se encontró una solución
        self.assertIsNotNone(best_route)
        self.assertGreater(best_fitness, 0)
        
        # Verificar que el fitness mejoró
        self.assertLessEqual(history[-1], history[0])


class TestGeneticOperators(unittest.TestCase):
    """Test cases for GeneticOperators"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.operators = GeneticOperators(mutation_rate=1.0)  # 100% para testing
        self.parent1 = np.array([0, 1, 2, 3, 4])
        self.parent2 = np.array([4, 3, 2, 1, 0])
    
    def test_order_crossover(self):
        """Test order crossover"""
        offspring = self.operators.crossover(self.parent1, self.parent2, method='order')
        
        # Verificar que el hijo tenga todas las ciudades
        self.assertEqual(len(offspring), 5)
        self.assertEqual(set(offspring), set(range(5)))
    
    def test_swap_mutation(self):
        """Test swap mutation"""
        route = np.array([0, 1, 2, 3, 4])
        mutated = self.operators._swap_mutation(route)
        
        # Verificar que sigue siendo una permutación válida
        self.assertEqual(set(mutated), set(range(5)))
        
        # Verificar que cambió
        self.assertFalse(np.array_equal(route, mutated))


if __name__ == '__main__':
    unittest.main()
