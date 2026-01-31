"""
Modulo de scoring para evaluacion de perfiles
Fase 1: Definiciones base (educacion, idiomas, experiencia)
Fase 2: Feature Engineering (scorers y extractor)
"""

from .education_levels import (
    EDUCATION_LEVELS,
    get_education_score,
    get_education_level_name
)

from .language_levels import (
    LANGUAGE_LEVELS,
    get_language_score,
    parse_language_entry,
    calculate_languages_score
)

from .experience_calculator import (
    calculate_experience_score,
    parse_experience_duration,
    calculate_total_experience
)

# Fase 2: Feature Engineering
from .feature_engineering import (
    # Feature Extractor
    extract_features,
    get_feature_names,
    validate_gemini_output,
    # Hard Skills
    calculate_hard_skills_score,
    # Soft Skills
    calculate_soft_skills_score,
)

__all__ = [
    # Education (Fase 1)
    "EDUCATION_LEVELS",
    "get_education_score",
    "get_education_level_name",
    # Languages (Fase 1)
    "LANGUAGE_LEVELS",
    "get_language_score",
    "parse_language_entry",
    "calculate_languages_score",
    # Experience (Fase 1)
    "calculate_experience_score",
    "parse_experience_duration",
    "calculate_total_experience",
    # Feature Engineering (Fase 2)
    "extract_features",
    "get_feature_names",
    "validate_gemini_output",
    "calculate_hard_skills_score",
    "calculate_soft_skills_score",
]
