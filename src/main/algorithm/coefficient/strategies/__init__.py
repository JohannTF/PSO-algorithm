"""Módulo con las implementaciones de estrategias de coeficientes."""

from src.main.algorithm.coefficient.strategies.constant import ConstantCoefficient
from src.main.algorithm.coefficient.strategies.linear_decreasing import LinearDecreasingCoefficient
from src.main.algorithm.coefficient.strategies.linear_increasing import LinearIncreasingCoefficient
from src.main.algorithm.coefficient.strategies.random import RandomCoefficient

__all__ = [
    "ConstantCoefficient",
    "LinearDecreasingCoefficient",
    "LinearIncreasingCoefficient",
    "RandomCoefficient",
]
