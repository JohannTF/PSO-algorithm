"""Clase base para el sistema de validación."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Set

from src.main.config.validation.context import ValidationContext


class BaseValidator(ABC):
    """Clase base para validadores."""
    
    def __init__(self, name: str) -> None:
        """Inicializa el validador.
        
        Args:
            name: Nombre del validador para identificación.
        """
        self.name = name
        self._dependencies: Set[str] = set()
    
    @property
    def dependencies(self) -> Set[str]:
        """Retorna el conjunto de dependencias de este validador."""
        return self._dependencies.copy()
    
    def add_dependency(self, validator_name: str) -> None:
        """Agrega una dependencia a este validador.
        
        Args:
            validator_name: Nombre del validador del que depende.
        """
        self._dependencies.add(validator_name)
    
    def depends_on(self, *validator_names: str) -> 'BaseValidator':
        """Método fluido para establecer dependencias.
        
        Args:
            validator_names: Nombres de los validadores de los que depende.
            
        Returns:
            Self para encadenamiento.
        """
        for name in validator_names:
            self.add_dependency(name)
        return self
    
    @abstractmethod
    def validate(self, config: Dict[str, Any], context: ValidationContext) -> None:
        """Valida la configuración y actualiza el contexto.
        
        Args:
            config: Configuración original a validar.
            context: Contexto de validación a actualizar.
            
        Raises:
            ValueError: Si la validación falla.
        """
        pass
