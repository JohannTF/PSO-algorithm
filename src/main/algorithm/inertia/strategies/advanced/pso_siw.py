"""Implementación de la estrategia de peso inercial PSO-SIW 

(Sugeno inertia weight).
"""

from typing import List, Tuple, Union

from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy
from src.main.algorithm.inertia.inertia_registry import InertiaRegistry


@InertiaRegistry.register("pso_siw")
class PSOSIW(InertiaStrategy):
    """Implementación de la estrategia de peso inercial PSO-SIW.

    Fórmula: w = w_min - (w_max^(i/Max_it)) / (1 + s^(i/Max_it))

    Esta estrategia utiliza una función sigmoidal para el control del peso inercial,
    proporcionando una transición suave entre exploración y explotación.
    """

    def __init__(self, w_min: float = 0.4, w_max: float = 0.5,
                 params: Union[List, Tuple] = None):
        """Inicializa la estrategia de peso inercial PSO-SIW.

        Args:
            w_min (float): Valor mínimo del peso inercial (w_min=0.4)
            w_max (float): Valor máximo del peso inercial (w_max=0.5)
            params (Union[List, Tuple], optional): Parámetros específicos: [s]
                   donde s es el parámetro de forma sigmoidal. Defaults to None.
        """
        self.w_min = w_min
        self.w_max = w_max
        self.s = 2.0  # Valor por defecto

        if params is not None and len(params) > 0:
            try:
                s_value = params[0]
                if not isinstance(s_value, (float, int)):
                    raise ValueError("El parámetro 's' para PSO-SIW debe ser un número.")

                s_value = float(s_value)
                if s_value <= 0:
                    raise ValueError(f"PSO-SIW parameter 's' must be positive, got: {s_value}")

                self.s = s_value
            except (IndexError, ValueError, TypeError) as e:
                raise ValueError(f"Error al procesar parámetro 's' para PSO-SIW: {e}") from e

    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: dict = None) -> float:
        """Calcula el valor del peso inercial para la iteración actual.

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

        # Fórmula PSO-SIW: w = w_min - (w_max*(i/Max_it)) / (1 + s*(i/Max_it))
        numerator = self.w_max * progress_ratio
        denominator = 1 + (self.s * progress_ratio)
        weight = self.w_min - (numerator / denominator)

        return weight
