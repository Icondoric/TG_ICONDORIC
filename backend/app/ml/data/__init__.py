"""
Data Generation Module
Generador de dataset sintetico y loader de configuraciones
"""

from .synthetic_generator import SyntheticDatasetGenerator
from .institutional_configs import InstitutionalConfigLoader, get_random_profile_config

__all__ = [
    "SyntheticDatasetGenerator",
    "InstitutionalConfigLoader",
    "get_random_profile_config",
]
