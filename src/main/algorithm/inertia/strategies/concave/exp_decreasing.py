"""Implementación de la estrategia de peso inercial cóncava exponencial decreciente."""

import math
from typing import Union, List, Tuple, Optional

from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy
from src.main.algorithm.inertia.inertia_registry import InertiaRegistry


@InertiaRegistry.register("concave_exp_decreasing")
class ConcaveExponentialDecreasing(InertiaStrategy):
    """Implementación de la estrategia de peso inercial cóncava exponencial decreciente para PSO."""

    def __init__(self, w_min: float = 0.4, w_max: float = 0.9, 
                 params: Union[List, Tuple] = None):
        """Inicializa la estrategia de peso inercial.

        Args:
            w_min (float): Valor final del peso inercial. Defaults to 0.4.
            w_max (float): Valor inicial del peso inercial. Defaults to 0.9.
            params (Union[List, Tuple], optional): Parámetros adicionales 
                (no utilizados en esta estrategia). Defaults to None.
        """
        self.w_max = w_max
        self.w_min = w_min

    def __call__(self, current_iteration: int, max_iterations: int, 
                 particle_info: Optional[dict] = None) -> float:
        """Calcula el valor del peso inercial para la iteración actual.

        Args:
            current_iteration (int): Iteración actual del algoritmo
            max_iterations (int): Número máximo de iteraciones
            particle_info (Optional[dict], optional): Información de partículas 
                (no utilizada). Defaults to None.

        Returns:
            float: Valor del peso inercial para la iteración actual
        """
        # Asegurar que no se divida por cero
        if max_iterations <= 1:
            return self.w_min
            
        # Calcular g como la relación entre iteración actual y máximo de iteraciones
        g = current_iteration / (max_iterations - 1)
        c = 10
        
        # Formula: w = w_max - (w_max - w_min)*((e^cg - 1)/(e^c - 1))
        numerator = math.exp(c * g) - 1
        denominator = math.exp(c) - 1
        
        w = self.w_max - (self.w_max - self.w_min) * (numerator / denominator)
        
        return w
