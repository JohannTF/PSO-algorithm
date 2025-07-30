"""Clase base para todas las visualizaciones."""

from abc import ABC, abstractmethod
from typing import Any, Dict

import matplotlib.pyplot as plt


class BasePlot(ABC):
    """Clase base abstracta para todas las visualizaciones."""

    def __init__(self, title: str = "", figsize: tuple = (10, 6)) -> None:
        """Inicializa la visualización base.

        Args:
            title (str): Título del gráfico.
            figsize (tuple): Tamaño de la figura (ancho, alto) en pulgadas.
        """
        self.title = title
        self.figsize = figsize
        self.fig = None
        self.ax = None

    def create_figure(self):
        """Crea nueva figura y eje para la visualización.
        
        Returns:
            tuple: Tupla (figura, eje) creada.
        """
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(111)
        return self.fig, self.ax

    def extract_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae y procesa datos específicos para esta visualización.

        Por defecto retorna todos los datos. Las subclases pueden
        sobrescribir para extraer solo datos necesarios.

        Args:
            data (Dict[str, Any]): Diccionario completo con todos los datos 
                disponibles.

        Returns:
            Dict[str, Any]: Datos procesados para esta visualización específica.
        """
        return data

    def plot(self, data: Dict[str, Any], **kwargs) -> tuple:
        """Genera la visualización con los datos proporcionados.

        Extrae automáticamente los datos necesarios y delega la creación
        del gráfico al método _create_plot.

        Args:
            data (Dict[str, Any]): Diccionario completo con todos los datos 
                disponibles.
            **kwargs: Argumentos adicionales.

        Returns:
            tuple: Tupla (figura, eje) con la visualización generada.
        """
        extracted_data = self.extract_data(data)

        if not self.fig or not self.ax:
            self.create_figure()

        return self._create_plot(extracted_data, **kwargs)
    
    @abstractmethod
    def _create_plot(self, data: Dict[str, Any], **kwargs) -> tuple:
        """Implementación específica del gráfico.

        Este método debe ser implementado por cada subclase.

        Args:
            data (Dict[str, Any]): Datos específicos ya extraídos para esta 
                visualización.
            **kwargs: Argumentos adicionales.

        Returns:
            tuple: Tupla (figura, eje) con la visualización generada.
        """
        pass

    def save(self, filepath: str, dpi: int = 300) -> None:
        """Guarda la visualización en un archivo.

        Args:
            filepath (str): Ruta donde guardar el archivo.
            dpi (int): Resolución de la imagen.
        """
        if self.fig:
            self.fig.savefig(filepath, dpi=dpi, bbox_inches='tight')

    def show(self) -> None:
        """Muestra la visualización."""
        if self.fig:
            self.fig.show()

    def close(self) -> None:
        """Cierra la figura para liberar memoria."""
        if self.fig:
            plt.close(self.fig)
