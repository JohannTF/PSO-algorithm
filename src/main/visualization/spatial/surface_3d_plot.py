"""Visualización para superficie 3D de función benchmark."""

from typing import Dict, Any

from src.main.visualization.base_plot import BasePlot
from src.main.visualization.plot_registry import PlotRegistry

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


@PlotRegistry.register_single_run("surface_3d")
class Surface3DPlot(BasePlot):
    """Visualización de superficie 3D de función benchmark."""
    
    def __init__(self, title: str = "", figsize: tuple = (14, 12)):
        """Inicializa visualización con figura más grande."""
        super().__init__(title, figsize)
    
    def create_figure(self):
        """Crea figura con eje 3D."""
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(111, projection='3d')
        return self.fig, self.ax
    
    def extract_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae datos específicos para gráfico de superficie 3D.
        
        Args:
            data: Diccionario completo con todos los datos disponibles
            
        Returns:
            Datos específicos para esta visualización
        """
        particles = data["pso_algorithm"].particles
        
        return {
            "bounds": data.get("config").get("bounds"),
            "benchmark_function": data.get("benchmark_function"),
            "particles": particles
        }
    
    def _create_plot(self, data: Dict[str, Any], **kwargs) -> tuple:
        """Grafica superficie 3D de función benchmark.
        
        Args:
            data: Datos específicos para la visualización
            **kwargs: Argumentos adicionales
            
        Returns:
            Tupla (figura, eje) con la visualización generada
        """
        bounds = data.get('bounds', (-10, 10))
        benchmark_function = data.get('benchmark_function')
        particles = data.get('particles', [])
        
        if not benchmark_function:
            self.ax.text(0.5, 0.5, "No hay datos disponibles", 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes)
            return self.fig, self.ax

        # Crear grid para superficie
        lower_bound, upper_bound = bounds
        x = np.linspace(lower_bound, upper_bound, 50)
        y = np.linspace(lower_bound, upper_bound, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # Evaluar función en cada punto del grid
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                pos = np.array([X[i, j], Y[i, j]])
                Z[i, j] = benchmark_function(pos)
        
        # Graficar superficie
        surf = self.ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.8, 
                                  rstride=1, cstride=1, linewidth=0, antialiased=True)
        
        # Barra de color
        plt.colorbar(surf, ax=self.ax, shrink=0.5, aspect=5, label="Valor de la función")
        
        # Mostrar partículas en superficie si están disponibles
        if particles and len(particles) > 0:
            if particles[0].dimensions == 2:
                positions = np.array([p.position for p in particles])
                fitness = np.array([p.fitness for p in particles])
                
                self.ax.scatter(positions[:, 0], positions[:, 1], fitness, 
                              c='red', s=50, marker='o', label="Partículas")
                
        # Mostrar mejor posición global si está disponible
        if hasattr(benchmark_function, "global_optimum_position"):
            opt_pos = benchmark_function.global_optimum_position
            opt_val = benchmark_function(opt_pos)
            self.ax.scatter([opt_pos[0]], [opt_pos[1]], [opt_val], 
                          c='yellow', s=200, marker='*', label="Óptimo global")
        
        self.ax.set_title(self.title or f"Superficie de {benchmark_function.__class__.__name__}")
        self.ax.set_xlabel("x[0]")
        self.ax.set_ylabel("x[1]")
        self.ax.set_zlabel("f(x)")
        
        if particles:
            self.ax.legend()
        
        return self.fig, self.ax
