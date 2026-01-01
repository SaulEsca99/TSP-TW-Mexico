"""
Tests for distance calculator
"""

import unittest
import numpy as np
import pandas as pd
from src.distance_calculator import DistanceCalculator


class TestDistanceCalculator(unittest.TestCase):
    """Test cases for DistanceCalculator"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Crear datos de prueba
        self.test_data = pd.DataFrame({
            'ciudad': ['Ciudad A', 'Ciudad B', 'Ciudad C'],
            'lat': [19.4326, 25.6866, 20.6597],
            'lon': [-99.1332, -100.3161, -103.3496]
        })
        self.calculator = DistanceCalculator(self.test_data)
    
    def test_calculate_distance(self):
        """Test distance calculation between two points"""
        # Ciudad de México a Monterrey (aproximadamente)
        city1 = (19.4326, -99.1332)
        city2 = (25.6866, -100.3161)
        
        distance = self.calculator.calculate_distance(city1, city2)
        
        # La distancia debería ser aproximadamente 760 km
        self.assertGreater(distance, 700)
        self.assertLess(distance, 800)
    
    def test_build_distance_matrix(self):
        """Test distance matrix construction"""
        matrix = self.calculator.build_distance_matrix()
        
        # Verificar dimensiones
        self.assertEqual(matrix.shape, (3, 3))
        
        # Verificar simetría
        np.testing.assert_array_almost_equal(matrix, matrix.T)
        
        # Verificar diagonal (distancia a sí mismo = 0)
        np.testing.assert_array_almost_equal(np.diag(matrix), np.zeros(3))
    
    def test_estimate_travel_time(self):
        """Test travel time estimation"""
        distance = 800  # km
        time = self.calculator.estimate_travel_time(distance, avg_speed_kmh=80)
        
        # Debería ser 10 horas
        self.assertEqual(time, 10.0)


if __name__ == '__main__':
    unittest.main()
