"""Visualización de fitness promedio por ejecución en formato boxplot."""

from typing import Dict, Any

from src.main.visualization.base_plot import BasePlot
from src.main.utils.constants import LOG_SCALE_THRESHOLD
from src.main.visualization.plot_registry import PlotRegistry


@PlotRegistry.register_multi_run("avg_fitness_per_run")
class AvgFitnessBoxplotPlot(BasePlot):
    """Visualización de fitness promedio por ejecución en boxplot."""
    
    def __init__(self, title: str = "", figsize: tuple = (14, 8)):
        """Inicializa visualización con figura más grande."""
        super().__init__(title, figsize)
    
    def extract_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae datos específicos para boxplot de fitness promedio.
        
        Args:
            data: Diccionario completo con todos los datos disponibles
            
        Returns:
            Datos específicos para esta visualización
        """
        multi_run_stats = data["multi_run_stats"]
        return {
            "all_avg_fitness_history": multi_run_stats.get("all_avg_fitness_history", []),
            "best_run_index": data.get("best_run_index", None)
        }
    
    def _create_plot(self, data: Dict[str, Any], **kwargs) -> tuple:
        """Crea diagrama de cajas para historial de fitness promedio.

        Args:
            data: Datos específicos para la visualización
            
        Returns:
            Tupla (figura, eje) con la visualización generada
        """
        all_avg_fitness_history = data.get('all_avg_fitness_history', [])
        best_run_index = data.get('best_run_index', None)
        
        if not all_avg_fitness_history:
            self.ax.text(0.5, 0.5, "No hay datos disponibles", 
                        horizontalalignment='center', verticalalignment='center')
            return self.fig, self.ax
        
        # Crear diagrama de cajas
        box_plot = self.ax.boxplot(all_avg_fitness_history, patch_artist=True)
        
        # Personalizar colores
        for box in box_plot['boxes']:
            box.set(facecolor='lightblue', alpha=0.8)
        
        for whisker in box_plot['whiskers']:
            whisker.set(color='blue', linewidth=1.5, linestyle=':')
        
        for cap in box_plot['caps']:
            cap.set(color='blue', linewidth=2)
        
        for median in box_plot['medians']:
            median.set(color='red', linewidth=2)
        
        for flier in box_plot['fliers']:
            flier.set(marker='o', color='red', alpha=0.5)

        self.ax.set_title(self.title or "Distribución de fitness promedio por ejecución")
        self.ax.set_xlabel("Ejecución")
        self.ax.set_ylabel("Fitness promedio")
        
        # Escala logarítmica si es necesario
        max_val = max([max(run) for run in all_avg_fitness_history]) if all_avg_fitness_history else 0
        if max_val > LOG_SCALE_THRESHOLD:
            self.ax.set_yscale('log')
        
        # Etiquetas del eje X
        num_runs = len(all_avg_fitness_history)
        self.ax.set_xticks(range(1, num_runs + 1))
        self.ax.set_xticklabels([f"{i+1}" for i in range(num_runs)])
        
        if best_run_index is not None and 0 <= best_run_index < num_runs:
            box_plot['boxes'][best_run_index].set(facecolor='gold', alpha=0.9)
        
        self.ax.grid(True, alpha=0.3)
        
        return self.fig, self.ax