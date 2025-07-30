"""Visualización para evolución del peso inercial."""

from typing import Any, Dict

from src.main.utils.constants import PSO_STATS_SAVE_INTERVAL
from src.main.visualization.base_plot import BasePlot
from src.main.visualization.plot_registry import PlotRegistry


@PlotRegistry.register_single_run("inertia_weight")
@PlotRegistry.register_multi_run("best_run_inertia")
class InertiaWeightPlot(BasePlot):
    """Visualización de evolución del peso inercial."""
    
    def extract_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae datos específicos para gráfico de peso inercial.
        
        Args:
            data: Diccionario completo con todos los datos disponibles.
            
        Returns:
            Datos específicos para esta visualización.
        """
        # Para ejecuciones individuales
        if "stats" in data:
            history = data["stats"].get("history")
            return {
                "inertia_weight": history.get("inertia_weight"),
                "generations": data.get("config").get("generations"),
                "inertia_type": data.get("config").get("inertia_type")
            }
        
        # Para múltiples ejecuciones
        if "best_stats" in data:
            history = data["best_stats"].get("history")
            return {
                "inertia_weight": history.get("inertia_weight"),
                "generations": data.get("config").get("generations"),
                "inertia_type": data.get("config").get("inertia_type")
            }
    
    def _create_plot(self, data: Dict[str, Any], **kwargs) -> tuple:
        """Grafica evolución del peso inercial a lo largo de iteraciones.
        
        Args:
            data: Datos específicos para la visualización
            **kwargs: Argumentos adicionales
            
        Returns:
            Tupla (figura, eje) con la visualización generada
        """
        inertia_history = data.get('inertia_weight', [])
        generations = data.get('generations', None)
        inertia_type = data.get('inertia_type', None)
        interval = PSO_STATS_SAVE_INTERVAL
        
        if generations is not None:
            x = [i*interval for i in range(len(inertia_history)-1)] + [generations-1]
        else:
            x = [i*interval for i in range(len(inertia_history))]
        
        # Crear título con tipo de estrategia
        title = self.title or "Historial de peso inercial"
        if inertia_type:
            if isinstance(inertia_type, str):
                title = f"{title} - {inertia_type}"
            elif (isinstance(inertia_type, (list, tuple)) and 
                  len(inertia_type) > 2 and isinstance(inertia_type[2], str)):
                title = f"{title} - {inertia_type[2]}"
            elif isinstance(inertia_type, (float, int)):
                title = f"{title} - constante ({inertia_type})"
            elif isinstance(inertia_type, (list, tuple)):
                title = f"{title} - decrecimiento lineal [{inertia_type[0]}-{inertia_type[1]}]"
                
        self.ax.plot(x, inertia_history, "-o", markersize=3)
        self.ax.set_title(title)
        self.ax.set_xlabel("Iteración")
        self.ax.set_ylabel("Peso inercial")
        self.ax.grid(True, alpha=0.3)
        
        return self.fig, self.ax
