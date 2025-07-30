"""Implementación de la estrategia de peso inercial DE-PSO 

(Double exponential adaptive inertia weight PSO).
"""

import math
from typing import List, Tuple, Union

from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy
from src.main.algorithm.inertia.inertia_registry import InertiaRegistry


@InertiaRegistry.register("de_pso")
class DEPSO(InertiaStrategy):
    """Implementación de la estrategia de peso inercial DE-PSO.

    Fórmulas:
    - R = (Max_it - i) / Max_it
    - w = exp(-e^(-R))

    Esta estrategia combina conceptos de Evolución Diferencial con PSO,
    utilizando una función exponencial doble para el control del peso inercial.
    """

    def __init__(self, w_min: float = 0.4, w_max: float = 0.8,
                 params: Union[List, Tuple] = None):
        """Inicializa la estrategia de peso inercial DE-PSO.

        Args:
            w_min (float): Valor mínimo del peso inercial
            w_max (float): Valor inicial del peso inercial (w_init=0.8)
            params (Union[List, Tuple], optional): No usado en esta estrategia,
                mantenido por compatibilidad. Defaults to None.
        """
        self.w_min = w_min
        self.w_max = w_max

    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: dict = None) -> float:
        """Calcula el valor del peso inercial para la iteración actual usando DE-PSO.

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

        # Calcular R = (Max_it - i) / Max_it
        R = (max_iterations - current_iteration) / max_iterations

        # Fórmula DE-PSO: w = exp(-e^(-R))
        inner_exp = math.exp(-R)
        weight = math.exp(-inner_exp)

        # Asegurar que el peso esté dentro de los límites razonables
        return weight
