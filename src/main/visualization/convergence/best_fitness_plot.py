"""Visualización para seguimiento del mejor fitness."""

from typing import Any, Dict

from src.main.utils.constants import LOG_SCALE_THRESHOLD, PSO_STATS_SAVE_INTERVAL
from src.main.visualization.base_plot import BasePlot
from src.main.visualization.plot_registry import PlotRegistry


@PlotRegistry.register_single_run("best_fitness")
@PlotRegistry.register_multi_run("best_run_fitness")
class BestFitnessPlot(BasePlot):
    """Visualización de convergencia del mejor fitness."""

    def extract_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae datos específicos para gráfico de mejor fitness.

        Args:
            data (Dict[str, Any]): Diccionario completo con todos los datos 
                disponibles.

        Returns:
            Dict[str, Any]: Datos específicos para esta visualización.
        """
        # Para ejecuciones individuales
        if "stats" in data:
            history = data["stats"].get("history", {})
            return {
                "best_fitness_per_generation": history.get("best_fitness_per_generation"),
                "generations": data.get("config", {}).get("generations")
            }

        # Para múltiples ejecuciones
        if "best_stats" in data:
            history = data["best_stats"].get("history", {})
            return {
                "best_fitness_per_generation": history.get("best_fitness_per_generation"),
                "generations": data.get("config").get("generations")
            }

    def _create_plot(self, data: Dict[str, Any], **kwargs) -> tuple:
        """Grafica curva de convergencia del algoritmo.

        Args:
            data (Dict[str, Any]): Datos específicos para la visualización.
            **kwargs: Argumentos adicionales.

        Returns:
            tuple: Tupla (figura, eje) con la visualización generada.
        """
        fitness_history = data.get('best_fitness_per_generation', [])
        generations = data.get('generations', None)
        interval = PSO_STATS_SAVE_INTERVAL

        # Omitir primer valor (posición inicial sin movimiento)
        if fitness_history and len(fitness_history) > 1:
            fitness_history = fitness_history[1:]

            # Calcular eje X real
            if generations is not None:
                x = ([interval * (i+1) for i in range(len(fitness_history)-1)] + 
                     [generations])
            else:
                x = [interval * (i+1) for i in range(len(fitness_history))]

            self.ax.plot(x, fitness_history, "-o", markersize=3)
        else:
            self.ax.text(0.5, 0.5, "Datos insuficientes",
                         horizontalalignment='center',
                         verticalalignment='center',
                         transform=self.ax.transAxes)

        self.ax.set_title(self.title or "Convergencia hacia el mejor")
        self.ax.set_xlabel("Iteración")
        self.ax.set_ylabel("Mejor fitness")

        if fitness_history and max(fitness_history) > LOG_SCALE_THRESHOLD:
            self.ax.set_yscale('log')

        self.ax.grid(True, alpha=0.3)

        return self.fig, self.ax
