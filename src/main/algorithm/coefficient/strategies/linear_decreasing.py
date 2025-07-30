"""Implementación de la estrategia de coeficiente linealmente decreciente."""

from src.main.algorithm.coefficient.coefficient_strategy import CoefficientStrategy


class LinearDecreasingCoefficient(CoefficientStrategy):
    """Estrategia que disminuye linealmente el coeficiente."""

    def __init__(self, start_value: float, end_value: float) -> None:
        """Inicializa la estrategia de coeficiente decreciente.

        Args:
            start_value (float): Valor inicial del coeficiente.
            end_value (float): Valor final del coeficiente.
        """
        self.start_value = start_value
        self.end_value = end_value

    def __call__(self, current_iteration: int, max_iterations: int) -> float:
        """Calcula el valor del coeficiente para la iteración actual.

        Args:
            current_iteration (int): Iteración actual.
            max_iterations (int): Número máximo de iteraciones.

        Returns:
            float: El valor calculado para la iteración actual.
        """
        if max_iterations <= 1:
            return self.end_value

        # Calcular el valor decreciente linealmente
        value = self.start_value + (self.end_value - self.start_value) * (
            current_iteration / (max_iterations - 1)
        )
        return value

    def __str__(self) -> str:
        """Representación en cadena del coeficiente decreciente.

        Returns:
            str: Descripción del coeficiente decreciente.
        """
        return (f"LinearDecreasingCoefficient(start={self.start_value}, "
                f"end={self.end_value})")
