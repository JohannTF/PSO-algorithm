"""Registry unificado para todas las estrategias de peso inercial."""

from typing import Dict, List, Tuple, Type, Union

from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy


class InertiaRegistry:
    """Registro central de todas las estrategias de peso inercial disponibles.

    Unifica estrategias básicas y adaptativas bajo un mismo patrón.
    """

    # Diccionario que mapea nombres de estrategias a sus clases
    _strategies: Dict[str, Type[InertiaStrategy]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorador para registrar una estrategia de inercia.

        Args:
            name (str): Nombre identificador de la estrategia.

        Returns:
            Callable: Decorador que registra la clase.
        """
        def decorator(strategy_class: Type[InertiaStrategy]):
            cls._strategies[name] = strategy_class
            return strategy_class
        return decorator

    @classmethod
    def get_available_strategies(cls) -> List[str]:
        """Retorna la lista de estrategias disponibles.

        Returns:
            List[str]: Lista con nombres de estrategias disponibles.
        """
        return list(cls._strategies.keys())

    @classmethod
    def create_strategy(cls, name: str, w_min: float, w_max: float,
                       params: Union[List, Tuple] = None) -> InertiaStrategy:
        """Crea una instancia de estrategia.

        Args:
            name (str): Nombre de la estrategia.
            w_min (float): Valor mínimo de peso inercial.
            w_max (float): Valor máximo de peso inercial.
            params (Union[List, Tuple], optional): Parámetros específicos de
                la estrategia. Defaults to None.

        Returns:
            InertiaStrategy: Instancia de la estrategia.

        Raises:
            ValueError: Si la estrategia no está registrada.
        """
        if name not in cls._strategies:
            available = cls.get_available_strategies()
            raise ValueError(
                f"Estrategia de inercia '{name}' no registrada. "
                f"Estrategias disponibles: {available}"
            )

        strategy_class = cls._strategies[name]

        # Patrón uniforme: todas las estrategias manejan sus parámetros
        return strategy_class(w_min=w_min, w_max=w_max, params=params)
    
    