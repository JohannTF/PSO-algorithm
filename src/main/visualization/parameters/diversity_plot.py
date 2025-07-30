"""Visualización para diversidad de la población."""

from src.main.visualization.base_plot import BasePlot
from src.main.utils.constants import PSO_STATS_SAVE_INTERVAL
from typing import Dict, Any
from src.main.visualization.plot_registry import PlotRegistry


@PlotRegistry.register_single_run("diversity")
@PlotRegistry.register_multi_run("diversity")
class DiversityPlot(BasePlot):
    """Visualización de diversidad de la población."""
    
    def extract_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae datos específicos para gráfico de diversidad.
        
        Args:
            data: Diccionario completo con todos los datos disponibles
            
        Returns:
            Datos específicos para esta visualización
        """
        # Para ejecuciones individuales
        if "stats" in data:
            history = data["stats"].get("history")
            return {
                "diversity": history.get("diversity"),
                "generations": data.get("config").get("generations")
            }
        
        # Para múltiples ejecuciones
        if "best_stats" in data:
            history = data["best_stats"].get("history")
            return {
                "diversity": history.get("diversity"),
                "generations": data.get("config").get("generations")
            }
    
    def _create_plot(self, data: Dict[str, Any], **kwargs) -> tuple:
        """Grafica diversidad de población en posición, velocidad y componente cognitiva.
        
        Args:
            data: Datos específicos para la visualización
            **kwargs: Argumentos adicionales
            
        Returns:
            Tupla (figura, eje) con la visualización generada
        """
        diversity_history = data.get('diversity', {})
        generations = data.get('generations', None)
        interval = PSO_STATS_SAVE_INTERVAL
        
        # Todas las listas tienen la misma longitud
        n_points = len(next(iter(diversity_history.values()), []))
        if generations is not None:
            x = [i*interval for i in range(n_points-1)] + [generations-1]
        else:
            x = [i*interval for i in range(n_points)]
        
        for key, values in diversity_history.items():
            self.ax.plot(x, values, label=f"Diversidad ({key})")
        
        self.ax.set_title(self.title or "Diversidad de la población")
        self.ax.set_xlabel("Iteración")
        self.ax.set_ylabel("Diversidad (Norma L1)")
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        
        return self.fig, self.ax
