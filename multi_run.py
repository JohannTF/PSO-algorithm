#!/usr/bin/env python3
"""Runner para probar todas las estrategias de inercia en PSO.

Este script ejecuta pruebas de las estrategias avanzadas con sus configuraciones
específicas de coeficientes c1 y c2, así como las estrategias básicas del sistema.
"""

import os
import json
import subprocess
import tempfile
import signal
import sys
import threading
import queue
from pathlib import Path
from typing import List, Dict, Any, Tuple
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

BENCHMARKS = ["sphere", "rastrigin", "rosenbrock", "griewank"]
DIMENSIONS = [10, 20, 30]

# Estrategias avanzadas con sus configuraciones específicas según strategy_inertia.tex
STRATEGIES = {
    # Estrategias avanzadas originales
    "linear_decreasing": {
        "inertia_config": [0.4, 0.9, "linear_decreasing"],
        "c1": 2,
        "c2": 2,
        "description": "PSO-LDIW (Linear Decreasing Inertia Weight)",
        # Configuración específica para esta estrategia
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "pso_niew": {
        "inertia_config": [0.4, 0.9, "pso_niew"],
        "c1": 2.0,
        "c2": 2.0,
        "description": "PSO-NIEW (Non-linear Exponential Inertia Weight)",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "pso_siw": {
        "inertia_config": [0.4, 0.5, "pso_siw", 2.0],  # w_min, w_max, strategy, s
        "c1": 2.0,
        "c2": 2.0,
        "description": "PSO-SIW (Sigmoidal Inertia Weight)",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "de_pso": {
        "inertia_config": [0.4, 0.8, "de_pso"],
        "c1": 2.8,
        "c2": 1.3,
        "description": "DE-PSO (Differential Evolution - PSO)",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "gpso": {
        "inertia_config": [0.5, 0.9, "gpso"],
        "c1": 2.0,
        "c2": 2.0,
        "description": "GPSO (Global PSO)",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "pso_tvac": {
        "inertia_config": [0.4, 0.9, "pso_tvac"],
        "c1": [0.5, 2.5, "linear_decreasing"],  # 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # 0.5 → 2.5
        "description": "PSO-TVAC (Time Varying Acceleration Coefficients)",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "dsi_pso": {
        "inertia_config": [0.2, 0.8, "dsi_pso", 0.5],  # w_f, w_i, strategy, sensitivity
        "c1": [0.5, 2.5, "linear_decreasing"],  # c_p: 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # c_g: 0.5 → 2.5
        "description": "PSO con DSI (Distance-dependent Sigmoidal Inertia)",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },

    # Nueva estrategia híbrida propuesta
    "hybrid_cosine": {
        "inertia_config": [0.4, 0.9, "hybrid_cosine", "linear_decreasing", "SEP", "convex_decreasing"],
        "c1": [0.5, 2.5, "linear_decreasing"],  # c_p: 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # c_g: 0.5 → 2.5
        "description": "Hybrid Cosine",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },

    # Estrategias básicas del runner 03 con configuración estándar
    "concave_decreasing": {
        "inertia_config": [0.4, 0.9, "concave_decreasing"],
        "c1": [0.5, 2.5, "linear_decreasing"],  # c_p: 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # c_g: 0.5 → 2.5
        "description": "Concave Decreasing Inertia Weight",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "convex_decreasing": {
        "inertia_config": [0.4, 0.9, "convex_decreasing"],
        "c1": [0.5, 2.5, "linear_decreasing"],  # c_p: 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # c_g: 0.5 → 2.5
        "description": "Convex Decreasing Inertia Weight",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "convex_exp_decreasing": {
        "inertia_config": [0.4, 0.9, "convex_exp_decreasing"],
        "c1": [0.5, 2.5, "linear_decreasing"],  # c_p: 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # c_g: 0.5 → 2.5
        "description": "Convex Exponential Decreasing Inertia Weight",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "concave_exp_decreasing": {
        "inertia_config": [0.4, 0.9, "concave_exp_decreasing"],
        "c1": [0.5, 2.5, "linear_decreasing"],  # c_p: 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # c_g: 0.5 → 2.5
        "description": "Concave Exponential Decreasing Inertia Weight",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "concave_exp_increasing": {
        "inertia_config": [0.4, 0.9, "concave_exp_increasing"],
        "c1": [0.5, 2.5, "linear_decreasing"],  # c_p: 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # c_g: 0.5 → 2.5
        "description": "Concave Exponential Increasing Inertia Weight",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "convex_exp_increasing": {
        "inertia_config": [0.4, 0.9, "convex_exp_increasing"],
        "c1": [0.5, 2.5, "linear_decreasing"],  # c_p: 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # c_g: 0.5 → 2.5
        "description": "Convex Exponential Increasing Inertia Weight",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    },
    "aleatory": {
        "inertia_config": [0.4, 0.9, "aleatory"],
        "c1": [0.5, 2.5, "linear_decreasing"],  # c_p: 2.5 → 0.5
        "c2": [0.5, 2.5, "linear_increasing"],  # c_g: 0.5 → 2.5
        "description": "Random Inertia Weight",
        "config": {
            "population_size": 100,
            "generations": 100,
            "multi_run_visualization": True
        }
    }
}

# Número de ejecuciones por combinación
RUNS = 30

# Directorio de salida
BASE_OUTPUT_DIR = Path("cases_inertia_strategies")


class UnifiedInertiaStrategiesRunner:
    def __init__(self):
        self.base_output_dir = BASE_OUTPUT_DIR
        self.benchmarks = BENCHMARKS
        self.dimensions = DIMENSIONS
        self.strategies = STRATEGIES
        self.runs = RUNS
        
        # Registrar manejador para interrupciones
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, signal_received, frame):
        print(f"\n{Fore.YELLOW}Ejecución interrumpida por el usuario. Saliendo...{Style.RESET_ALL}")
        sys.exit(0)

    def _create_config_for_strategy(self, strategy_config: Dict[str, Any], 
                                   benchmark: str, dimension: int) -> Dict[str, Any]:
        """
        Crea la configuración específica para una estrategia.
        
        Args:
            strategy_config (Dict[str, Any]): Configuración de la estrategia
            benchmark (str): Nombre del benchmark
            dimension (int): Dimensión del problema
            
        Returns:
            Dict[str, Any]: Configuración completa para la estrategia
        """
        # Comenzar con la configuración específica de la estrategia
        config = strategy_config["config"].copy()
        
        # Agregar configuraciones dinámicas
        config["dimensions"] = dimension
        config["benchmark"] = benchmark
        config["runs"] = self.runs
        
        # Configurar estrategia de inercia
        config["inertia_type"] = strategy_config["inertia_config"]
        
        # Configurar coeficientes c1 y c2
        config["c1"] = strategy_config["c1"]
        config["c2"] = strategy_config["c2"]
        
        return config

    def run_all(self):
        """
        Ejecuta todas las pruebas para las estrategias avanzadas configuradas.
        """
        print(f"{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}= {Fore.WHITE}Runner PSO unificado - Todas las estrategias de inercia{Fore.CYAN}")
        print(f"{Fore.CYAN}= {Fore.WHITE}Incluye estrategias avanzadas, básicas e híbridas{Fore.CYAN}")
        print(f"{Fore.CYAN}= {Fore.WHITE}Configuraciones integradas por estrategia{Fore.CYAN}")
        print(f"{Fore.CYAN}{'='*80}")

        try:
            for strategy_name, strategy_config in self.strategies.items():
                print(f"\n{Fore.MAGENTA}{'='*60}")
                print(f"{Fore.MAGENTA}= {Fore.WHITE}Estrategia: {strategy_config['description']}{Fore.MAGENTA}")
                print(f"{Fore.MAGENTA}{'='*60}")
                
                # Crear directorio para esta estrategia
                strategy_dir = self.base_output_dir / f"strategy_{strategy_name}"
                strategy_dir.mkdir(parents=True, exist_ok=True)
                
                for dimension in self.dimensions:
                    print(f"\n{Fore.YELLOW}  📊 Dimensión: {dimension}")
                    
                    # Crear directorio para esta dimensión
                    dim_dir = strategy_dir / f"dimension{dimension}"
                    dim_dir.mkdir(exist_ok=True)
                    
                    # Crear directorio para visualizaciones
                    vis_dir = dim_dir / "visualizations"
                    vis_dir.mkdir(exist_ok=True)
                    
                    for benchmark in self.benchmarks:
                        self._run_benchmark(
                            benchmark=benchmark,
                            dimension=dimension,
                            strategy_name=strategy_name,
                            strategy_config=strategy_config,
                            dim_dir=dim_dir,
                            vis_dir=vis_dir
                        )
                        
            print(f"\n{Fore.GREEN}{'='*80}")
            print(f"{Fore.GREEN}= {Fore.WHITE}¡Todas las ejecuciones completadas con éxito!{Fore.GREEN}")
            print(f"{Fore.GREEN}= {Fore.WHITE}Resultados guardados en: {self.base_output_dir}{Fore.GREEN}")
            print(f"{Fore.GREEN}{'='*80}")
            
        except Exception as e:
            print(f"\n{Fore.RED}Error durante la ejecución: {str(e)}")
            sys.exit(1)

    def _run_benchmark(self, benchmark, dimension, strategy_name, strategy_config, 
                      dim_dir, vis_dir):
        """
        Ejecuta una prueba con una configuración específica.
        
        Args:
            benchmark (str): Nombre de la función benchmark
            dimension (int): Dimensión del problema
            strategy_name (str): Nombre de la estrategia
            strategy_config (Dict[str, Any]): Configuración de la estrategia
            dim_dir (Path): Directorio para resultados
            vis_dir (Path): Directorio para visualizaciones
        """
        # Crear configuración específica para esta prueba usando la configuración de la estrategia
        config = self._create_config_for_strategy(strategy_config, benchmark, dimension)
        
        # Configurar rutas de salida
        output_file = f"{benchmark}_dim{dimension}"
        config["output_file"] = output_file
        config["base_output_path"] = str(dim_dir)
        config["visualization_path"] = str(vis_dir / output_file)
        
        # Configurar visualizaciones
        config["show_multiple_visualizations"] = False
        config["save_multiple_visualizations"] = True
        config["multi_run_visualization"] = {
            "best_run_fitness": True,
            "best_run_inertia": True,
            "best_fitness_per_run": True,
            "avg_fitness_per_run": True,
            "diversity": True
        }

        print(f"\n  {Fore.BLUE}        • 🚀 Ejecutando {Fore.WHITE}{benchmark}{Fore.BLUE} "
              f"con {strategy_name}: c1={strategy_config['c1']}, c2={strategy_config['c2']}")

        # Crear archivo temporal con la configuración
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as tmp:
            temp_filename = tmp.name
            json.dump(config, tmp, indent=2)              
        
        try:
            # Ejecutar el algoritmo PSO
            result = subprocess.run(
                f"python main.py {temp_filename}",
                shell=True,
                check=False
            )
            
            if result.returncode == 0:
                print(f"  {Fore.GREEN}           ✓ Completado{Fore.RESET} → Resultados: {dim_dir / (output_file + '.json')}")
            else:
                print(f"  {Fore.RED}            ✗ Error (código: {result.returncode})")
                
        except Exception as e:
            print(f"  {Fore.RED}✗ Excepción: {str(e)}")
        finally:
            # Limpiar archivo temporal
            try:
                os.unlink(temp_filename)
            except OSError:
                pass
            print(f"  {Fore.CYAN}{'─'*50}")

    def print_strategy_summary(self):
        """
        Imprime un resumen de las estrategias que se van a probar.
        """
        print(f"\n{Fore.CYAN}📋 Resumen de estrategias a probar:")
        print(f"{Fore.CYAN}{'='*50}")
        
        for strategy_name, config in self.strategies.items():
            print(f"\n{Fore.YELLOW}🔧 {config['description']}")
            print(f"   • Inercia: {config['inertia_config']}")
            print(f"   • c1: {config['c1']}")
            print(f"   • c2: {config['c2']}")
        
        print(f"\n{Fore.CYAN}📊 Benchmarks: {', '.join(self.benchmarks)}")
        print(f"{Fore.CYAN}📐 Dimensiones: {', '.join(map(str, self.dimensions))}")
        print(f"{Fore.CYAN}🔄 Ejecuciones por configuración: {self.runs}")
        print(f"{Fore.CYAN}📁 Directorio de salida: {self.base_output_dir}")
        print(f"\n{Fore.WHITE}Total de estrategias: {Fore.YELLOW}{len(self.strategies)}")
        print(f"{Fore.WHITE}Total de configuraciones a ejecutar: {Fore.YELLOW}{len(self.strategies) * len(self.benchmarks) * len(self.dimensions)}")


def main():
    runner = UnifiedInertiaStrategiesRunner()
    
    # Mostrar resumen antes de empezar
    runner.print_strategy_summary()
    
    # Preguntar confirmación
    print(f"\n{Fore.YELLOW}¿Desea continuar con la ejecución? (y/N): ", end="")
    response = input().strip().lower()
    
    if response in ['y', 'yes', 'sí', 'si']:
        runner.run_all()
    else:
        print(f"{Fore.CYAN}Ejecución cancelada por el usuario.")


if __name__ == "__main__":
    main()
