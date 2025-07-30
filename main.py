"""Script principal para ejecutar el algoritmo PSO con configuración especificada."""

import sys
from src.main.utils.loader import load_config
from src.main.handlers.pso_runner import PSORunner


def main():
    """Ejecuta el algoritmo PSO según la configuración proporcionada."""
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_configuracion.json>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        config = load_config(config_file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{config_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        sys.exit(1)

    try:
        runner = PSORunner(config)
        runner.run()
    except ValueError as e:
        print(f"\nError de validación: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError durante la ejecución: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
