"""Implementación de la función benchmark Griewank."""

from typing import Optional, Tuple

import numpy as np

from src.main.benchmarks.benchmark_registry import BenchmarkRegistry
from src.main.benchmarks.benchmark_strategy import BenchmarkStrategy


@BenchmarkRegistry.register("griewank")
class Griewank(BenchmarkStrategy):
    """Implementación de la función Griewank."""

    def __init__(self, dimensions: int,
                 bounds: Optional[Tuple[float, float]] = None) -> None:
        """Inicializa la función Griewank con dimensiones y límites.

        Args:
            dimensions (int): Número de dimensiones para la función.
            bounds (Optional[Tuple[float, float]]): Tupla (min, max) con límites.
        """
        super().__init__(
            dimensions, 
            bounds if bounds is not None else (-100.0, 100.0)
        )

    def _evaluate(self, x: np.ndarray) -> float:
        """Evalúa la función Griewank en un punto.

        Args:
            x (np.ndarray): Vector de posición a evaluar.

        Returns:
            float: Valor de la función en la posición dada.
        """
        sum_part = np.sum(x**2) / 4000.0

        # Calcular el producto de los cosenos
        prod_part = 1.0
        for i in range(len(x)):
            prod_part *= np.cos(x[i] / np.sqrt(i + 1))

        return 1.0 + sum_part - prod_part

    def _get_global_optimum(self) -> np.ndarray:
        """Devuelve la posición del óptimo global para la función Griewank.

        Returns:
            np.ndarray: Vector de posición del óptimo global.
        """
        return np.zeros(self.dimensions)