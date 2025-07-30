"""Implementaciones específicas de funciones benchmark."""

# Importar todas las funciones benchmark para que se registren automáticamente
from .griewank import Griewank
from .rastrigin import Rastrigin
from .rosenbrock import Rosenbrock
from .sphere import Sphere

__all__ = ['Griewank', 'Rastrigin', 'Rosenbrock', 'Sphere']
