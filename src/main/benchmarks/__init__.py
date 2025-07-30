"""Paquete de funciones benchmark para algoritmos de optimización."""

from .benchmark_registry import BenchmarkRegistry
from .benchmark_factory import get_benchmark_function
from .benchmark_strategy import BenchmarkStrategy

# Importar funciones para que se registren automáticamente
from . import functions

__all__ = ['BenchmarkRegistry', 'get_benchmark_function', 'BenchmarkStrategy']
