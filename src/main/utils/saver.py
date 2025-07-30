"""Módulo para guardar resultados del algoritmo PSO."""

import json
import os
from typing import Any, Dict, Optional, Set

from src.main.utils.constants import EXCLUDED_FIELDS, NON_SERIALIZABLE_KEYS


def save_results(
    config: Dict[str, Any],
    stats: Dict[str, Any],
    multi_run_stats: Optional[Dict[str, Any]] = None,
) -> str:
    """Guarda resultados del algoritmo en archivo JSON estructurado.

    Args:
        config (Dict[str, Any]): Configuración del algoritmo.
        stats (Dict[str, Any]): Estadísticas de ejecución (o mejor ejecución 
            si hay múltiples).
        multi_run_stats (Optional[Dict[str, Any]]): Estadísticas agregadas de 
            múltiples ejecuciones.

    Returns:
        str: Ruta del archivo guardado.
    """
    base_path = config["base_output_path"]
    output_file = config["output_file"]

    os.makedirs(base_path, exist_ok=True)

    file_path = os.path.join(base_path, f"{output_file}.json")

    # Preparar contenido a guardar
    content = {
        "configuration": filter_data(config, NON_SERIALIZABLE_KEYS),
        "statistics": {
            "best_execution": filter_data(stats, EXCLUDED_FIELDS),
        }
    }

    # Añadir estadísticas múltiples si están disponibles
    if multi_run_stats:
        content["statistics"]["multi_run"] = filter_data(
            multi_run_stats, EXCLUDED_FIELDS
        )

    with open(file_path, "w") as f:
        json.dump(content, f, indent=2)

    return file_path


def filter_data(data: Dict[str, Any], excluded_keys: Set[str]) -> Dict[str, Any]:
    """Filtra diccionario excluyendo claves especificadas.

    Procesa recursivamente diccionarios anidados.

    Args:
        data (Dict[str, Any]): Diccionario a filtrar.
        excluded_keys (Set[str]): Conjunto de claves a excluir.

    Returns:
        Dict[str, Any]: Diccionario filtrado.
    """
    filtered_data = {}

    for key, value in data.items():
        if key in excluded_keys:
            continue

        if isinstance(value, dict):
            filtered_data[key] = filter_data(value, excluded_keys)
        else:
            filtered_data[key] = value

    return filtered_data
