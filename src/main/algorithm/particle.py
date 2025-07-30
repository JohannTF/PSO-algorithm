"""Implementación de partícula para el algoritmo PSO (Particle Swarm Optimization)."""

from typing import Any, Callable, Dict, Tuple

import numpy as np


class PSOParticle:
    """Partícula para el algoritmo PSO (Particle Swarm Optimization).
    
    Almacena posición, velocidad, fitness y mejor posición histórica.
    """

    def __init__(
        self,
        dimensions: int,
        bounds: Tuple[float, float],
        velocity_bounds: Tuple[float, float],
    ) -> None:
        """Inicializa una partícula PSO.

        Args:
            dimensions (int): Número de dimensiones del espacio de búsqueda.
            bounds (Tuple[float, float]): Tupla (min, max) con los límites del 
                espacio de búsqueda.
            velocity_bounds (Tuple[float, float]): Tupla (min, max) con los 
                límites de velocidad.
        """
        self.dimensions = dimensions
        self.bounds = bounds
        self.velocity_bounds = velocity_bounds

        lower_bound, upper_bound = bounds
        lower_vel, upper_vel = velocity_bounds

        # Inicializar posición aleatoria dentro de los límites
        self.position = np.random.uniform(
            low=lower_bound, high=upper_bound, size=dimensions
        )

        # Inicializar velocidad aleatoria
        self.velocity = np.random.uniform(
            low=lower_vel, high=upper_vel, size=dimensions
        )

        # Inicializar valores de fitness
        self.fitness = float("inf")
        self.best_position = np.copy(self.position)
        self.best_fitness = float("inf")

    def update(
        self, global_best_position: np.ndarray, w: float, c1: float, c2: float
    ) -> None:
        """Actualiza la velocidad y posición de la partícula según el algoritmo PSO.

        Args:
            global_best_position (np.ndarray): Mejor posición global encontrada 
                por el enjambre.
            w (float): Factor de inercia.
            c1 (float): Coeficiente cognitivo (peso de la experiencia personal).
            c2 (float): Coeficiente social (peso de la experiencia del enjambre).
        """
        # Componentes aleatorios (un único valor para cada uno)
        r1 = np.random.random()
        r2 = np.random.random()

        # Actualizar velocidad
        inertia = w * self.velocity
        cognitive_component = c1 * r1 * (self.best_position - self.position)
        social_component = c2 * r2 * (global_best_position - self.position)

        self.velocity = inertia + cognitive_component + social_component

        # Limitar velocidad si es necesario
        lower_vel, upper_vel = self.velocity_bounds
        self.velocity = np.clip(self.velocity, lower_vel, upper_vel)

        # Actualizar posición
        self.position = self.position + self.velocity

        # Aplicar mecanismo de rebote en los límites
        self._apply_bounce_mechanism()

    def _apply_bounce_mechanism(self) -> None:
        """Aplica el mecanismo de rebote para mantener la partícula dentro de los límites.
        
        Si la partícula sobrepasa un límite, rebota invirtiendo la dirección de 
        la velocidad.
        """
        lower_bound, upper_bound = self.bounds

        for i in range(self.dimensions):
            # Comprobar límite inferior
            if self.position[i] < lower_bound:
                # Rebote: invertir la velocidad y colocar en el límite
                self.position[i] = lower_bound + (lower_bound - self.position[i])
                self.velocity[i] = -self.velocity[i] * 0.8  # Amortiguación en el rebote

            # Comprobar límite superior
            elif self.position[i] > upper_bound:
                # Rebote: invertir la velocidad y colocar en el límite
                self.position[i] = upper_bound - (self.position[i] - upper_bound)
                self.velocity[i] = -self.velocity[i] * 0.8  # Amortiguación en el rebote

        # Verificar que la posición siga dentro de los límites después del rebote
        # (por si acaso el rebote pone la partícula fuera de los límites otra vez)
        self.position = np.clip(self.position, lower_bound, upper_bound)

    def evaluate(self, objective_function: Callable[[np.ndarray], float]) -> float:
        """Evalúa la partícula con la función objetivo.
        
        Actualiza la mejor posición y aptitud histórica para esta partícula si 
        es necesario.

        Args:
            objective_function (Callable[[np.ndarray], float]): Función que evalúa 
                la posición actual.

        Returns:
            float: Valor de aptitud calculado.
        """
        self.fitness = objective_function(self.position)

        # Actualizar mejor posición histórica si la actual es mejor
        if self.fitness < self.best_fitness:
            self.best_fitness = self.fitness
            self.best_position = np.copy(self.position)

        return self.fitness

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la partícula a un diccionario.
        
        Facilita el registro y visualización.

        Returns:
            Dict[str, Any]: Representación en diccionario de la partícula.
        """
        return {
            "position": self.position.tolist(),
            "fitness": self.fitness,
            "velocity": self.velocity.tolist(),
            "best_position": self.best_position.tolist(),
            "best_fitness": self.best_fitness,
        }

    def __str__(self) -> str:
        """Representación en cadena de la partícula.

        Returns:
            str: Cadena que describe la partícula.
        """
        return (
            f"PSOParticle(fitness={self.fitness:.6f}, "
            f"best_fitness={self.best_fitness:.6f})"
        )
