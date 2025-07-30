"""Módulo con las implementaciones de estrategias de peso inercial."""

# Estrategias básicas
from src.main.algorithm.inertia.strategies.basic.constant import Constant
from src.main.algorithm.inertia.strategies.basic.linear_decreasing import (
    LinearDecreasing
)
from src.main.algorithm.inertia.strategies.basic.random import Random

# Estrategias cóncavas
from src.main.algorithm.inertia.strategies.concave.decreasing import (
    ConcaveDecreasing
)
from src.main.algorithm.inertia.strategies.concave.exp_decreasing import (
    ConcaveExponentialDecreasing
)
from src.main.algorithm.inertia.strategies.concave.exp_increasing import (
    ConcaveExponentialIncreasing
)

# Estrategias convexas
from src.main.algorithm.inertia.strategies.convex.decreasing import (
    ConvexDecreasing
)
from src.main.algorithm.inertia.strategies.convex.exp_decreasing import (
    ConvexExponentialDecreasing
)
from src.main.algorithm.inertia.strategies.convex.exp_increasing import (
    ConvexExponentialIncreasing
)

# Estrategias avanzadas
from src.main.algorithm.inertia.strategies.advanced.pso_niew import PSONIEW
from src.main.algorithm.inertia.strategies.advanced.pso_siw import PSOSIW
from src.main.algorithm.inertia.strategies.advanced.de_pso import DEPSO
from src.main.algorithm.inertia.strategies.advanced.gpso import GPSO
from src.main.algorithm.inertia.strategies.advanced.pso_tvac import PSOTVAC
from src.main.algorithm.inertia.strategies.advanced.hybrid_cosine import (
    HybridCosine
)

# Estrategias adaptativas
from src.main.algorithm.inertia.strategies.adaptive.dsi_pso import DSIPSO

__all__ = [
    # Básicas
    "Constant",
    "LinearDecreasing",
    "Random",
    # Cóncavas
    "ConcaveDecreasing",
    "ConcaveExponentialDecreasing",
    "ConcaveExponentialIncreasing",
    # Convexas
    "ConvexDecreasing",
    "ConvexExponentialDecreasing",
    "ConvexExponentialIncreasing",
    # Avanzadas
    "DEPSO",
    "GPSO",
    "HybridCosine",
    "PSONIEW",
    "PSOSIW",
    "PSOTVAC",
    # Adaptativas
    "DSIPSO"
]
