"""Paquete para la visualización de resultados de algoritmos de optimización."""

# Importar clases base
from src.main.visualization.base_plot import BasePlot
from src.main.visualization.plot_registry import PlotRegistry

# Definir una lista de módulos que contienen visualizaciones
_VISUALIZATION_MODULES = [
    'src.main.visualization.convergence.best_fitness_plot',
    'src.main.visualization.convergence.best_fitness_per_run_plot',
    'src.main.visualization.parameters.diversity_plot',
    'src.main.visualization.parameters.inertia_weight_plot',
    'src.main.visualization.spatial.particles_2d_plot',
    'src.main.visualization.spatial.surface_3d_plot',
    'src.main.visualization.multi_run.avg_fitness_boxplot_plot',
]

# Importar todos los módulos que contienen visualizaciones
# Esto asegura que todas las visualizaciones se registren
for module_name in _VISUALIZATION_MODULES:
    try:
        __import__(module_name)
    except ImportError as e:
        print(f"ADVERTENCIA: No se pudo importar el módulo {module_name}: {e}")

# Exportar clases principales
__all__ = [
    "BasePlot",
    "PlotRegistry",
    "BestFitnessPlot",
    "BestFitnessPerRunPlot",
    "InertiaWeightPlot",
    "DiversityPlot",
    "Particles2DPlot",
    "Surface3DPlot",
    "AvgFitnessBoxplotPlot",
]
