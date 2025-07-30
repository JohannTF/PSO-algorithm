"""Implementación de la estrategia de coeficiente aleatorio."""

import numpy as np

from src.main.algorithm.coefficient.coefficient_strategy import CoefficientStrategy


class RandomCoefficient(CoefficientStrategy):
    """Estrategia que genera un valor aleatorio para el coeficiente.
    
    Genera un valor aleatorio dentro de un rango especificado.
    """

    def __init__(self, min_value: float, max_value: float) -> None:
        """Inicializa la estrategia de coeficiente aleatorio.

        Args:
            min_value (float): Valor mínimo del coeficiente.
            max_value (float): Valor máximo del coeficiente.
        """
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, current_iteration: int, max_iterations: int) -> float:
        """Genera un único valor aleatorio para el coeficiente.

        Args:
            current_iteration (int): Iteración actual (no utilizado).
            max_iterations (int): Número máximo de iteraciones (no utilizado).

        Returns:
            float: Un único valor aleatorio para usar como coeficiente.
        """
        return np.random.uniform(self.min_value, self.max_value)

    def __str__(self) -> str:
        """Representación en cadena del coeficiente aleatorio.

        Returns:
            str: Descripción del coeficiente aleatorio.
        """
        return f"RandomCoefficient(min={self.min_value}, max={self.max_value})"
