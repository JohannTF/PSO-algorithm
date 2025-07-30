"""Módulo con estrategias básicas de peso inercial."""

from src.main.algorithm.inertia.strategies.basic.constant import Constant
from src.main.algorithm.inertia.strategies.basic.linear_decreasing import (
    LinearDecreasing
)
from src.main.algorithm.inertia.strategies.basic.random import Random

__all__ = ["Constant", "LinearDecreasing", "Random"]
