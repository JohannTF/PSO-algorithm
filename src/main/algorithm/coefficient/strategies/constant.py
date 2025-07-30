"""Implementación de la estrategia de coeficiente constante."""

from src.main.algorithm.coefficient.coefficient_strategy import CoefficientStrategy


class ConstantCoefficient(CoefficientStrategy):
    """Estrategia que mantiene un coeficiente constante."""

    def __init__(self, value: float) -> None:
        """Inicializa el coeficiente constante.

        Args:
            value (float): Valor constante del coeficiente.
        """
        self.value = value

    def __call__(self, current_iteration: int, max_iterations: int) -> float:
        """Devuelve el valor constante.

        Args:
            current_iteration (int): Iteración actual (no utilizado).
            max_iterations (int): Número máximo de iteraciones (no utilizado).

        Returns:
            float: El valor constante del coeficiente.
        """
        return self.value

    def __str__(self) -> str:
        """Representación en cadena del coeficiente constante.

        Returns:
            str: Descripción del coeficiente constante.
        """
        return f"ConstantCoefficient(value={self.value})"
