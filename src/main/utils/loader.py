"""Módulo para cargar configuraciones desde archivos JSON."""

import json
import sys
from typing import Any, Dict


def load_config(config_file: str) -> Dict[str, Any]:
    """Carga configuración desde archivo JSON.

    Args:
        config_file (str): Ruta al archivo de configuración JSON.

    Returns:
        Dict[str, Any]: Diccionario con la configuración cargada.

    Raises:
        SystemExit: Si el archivo no existe o contiene JSON inválido.
    """
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo JSON: '{config_file}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{config_file}' no contiene JSON válido")
        sys.exit(1)