"""Implementación de la estrategia de peso inercial DSI-PSO.

(Distance-Dependent Sigmodal Inertia Weight).
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

from src.main.algorithm.inertia.inertia_registry import InertiaRegistry
from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy


@InertiaRegistry.register("dsi_pso")
class DSIPSO(InertiaStrategy):
    """Implementación de la estrategia de peso inercial DSI-PSO.

    (Distance-Dependent Sigmodal Inertia Weight)

    Fórmulas:
    1. D = abs(Gb - Pbi) * (Maxit - k) / Maxit
    2. wik = w_max / (w_min + e^(-0.5 * D))

    donde:
    - D es la distancia ponderada
    - Gb es la mejor posición global
    - Pbi es la mejor posición individual de cada partícula
    - Maxit es el número total de iteraciones
    - k es la iteración actual
    - wik es el peso inercial para la partícula i en la iteración k
    """

    def __init__(
        self,
        w_min: float = 0.4,
        w_max: float = 0.9,
        params: Union[List, Tuple] = None
    ) -> None:
        """Inicializa la estrategia de peso inercial DSI-PSO.

        Args:
            w_min (float): Valor mínimo del peso inercial.
            w_max (float): Valor máximo del peso inercial.
            params (Union[List, Tuple], optional): Parámetros específicos:
                [sensitivity]. Defaults to None.
        """
        self.w_min = w_min
        self.w_max = w_max
        self.sensitivity = 0.5  # Valor por defecto

        if params is not None and len(params) > 0:
            try:
                sensitivity_value = params[0]
                if not isinstance(sensitivity_value, (float, int)):
                    raise ValueError(
                        "El parámetro 'sensitivity' para DSI-PSO debe ser un número."
                    )

                sensitivity_value = float(sensitivity_value)
                if not (0.0 <= sensitivity_value <= 1.0):
                    raise ValueError(
                        f"DSI-PSO sensitivity must be between 0.0 and 1.0, got: {sensitivity_value}"
                    )

                self.sensitivity = sensitivity_value
            except (IndexError, ValueError, TypeError) as e:
                raise ValueError(
                    f"Error al procesar parámetro sensitivity para DSI-PSO: {e}"
                ) from e

    @property
    def requires_particle_info(self) -> bool:
        """Esta estrategia requiere información específica de las partículas.

        Returns:
            bool: Siempre True para DSI-PSO
        """
        return True

    def collect_required_info(self, pso_state: Dict[str, Any]) -> Dict[str, Any]:
        """Recopila la información necesaria para la estrategia DSI-PSO.

        Args:
            pso_state (Dict[str, Any]): Diccionario con el estado actual del algoritmo PSO

        Returns:
            Dict[str, Any]: Diccionario con la información requerida por la estrategia

        Raises:
            ValueError: Si no se encuentran las partículas o la mejor solución global
        """
        particles = pso_state.get('particles', [])
        best_solution = pso_state.get('best_solution', None)

        if not particles or not best_solution:
            raise ValueError(
                "La estrategia DSI-PSO requiere acceso a las partículas y a la mejor solución global"
            )

        return {
            'best_positions_per_particle': [p.best_position for p in particles],
            'global_best_position': best_solution.position
        }

    def __call__(
        self,
        current_iteration: int,
        max_iterations: int,
        particle_info: dict = None
    ) -> np.ndarray:
        """Calcula el valor del peso inercial para cada partícula en la iteración actual.

        Args:
            current_iteration (int): Iteración actual del algoritmo
            max_iterations (int): Número máximo de iteraciones
            particle_info (dict, optional): Diccionario con información de las partículas:
                - 'best_positions_per_particle': Lista de mejores posiciones históricas de cada partícula
                - 'global_best_position': Mejor posición global del enjambre
                Defaults to None.

        Returns:
            np.ndarray: Array con los valores de peso inercial para cada partícula

        Raises:
            ValueError: Si no se proporciona la información requerida de las partículas
        """
        if (
            not particle_info or
            'best_positions_per_particle' not in particle_info or
            'global_best_position' not in particle_info
        ):
            raise ValueError(
                "La estrategia DSI-PSO requiere información de las partículas y posición global"
            )

        best_positions_per_particle = particle_info['best_positions_per_particle']
        global_best = particle_info['global_best_position']

        # Asegurar que no se divida por cero
        if max_iterations <= 1:
            return np.full(len(best_positions_per_particle), self.w_min)

        # Factor temporal: (Maxit - k) / Maxit
        time_factor = (max_iterations - current_iteration) / max_iterations

        # Distancia para cada partícula
        distances = []
        for best_pos in best_positions_per_particle:
            # D_i = |Gb - Pb_i| * time_factor
            abs_diff = np.abs(best_pos - global_best)
            distance = np.sum(abs_diff) * time_factor
            distances.append(distance)

        # array -> numpy
        distances = np.array(distances)

        # Calcular el peso inercial
        # wik = w_max / (w_min + e^(-sensitivity * D))
        weights = self.w_max / (self.w_min + np.exp(-self.sensitivity * distances))

        return weights
