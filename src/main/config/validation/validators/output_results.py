"""Validador de configuración de salida y directorios según formato JSON."""

import os
from typing import Dict, Any
from datetime import datetime

from src.main.config.validation.pipeline.registry import validator
from src.main.config.validation.base_validator import BaseValidator
from src.main.config.validation.context import ValidationContext


@validator()
class OutputResultsValidador(BaseValidator):
    """Validador para configuración de salida.
    
    Valida parámetros de salida del formato JSON:
    - base_output_path (directorio base de salida)
    - output_file (nombre del archivo de resultados)
    - save_results (boolean para guardar resultados)
    - visualization_path (directorio para visualizaciones)
    - show_progress_bar (boolean para mostrar barra de progreso)
    
    No depende de otros validadores.
    """
    
    def __init__(self):
        super().__init__("output")
    
    def validate(self, config: Dict[str, Any], 
                 context: ValidationContext) -> None:
        """Valida la configuración de salida según el formato JSON.
        
        Args:
            config: Configuración original
            context: Contexto a actualizar
            
        Raises:
            ValueError: Si la configuración de salida es inválida
        """
        # Validar save_results (opcional, por defecto True)
        save_results = config.get('save_results', True)
        if not isinstance(save_results, bool):
            raise ValueError(
                f"'save_results' must be a boolean, got: {type(save_results)}"
            )
        
        # Validar base_output_path (opcional, por defecto "data")
        base_output_path = config.get('base_output_path', 'data')
        if not isinstance(base_output_path, str):
            raise ValueError(
                f"'base_output_path' must be a string, got: {type(base_output_path)}"
            )
        
        if not base_output_path.strip():
            raise ValueError("'base_output_path' cannot be empty")
        
        # Normalizar el path
        base_output_path = os.path.normpath(base_output_path.strip())
        
        # Crear el directorio si no existe
        try:
            if not os.path.exists(base_output_path):
                os.makedirs(base_output_path, exist_ok=True)
            
            # Verificar que es un directorio
            if not os.path.isdir(base_output_path):
                raise ValueError(
                    f"'base_output_path' exists but is not a directory: "
                    f"{base_output_path}"
                )
            
            # Verificar permisos de escritura
            if not os.access(base_output_path, os.W_OK):
                raise ValueError(
                    f"No write permission for base output directory: "
                    f"{base_output_path}"
                )
            
        except OSError as e:
            raise ValueError(
                f"Cannot create or access base output directory "
                f"'{base_output_path}': {e}"
            ) from e
        
        # Validar output_file (opcional, se genera automáticamente)
        output_file = config.get('output_file')
        if output_file is not None:
            if not isinstance(output_file, str):
                raise ValueError(
                    f"'output_file' must be a string, got: {type(output_file)}"
                )
            
            if not output_file.strip():
                raise ValueError("'output_file' cannot be empty")
            
            # Validar caracteres válidos en el nombre del archivo
            import re
            if not re.match(r'^[a-zA-Z0-9_.-]+$', output_file.strip()):
                raise ValueError(
                    f"'output_file' contains invalid characters. "
                    f"Only letters, numbers, underscore, dot and hyphen are "
                    f"allowed: {output_file}"
                )
            
            output_file = output_file.strip()
        else:
            # Generar nombre automático con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"pso_results_{timestamp}"
        
        # Validar visualization_path (opcional)
        visualization_path = config.get('visualization_path')
        if visualization_path is not None:
            if not isinstance(visualization_path, str):
                raise ValueError(
                    f"'visualization_path' must be a string, "
                    f"got: {type(visualization_path)}"
                )
            
            if not visualization_path.strip():
                raise ValueError("'visualization_path' cannot be empty")
            
            visualization_path = os.path.normpath(visualization_path.strip())
        else:
            # Generar path de visualización por defecto
            visualization_path = self._setup_visualization_path(
                None, base_output_path, output_file
            )
        
        # Crear directorio de visualizaciones si no existe
        try:
            if not os.path.exists(visualization_path):
                os.makedirs(visualization_path, exist_ok=True)
        except OSError as e:
            raise ValueError(
                f"Cannot create visualization directory '{visualization_path}': {e}"
            ) from e
        
        # Validar show_progress_bar (opcional, por defecto True)
        show_progress_bar = config.get('show_progress_bar', True)
        if not isinstance(show_progress_bar, bool):
            raise ValueError(
                f"'show_progress_bar' must be a boolean, "
                f"got: {type(show_progress_bar)}"
            )
        
        # Establecer valores en el contexto
        context.base_output_path = base_output_path
        context.output_file = output_file
        context.save_results = save_results
        context.visualization_path = visualization_path
        context.show_progress_bar = show_progress_bar
    
    def _setup_visualization_path(self, 
                                 visualization_path: str, 
                                 base_output_path: str, 
                                 output_file: str, 
                                 benchmark_name: str = "unknown") -> str:
        """Configura la ruta para guardar las visualizaciones.
        
        Args:
            visualization_path: Ruta explícita para visualizaciones (opcional)
            base_output_path: Ruta base para salidas
            output_file: Nombre del archivo de resultados
            benchmark_name: Nombre del benchmark utilizado
            
        Returns:
            str: Ruta completa para guardar visualizaciones
        """
        # Si se proporciona una ruta explícita, usarla
        if visualization_path:
            return os.path.normpath(visualization_path)
        
        # Crear una ruta basada en la estructura estándar
        if output_file:
            vis_dir = os.path.join(
                base_output_path, "visualizations", output_file
            )
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            vis_dir = os.path.join(
                base_output_path, "visualizations", 
                f"{benchmark_name}_{timestamp}"
            )
            
        return os.path.normpath(vis_dir)
