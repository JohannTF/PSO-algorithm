"""Implementación de la estrategia de peso inercial híbrida con coseno."""

import math
from typing import Any, Dict, List, Tuple, Union

import numpy as np

from src.main.algorithm.inertia.inertia_strategy import InertiaStrategy
from src.main.algorithm.inertia.inertia_registry import InertiaRegistry


@InertiaRegistry.register("hybrid_cosine")
class HybridCosine(InertiaStrategy):
    """
    Implementación de la estrategia de peso inercial híbrida con interpolación coseno.

    Fórmula: P(k) = [(1 + cos((k*π)/phi))/2] * g(k) + [(1 - cos((k*π))/phi)/2] * h(k)

    donde:
    - k es la iteración actual normalizada (current_iteration / max_iterations)
    - g(k) y h(k) son dos estrategias de peso inercial diferentes
    - La función coseno actúa como peso de interpolación entre las dos estrategias

    Esta estrategia permite combinar dos enfoques diferentes de peso inercial,
    creando transiciones suaves y comportamientos adaptativos únicos.
    """

    def __init__(self, w_min: float = 0.4, w_max: float = 0.9,
                 params: Union[List, Tuple] = None):
        """
        Inicializa la estrategia de peso inercial híbrida.

        Args:
            w_min (float): Valor mínimo del peso inercial (usado por defecto para estrategias que lo requieran)
            w_max (float): Valor máximo del peso inercial (usado por defecto para estrategias que lo requieran)
            params (Union[List, Tuple], optional): Parámetros específicos: [strategy1_name, strategy1_params..., "SEP", strategy2_name, strategy2_params...]

                   Ejemplo:
                   ["linear_decreasing", "SEP", "pso_siw", 2.0]
                   ["constant", 0.7, "SEP", "dsi_pso", 0.5]
                   Defaults to None.
        """
        self.w_min = w_min
        self.w_max = w_max
        self.strategy_g = None  # Primera estrategia g(k)
        self.strategy_h = None  # Segunda estrategia h(k)

        if params is not None:
            self._parse_and_create_strategies(params)
        else:
            # Configuración por defecto: linear_decreasing + constant
            self._create_default_strategies()

    def _parse_and_create_strategies(self, params: Union[List, Tuple]) -> None:
        """
        Parsea los parámetros y crea las dos estrategias híbridas.

        Args:
            params (Union[List, Tuple]): Parámetros específicos: [strategy1_name, strategy1_params..., "SEP", strategy2_name, strategy2_params...]

        Raises:
            ValueError: Si el formato de parámetros es incorrecto
        """
        if len(params) < 3:  # Mínimo: [strategy1, "SEP", strategy2]
            raise ValueError("Hybrid cosine strategy requires at least 3 parameters: "
                           "[strategy1_name, 'SEP', strategy2_name, ...]")

        try:
            # Buscar el separador "SEP"
            sep_index = None
            for i, param in enumerate(params):
                if isinstance(param, str) and param.upper() == "SEP":
                    sep_index = i
                    break

            if sep_index is None:
                raise ValueError("Missing 'SEP' separator between strategies in hybrid_cosine parameters")

            # Extraer parámetros de la primera estrategia (g)
            strategy1_params = params[0:sep_index]
            strategy1_name = strategy1_params[0]
            strategy1_extra_params = strategy1_params[1:] if len(strategy1_params) > 1 else []

            # Extraer parámetros de la segunda estrategia (h)
            strategy2_params = params[sep_index + 1:]
            if not strategy2_params:
                raise ValueError("Missing second strategy parameters after 'SEP' in hybrid_cosine")

            strategy2_name = strategy2_params[0]
            strategy2_extra_params = strategy2_params[1:] if len(strategy2_params) > 1 else []

            # Crear las estrategias usando el registry
            self.strategy_g = self._create_strategy(strategy1_name, strategy1_extra_params)
            self.strategy_h = self._create_strategy(strategy2_name, strategy2_extra_params)

        except Exception as e:
            raise ValueError(f"Error parsing hybrid_cosine parameters: {e}") from e

    def _create_strategy(self, strategy_name: str, extra_params: List) -> InertiaStrategy:
        """
        Crea una estrategia individual para usar en la híbrida.

        Args:
            strategy_name (str): Nombre de la estrategia
            extra_params (List): Parámetros adicionales específicos de la estrategia

        Returns:
            InertiaStrategy: Instancia de la estrategia creada
        """
        # Importación tardía para evitar importación circular
        from src.main.algorithm.inertia.inertia_factory import get_inertia_strategy

        # Construir el formato de parámetros que espera get_inertia_strategy
        if strategy_name == "constant" and extra_params:
            # Para estrategia constante, usar el valor proporcionado
            constant_value = extra_params[0]
            inertia_info = constant_value  # Formato para valor constante
        else:
            # Para otras estrategias, usar el formato [w_min, w_max, strategy_name, ...params]
            inertia_info = [self.w_min, self.w_max, strategy_name] + extra_params

        return get_inertia_strategy(inertia_info)

    def _create_default_strategies(self) -> None:
        """
        Crea estrategias por defecto cuando no se proporcionan parámetros.
        """
        # Importación tardía para evitar importación circular
        from src.main.algorithm.inertia.inertia_factory import get_inertia_strategy

        # Por defecto: linear_decreasing + constant(w_min)
        self.strategy_g = get_inertia_strategy([self.w_min, self.w_max, "linear_decreasing"])
        self.strategy_h = get_inertia_strategy(self.w_min)  # Valor constante

    @property
    def requires_particle_info(self) -> bool:
        """
        Verifica si alguna de las estrategias híbridas requiere información de partículas.

        Returns:
            bool: True si cualquiera de las estrategias requiere información de partículas
        """
        return (self.strategy_g and self.strategy_g.requires_particle_info) or \
               (self.strategy_h and self.strategy_h.requires_particle_info)

    @property
    def returns_array(self) -> bool:
        """
        Verifica si la estrategia híbrida debe retornar un array.
        Retorna True si cualquiera de las estrategias componentes retorna un array.

        Returns:
            bool: True si debe retornar un array, False si retorna un valor escalar
        """
        return (self.strategy_g and self.strategy_g.returns_array) or \
               (self.strategy_h and self.strategy_h.returns_array)

    def collect_required_info(self, pso_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recopila información requerida por las estrategias híbridas.

        Args:
            pso_state (Dict[str, Any]): Estado actual del algoritmo PSO

        Returns:
            Dict[str, Any]: Información requerida
        """
        info = {}

        if self.strategy_g and self.strategy_g.requires_particle_info:
            info.update(self.strategy_g.collect_required_info(pso_state))

        if self.strategy_h and self.strategy_h.requires_particle_info:
            info.update(self.strategy_h.collect_required_info(pso_state))

        return info

    def __call__(self, current_iteration: int, max_iterations: int,
                 particle_info: dict = None) -> Union[float, np.ndarray]:
        """
        Calcula el valor del peso inercial híbrido para la iteración actual.

        Args:
            current_iteration (int): Iteración actual del algoritmo
            max_iterations (int): Número máximo de iteraciones
            particle_info (dict, optional): Información de partículas (si es requerida por alguna estrategia).
                Defaults to None.

        Returns:
            Union[float, np.ndarray]: Valor(es) del peso inercial híbrido

        Raises:
            ValueError: Si la estrategia híbrida no está correctamente inicializada
        """
        if not self.strategy_g or not self.strategy_h:
            raise ValueError("Hybrid cosine strategy not properly initialized")

        # Asegurar que no se divida por cero
        if max_iterations <= 1:
            # En caso extremo, retornar promedio de ambas estrategias
            g_value = self.strategy_g(current_iteration, max_iterations, particle_info)
            h_value = self.strategy_h(current_iteration, max_iterations, particle_info)

            if isinstance(g_value, np.ndarray) or isinstance(h_value, np.ndarray):
                return (np.asarray(g_value) + np.asarray(h_value)) / 2
            else:
                return (g_value + h_value) / 2

        # Calcular los pesos de interpolación coseno
        phi = (1 + math.sqrt(5)) / 2
        cos_k_pi = math.cos((current_iteration * math.pi) / phi)
        weight_g = (1 + cos_k_pi) / 2  # Peso para g(k)
        weight_h = (1 - cos_k_pi) / 2  # Peso para h(k)

        # Obtener valores de ambas estrategias
        g_value = self.strategy_g(current_iteration, max_iterations, particle_info)
        h_value = self.strategy_h(current_iteration, max_iterations, particle_info)

        # Normalizar a arrays si es necesario para consistencia
        if isinstance(g_value, np.ndarray) or isinstance(h_value, np.ndarray):
            # Al menos una estrategia retorna array, convertir ambas a arrays
            g_array = np.asarray(g_value) if not isinstance(g_value, np.ndarray) else g_value
            h_array = np.asarray(h_value) if not isinstance(h_value, np.ndarray) else h_value

            # Si una es escalar y otra array, expandir la escalar para coincidir
            if g_array.ndim == 0 and h_array.ndim > 0:
                g_array = np.full_like(h_array, g_array.item())
            elif h_array.ndim == 0 and g_array.ndim > 0:
                h_array = np.full_like(g_array, h_array.item())

            # Aplicar la fórmula híbrida
            return weight_g * g_array + weight_h * h_array
        else:
            # Ambas son escalares
            return weight_g * g_value + weight_h * h_value

    def __str__(self) -> str:
        """
        Representación en cadena de la estrategia híbrida.

        Returns:
            str: Descripción de la estrategia
        """
        g_name = type(self.strategy_g).__name__ if self.strategy_g else "None"
        h_name = type(self.strategy_h).__name__ if self.strategy_h else "None"
        return f"HybridCosine(g={g_name}, h={h_name})"
