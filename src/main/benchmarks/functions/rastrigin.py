"""Implementación de la función benchmark Rastrigin."""

from typing import Optional, Tuple

import numpy as np

from src.main.benchmarks.benchmark_registry import BenchmarkRegistry
from src.main.benchmarks.benchmark_strategy import BenchmarkStrategy


@BenchmarkRegistry.register("rastrigin")
class Rastrigin(BenchmarkStrategy):
    """Implementación de la función Rastrigin."""

    def __init__(self, dimensions: int,
                 bounds: Optional[Tuple[float, float]] = None) -> None:
        """Inicializa la función Rastrigin con dimensiones y límites.

        Args:
            dimensions (int): Número de dimensiones para la función.
            bounds (Optional[Tuple[float, float]]): Tupla (min, max) con límites.
        """
        # Los límites predeterminados para Rastrigin son [-5.12, 5.12]
        super().__init__(
            dimensions, 
            bounds if bounds is not None else (-5.12, 5.12)
        )

    def _evaluate(self, x: np.ndarray) -> float:
        """Evalúa la función Rastrigin en un punto.

        Args:
            x (np.ndarray): Vector de posición a evaluar.

        Returns:
            float: Valor de la función en la posición dada.
        """
        d = len(x)
        sum_term = np.sum(x**2 - 10 * np.cos(2 * np.pi * x))
        return 10 * d + sum_term

    def _get_global_optimum(self) -> np.ndarray:
        """Devuelve la posición del óptimo global para la función Rastrigin.

        Returns:
            np.ndarray: Vector de posición del óptimo global.
        """
        return np.zeros(self.dimensions)