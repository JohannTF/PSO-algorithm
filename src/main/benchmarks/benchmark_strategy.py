"""Estrategia base para funciones benchmark."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

import numpy as np


class BenchmarkStrategy(ABC):
    """Clase base abstracta para todas las funciones benchmark.

    Define la interfaz común que deben implementar todas las funciones de prueba.
    """

    def __init__(self, dimensions: int = 2,
                 bounds: Optional[Tuple[float, float]] = None) -> None:
        """Inicializa la función benchmark con dimensiones y límites.

        Args:
            dimensions (int): Número de dimensiones para la función.
            bounds (Optional[Tuple[float, float]]): Tupla (min, max) con los 
                límites.
        """
        self.bounds = bounds
        self.dimensions = dimensions
        self.global_optimum_position = self._get_global_optimum()
        self.global_optimum_value = self._evaluate(self.global_optimum_position)
        self.name = self.__class__.__name__

    @abstractmethod
    def _evaluate(self, x: np.ndarray) -> float:
        """Implementación de la función objetivo que evalúa un vector de posición.

        Args:
            x (np.ndarray): Vector de posición a evaluar.

        Returns:
            float: Valor de la función en la posición dada.
        """
        pass

    @abstractmethod
    def _get_global_optimum(self) -> np.ndarray:
        """Devuelve la posición del óptimo global para esta función benchmark.

        Returns:
            np.ndarray: Vector de posición del óptimo global.
        """
        pass

    def __call__(self, x: np.ndarray) -> float:
        """Permite que la instancia sea llamable directamente.

        Args:
            x (np.ndarray): Vector de posición a evaluar.

        Returns:
            float: Resultado de la evaluación.
        """
        # Verificar dimensiones
        if len(x) != self.dimensions:
            raise ValueError(
                f"La dimensión del vector de entrada ({len(x)}) no coincide "
                f"con la dimensión de la función ({self.dimensions})"
            )

        return self._evaluate(x)

    def get_info(self) -> Dict[str, Any]:
        """Devuelve información sobre la función benchmark.

        Returns:
            Dict[str, Any]: Diccionario con información de la función.
        """
        return {
            "name": self.name,
            "dimensions": self.dimensions,
            "bounds": self.bounds,
            "global_optimum_position": self.global_optimum_position.tolist(),
            "global_optimum_value": self.global_optimum_value,
        }

    def is_within_bounds(self, x: np.ndarray) -> bool:
        """Comprueba si un vector de posición está dentro de los límites.

        Args:
            x (np.ndarray): Vector de posición a comprobar.

        Returns:
            bool: True si está dentro de los límites, False en caso contrario.
        """
        lower_bound, upper_bound = self.bounds
        return np.all(x >= lower_bound) and np.all(x <= upper_bound)

    def __str__(self) -> str:
        """Representación en cadena de la función benchmark.

        Returns:
            str: Cadena descriptiva de la función.
        """
        return f"{self.name}(dimensions={self.dimensions}, bounds={self.bounds})"