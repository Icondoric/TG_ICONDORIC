"""
Configuraciones base para el módulo ML
Incluye escalas de evaluación y calculadoras
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

__all__ = [
    # Education
    'EDUCATION_LEVELS',
    'get_education_score',
    'get_education_level_name',
    
    # Languages
    'LANGUAGE_LEVELS',
    'get_language_score',
    'parse_language_entry',
    'calculate_languages_score',
    
    # Experience
    'calculate_experience_score',
    'parse_experience_duration',
    'calculate_total_experience'
]
