"""
Machine Learning Module
Fase 3: Dataset sintetico
Fase 4: Modelo Ridge
"""

from .data import (
    SyntheticDatasetGenerator,
    InstitutionalConfigLoader,
    get_random_profile_config
)

from .models import (
    InstitutionalMatchModel,
    ModelTrainer,
    MatchPredictor
)

__all__ = [
    # Fase 3 - Dataset
    "SyntheticDatasetGenerator",
    "InstitutionalConfigLoader",
    "get_random_profile_config",
    # Fase 4 - Modelo
    "InstitutionalMatchModel",
    "ModelTrainer",
    "MatchPredictor",
]
