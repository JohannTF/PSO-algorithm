"""Implementación de la estrategia de peso inercial PSO-NIEW.

PSO-NIEW (Non-linear Exponential Inertia Weight).
"""

import math
from typing import List, Optional, Tuple, Union

from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy
from src.main.algorithm.inertia.inertia_registry import InertiaRegistry


@InertiaRegistry.register("pso_niew")
class PSONIEW(InertiaStrategy):
    """Implementación de la estrategia de peso inercial PSO-NIEW.

    Fórmula: w = w_min + (w_max - w_min) * exp(-10 * i / Max_it)
    """

    def __init__(self, w_min: float = 0.4, w_max: float = 0.9,
                 params: Union[List, Tuple] = None):
        """Inicializa la estrategia de peso inercial PSO-NIEW.

        Args:
            w_min (float): Valor mínimo del peso inercial. Defaults to 0.4.
            w_max (float): Valor máximo del peso inercial. Defaults to 0.9.
            params (Union[List, Tuple], optional): Parámetros adicionales
                (no utilizados en esta estrategia). Defaults to None.
        """
        self.w_max = w_max
        self.w_min = w_min

    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: Optional[dict] = None) -> float:
        """Calcula el peso inercial usando PSO-NIEW.

        Args:
            current_iteration (int): Iteración actual del algoritmo
            max_iterations (int): Número máximo de iteraciones
            particle_info (Optional[dict], optional): No utilizado en esta
                estrategia. Defaults to None.

        Returns:
            float: Valor del peso inercial para la iteración actual
        """
        # Asegurar que no se divida por cero
        if max_iterations <= 1:
            return self.w_min

        # Calcular el ratio de progreso
        progress_ratio = current_iteration / max_iterations

        # Fórmula PSO-NIEW: w = w_min + (w_max - w_min) * exp(-10 * i / Max_it)
        exponential_factor = math.exp(-10.0 * progress_ratio)
        weight = self.w_min + (self.w_max - self.w_min) * exponential_factor

        return weight
