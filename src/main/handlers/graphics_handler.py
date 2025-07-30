"""Manejador de visualización y almacenamiento de gráficos PSO."""

import os
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt

from src.main.utils.constants import MULTI_RUN_GRAPHS, SINGLE_RUN_GRAPHS
from src.main.visualization.plot_registry import PlotRegistry


class GraphicsHandler:
    """Gestor de visualización y almacenamiento de gráficos PSO."""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Inicializa el manejador de gráficos.

        Args:
            config: Configuración del algoritmo.
        """
        self.config = config
        self.single_run_viz_config = config["single_run_visualization"]
        self.multi_run_viz_config = config["multi_run_visualization"]
        self.save_path = config["visualization_path"]
        
        # Crear directorio si el guardado está habilitado
        if (config["save_individual_visualizations"] or 
            config["save_multiple_visualizations"]):
            os.makedirs(self.save_path, exist_ok=True)
        
        plt.close("all")
    
    def create_single_run_visualizations(
        self,
        stats: Dict[str, Any],
        pso_algorithm: Any,
        benchmark_function: Any,
        run_index: Optional[int] = None,
    ) -> None:
        """Crea visualizaciones para ejecución individual.

        Args:
            stats: Estadísticas del algoritmo.
            pso_algorithm: Instancia del algoritmo PSO.
            benchmark_function: Función de benchmark utilizada.
            run_index: Índice de la ejecución actual para múltiples ejecuciones.
        """
        show = self.config["show_individual_visualizations"]
        save = self.config["save_individual_visualizations"]
        
        if not (show or save):
            return

        run_suffix = f"_run{run_index+1}" if run_index is not None else ""
        benchmark_name = self.config["benchmark"].capitalize()
        figures_to_show = []
        
        # Datos completos para visualizaciones
        complete_data = {
            "stats": stats,
            "config": self.config,
            "pso_algorithm": pso_algorithm,
            "benchmark_function": benchmark_function
        }
        
        # Generar visualizaciones habilitadas en configuración
        for plot_type, enabled in self.single_run_viz_config.items():
            if not enabled:
                continue
            
            title = f"{SINGLE_RUN_GRAPHS.get(plot_type, plot_type)} - {benchmark_name}"
            
            try:
                plot = PlotRegistry.get_single_run_plot(plot_type, title=title)
                fig, ax = plot.plot(complete_data)
                
                if save:
                    filename = f"{plot_type}_{benchmark_name}{run_suffix}.png"
                    filepath = os.path.join(self.save_path, filename)
                    plot.save(filepath)
                
                if show:
                    figures_to_show.append(fig)
                else:
                    plot.close()
                    
            except Exception as e:
                print(f"Error al generar visualización '{plot_type}': {e}")
                
        if show and figures_to_show:
            for fig in figures_to_show:
                fig.show()
            plt.show()

    def create_multi_run_visualizations(
        self,
        all_stats: List[Dict[str, Any]],
        best_stats: Dict[str, Any],
        best_run_index: int,
        multi_run_stats: Dict[str, Any],
    ) -> None:
        """Crea visualizaciones comparativas para múltiples ejecuciones.

        Args:
            all_stats: Lista con estadísticas de todas las ejecuciones
            best_stats: Estadísticas de la mejor ejecución
            best_run_index: Índice de la mejor ejecución
            multi_run_stats: Estadísticas adicionales de múltiples ejecuciones
        """
        show = self.config["show_multiple_visualizations"]
        save = self.config["save_multiple_visualizations"]
        if not (show or save):
            return
        
        benchmark_name = self.config["benchmark"].capitalize()
        figures_to_show = []
        
        # Datos completos para múltiples visualizaciones
        complete_data = {
            "all_stats": all_stats,
            "best_stats": best_stats,
            "best_run_index": best_run_index,
            "multi_run_stats": multi_run_stats,
            "config": self.config
        }
        
        # Crear visualizaciones habilitadas en configuración
        for plot_type, enabled in self.multi_run_viz_config.items():
            if not enabled:
                continue
            
            title = f"{MULTI_RUN_GRAPHS.get(plot_type, plot_type)}"
            
            try:
                plot = PlotRegistry.get_multi_run_plot(plot_type, title=title)
                fig, ax = plot.plot(complete_data)
                
                if save:
                    filename = f"{plot_type}_{benchmark_name}.png"
                    filepath = os.path.join(self.save_path, filename)
                    plot.save(filepath)
                
                if show:
                    figures_to_show.append(fig)
                else:
                    plot.close()
                    
            except Exception as e:
                print(f"Error al generar visualización múltiple '{plot_type}': {e}")
        
        if show and figures_to_show:
            for fig in figures_to_show:
                fig.show()
            plt.show()