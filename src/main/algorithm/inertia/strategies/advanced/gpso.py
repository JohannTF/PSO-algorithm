"""Implementación de la estrategia de peso inercial GPSO 

(Guided Particle Swarm Optimization).
"""

from typing import List, Tuple, Union

from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy
from src.main.algorithm.inertia.inertia_registry import InertiaRegistry


@InertiaRegistry.register("gpso")
class GPSO(InertiaStrategy):
    """
    Implementación de la estrategia de peso inercial GPSO (Global PSO).

    Fórmula: w = (w_max - w_min) * (i / Max_it)

    Esta estrategia utiliza un incremento lineal del peso inercial a lo largo
    de las iteraciones.

    Nota: Si prefieres valores entre w_min y w_max, usa la fórmula completa:
    w = (w_max - w_min) * (i / Max_it) + w_min
    """

    def __init__(self, w_min: float = 0.5, w_max: float = 0.9,
                 params: Union[List, Tuple] = None):
        """Inicializa la estrategia de peso inercial GPSO.

        Args:
            w_min (float): Valor mínimo del peso inercial (w_min=0.5)
            w_max (float): Valor máximo del peso inercial (w_max=0.9)
            params (Union[List, Tuple], optional): No usado en esta estrategia,
                mantenido por compatibilidad. Defaults to None.
        """
        self.w_min = w_min
        self.w_max = w_max

    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: dict = None) -> float:
        """Calcula el valor del peso inercial para la iteración actual usando GPSO.

        Args:
            current_iteration (int): Iteración actual del algoritmo
            max_iterations (int): Número máximo de iteraciones
            particle_info (dict, optional): No utilizado en esta estrategia.
                Defaults to None.

        Returns:
            float: Valor del peso inercial para la iteración actual
        """
        # Asegurar que no se divida por cero
        if max_iterations <= 1:
            return self.w_min

        # Calcular el ratio de progreso
        progress_ratio = current_iteration / max_iterations

        # Fórmula GPSO: w = (w_max - w_min) * (i / Max_it)
        weight = (self.w_max - self.w_min) * progress_ratio

        return weight