"""Módulo con estrategias de peso inercial convexas."""

from src.main.algorithm.inertia.strategies.convex.decreasing import ConvexDecreasing
from src.main.algorithm.inertia.strategies.convex.exp_decreasing import ConvexExponentialDecreasing
from src.main.algorithm.inertia.strategies.convex.exp_increasing import ConvexExponentialIncreasing

__all__ = [
    "ConvexDecreasing",
    "ConvexExponentialDecreasing", 
    "ConvexExponentialIncreasing"
]
