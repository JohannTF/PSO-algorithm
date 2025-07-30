"""Módulo para registrar y obtener funciones benchmark."""

from typing import Dict, Optional, Tuple, Type

from src.main.benchmarks.benchmark_strategy import BenchmarkStrategy


class BenchmarkRegistry:
    """Registro central de funciones benchmark disponibles."""
    
    # Diccionario que mapea nombres de funciones a sus clases
    _benchmark_functions: Dict[str, Type[BenchmarkStrategy]] = {}
    
    @classmethod
    def register(cls, name: str):
        """Decorador para registrar una función benchmark.
        
        Args:
            name (str): Nombre identificador de la función benchmark.
            
        Returns:
            Callable: Decorador que registra la clase.
        """
        def decorator(benchmark_class: Type[BenchmarkStrategy]):
            cls._benchmark_functions[name] = benchmark_class
            return benchmark_class
        return decorator
    
    @classmethod
    def create_benchmark(cls, name: str, dimensions: int, 
                        bounds: Optional[Tuple[float, float]] = None
                        ) -> BenchmarkStrategy:
        """Crea una instancia de la función benchmark especificada.
        
        Args:
            name (str): Nombre de la función benchmark.
            dimensions (int): Número de dimensiones para la función.
            bounds (Optional[Tuple[float, float]]): Límites del espacio de búsqueda.
            
        Returns:
            BenchmarkStrategy: Instancia de la función benchmark.
            
        Raises:
            KeyError: Si la función benchmark no está registrada.
        """
        if name not in cls._benchmark_functions:
            raise KeyError(
                f"No se encontró una función benchmark con nombre '{name}'. "
                f"Opciones disponibles: {list(cls._benchmark_functions.keys())}"
            )
        
        return cls._benchmark_functions[name](dimensions=dimensions, bounds=bounds)
    
    @classmethod
    def get_available_benchmarks(cls) -> Dict[str, str]:
        """Devuelve un diccionario con los nombres de las funciones disponibles.
        
        Returns:
            Dict[str, str]: Diccionario con nombre -> descripción de cada función
        """
        return {
            name: benchmark_class.__doc__ or name 
            for name, benchmark_class in cls._benchmark_functions.items()
        }
    
    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Verifica si una función benchmark está registrada.
        
        Args:
            name (str): Nombre de la función benchmark
            
        Returns:
            bool: True si está registrada, False en caso contrario
        """
        return name in cls._benchmark_functions
    
    @classmethod
    def get_all_benchmarks(cls) -> Dict[str, Type[BenchmarkStrategy]]:
        """Devuelve todas las funciones benchmark registradas.
        
        Returns:
            Dict[str, Type[BenchmarkStrategy]]: Diccionario con todas las funciones
        """
        return cls._benchmark_functions.copy()
    
    @classmethod
    def clear_registrations(cls) -> None:
        """Limpia todas las registraciones (útil para pruebas)."""
        cls._benchmark_functions.clear()
