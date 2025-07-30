"""Implementación del algoritmo Particle Swarm Optimization (PSO)."""

from typing import Any, Dict, List, Union

import numpy as np
from tqdm import tqdm

from src.main.algorithm.particle import PSOParticle
from src.main.core.solution import Solution
from src.main.utils.constants import PSO_STATS_SAVE_INTERVAL


class PSO:
    """Implementación del algoritmo Particle Swarm Optimization (PSO)."""

    def __init__(
        self,
        config: Dict[str, Any],
        show_progress: bool = True,
    ) -> None:
        """Inicializa el algoritmo PSO.

        Args:
            config (Dict[str, Any]): Diccionario con la configuración ya validada.
            show_progress (bool, optional): Si se debe mostrar barra de progreso. 
                Defaults to True.
        """
        # Extraer parámetros de la configuración
        self.dimensions = config["dimensions"]
        self.population_size = config["population_size"]
        self.generations = config["generations"]
        self.show_progress = show_progress

        # Usar componentes ya validados y creados
        self.bounds = config["bounds"]
        self.velocity_bounds = config["velocity_bounds"]
        self.objective_function = config["benchmark_function"]
        self.c1_strategy = config["c1_strategy"]
        self.c2_strategy = config["c2_strategy"]
        self.inertia_strategy = config["inertia_strategy"]

        # Inicializar estado
        self.iteration = 0
        self.particles: List[PSOParticle] = []
        self.best_solution: Solution = None

        # Historial de estadísticas para visualización
        self.history = {
            "best_fitness_per_generation": [],
            "avg_fitness_per_generation": [],
            "inertia_weight": [],
            "diversity": {"velocity": [], "position": [], "cognitive": []},
        }

    def run(self) -> Dict[str, Any]:
        """Ejecuta el algoritmo por el número máximo de iteraciones.
        
        Devuelve las estadísticas de la ejecución.

        Returns:
            Dict[str, Any]: Estadísticas de la ejecución, incluyendo la mejor 
                solución.
        """
        self.initialize_particles()

        # Crear barra de progreso si está habilitada
        progress_bar = None
        if self.show_progress:
            progress_bar = tqdm(total=self.generations, desc="PSO progreso")

        # Iterar para cada generación
        for i in range(self.generations):
            self.iteration = i
            self._update_generation()

            # Actualizar la barra de progreso
            if progress_bar:
                progress_bar.update(1)

        # Cerrar la barra de progreso si está habilitada
        if progress_bar:
            progress_bar.close()

        return self.get_stats()

    def initialize_particles(self) -> None:
        """Inicializa la población de partículas y configura el estado inicial.
        
        Optimizado para encontrar la mejor partícula durante la inicialización.
        """
        self.particles = []
        best_particle = None
        best_fitness = float('inf')

        # Crear y evaluar partículas iniciales
        for _ in range(self.population_size):
            particle = PSOParticle(
                dimensions=self.dimensions,
                bounds=self.bounds,
                velocity_bounds=self.velocity_bounds,
            )

            # Evaluar la partícula
            fitness = particle.evaluate(self.objective_function)
            self.particles.append(particle)

            # Actualizar mejor partícula si es necesario
            if fitness < best_fitness:
                best_fitness = fitness
                best_particle = particle

        # Configurar mejor solución global directamente
        if best_particle:
            self.best_solution = Solution(
                fitness=best_particle.fitness,
                position=np.copy(best_particle.position),
                velocity=np.copy(best_particle.velocity)
            )

    def _update_generation(self) -> None:
        """Actualiza la población para una iteración del algoritmo PSO."""
        # Calcular coeficientes para la iteración actual
        c1_value = self.c1_strategy(self.iteration, self.generations)
        c2_value = self.c2_strategy(self.iteration, self.generations)

        # Obtener el peso inercial para esta iteración (para toda la población 
        # o por partícula)
        w_values = self._compute_inertia_weights()

        # Actualizar cada partícula y evaluar su nueva posición
        self._update_particles(w_values, c1_value, c2_value)

    def _compute_inertia_weights(self) -> Union[float, np.ndarray]:
        """Calcula los pesos inerciales para la iteración actual.
        
        Returns:
            Union[float, np.ndarray]: Un único valor de peso inercial o un array 
                con valores para cada partícula.
        """
        # Preparar información del estado actual para la estrategia de inercia 
        # si la necesita
        particle_info = None
        if self.inertia_strategy.requires_particle_info:
            # Recolectar la información específica que esta estrategia necesita
            pso_state = {
                'particles': self.particles,
                'best_solution': self.best_solution,
                'iteration': self.iteration,
                'generations': self.generations,
                'dimensions': self.dimensions
            }
            particle_info = self.inertia_strategy.collect_required_info(pso_state)

        # Calcular los pesos inerciales
        w_values = self.inertia_strategy(self.iteration, self.generations, 
                                         particle_info)

        # Guardar el valor de inercia para estadísticas
        if (self.iteration % PSO_STATS_SAVE_INTERVAL == 0 or 
            self.iteration + 1 == self.generations):
            if self.inertia_strategy.returns_array:
                self.history["inertia_weight"].append(np.mean(w_values))
            else:
                self.history["inertia_weight"].append(w_values)

        return w_values

    def _update_particles(self, w_values: Union[float, np.ndarray], 
                         c1_value: float, c2_value: float) -> None:
        """Actualiza la posición, velocidad y fitness de cada partícula.

        Args:
            w_values (Union[float, np.ndarray]): Valor(es) de peso inercial para 
                la iteración actual.
            c1_value (float): Valor del coeficiente cognitivo para la iteración 
                actual.
            c2_value (float): Valor del coeficiente social para la iteración 
                actual.
        """

        # Actualizar cada partícula
        for i, particle in enumerate(self.particles):
            # Seleccionar el peso inercial para esta partícula
            w = w_values[i] if self.inertia_strategy.returns_array else w_values

            # Actualizar velocidad y posición
            particle.update(self.best_solution.position, w, c1_value, c2_value)

            # Evaluar la nueva posición
            fitness = particle.evaluate(self.objective_function)

            # Actualizar la mejor solución global si es necesario
            if fitness < self.best_solution.fitness:
                self.best_solution = Solution(
                    position=np.copy(particle.position),
                    fitness=fitness,
                    velocity=np.copy(particle.velocity)
                )

        # Actualizar estadísticas para esta iteración
        if (self.iteration % PSO_STATS_SAVE_INTERVAL == 0 or 
            self.iteration + 1 == self.generations):
            self._update_history()

    def _update_history(self) -> None:
        """Actualiza el historial de estadísticas del algoritmo."""
        # Extraer valores de fitness para cálculos
        fitness_values = np.array([p.fitness for p in self.particles])

        # Calcular y almacenar estadísticas básicas
        self.history["best_fitness_per_generation"].append(
            self.best_solution.fitness)
        self.history["avg_fitness_per_generation"].append(
            np.mean(fitness_values))

        # Calcular la partícula promedio (posición, velocidad y mejor posición 
        # personal)
        avg_position = np.mean([p.position for p in self.particles], axis=0)
        avg_velocity = np.mean([p.velocity for p in self.particles], axis=0)
        avg_best_position = np.mean([p.best_position for p in self.particles], 
                                    axis=0)

        # Calcular diversidad de la población usando la partícula promedio como 
        # referencia
        diversity_velocity = np.mean([
            np.linalg.norm(p.velocity - avg_velocity, ord=1) 
            for p in self.particles
        ])
        diversity_position = np.mean([
            np.linalg.norm(p.position - avg_position, ord=1) 
            for p in self.particles
        ])
        diversity_cognitive = np.mean([
            np.linalg.norm(p.best_position - avg_best_position, ord=1) 
            for p in self.particles
        ])

        # Almacenar diversidad en el historial
        self.history["diversity"]["velocity"].append(diversity_velocity)
        self.history["diversity"]["position"].append(diversity_position)
        self.history["diversity"]["cognitive"].append(diversity_cognitive)

    def get_stats(self) -> Dict[str, Any]:
        """Devuelve estadísticas del algoritmo PSO.

        Returns:
            Dict[str, Any]: Diccionario con estadísticas del algoritmo.
        """
        # Para visualizaciones
        self.history["generations"] = self.generations
        return {
            "best_solution": self.best_solution.to_dict(),
            "history": self.history,
        }
