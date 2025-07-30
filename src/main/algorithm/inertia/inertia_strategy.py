"""Clase base para todas las estrategias de peso inercial."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

import numpy as np


class InertiaStrategy(ABC):
    """Clase base abstracta para estrategias de peso inercial."""

    @abstractmethod
    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: Optional[dict] = None) -> Union[float, np.ndarray]:
        """Calcula el valor del peso inercial para la iteración actual.

        Args:
            current_iteration (int): Iteración actual.
            max_iterations (int): Número máximo de iteraciones.
            particle_info (Optional[dict], optional): Diccionario opcional con
                información adicional de las partículas según lo requerido por
                la estrategia. Defaults to None.

        Returns:
            Union[float, np.ndarray]: Un valor único de peso inercial para toda
                la población, o un array con valores específicos para cada
                partícula.
        """
        pass

    def collect_required_info(self, pso_state: Dict[str, Any]) -> Dict[str, Any]:
        """Recopila la información necesaria para esta estrategia.

        Cada estrategia que requiera información específica debe sobrescribir
        este método.

        Args:
            pso_state (Dict[str, Any]): Diccionario con el estado actual del
                algoritmo PSO, que incluye:
                - 'particles': Lista de todas las partículas
                - 'best_solution': Mejor solución global encontrada
                - 'iteration': Iteración actual
                - 'generations': Número total de generaciones
                - otros parámetros específicos del algoritmo

        Returns:
            Dict[str, Any]: Diccionario con la información requerida por la
                estrategia.
        """
        return {}

    @property
    def requires_particle_info(self) -> bool:
        """Indica si esta estrategia requiere información específica.

        Por defecto, las estrategias clásicas no requieren esta información.

        Returns:
            bool: True si la estrategia necesita información de las partículas,
                False en caso contrario.
        """
        return False

    @property
    def returns_array(self) -> bool:
        """Indica si esta estrategia devuelve un array de valores.

        Returns:
            bool: True si la estrategia devuelve un array (un valor por
                partícula), False si devuelve un único valor para toda la
                población.
        """
        return self.requires_particle_info
