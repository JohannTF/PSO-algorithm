"""Registro para tipos de visualizaciones disponibles."""

from typing import Dict, Type

from src.main.visualization.base_plot import BasePlot


class PlotRegistry:
    """Registro central de visualizaciones disponibles."""

    _single_run_plots: Dict[str, Type[BasePlot]] = {}
    _multi_run_plots: Dict[str, Type[BasePlot]] = {}

    @classmethod
    def register_single_run(cls, name: str):
        """Decorador para registrar visualización de ejecución individual.

        Args:
            name (str): Identificador del gráfico.

        Returns:
            Callable: Decorador que registra la clase.
        """
        def decorator(plot_class: Type[BasePlot]):
            cls._single_run_plots[name] = plot_class
            return plot_class
        return decorator

    @classmethod
    def register_multi_run(cls, name: str):
        """Decorador para registrar visualización de múltiples ejecuciones.

        Args:
            name (str): Identificador del gráfico.

        Returns:
            Callable: Decorador que registra la clase.
        """
        def decorator(plot_class: Type[BasePlot]):
            cls._multi_run_plots[name] = plot_class
            return plot_class
        return decorator

    @classmethod
    def get_single_run_plot(cls, name: str, **kwargs) -> BasePlot:
        """Obtiene instancia de gráfico para ejecuciones individuales.

        Args:
            name (str): Identificador del gráfico.
            **kwargs: Argumentos para inicializar el gráfico.

        Returns:
            BasePlot: Instancia del gráfico solicitado.

        Raises:
            KeyError: Si el gráfico no está registrado.
        """
        if name not in cls._single_run_plots:
            available = list(cls._single_run_plots.keys())
            raise KeyError(f"Gráfico '{name}' no encontrado. "
                          f"Disponibles: {available}")

        return cls._single_run_plots[name](**kwargs)

    @classmethod
    def get_multi_run_plot(cls, name: str, **kwargs) -> BasePlot:
        """Obtiene instancia de gráfico para múltiples ejecuciones.

        Args:
            name (str): Identificador del gráfico.
            **kwargs: Argumentos para inicializar el gráfico.

        Returns:
            BasePlot: Instancia del gráfico solicitado.

        Raises:
            KeyError: Si el gráfico no está registrado.
        """
        if name not in cls._multi_run_plots:
            available = list(cls._multi_run_plots.keys())
            raise KeyError(f"Gráfico '{name}' no encontrado. "
                          f"Disponibles: {available}")

        return cls._multi_run_plots[name](**kwargs)

    @classmethod
    def clear_registrations(cls) -> None:
        """Limpia todas las registraciones (útil para pruebas)."""
        cls._single_run_plots.clear()
        cls._multi_run_plots.clear()
