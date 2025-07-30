"""Visualización para mejores fitness por ejecución."""

from typing import Any, Dict

from src.main.visualization.base_plot import BasePlot
from src.main.visualization.plot_registry import PlotRegistry


@PlotRegistry.register_multi_run("best_fitness_per_run")
class BestFitnessPerRunPlot(BasePlot):
    """Visualización de mejores fitness por ejecución."""
    
    def extract_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae datos específicos para gráfico de mejor fitness por ejecución.
        
        Args:
            data: Diccionario completo con todos los datos disponibles.
            
        Returns:
            Datos específicos para esta visualización.
        """
        multi_run_stats = data["multi_run_stats"]
        return {
            "best_fitness_per_run": multi_run_stats.get("best_fitness_per_run", []),
            "best_run_index": data.get("best_run_index", 0),
            "global_avg_best_fitness": multi_run_stats.get("global_avg_best_fitness", 0)
        }
    
    def _create_plot(self, data: Dict[str, Any], **kwargs) -> tuple:
        """Crea gráfico con mejores fitness de cada ejecución.
        
        Args:
            data: Datos específicos para la visualización.
            **kwargs: Argumentos adicionales.
            
        Returns:
            Tupla (figura, eje) con la visualización generada.
        """
        best_fitness_per_run = data.get('best_fitness_per_run', [])
        best_run_index = data.get('best_run_index', 0)
        global_avg_fitness = data.get('global_avg_best_fitness', 0)
        
        if not best_fitness_per_run:
            self.ax.text(0.5, 0.5, "No hay datos disponibles", 
                         horizontalalignment='center', verticalalignment='center')
            return self.fig, self.ax
            
        runs = list(range(1, len(best_fitness_per_run) + 1))
        best_value = best_fitness_per_run[best_run_index]

        # Línea de tendencia
        self.ax.plot(runs, best_fitness_per_run, "b-", alpha=0.7)
        
        # Puntos para cada valor
        self.ax.scatter(runs, best_fitness_per_run, c="blue", marker="o", s=50)
        
        # Marcar mejor fitness
        self.ax.scatter(
            [best_run_index + 1], [best_value], c="red", marker="*", s=200,
            label=f"Mejor fitness: {best_value:.6f} (Run {best_run_index+1})"
        )
        
        # Línea promedio
        self.ax.axhline(
            y=global_avg_fitness, color="green", linestyle="--",
            label=f"Promedio: {global_avg_fitness:.6f}"
        )
        
        self.ax.set_title(self.title or "Mejores fitness por ejecución")
        self.ax.set_xlabel("Ejecución")
        self.ax.set_ylabel("Mejor fitness")
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        
        return self.fig, self.ax
