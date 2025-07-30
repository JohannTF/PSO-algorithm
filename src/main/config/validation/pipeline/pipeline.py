"""Pipeline de validación con registro automático integrado.

Maneja el orden de ejecución basado en dependencias sin archivos auxiliares.
"""

from typing import Dict, Any, List
from collections import defaultdict, deque
import logging

from src.main.config.validation.base_validator import BaseValidator
from src.main.config.validation.context import ValidationContext
from src.main.config.validation.pipeline.registry import get_registered_validators

logger = logging.getLogger(__name__)


class ValidationPipeline:
    """Pipeline de validación que maneja dependencias entre validadores.
    
    Utiliza ordenamiento topológico para ejecutar validadores en orden correcto.
    """
    
    def __init__(self):
        """Inicializa el pipeline vacío."""
        self._validators: Dict[str, BaseValidator] = {}
        self._execution_order: List[str] = []
        self._dependencies_resolved = False
    
    def add_validator(self, validator: BaseValidator) -> None:
        """Agrega un validador al pipeline verificando que no exista previamente.
        
        Args:
            validator: Instancia del validador a agregar
        """
        if validator.name in self._validators:
            raise ValueError(f"Validator '{validator.name}' already exists in pipeline")
        self._validators[validator.name] = validator
    
    def _resolve_dependencies(self) -> None:
        """Resuelve dependencias y calcula orden de ejecución.
        
        Utiliza ordenamiento topológico (algoritmo de Kahn).
        """
        # Verificar que todas las dependencias existen
        for validator_name, validator in self._validators.items():
            for dep in validator.dependencies:
                if dep not in self._validators:
                    raise ValueError(
                        f"Validator '{validator_name}' depends on '{dep}' which doesn't exist"
                    )
        
        # Algoritmo de Kahn para ordenamiento topológico
        in_degree = defaultdict(int)
        graph = defaultdict(list)
        
        # Construir grafo y calcular grados de entrada
        for validator_name in self._validators:
            in_degree[validator_name] = 0
        
        for validator_name, validator in self._validators.items():
            for dep in validator.dependencies:
                graph[dep].append(validator_name)
                in_degree[validator_name] += 1
        
        # Encontrar nodos sin dependencias
        queue = deque([name for name in self._validators if in_degree[name] == 0])
        execution_order = []
        
        while queue:
            current = queue.popleft()
            execution_order.append(current)
            
            # Reducir grado de entrada de vecinos
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Verificar dependencias circulares
        if len(execution_order) != len(self._validators):
            remaining = set(self._validators.keys()) - set(execution_order)
            raise ValueError(f"Circular dependencies detected among validators: {remaining}")
        
        self._execution_order = execution_order
        self._dependencies_resolved = True
        
        logger.info(f"Resolved execution order: {' -> '.join(execution_order)}")    
    
    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta validación completa de la configuración.
        
        Args:
            config: Configuración a validar
            
        Returns:
            Configuración validada
        """
        if not self._validators:
            logger.warning("No validators in pipeline, returning original config")
            return config.copy()
        
        # Resolver dependencias si es necesario
        if not self._dependencies_resolved:
            self._resolve_dependencies()
        
        # Crear contexto de validación
        context = ValidationContext()
                
        for validator_name in self._execution_order:
            validator = self._validators[validator_name]
            
            try:
                validator.validate(config, context)                
            except Exception as e:
                raise ValueError(f"Validation failed at '{validator_name}': {e}") from e
        
        # Retornar configuración validada
        validated_config = context.get_validated_config()
                
        return validated_config


def create_pipeline() -> ValidationPipeline:
    """Crea pipeline con todos los validadores registrados."""
    pipeline = ValidationPipeline()
    for validator_class in get_registered_validators().values():
        pipeline.add_validator(validator_class())
    return pipeline
