"""Módulo para cargar estrategias de peso inercial."""

from src.main.algorithm.inertia.inertia_registry import InertiaRegistry
from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy
from src.main.algorithm.inertia.strategies import *


def get_inertia_strategy(inertia_info) -> InertiaStrategy:
    """Obtiene una estrategia de peso inercial basada en el tipo especificado.

    Args:
        inertia_info (Union[float, int, List, Tuple]): Tipo de estrategia 
            validado (float fijo, tupla con parámetros, etc.).

    Returns:
        InertiaStrategy: Objeto de estrategia para calcular el peso inercial.

    Raises:
        ValueError: Si el tipo de estrategia no está soportado.
    """
    # Caso 1: Valor constante de inercia
    if isinstance(inertia_info, (float, int)):
        return Constant(
            w_min=float(inertia_info),
            w_max=float(inertia_info)
        )

    # Caso 2: Parámetros en formato tupla/lista
    elif isinstance(inertia_info, (list, tuple)):
        # Extraer parámetros básicos (ya validados)
        w_min, w_max = float(inertia_info[0]), float(inertia_info[1])
        strategy_name = inertia_info[2]

        strategy_params = inertia_info[3:] if len(inertia_info) > 3 else []
        return InertiaRegistry.create_strategy(
            name=strategy_name,
            w_min=w_min,
            w_max=w_max,
            params=strategy_params
        )

    # Caso 3: Tipo no soportado
    else:
        raise ValueError(
            f"Tipo de estrategia de peso inercial '{inertia_info}' no soportado."
        )
