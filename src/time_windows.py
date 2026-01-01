"""
Time Windows Module
Manejo de ventanas de tiempo para TSP-TW
"""

from datetime import datetime, timedelta
from typing import List, Tuple
import numpy as np


class TimeWindow:
    """Clase para manejar ventanas de tiempo en el TSP-TW"""
    
    def __init__(self, opening_hour: float = 9.0, closing_hour: float = 21.0):
        """
        Inicializar ventanas de tiempo
        
        Args:
            opening_hour: Hora de apertura (default: 9:00 AM)
            closing_hour: Hora de cierre (default: 21:00 PM / 9:00 PM)
        """
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
        self.window_duration = closing_hour - opening_hour  # 12 horas
        
    def is_within_window(self, arrival_time: float) -> bool:
        """
        Verificar si un tiempo de llegada está dentro de la ventana
        
        Args:
            arrival_time: Tiempo de llegada en horas desde las 00:00
            
        Returns:
            True si está dentro de la ventana, False en caso contrario
        """
        # Normalizar el tiempo al día actual (módulo 24)
        time_of_day = arrival_time % 24
        return self.opening_hour <= time_of_day <= self.closing_hour
    
    def calculate_waiting_time(self, arrival_time: float) -> float:
        """
        Calcular tiempo de espera si se llega antes de la apertura
        
        Args:
            arrival_time: Tiempo de llegada en horas desde inicio
            
        Returns:
            Tiempo de espera en horas
        """
        time_of_day = arrival_time % 24
        
        # Si llega antes de la apertura, debe esperar
        if time_of_day < self.opening_hour:
            return self.opening_hour - time_of_day
        
        # Si llega después del cierre del día anterior
        if time_of_day > self.closing_hour:
            # Esperar hasta la apertura del siguiente día
            return (24 - time_of_day) + self.opening_hour
        
        return 0.0
    
    def calculate_penalty(self, arrival_time: float, penalty_weight: float = 100.0) -> float:
        """
        Calcular penalización por violación de ventana de tiempo
        
        Args:
            arrival_time: Tiempo de llegada en horas desde inicio
            penalty_weight: Peso de la penalización (default: 100.0)
            
        Returns:
            Penalización (0 si está dentro de la ventana)
        """
        time_of_day = arrival_time % 24
        
        # Si está dentro de la ventana, no hay penalización
        if self.is_within_window(arrival_time):
            return 0.0
        
        # Penalización por llegar tarde (después del cierre)
        if time_of_day > self.closing_hour:
            overtime = time_of_day - self.closing_hour
            return penalty_weight * overtime
        
        # Penalización por llegar muy temprano (antes de apertura)
        # Esto normalmente se maneja con tiempo de espera, pero puede haber penalización
        if time_of_day < self.opening_hour:
            early_time = self.opening_hour - time_of_day
            return penalty_weight * early_time * 0.5  # Penalización menor por llegar temprano
        
        return 0.0


class RouteTimeCalculator:
    """Calculador de tiempos para rutas con ventanas de tiempo"""
    
    def __init__(self, time_matrix: np.ndarray, start_time: float = 9.0):
        """
        Inicializar calculador de tiempos de ruta
        
        Args:
            time_matrix: Matriz de tiempos de viaje entre ciudades
            start_time: Hora de inicio del viaje (default: 9:00 AM)
        """
        self.time_matrix = time_matrix
        self.start_time = start_time
        self.time_window = TimeWindow()
        
    def calculate_route_time(self, route: List[int], 
                            include_waiting: bool = True,
                            include_penalties: bool = True) -> Tuple[float, float, float]:
        """
        Calcular tiempo total de una ruta considerando ventanas de tiempo
        
        Args:
            route: Lista de índices de ciudades en orden de visita
            include_waiting: Si incluir tiempos de espera
            include_penalties: Si incluir penalizaciones
            
        Returns:
            Tupla (tiempo_total, tiempo_espera_total, penalizacion_total)
        """
        current_time = self.start_time
        total_travel_time = 0.0
        total_waiting_time = 0.0
        total_penalty = 0.0
        
        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            
            # Tiempo de viaje entre ciudades
            travel_time = self.time_matrix[from_city, to_city]
            total_travel_time += travel_time
            
            # Actualizar tiempo actual
            current_time += travel_time
            
            # Calcular tiempo de espera si es necesario
            if include_waiting:
                waiting_time = self.time_window.calculate_waiting_time(current_time)
                total_waiting_time += waiting_time
                current_time += waiting_time
            
            # Calcular penalización si es necesario
            if include_penalties:
                penalty = self.time_window.calculate_penalty(current_time)
                total_penalty += penalty
        
        total_time = total_travel_time + total_waiting_time + total_penalty
        
        return total_time, total_waiting_time, total_penalty
    
    def get_arrival_times(self, route: List[int]) -> List[float]:
        """
        Obtener tiempos de llegada a cada ciudad en la ruta
        
        Args:
            route: Lista de índices de ciudades en orden de visita
            
        Returns:
            Lista de tiempos de llegada (en horas desde inicio)
        """
        current_time = self.start_time
        arrival_times = [current_time]  # Tiempo de inicio en primera ciudad
        
        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            
            # Tiempo de viaje
            travel_time = self.time_matrix[from_city, to_city]
            current_time += travel_time
            
            # Tiempo de espera si llega antes de apertura
            waiting_time = self.time_window.calculate_waiting_time(current_time)
            current_time += waiting_time
            
            arrival_times.append(current_time)
        
        return arrival_times
    
    def format_time(self, hours_from_start: float) -> str:
        """
        Formatear tiempo en formato legible (HH:MM)
        
        Args:
            hours_from_start: Horas desde el inicio (9:00 AM)
            
        Returns:
            String con formato "Día X, HH:MM"
        """
        total_hours = self.start_time + hours_from_start
        day = int(total_hours // 24) + 1
        hour_of_day = total_hours % 24
        hours = int(hour_of_day)
        minutes = int((hour_of_day - hours) * 60)
        
        return f"Día {day}, {hours:02d}:{minutes:02d}"
