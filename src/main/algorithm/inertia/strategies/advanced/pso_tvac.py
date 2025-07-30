"""Implementación de la estrategia de peso inercial PSO-TVAC 

(Time Varying Acceleration Coefficients).
"""

from typing import List, Optional, Tuple, Union

from src.main.algorithm.inertia.inertia_registry import InertiaRegistry
from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy


@InertiaRegistry.register("pso_tvac")
class PSOTVAC(InertiaStrategy):
    """Implementación de la estrategia de peso inercial PSO-TVAC.

    Fórmulas:
    - w = w_max - ((w_max - w_min) / iter_max) * k
    - c1: 2.5 → 0.5 (decreciente linealmente)
    - c2: 0.5 → 2.5 (creciente linealmente)

    Nota: Esta clase solo maneja el peso inercial lineal decreciente.
    Los coeficientes c1 y c2 deben ser manejados por el algoritmo PSO principal.
    """

    def __init__(self, w_min: float = 0.4, w_max: float = 0.9,
                 params: Union[List, Tuple] = None) -> None:
        """Inicializa la estrategia de peso inercial PSO-TVAC.

        Args:
            w_min (float): Valor mínimo del peso inercial (w_min=0.4).
            w_max (float): Valor máximo del peso inercial (w_max=0.9).
            params (Union[List, Tuple], optional): No usado en esta estrategia,
                mantenido por compatibilidad. Defaults to None.
        """
        self.w_min = w_min
        self.w_max = w_max

    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: Optional[dict] = None) -> float:
        """Calcula el valor del peso inercial para la iteración actual usando PSO-TVAC.

        Args:
            current_iteration (int): Iteración actual del algoritmo (k).
            max_iterations (int): Número máximo de iteraciones (iter_max).
            particle_info (Optional[dict], optional): No utilizado en esta 
                estrategia. Defaults to None.

        Returns:
            float: Valor del peso inercial para la iteración actual.
        """
        # Asegurar que no se divida por cero
        if max_iterations <= 1:
            return self.w_min

        # Fórmula PSO-TVAC: w = w_max - ((w_max - w_min) / iter_max) * k
        weight = (self.w_max - 
                  ((self.w_max - self.w_min) / max_iterations) * current_iteration)

        # Asegurar que el peso esté dentro de los límites
        return weight