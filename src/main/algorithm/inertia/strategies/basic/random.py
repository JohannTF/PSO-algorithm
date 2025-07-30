"""Implementación de la estrategia de peso inercial aleatorio."""

import random
from typing import List, Optional, Tuple, Union

from src.main.algorithm.inertia.inertia_registry import InertiaRegistry
from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy


@InertiaRegistry.register("aleatory")
class Random(InertiaStrategy):
    """Estrategia de peso inercial aleatorio para PSO."""

    def __init__(self, w_min: float = 0.4, w_max: float = 0.9,
                 params: Union[List, Tuple] = None) -> None:
        """Inicializa la estrategia de peso inercial.

        Args:
            w_min (float): Valor mínimo del peso inercial. Defaults to 0.4.
            w_max (float): Valor máximo del peso inercial. Defaults to 0.9.
            params (Union[List, Tuple], optional): No usado en esta estrategia,
                mantenido por compatibilidad. Defaults to None.
        """
        self.w_min = w_min
        self.w_max = w_max

    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: Optional[dict] = None) -> float:
        """Calcula un peso inercial aleatorio.

        Args:
            current_iteration (int): Iteración actual (no utilizada).
            max_iterations (int): Número máximo de iteraciones (no utilizado).
            particle_info (Optional[dict], optional): Información de partículas
                (no utilizada). Defaults to None.

        Returns:
            float: Valor aleatorio del peso inercial entre w_min y w_max.
        """
        return random.uniform(self.w_min, self.w_max)
