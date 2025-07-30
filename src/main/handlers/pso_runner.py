"""Ejecutor PSO."""

from typing import Any, Dict, Tuple

import numpy as np
from tqdm import tqdm

from src.main.algorithm.pso import PSO
from src.main.config.validation.pipeline.pipeline import create_pipeline
from src.main.handlers.graphics_handler import GraphicsHandler
from src.main.utils.saver import save_results


class PSORunner:
    """Ejecutor de algoritmos PSO con validación."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Inicializa el ejecutor del algoritmo PSO.

        Args:
            config: Diccionario con la configuración del algoritmo.
        """
        self.config = self._validate_configuration(config)
        
        # Variables de estado
        self.all_stats = []
        self.best_stats = None
        self.best_run_index = -1
        self.multi_run_stats = None
        
        self._initialize_graphics_handler()
    
    def _validate_configuration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Valida configuración usando pipeline auto-generado.
        
        Args:
            config: Configuración original.
            
        Returns:
            Configuración validada.
            
        Raises:
            ValueError: Si la validación falla.
        """
        try:
            pipeline = create_pipeline()
            return pipeline.validate(config)
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {e}") from e

    def _initialize_graphics_handler(self) -> None:
        """Inicializa el manejador de gráficos si es necesario."""
        visualization_enabled = (
            self.config.get("show_individual_visualizations", False) or 
            self.config.get("save_individual_visualizations", False) or
            self.config.get("show_multiple_visualizations", False) or 
            self.config.get("save_multiple_visualizations", False)
        )
        if visualization_enabled:
            self.graphics_handler = GraphicsHandler(self.config)
        else:
            self.graphics_handler = None

    def run(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Ejecuta el algoritmo PSO según la configuración.

        Returns:
            Tupla con estadísticas y configuración validada
        """
        num_runs = self.config["runs"]
        
        try:
            if num_runs == 1:
                stats = self._run_single()

                if self.config.get("save_results", False):
                    save_results(self.config, stats)
                    
                return stats, self.config
            else:
                self._run_multiple(num_runs)

                if self.config.get("save_results", False):
                    save_results(self.config, self.best_stats, self.multi_run_stats)
                    
                return self.best_stats, self.config
                
        except Exception as e:
            raise RuntimeError(f"PSO execution failed: {e}") from e

    def _run_single(self, is_only_one_run: bool = True) -> Dict[str, Any]:
        """Ejecuta una vez el algoritmo PSO.

        Args:
            is_only_one_run: Indica si es ejecución única aislada

        Returns:
            Estadísticas de la ejecución
        """
        show_progress = self.config.get("show_progress_bar", True) and is_only_one_run
        
        pso_algorithm = PSO(
            config=self.config,
            show_progress=show_progress,
        )
        
        stats = pso_algorithm.run()

        # Crear visualizaciones si corresponde
        if self.graphics_handler and (
            self.config.get("show_individual_visualizations", False) or 
            self.config.get("save_individual_visualizations", False)
        ):
            self.graphics_handler.create_single_run_visualizations(
                stats=stats,
                pso_algorithm=pso_algorithm,
                benchmark_function=pso_algorithm.objective_function,
            )

        return stats

    def _run_multiple(self, num_runs: int) -> None:
        """Ejecuta el algoritmo PSO múltiples veces.

        Args:
            num_runs: Número de ejecuciones a realizar
        """
        show_progress = self.config.get("show_progress_bar", True)
        runs_progress = (
            tqdm(total=num_runs, desc="Progreso de las ejecuciones") 
            if show_progress else None
        )

        best_fitness_per_run, avg_fitness_per_run = [], []
        all_avg_fitness_history = []

        for run in range(num_runs):
            stats = self._run_single(is_only_one_run=False)
            self.all_stats.append(stats)

            # Actualizar estadísticas
            best_fitness_per_run.append(stats["best_solution"]["fitness"])
            avg_fitness_per_run.append(
                np.mean(stats["history"]["avg_fitness_per_generation"])
            )
            
            all_avg_fitness_history.append(
                stats["history"]["avg_fitness_per_generation"]
            )

            # Actualizar mejor resultado
            if (self.best_stats is None or 
                stats["best_solution"]["fitness"] < 
                self.best_stats["best_solution"]["fitness"]):
                self.best_stats, self.best_run_index = stats, run

            # Guardar visualizaciones individuales si corresponde
            if (self.graphics_handler and 
                self.config.get("save_individual_visualizations", False)):
                temp_pso = PSO(config=self.config, show_progress=False)
                
                self.graphics_handler.create_single_run_visualizations(
                    stats=stats,
                    pso_algorithm=temp_pso,
                    benchmark_function=temp_pso.objective_function,
                    run_index=run,
                )

            if show_progress:
                runs_progress.update(1)

        if show_progress:
            runs_progress.close()

        # Calcular estadísticas globales
        self.multi_run_stats = {
            "best_run_index": self.best_run_index + 1,
            "best_fitness_per_run": best_fitness_per_run,
            "avg_fitness_per_run": avg_fitness_per_run,
            "all_avg_fitness_history": all_avg_fitness_history,
            "global_avg_best_fitness": np.mean(best_fitness_per_run),
            "global_avg_fitness": np.mean(avg_fitness_per_run),
            "variance": np.var(best_fitness_per_run),
            "std_deviation": np.std(best_fitness_per_run),
        }
        
        # Crear visualizaciones múltiples
        if self.graphics_handler:
            self.graphics_handler.create_multi_run_visualizations(
                all_stats=self.all_stats,
                best_stats=self.best_stats,
                best_run_index=self.best_run_index,
                multi_run_stats=self.multi_run_stats,
            )
