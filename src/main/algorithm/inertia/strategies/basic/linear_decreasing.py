"""Implementación de la estrategia de peso inercial decreciente lineal."""

from typing import List, Optional, Tuple, Union

import numpy as np

from src.main.algorithm.inertia.inertia_registry import InertiaRegistry
from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy


@InertiaRegistry.register("linear_decreasing")
class LinearDecreasing(InertiaStrategy):
    """Implementación de la estrategia de peso inercial decreciente lineal para PSO.

    El peso inercial decrece linealmente desde un valor inicial hasta un valor
    final a lo largo de las iteraciones del algoritmo.
    """

    def __init__(self, w_min: float = 0.4, w_max: float = 0.9,
                 params: Union[List, Tuple] = None) -> None:
        """Inicializa la estrategia de peso inercial.

        Args:
            w_min (float): Valor final del peso inercial. Defaults to 0.4.
            w_max (float): Valor inicial del peso inercial. Defaults to 0.9.
            params (Union[List, Tuple], optional): No usado en esta estrategia,
                mantenido por compatibilidad. Defaults to None.
        """
        self.w_min = w_min
        self.w_max = w_max

    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: Optional[dict] = None) -> Union[float, np.ndarray]:
        """Calcula el valor del peso inercial para la iteración actual.

        Args:
            current_iteration (int): Iteración actual del algoritmo.
            max_iterations (int): Número máximo de iteraciones.
            particle_info (Optional[dict], optional): No utilizado en esta
                estrategia. Defaults to None.

        Returns:
            float: Valor del peso inercial para la iteración actual.
        """
        # Asegurar que no se divida por cero
        if max_iterations <= 1:
            return self.w_min

        # Calcular el peso inercial decreciente linealmente
        return self.w_max + (self.w_min - self.w_max) * (
            current_iteration / (max_iterations - 1)
        )
