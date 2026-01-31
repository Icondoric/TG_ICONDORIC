"""
Feature Engineering Module
Orquesta todos los scorers para generar el vector de features completo
"""

from .hard_skills_scorer import (
    calculate_hard_skills_score,
    calculate_jaccard_similarity,
    calculate_tfidf_similarity,
    normalize_skill,
    extract_hard_skills_from_gemini
)

from .soft_skills_scorer import (
    calculate_soft_skills_score,
    normalize_soft_skill,
    get_soft_skill_category,
    extract_soft_skills_from_gemini
)

from .education_scorer import (
    calculate_education_score,
    extract_education_from_gemini
)

from .experience_scorer import (
    calculate_experience_score_from_cv,
    extract_experience_from_gemini
)

from .languages_scorer import (
    calculate_languages_score_from_cv,
    extract_languages_from_gemini
)

from .feature_extractor import (
    extract_features,
    get_feature_names,
    validate_gemini_output
)

__all__ = [
    # Hard Skills
    "calculate_hard_skills_score",
    "calculate_jaccard_similarity",
    "calculate_tfidf_similarity",
    "normalize_skill",
    "extract_hard_skills_from_gemini",
    # Soft Skills
    "calculate_soft_skills_score",
    "normalize_soft_skill",
    "get_soft_skill_category",
    "extract_soft_skills_from_gemini",
    # Education
    "calculate_education_score",
    "extract_education_from_gemini",
    # Experience
    "calculate_experience_score_from_cv",
    "extract_experience_from_gemini",
    # Languages
    "calculate_languages_score_from_cv",
    "extract_languages_from_gemini",
    # Feature Extractor
    "extract_features",
    "get_feature_names",
    "validate_gemini_output",
]
