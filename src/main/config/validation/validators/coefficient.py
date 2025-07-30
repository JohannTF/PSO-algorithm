"""Validador de coeficientes de aceleración con dependencia de parámetros básicos."""

from typing import Dict, Any, Union, List, Tuple

from src.main.config.validation.pipeline.registry import validator
from src.main.config.validation.base_validator import BaseValidator
from src.main.config.validation.context import ValidationContext
from src.main.algorithm.coefficient.coefficient_factory import (
    get_coefficient_strategy
)


@validator(dependencies=["basic_parameters"])
class CoefficientValidador(BaseValidator):
    """Validador para estrategias de coeficientes de aceleración (c1 y c2).
    
    Valida los coeficientes según el formato:
    - c1: número constante o [min, max, "strategy"]
    - c2: número constante o [min, max, "strategy"]

    Depende de: basic_parameters
    """
    
    def __init__(self):
        super().__init__("coefficient")
    
    def validate(self, config: Dict[str, Any], 
                 context: ValidationContext) -> None:
        """Valida las estrategias de coeficientes y sus parámetros."""
        # Verificar que las dependencias están satisfechas
        if context.generations is None:
            raise ValueError(
                "Coefficient validator requires basic_parameters to be "
                "validated first"
            )
        
        # Validar coeficiente c1
        self._validate_coefficient(config, context, "c1")
        
        # Validar coeficiente c2
        self._validate_coefficient(config, context, "c2")
    
    def _validate_coefficient(self, config: Dict[str, Any], 
                             context: ValidationContext,
                             coeff_type: str) -> None:
        
        """Valida un coeficiente específico (c1 o c2).
        
        Args:
            config: Configuración original
            context: Contexto a actualizar
            coeff_type: Tipo de coeficiente ("c1" o "c2")
            
        Raises:
            ValueError: Si el coeficiente es inválido
        """
        coeff_value = config.get(coeff_type)
        if coeff_value is None:
            raise ValueError(f"Parameter '{coeff_type}' is required")
        
        # Validar formato del coeficiente
        validated_config_coefficient = self._validate_coefficient_format(
            coeff_value, coeff_type
        )
        
        # Crear estrategia usando el factory
        try:
            strategy = get_coefficient_strategy(validated_config_coefficient)
        except Exception as e:
            raise ValueError(
                f"Failed to create {coeff_type} strategy: {e}"
            ) from e
        
        # Establecer en contexto
        if coeff_type == "c1":
            context.c1_strategy = strategy
            context.c1 = validated_config_coefficient
        else:
            context.c2_strategy = strategy
            context.c2 = validated_config_coefficient
    
    def _validate_coefficient_format(self, coeff_value: Any, 
                                   coeff_type: str) -> Union[float, Tuple]:
        
        """Valida el formato del coeficiente según las especificaciones.
        
        Args:
            coeff_value: Valor del coeficiente a validar
            coeff_type: Tipo de coeficiente para mensajes de error
            
        Returns:
            Valor validado en formato apropiado
            
        Raises:
            ValueError: Si el formato es inválido
        """
        # Caso 1: Valor constante
        if isinstance(coeff_value, (int, float)):
            value = float(coeff_value)
            if value < 0:
                raise ValueError(
                    f"'{coeff_type}' must be non-negative, got: {value}"
                )
            return value
        
        # Caso 2: Lista/tupla con estrategia dinámica
        if isinstance(coeff_value, (list, tuple)):
            if len(coeff_value) < 2:
                raise ValueError(
                    f"'{coeff_type}' list must have at least 2 elements "
                    f"[min, max], got: {len(coeff_value)}"
                )
            
            # Validar valores mínimo y máximo
            try:
                min_val = float(coeff_value[0])
                max_val = float(coeff_value[1])
            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"'{coeff_type}' min and max values must be numeric, "
                    f"got: {coeff_value[:2]}"
                ) from e
            
            if min_val < 0:
                raise ValueError(
                    f"'{coeff_type}' min value must be non-negative, "
                    f"got: {min_val}"
                )
            if max_val < 0:
                raise ValueError(
                    f"'{coeff_type}' max value must be non-negative, "
                    f"got: {max_val}"
                )
            if min_val > max_val:
                raise ValueError(
                    f"'{coeff_type}' min value must be <= max value, "
                    f"got: {min_val} > {max_val}"
                )
            
            # Validar estrategia (opcional, por defecto "linear_decreasing")
            strategy = "linear_decreasing"  # Valor por defecto
            if len(coeff_value) > 2:
                if not isinstance(coeff_value[2], str):
                    raise ValueError(
                        f"'{coeff_type}' strategy must be a string, "
                        f"got: {type(coeff_value[2])}"
                    )
            
            return [min_val, max_val, strategy]
        
        # Caso 3: Formato no soportado
        raise ValueError(
            f"'{coeff_type}' must be a number or list [min, max, strategy], "
            f"got: {type(coeff_value)}"
        )
