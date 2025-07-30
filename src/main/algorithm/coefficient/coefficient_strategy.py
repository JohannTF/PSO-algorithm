"""Clase base para todas las estrategias de coeficientes."""

from abc import ABC, abstractmethod


class CoefficientStrategy(ABC):
    """Clase base abstracta para estrategias de coeficientes."""

    @abstractmethod
    def __call__(self, current_iteration: int, max_iterations: int) -> float:
        """Calcula el valor del coeficiente para la iteración actual.

        Args:
            current_iteration (int): Iteración actual.
            max_iterations (int): Número máximo de iteraciones.

        Returns:
            float: El valor calculado para la iteración actual.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Representación en cadena de la estrategia.

        Returns:
            str: Representación en cadena.
        """
        pass
