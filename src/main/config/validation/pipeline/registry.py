"""Registro de validadores con decorador para auto-registro."""

from typing import List, Type, Dict
from functools import wraps

from src.main.config.validation.base_validator import BaseValidator

_REGISTERED_VALIDATORS: Dict[str, Type[BaseValidator]] = {}


def validator(dependencies: List[str] = None):
    """Decorador para auto-registrar validadores con dependencias opcionales.
    
    Args:
        dependencies: Lista de nombres de validadores de los que depende
        
    Returns:
        Decorador que registra la clase
    """
    def decorator(cls: Type[BaseValidator]):
        temp_instance = cls()
        _REGISTERED_VALIDATORS[temp_instance.name] = cls

        if dependencies:
            original_init = cls.__init__
            
            @wraps(original_init)
            def enhanced_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                for dep in dependencies:
                    self.depends_on(dep)
            cls.__init__ = enhanced_init

        return cls
    return decorator


def get_registered_validators() -> Dict[str, Type[BaseValidator]]:
    """Retorna copia de todos los validadores registrados."""
    return _REGISTERED_VALIDATORS.copy()
