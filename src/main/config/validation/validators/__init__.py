"""Validadores específicos con auto-registro mediante decoradores."""

# Importar validadores para activar el auto-registro
from src.main.config.validation.validators.basic_parameters import (
    BasicParametersValidador
)
from src.main.config.validation.validators.coefficient import (
    CoefficientValidador
)
from src.main.config.validation.validators.inertia import InertiaValidador
from src.main.config.validation.validators.output_results import (
    OutputResultsValidador
)
from src.main.config.validation.validators.visualizations import (
    VisualizationValidador
)

__all__ = [
    'BasicParametersValidador',
    'InertiaValidador',
    'CoefficientValidador',
    'VisualizationValidador',
    'OutputResultsValidador'
]
