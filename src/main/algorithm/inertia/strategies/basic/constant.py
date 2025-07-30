"""Implementación de la estrategia de peso inercial constante."""

from typing import List, Optional, Tuple, Union

from src.main.algorithm.inertia.inertia_registry import InertiaRegistry
from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy


@InertiaRegistry.register("constant")
class Constant(InertiaStrategy):
    """Estrategia de peso inercial fijo para PSO."""

    def __init__(self, w_min: float = 0.4, w_max: float = 0.9,
                 params: Union[List, Tuple] = None) -> None:
        """Inicializa la estrategia de peso inercial constante.

        Args:
            w_min (float): Valor mínimo del peso inercial (no usado directamente).
                Defaults to 0.4.
            w_max (float): Valor máximo del peso inercial (usado como valor
                constante por defecto). Defaults to 0.9.
            params (Union[List, Tuple], optional): Parámetros específicos:
                [value] (opcional). Si se proporciona, params[0] será usado
                como el valor constante. Defaults to None.

        Raises:
            ValueError: Si el parámetro 'value' no es un número válido.
        """
        # Si se proporciona un valor específico en params, usarlo
        if params is not None and len(params) > 0:
            try:
                value = params[0]
                if not isinstance(value, (float, int)):
                    raise ValueError(
                        "El parámetro 'value' para constant debe ser un número."
                    )
                self.value = float(value)
            except (IndexError, ValueError, TypeError) as e:
                raise ValueError(
                    f"Error al procesar parámetro 'value' para constant: {e}"
                ) from e
        else:
            # Por defecto, usar w_max como valor constante
            self.value = w_max

    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: Optional[dict] = None) -> float:
        """Calcula el peso inercial constante.

        Args:
            current_iteration (int): Iteración actual.
            max_iterations (int): Número máximo de iteraciones.
            particle_info (Optional[dict], optional): Información de partículas
                (no utilizada). Defaults to None.

        Returns:
            float: Valor constante del peso inercial.
        """
        return self.value
