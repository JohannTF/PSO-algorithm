"""Validador de estrategias de inercia con dependencia de parámetros básicos."""

from typing import Dict, Any, Union, List, Tuple
import logging

from src.main.algorithm.inertia.inertia_factory import get_inertia_strategy
from src.main.config.validation.pipeline.registry import validator
from src.main.config.validation.base_validator import BaseValidator
from src.main.config.validation.context import ValidationContext


@validator(dependencies=["basic_parameters"])
class InertiaValidador(BaseValidator):
    """Validador para estrategias de peso inercial.
    
    Valida el parámetro inertia_type en formato:
    - Número constante o [w_min, w_max, "strategy", ...params]
    """
    
    # Rangos válidos para pesos de inercia
    MIN_INERTIA = 0.2
    MAX_INERTIA = 0.9
    
    def __init__(self):
        super().__init__("inertia")
    
    def validate(self, config: Dict[str, Any], 
                 context: ValidationContext) -> None:
        """Valida la estrategia de inercia y sus parámetros."""
        # Verificar que las dependencias están satisfechas
        if context.generations is None:
            raise ValueError(
                "Inertia validator requires basic_parameters to be validated first"
            )
        
        # Obtener inertia_type con valor por defecto
        inertia_type = config.get(
            'inertia_type', 
            [self.MIN_INERTIA, self.MAX_INERTIA, "linear_decreasing"]
        )
        
        # Validar formato del inertia_type
        validated_inertia = self._validate_inertia_format(inertia_type)
        
        # Crear estrategia usando el factory
        try:
            strategy = get_inertia_strategy(validated_inertia)
        except Exception as e:
            raise ValueError(f"Failed to create inertia strategy: {e}") from e
        
        # Establecer en contexto
        context.inertia_strategy = strategy
        context.inertia_type = validated_inertia
    
    def _validate_inertia_format(self, inertia_type: Any) -> Union[float, Tuple]:
        """Valida el formato del inertia_type según las especificaciones.
        
        Args:
            inertia_type: Valor del inertia_type a validar
            
        Returns:
            Valor validado en formato apropiado
            
        Raises:
            ValueError: Si el formato es inválido
        """
        # Caso 1: Valor constante
        if isinstance(inertia_type, (int, float)):
            value = float(inertia_type)
            if not (self.MIN_INERTIA <= value <= self.MAX_INERTIA):
                raise ValueError(
                    f"Inertia value must be between {self.MIN_INERTIA} and "
                    f"{self.MAX_INERTIA}, got: {value}"
                )
            return value
        
        # Caso 2: Lista/tupla con estrategia dinámica
        if isinstance(inertia_type, (list, tuple)):
            if len(inertia_type) < 2:
                raise ValueError(
                    f"Inertia list must have at least 2 elements [w_min, w_max], "
                    f"got: {len(inertia_type)}"
                )
            
            # Validar valores mínimo y máximo
            try:
                w_min = float(inertia_type[0])
                w_max = float(inertia_type[1])
            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"Inertia min and max values must be numeric, "
                    f"got: {inertia_type[:2]}"
                ) from e
            
            # Validar rangos
            if not (self.MIN_INERTIA <= w_min <= self.MAX_INERTIA):
                raise ValueError(
                    f"Inertia min value must be between {self.MIN_INERTIA} and "
                    f"{self.MAX_INERTIA}, got: {w_min}"
                )
            if not (self.MIN_INERTIA <= w_max <= self.MAX_INERTIA):
                raise ValueError(
                    f"Inertia max value must be between {self.MIN_INERTIA} and "
                    f"{self.MAX_INERTIA}, got: {w_max}"
                )
            if w_min > w_max:
                raise ValueError(
                    f"Inertia min value must be <= max value, "
                    f"got: {w_min} > {w_max}"
                )
            
            # Validar estrategia (opcional, por defecto "linear_decreasing")
            if len(inertia_type) > 2:
                if not isinstance(inertia_type[2], str):
                    raise ValueError(
                        f"Inertia strategy must be a string, "
                        f"got: {type(inertia_type[2])}"
                    )
                strategy = inertia_type[2].lower()
            
            # Los parámetros específicos se validan en la clase correspondiente
            return list(inertia_type)
        
        # Caso 3: Formato no soportado
        raise ValueError(
            f"Inertia type must be a number or list [w_min, w_max, strategy, ...], "
            f"got: {type(inertia_type)}"
        )
