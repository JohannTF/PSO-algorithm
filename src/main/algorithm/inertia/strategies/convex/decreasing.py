"""Implementación de la estrategia de peso inercial convexa decreciente."""

from typing import Union, List, Tuple, Optional
from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy
from src.main.algorithm.inertia.inertia_registry import InertiaRegistry


@InertiaRegistry.register("convex_decreasing")
class ConvexDecreasing(InertiaStrategy):
    """Implementación de la estrategia de peso inercial convexa decreciente para PSO."""

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
            
        # Calcular g
        g = current_iteration / (max_iterations - 1)
        
        # Implementación de la función convexa decreciente:
        # w = (wmax - wmin) * (g - 1)^2 + wmin
        return (self.w_max - self.w_min) * ((g - 1) ** 2) + self.w_min
