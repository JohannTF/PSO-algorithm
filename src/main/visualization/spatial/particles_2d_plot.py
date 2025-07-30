"""Visualización para partículas en espacio 2D."""

from typing import Dict, Any

from src.main.visualization.base_plot import BasePlot
from src.main.visualization.plot_registry import PlotRegistry

import numpy as np
import matplotlib.pyplot as plt

@PlotRegistry.register_single_run("particles_2d")
class Particles2DPlot(BasePlot):
    """Visualización de partículas en espacio 2D."""
    
    def __init__(self, title: str = "", figsize: tuple = (12, 10)):
        """Inicializa visualización con figura más grande."""
        super().__init__(title, figsize)
    
    def extract_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae datos específicos para gráfico de partículas 2D.
        
        Args:
            data: Diccionario completo con todos los datos disponibles
            
        Returns:
            Datos específicos para esta visualización
        """
        return {
            "particles": data.get("pso_algorithm").particles,
            "bounds": data.get("config").get("bounds"),
            "benchmark_function": data.get("benchmark_function")
        }
    
    def _create_plot(self, data: Dict[str, Any], **kwargs) -> tuple:
        """Grafica distribución de partículas en espacio 2D con contorno de función.
        
        Args:
            data: Datos específicos para la visualización
            **kwargs: Argumentos adicionales
            
        Returns:
            Tupla (figura, eje) con la visualización generada
        """
        particles = data.get('particles')
        bounds = data.get('bounds')
        benchmark_function = data.get('benchmark_function')

        # Crear grid para contorno de función
        lower_bound, upper_bound = bounds
        x = np.linspace(lower_bound, upper_bound, 100)
        y = np.linspace(lower_bound, upper_bound, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)

        # Evaluar función en cada punto del grid
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                pos = np.array([X[i, j], Y[i, j]])
                Z[i, j] = benchmark_function(pos)

        # Dibujar contorno de función
        contour = self.ax.contourf(X, Y, Z, 50, cmap="viridis", alpha=0.7)
        plt.colorbar(contour, ax=self.ax, label="Valor de la función")

        # Extraer posiciones de partículas
        positions = np.array([p.position for p in particles])
        best_positions = np.array([p.best_position for p in particles])

        # Dibujar posiciones actuales
        self.ax.scatter(
            positions[:, 0], positions[:, 1], c="white", edgecolor="black",
            s=60, label="Posición actual"
        )

        # Dibujar mejores posiciones
        self.ax.scatter(
            best_positions[:, 0], best_positions[:, 1], c="red", edgecolor="black",
            s=40, label="Mejor posición"
        )

        # Dibujar óptimo global si está disponible
        if hasattr(benchmark_function, "global_optimum_position"):
            opt_pos = benchmark_function.global_optimum_position
            self.ax.scatter(
                [opt_pos[0]], [opt_pos[1]], c="yellow", edgecolor="black",
                s=150, marker="*", label="Óptimo global"
            )

        self.ax.set_title(self.title or "Distribución de partículas")
        self.ax.set_xlabel("x[0]")
        self.ax.set_ylabel("x[1]")
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        
        return self.fig, self.ax