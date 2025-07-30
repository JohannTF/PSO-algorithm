"""Validador de parámetros básicos del algoritmo PSO."""

from typing import Any, Dict, List

from src.main.benchmarks.benchmark_factory import get_benchmark_function
from src.main.config.validation.base_validator import BaseValidator
from src.main.config.validation.context import ValidationContext
from src.main.config.validation.pipeline.registry import validator


@validator()
class BasicParametersValidador(BaseValidator):
    """Validador para parámetros básicos del algoritmo PSO.
    
    Valida: dimensions, population_size, generations, runs, benchmark,
    bounds, velocity_bounds, benchmark_function.
    """
    
    def __init__(self) -> None:
        """Inicializa el validador de parámetros básicos."""
        super().__init__("basic_parameters")
    
    def validate(self, config: Dict[str, Any], 
                 context: ValidationContext) -> None:
        """Valida y establece los parámetros básicos en el contexto.
        
        Args:
            config: Configuración a validar.
            context: Contexto de validación a actualizar.
            
        Raises:
            ValueError: Si algún parámetro es inválido.
        """
        # Validar dimensions
        dimensions = config.get('dimensions')
        if dimensions is None:
            raise ValueError("Parameter 'dimensions' is required")
        if not isinstance(dimensions, int) or dimensions <= 0:
            raise ValueError(
                f"'dimensions' must be a positive integer, got: {dimensions}"
            )
        context.dimensions = dimensions
        
        # Validar population_size
        population_size = config.get('population_size')
        if population_size is None:
            raise ValueError("Parameter 'population_size' is required")
        if not isinstance(population_size, int) or population_size <= 0:
            raise ValueError(
                f"'population_size' must be a positive integer, "
                f"got: {population_size}"
            )
        context.population_size = population_size
        
        # Validar generations
        generations = config.get('generations')
        if generations is None:
            raise ValueError("Parameter 'generations' is required")
        if not isinstance(generations, int) or generations <= 0:
            raise ValueError(
                f"'generations' must be a positive integer, "
                f"got: {generations}"
            )
        context.generations = generations
        
        # Validar runs
        runs = config.get('runs')
        if runs is None:
            raise ValueError("Parameter 'runs' is required")
        if not isinstance(runs, int) or runs <= 0:
            raise ValueError(
                f"'runs' must be a positive integer, got: {runs}"
            )
        context.runs = runs
        
        # Validar benchmark
        benchmark = config.get('benchmark')
        if benchmark is None:
            raise ValueError("Parameter 'benchmark' is required")
        if not isinstance(benchmark, str):
            raise ValueError(
                f"'benchmark' must be a string, got: {type(benchmark)}"
            )
        
        # Validar bounds
        bounds_config = config.get('bounds')
        if bounds_config is not None:
            bounds = self._validate_bounds(
                bounds_config, dimensions, 'bounds', required=False
            )
        else:
            bounds = None
            
        # Generar función de benchmark
        try:
            benchmark_function = get_benchmark_function(
                benchmark, dimensions, bounds
            )
            context.benchmark = benchmark
            context.benchmark_function = benchmark_function
            
            # Si bounds era None, obtener los bounds por defecto
            if bounds is None:
                bounds = [
                    float(benchmark_function.bounds[0]), 
                    float(benchmark_function.bounds[1])
                ]
            
            context.bounds = bounds
        except Exception as e:
            raise ValueError(
                f"Invalid benchmark function '{benchmark}': {e}"
            ) from e
        
        # Validar velocity_bounds (opcional)
        velocity_bounds = config.get('velocity_bounds')        
        if velocity_bounds is not None:
            velocity_bounds = self._validate_bounds(
                velocity_bounds, dimensions, 'velocity_bounds', required=False
            )
        else:
            # Generar velocity_bounds automáticamente como 50% del rango
            bounds_range = bounds[1] - bounds[0]
            velocity_max = bounds_range * 0.5
            velocity_bounds = [-velocity_max, velocity_max]
        
        context.velocity_bounds = velocity_bounds
    
    def _validate_bounds(self, bounds: Any, dimensions: int, 
                        param_name: str, required: bool = True) -> List[float]:
        """Valida los bounds que se aplican a todas las dimensiones."""
        if bounds is None:
            if required:
                raise ValueError(f"Parameter '{param_name}' is required")
            return None
        
        if not isinstance(bounds, list):
            raise ValueError(
                f"'{param_name}' must be a list, got: {type(bounds)}"
            )
        
        if len(bounds) != 2:
            raise ValueError(
                f"'{param_name}' must have exactly 2 elements [min, max], "
                f"got: {len(bounds)}"
            )
        
        try:
            min_val, max_val = float(bounds[0]), float(bounds[1])
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"'{param_name}' elements must be numeric, got: {bounds}"
            ) from e
        
        if min_val >= max_val:
            raise ValueError(
                f"'{param_name}' min value must be less than max value, "
                f"got: min={min_val}, max={max_val}"
            )
        
        return [min_val, max_val]
