"""Módulo para cargar funciones benchmark dinámicamente."""

from typing import Callable, Optional, Tuple

import numpy as np

from src.main.benchmarks.benchmark_registry import BenchmarkRegistry


def get_benchmark_function(
    benchmark_name: str, 
    dimensions: int, 
    bounds: Optional[Tuple[float, float]] = None
) -> Callable[[np.ndarray], float]:
    """Carga dinámicamente una función benchmark basada en su nombre.

    Args:
        benchmark_name (str): Nombre de la función benchmark a cargar.
        dimensions (int): Número de dimensiones para la función.
        bounds (Optional[Tuple[float, float]]): Límites del espacio de búsqueda.

    Returns:
        Callable[[np.ndarray], float]: Función callable que evalúa una posición.

    Raises:
        ValueError: Si no se encuentra la función benchmark.
    """
    try:
        # Convertir nombre a formato de registro (lowercase)
        registry_name = benchmark_name.lower()
        
        # Crear instancia usando el registro
        benchmark_instance = BenchmarkRegistry.create_benchmark(
            name=registry_name, 
            dimensions=dimensions, 
            bounds=bounds
        )
        
        # Devolver la instancia (que es callable)
        return benchmark_instance

    except KeyError as e:
        available = list(BenchmarkRegistry.get_available_benchmarks().keys())
        raise ValueError(
            f"Error al cargar la función benchmark '{benchmark_name}': {str(e)}. "
            f"Funciones disponibles: {available}"
        ) from e
