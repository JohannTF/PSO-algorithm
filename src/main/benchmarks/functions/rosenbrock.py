"""Implementación de la función benchmark Rosenbrock."""

from typing import Optional, Tuple

import numpy as np

from src.main.benchmarks.benchmark_registry import BenchmarkRegistry
from src.main.benchmarks.benchmark_strategy import BenchmarkStrategy


@BenchmarkRegistry.register("rosenbrock")
class Rosenbrock(BenchmarkStrategy):
    """Implementación de la función Rosenbrock."""

    def __init__(self, dimensions: int,
                 bounds: Optional[Tuple[float, float]] = None) -> None:
        """Inicializa la función Rosenbrock con dimensiones y límites.

        Args:
            dimensions (int): Número de dimensiones para la función.
            bounds (Optional[Tuple[float, float]]): Tupla (min, max) con límites.
        """
        # Los límites típicos para Rosenbrock son más amplios
        super().__init__(
            dimensions, 
            bounds if bounds is not None else (-2.048, 2.048)
        )

    def _evaluate(self, x: np.ndarray) -> float:
        """Evalúa la función Rosenbrock en un punto.

        Args:
            x (np.ndarray): Vector de posición a evaluar.

        Returns:
            float: Valor de la función en la posición dada.
        """
        sum_value = 0.0
        for i in range(len(x) - 1):
            sum_value += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1) ** 2
        return sum_value

    def _get_global_optimum(self) -> np.ndarray:
        """Devuelve la posición del óptimo global para la función Rosenbrock.

        Returns:
            np.ndarray: Vector de posición del óptimo global (en [1,1,...,1]).
        """
        return np.ones(self.dimensions)