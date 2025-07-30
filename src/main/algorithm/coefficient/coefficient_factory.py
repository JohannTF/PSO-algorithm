"""Módulo para cargar estrategias de coeficientes para algoritmos de optimización."""

from typing import Tuple, Union

from src.main.algorithm.coefficient.coefficient_strategy import CoefficientStrategy
from src.main.algorithm.coefficient.strategies import *


def get_coefficient_strategy(
    config: Union[float, Tuple[float, float, str]]
) -> CoefficientStrategy:
    """Obtiene una estrategia de coeficiente basada en la configuración.

    Args:
        config (Union[float, Tuple[float, float, str]]): Puede ser un número 
            (valor constante) o una tupla (min, max, tipo) donde 'tipo' puede 
            ser 'decreasing', 'increasing', o 'random'.

    Returns:
        CoefficientStrategy: Función de estrategia para el coeficiente.

    Raises:
        ValueError: Si la configuración no es soportada.
    """
    if isinstance(config, (int, float)):
        return ConstantCoefficient(float(config))

    if isinstance(config, (list, tuple)) and len(config) >= 2:
        min_val, max_val = config[0], config[1]

        # Si se especifica un tipo, usarlo; de lo contrario, usar aleatorio
        strategy_type = config[2] if len(config) > 2 else "random"

        if strategy_type.lower() == "decreasing":
            return LinearDecreasingCoefficient(max_val, min_val)
        elif strategy_type.lower() == "increasing":
            return LinearIncreasingCoefficient(min_val, max_val)
        else:  # Default to random
            return RandomCoefficient(min_val, max_val)

    raise ValueError(f"Configuración de coeficiente no soportada: {config}")
