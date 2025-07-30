"""Validador de configuración de visualización con dependencia de parámetros básicos."""

from typing import Dict, Any, List, Union
import logging

from src.main.config.validation.pipeline.registry import validator
from src.main.config.validation.base_validator import BaseValidator
from src.main.config.validation.context import ValidationContext
from src.main.utils.constants import SINGLE_RUN_GRAPHS, MULTI_RUN_GRAPHS

logger = logging.getLogger(__file__)


@validator(dependencies=["basic_parameters"])
class VisualizationValidador(BaseValidator):
    """Validador para configuración de visualización.
    
    Valida: single_run_visualization, multi_run_visualization,
    show_individual_visualizations, save_individual_visualizations,
    show_multiple_visualizations, save_multiple_visualizations.
    
    Depende de: basic_parameters
    """
    
    def __init__(self):
        super().__init__("visualization")
    
    def validate(self, config: Dict[str, Any], 
                 context: ValidationContext) -> None:
        """Valida la configuración de visualización.
        
        Args:
            config: Configuración original
            context: Contexto con parámetros básicos ya validados
        
        Raises:
            ValueError: Si la configuración de visualización es inválida
        """
     
        # Verificar que las dependencias están satisfechas
        if context.runs is None or context.dimensions is None:
            raise ValueError(
                "Visualization validator requires basic_parameters to be "
                "validated first"
            )
        
        # Validar single_run_visualization (puede ser bool o dict)
        single_run_viz = config.get('single_run_visualization')
        if single_run_viz is not None:
            context.single_run_visualization = self._validate_visualization_config(
                single_run_viz, SINGLE_RUN_GRAPHS, "single_run_visualization", 
                context.dimensions
            )
        else:
            # Si no se especifica, crear dict con todas las opciones en False
            context.single_run_visualization = {
                viz_type: False for viz_type in SINGLE_RUN_GRAPHS
            }
        
        # Validar multi_run_visualization (puede ser bool o dict)
        multi_run_viz = config.get('multi_run_visualization')
        if multi_run_viz is not None:
            # Advertir si se especifica multi_run pero hay solo 1 run
            if isinstance(multi_run_viz, bool) and multi_run_viz and context.runs <= 1:
                logger.warning("multi_run_visualization is True but runs <= 1")
            elif isinstance(multi_run_viz, dict) and context.runs <= 1:
                logger.warning("multi_run_visualization specified but runs <= 1")
            
            context.multi_run_visualization = self._validate_visualization_config(
                multi_run_viz, MULTI_RUN_GRAPHS, "multi_run_visualization", 
                context.dimensions
            )
        else:
            # Si no se especifica, crear dict con todas las opciones en False
            context.multi_run_visualization = {
                viz_type: False for viz_type in MULTI_RUN_GRAPHS
            }
        
        # Validar opciones de mostrar/guardar (solo booleanos)
        context.show_individual_visualizations = self._validate_boolean_option(
            config, 'show_individual_visualizations', False
        )
        context.save_individual_visualizations = self._validate_boolean_option(
            config, 'save_individual_visualizations', True
        )
        context.show_multiple_visualizations = self._validate_boolean_option(
            config, 'show_multiple_visualizations', False
        )
        context.save_multiple_visualizations = self._validate_boolean_option(
            config, 'save_multiple_visualizations', True
        )
    
    def _validate_visualization_config(self, viz_config: Union[bool, Dict[str, Any]], 
                                      valid_options: List[str], param_name: str, 
                                      dimensions: int) -> Dict[str, bool]:
        """
        Valida configuración de visualización que puede ser bool o dict.
        
        Args:
            viz_config: Configuración de visualización (bool o dict)
            valid_options: Opciones válidas de visualización
            param_name: Nombre del parámetro para mensajes de error
            dimensions: Número de dimensiones para validaciones específicas
            
        Returns:
            dict con configuración validada (siempre devuelve dict)
            
        Raises:
            ValueError: Si la configuración es inválida
        """
        if isinstance(viz_config, bool):
            # Convertir bool a dict con todas las opciones establecidas
            validated_dict = {}
            for viz_type in valid_options:
                # Aplicar validaciones específicas por tipo de visualización
                if viz_type in ['surface_3d', 'particles_2d'] and dimensions < 2:
                    # Para visualizaciones que requieren múltiples dimensiones
                    validated_dict[viz_type] = False
                else:
                    validated_dict[viz_type] = viz_config
            return validated_dict
        
        elif isinstance(viz_config, dict):
            validated_dict = {}
            for viz_type, enabled in viz_config.items():
                if not isinstance(viz_type, str):
                    raise ValueError(
                        f"Visualization type in '{param_name}' must be string, "
                        f"got: {type(viz_type)}"
                    )
                
                if viz_type not in valid_options:
                    raise ValueError(
                        f"Invalid visualization type '{viz_type}' in '{param_name}'. "
                        f"Valid options: {valid_options}"
                    )
                
                if not isinstance(enabled, bool):
                    raise ValueError(
                        f"Value for '{viz_type}' in '{param_name}' must be boolean, "
                        f"got: {type(enabled)}"
                    )
                
                # Validaciones específicas por tipo de visualización
                if viz_type in ['surface_3d', 'particles_2d'] and dimensions < 2:
                    raise ValueError(
                        f"Visualization '{viz_type}' requires at least 2 dimensions, "
                        f"got: {dimensions}"
                    )
                
                validated_dict[viz_type] = enabled
            
            return validated_dict
        
        else:
            raise ValueError(
                f"'{param_name}' must be boolean or dictionary, "
                f"got: {type(viz_config)}"
            )
    
    def _validate_boolean_option(self, config: Dict[str, Any], 
                                param_name: str, 
                                default_value: bool) -> bool:
        
        """
        Valida una opción booleana de visualización.
        
        Args:
            config: Configuración original
            param_name: Nombre del parámetro
            default_value: Valor por defecto
            
        Returns:
            Valor booleano validado
            
        Raises:
            ValueError: Si el valor no es booleano
        """
        value = config.get(param_name, default_value)
        if not isinstance(value, bool):
            raise ValueError(
                f"'{param_name}' must be boolean, got: {type(value)}"
            )
        return value
    
    def _validate_single_run_config(self, config: Dict[str, Any], 
                                   context: ValidationContext,
                                   visualization_config: Dict[str, Any]) -> None:
        """
        Valida configuración de visualización para runs individuales.
        
        Args:
            config: Configuración original
            context: Contexto con parámetros validados
            visualization_config: Diccionario a actualizar con configuración 
            validada
        """
        single_run_viz = config.get('single_run_visualization')
        if single_run_viz is not None:
            validated_single = self._validate_visualization_list(
                single_run_viz, SINGLE_RUN_GRAPHS, 
                "single_run_visualization", context.dimensions
            )
            visualization_config['single_run_visualization'] = validated_single
    
    def _validate_multi_run_config(self, config: Dict[str, Any], 
                                  context: ValidationContext,
                                  visualization_config: Dict[str, Any]) -> None:
        
        """
        Valida configuración de visualización para múltiples runs.
        
        Args:
            config: Configuración original
            context: Contexto con parámetros validados
            visualization_config: Diccionario a actualizar con configuración 
            validada
        """
        multi_run_viz = config.get('multi_run_visualization')
        if multi_run_viz is not None:
            # Solo validar si hay múltiples runs
            if context.runs <= 1:
                logger.warning(
                    "multi_run_visualization specified but runs <= 1, ignoring"
                )
            else:
                validated_multi = self._validate_visualization_list(
                    multi_run_viz, MULTI_RUN_GRAPHS, 
                    "multi_run_visualization", context.dimensions
                )
                visualization_config['multi_run_visualization'] = validated_multi
    
    def _validate_display_options(self, config: Dict[str, Any], 
                                 visualization_config: Dict[str, Any]) -> None:
        
        """
        Valida opciones de mostrar y guardar visualizaciones.
        
        Args:
            config: Configuración original
            visualization_config: Diccionario a actualizar con configuración validada
        """
        # Opciones de visualización individual
        show_individual = config.get('show_individual_visualizations', False)
        save_individual = config.get('save_individual_visualizations', True)
        
        if not isinstance(show_individual, bool):
            raise ValueError(
                f"'show_individual_visualizations' must be boolean, "
                f"got: {type(show_individual)}"
            )
        if not isinstance(save_individual, bool):
            raise ValueError(
                f"'save_individual_visualizations' must be boolean, "
                f"got: {type(save_individual)}"
            )
        
        visualization_config['show_individual_visualizations'] = show_individual
        visualization_config['save_individual_visualizations'] = save_individual
        
        # Opciones de visualización múltiple
        show_multiple = config.get('show_multiple_visualizations', False)
        save_multiple = config.get('save_multiple_visualizations', True)
        
        if not isinstance(show_multiple, bool):
            raise ValueError(
                f"'show_multiple_visualizations' must be boolean, "
                f"got: {type(show_multiple)}"
            )
        if not isinstance(save_multiple, bool):
            raise ValueError(
                f"'save_multiple_visualizations' must be boolean, "
                f"got: {type(save_multiple)}"
            )
        
        visualization_config['show_multiple_visualizations'] = show_multiple
        visualization_config['save_multiple_visualizations'] = save_multiple
    
    def _validate_visualization_list(self, viz_list: Any, 
                                    valid_options: List[str],
                                    param_name: str, 
                                    dimensions: int) -> List[str]:
        """Valida una lista de tipos de visualización.
        Args:
            viz_list: Lista de visualizaciones a validar
            valid_options: Opciones válidas disponibles
            param_name: Nombre del parámetro para mensajes de error
            dimensions: Número de dimensiones para validaciones específicas
            
        Returns:
            Lista validada de visualizaciones
            
        Raises:
            ValueError: Si alguna visualización es inválida
        """
        if not isinstance(viz_list, list):
            raise ValueError(
                f"'{param_name}' must be a list, got: {type(viz_list)}"
            )
        
        if not viz_list:
            raise ValueError(f"'{param_name}' cannot be empty")
        
        validated_list = []
        for viz in viz_list:
            if not isinstance(viz, str):
                raise ValueError(
                    f"All elements in '{param_name}' must be strings, "
                    f"got: {type(viz)}"
                )
            
            if viz not in valid_options:
                raise ValueError(
                    f"Invalid visualization type '{viz}' in '{param_name}'. "
                    f"Valid options: {valid_options}"
                )
            
            # Validaciones específicas por tipo de visualización
            if viz in ['surface_3d', 'particles_2d'] and dimensions < 2:
                raise ValueError(
                    f"Visualization '{viz}' requires at least 2 dimensions, "
                    f"got: {dimensions}"
                )
            
            if viz not in validated_list:  # Evitar duplicados
                validated_list.append(viz)
        
        return validated_list
