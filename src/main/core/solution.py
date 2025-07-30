"""Clase para representar soluciones del algoritmo PSO."""

from typing import Any, Dict, Optional

import numpy as np


class Solution:
    """Clase para representar la mejor solución encontrada por el algoritmo PSO.
    
    Almacena la posición, velocidad y el valor de fitness.
    """

    def __init__(
        self,
        position: np.ndarray,
        fitness: float,
        velocity: Optional[np.ndarray] = None
    ) -> None:
        """Inicializa una solución.

        Args:
            position (np.ndarray): Vector de posición de la solución.
            fitness (float): Valor de aptitud asociado.
            velocity (Optional[np.ndarray], optional): Vector de velocidad de la 
                partícula. Defaults to None.
        """
        self.position = np.copy(position)
        self.fitness = fitness
        self.velocity = (
            np.copy(velocity) if velocity is not None else np.zeros_like(position)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la solución a un diccionario.
        

        Returns:
            Dict[str, Any]: Representación en diccionario de la solución.
        """
        return {
            "position": (
                self.position.tolist()
                if isinstance(self.position, np.ndarray)
                else self.position
            ),
            "fitness": float(self.fitness),
            "velocity": (
                self.velocity.tolist()
                if isinstance(self.velocity, np.ndarray)
                else self.velocity
            ),
        }

    def __str__(self) -> str:
        """Representación en cadena de la solución.

        Returns:
            str: Cadena que describe la solución.
        """
        position_str = np.array2string(self.position, precision=6, separator=", ")
        velocity_str = np.array2string(self.velocity, precision=6, separator=", ")
        return (f"Solution(fitness={self.fitness:.6f}, position={position_str}, "
                f"velocity={velocity_str})")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Solution":
        """Crea una solución a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Diccionario con los datos de la solución.

        Returns:
            Solution: Nueva instancia de solución.
        """
        return cls(
            position=np.array(data["position"]),
            fitness=data["fitness"],
            velocity=np.array(data["velocity"]) if "velocity" in data else None,
        )
