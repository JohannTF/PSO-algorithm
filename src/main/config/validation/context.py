"""Contexto compartido entre validadores para datos validados."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ValidationContext:
    """Contexto compartido entre validadores.
    
    Contiene datos validados que pueden ser reutilizados por otros validadores.
    """
    # Parámetros básicos validados
    dimensions: Optional[int] = None
    population_size: Optional[int] = None
    generations: Optional[int] = None
    runs: Optional[int] = None
    benchmark: Optional[str] = None
    bounds: Optional[List[float]] = None
    velocity_bounds: Optional[List[float]] = None
    benchmark_function: Optional[Any] = None
    
    # Estrategias validadas
    inertia_strategy: Optional[str] = None
    inertia_type: Optional[Dict[str, Any]] = None
    c1_strategy: Optional[str] = None
    c2_strategy: Optional[str] = None
    c1: Optional[List[Any]] = None
    c2: Optional[List[Any]] = None
    
    # Configuración de salida
    output_dir: Optional[str] = None
    base_output_path: Optional[str] = None
    output_file: Optional[str] = None
    save_results: Optional[bool] = None
    visualization_path: Optional[str] = None
    show_progress_bar: Optional[bool] = None
    
    # Configuración de visualización
    single_run_visualization: Optional[Dict[str, bool]] = None
    multi_run_visualization: Optional[Dict[str, bool]] = None
    show_individual_visualizations: Optional[bool] = None
    save_individual_visualizations: Optional[bool] = None
    show_multiple_visualizations: Optional[bool] = None
    save_multiple_visualizations: Optional[bool] = None
    
    def get_validated_config(self) -> Dict[str, Any]:
        """Retorna la configuración validada como diccionario."""
        config = {}
        
        # Agregar parámetros básicos
        if self.dimensions is not None:
            config['dimensions'] = self.dimensions
        if self.population_size is not None:
            config['population_size'] = self.population_size
        if self.generations is not None:
            config['generations'] = self.generations
        if self.runs is not None:
            config['runs'] = self.runs
        if self.benchmark is not None:
            config['benchmark'] = self.benchmark
        if self.bounds is not None:
            config['bounds'] = self.bounds
        if self.velocity_bounds is not None:
            config['velocity_bounds'] = self.velocity_bounds
        if self.benchmark_function is not None:
            config['benchmark_function'] = self.benchmark_function
        
        # Agregar estrategias
        if self.inertia_strategy is not None:
            config['inertia_strategy'] = self.inertia_strategy
        if self.inertia_type is not None:
            config['inertia_type'] = self.inertia_type
        if self.c1_strategy is not None:
            config['c1_strategy'] = self.c1_strategy
        if self.c1 is not None:
            config['c1'] = self.c1
        if self.c2_strategy is not None:
            config['c2_strategy'] = self.c2_strategy
        if self.c2 is not None:
            config['c2'] = self.c2

        # Agregar configuración de salida
        if self.base_output_path is not None:
            config['base_output_path'] = self.base_output_path
        if self.output_file is not None:
            config['output_file'] = self.output_file
        if self.save_results is not None:
            config['save_results'] = self.save_results
        if self.visualization_path is not None:
            config['visualization_path'] = self.visualization_path
        if self.show_progress_bar is not None:
            config['show_progress_bar'] = self.show_progress_bar
            
        # Agregar configuración de visualización
        if self.single_run_visualization is not None:
            config['single_run_visualization'] = self.single_run_visualization
        if self.multi_run_visualization is not None:
            config['multi_run_visualization'] = self.multi_run_visualization
        if self.show_individual_visualizations is not None:
            config['show_individual_visualizations'] = self.show_individual_visualizations
        if self.save_individual_visualizations is not None:
            config['save_individual_visualizations'] = self.save_individual_visualizations
        if self.show_multiple_visualizations is not None:
            config['show_multiple_visualizations'] = self.show_multiple_visualizations
        if self.save_multiple_visualizations is not None:
            config['save_multiple_visualizations'] = self.save_multiple_visualizations
            
        return config