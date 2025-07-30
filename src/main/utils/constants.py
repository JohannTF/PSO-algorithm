"""Constantes para configuración y visualización del algoritmo PSO."""

# Gráficos para ejecuciones individuales
SINGLE_RUN_GRAPHS = {
    "best_fitness": "Convergencia de la mejor aptitud",
    "inertia_weight": "Evolución del peso inercial",
    "particles_2d": "Distribución de partículas (solo 2D)",
    "surface_3d": "Superficie de la función (solo 2D)",
    "diversity": "Diversidad en posición, velocidad, aptitud y componente cognitiva"
}

# Gráficos para múltiples ejecuciones
MULTI_RUN_GRAPHS = {
    "best_run_fitness": "Mejor aptitud en la mejor ejecución",
    "best_run_inertia": "Peso inercial",
    "best_fitness_per_run": "Mejores fitness por ejecución",
    "avg_fitness_per_run": "Historial de fitness promedio por ejecución",
    "diversity": "Diversidad en posición, velocidad, aptitud y componente cognitiva"
}

# Campos excluidos al guardar resultados (muy grandes o redundantes)
EXCLUDED_FIELDS = {
    "all_avg_fitness_history",
}

# Claves no serializables directamente a JSON
NON_SERIALIZABLE_KEYS = {
    "c1_strategy",
    "c2_strategy",
    "inertia_strategy",
    "benchmark_function"
}

# Intervalo para guardar estadísticas PSO (en generaciones)
PSO_STATS_SAVE_INTERVAL = 5

# Umbral para escala logarítmica en gráficos
LOG_SCALE_THRESHOLD = 10