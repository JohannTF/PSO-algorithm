"""Implementación de la función Sphere."""

import numpy as np

from src.main.benchmarks.benchmark_registry import BenchmarkRegistry
from src.main.benchmarks.benchmark_strategy import BenchmarkStrategy


@BenchmarkRegistry.register("sphere")
class Sphere(BenchmarkStrategy):
    """Implementación de la función Sphere."""

    def __init__(self, dimensions, bounds=None) -> None:
        """Inicializa la función Sphere con dimensiones y límites.

        Args:
            dimensions (int): Número de dimensiones para la función.
            bounds (Optional[Tuple[float, float]]): Tupla (min, max) con límites.
        """
        # Los límites predeterminados para Sphere son [-100, 100]
        super().__init__(
            dimensions,
            bounds if bounds is not None else (-100.0, 100.0)
        )

    def _evaluate(self, x: np.ndarray) -> float:
        """Evalúa la función Sphere en un punto.

        Args:
            x (np.ndarray): Vector de posición a evaluar.

        Returns:
            float: Valor de la función en la posición dada.
        """
        return np.sum(x**2)

    def _get_global_optimum(self) -> np.ndarray:
        """Devuelve la posición del óptimo global para la función Sphere.

        Returns:
            np.ndarray: Vector de posición del óptimo global.
        """
        return np.zeros(self.dimensions)