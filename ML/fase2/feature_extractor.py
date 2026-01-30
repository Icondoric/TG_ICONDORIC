"""
Feature Extractor
Orquesta todos los scorers para generar el vector de features completo
"""

from typing import Dict, List
import numpy as np

from .hard_skills_scorer import (
    calculate_hard_skills_score,
    extract_hard_skills_from_gemini
)
from .soft_skills_scorer import (
    calculate_soft_skills_score,
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


def extract_features(
    gemini_output: Dict,
    institutional_config: Dict
) -> Dict:
    """
    Extrae features completos desde el CV procesado por Gemini
    y la configuración institucional
    
    Este es el CORE del Feature Engineering. Combina los 5 scorers
    y genera el vector de features listo para el modelo ML.
    
    Args:
        gemini_output: Output de Gemini con estructura JSON del CV
        institutional_config: Configuración de la institución (pesos, requisitos)
    
    Returns:
        Dict con:
            - cv_scores: Scores individuales del CV [0-1]
            - institutional_params: Parámetros de la institución
            - feature_vector: Vector numérico completo para ML
            - metadata: Información adicional
    
    Example:
        >>> gemini_output = {
        ...     'hard_skills': ['Python', 'React', 'SQL'],
        ...     'soft_skills': ['Liderazgo', 'Trabajo en equipo'],
        ...     'education': [{'degree': 'Ingeniería', 'institution': 'EMI'}],
        ...     'experience': [{'role': 'Developer', 'duration': '2 años'}],
        ...     'personal_info': {'languages': ['Español (Nativo)', 'Inglés (B2)']}
        ... }
        >>> institutional_config = {
        ...     'weights': {
        ...         'hard_skills': 0.35,
        ...         'soft_skills': 0.15,
        ...         'experience': 0.25,
        ...         'education': 0.15,
        ...         'languages': 0.10
        ...     },
        ...     'requirements': {
        ...         'min_experience_years': 1.0,
        ...         'required_skills': ['Python', 'SQL'],
        ...         'preferred_skills': ['Docker'],
        ...         'required_education_level': 'Licenciatura',
        ...         'required_languages': ['Inglés']
        ...     }
        ... }
        >>> features = extract_features(gemini_output, institutional_config)
        >>> features['cv_scores']['hard_skills_score']
        0.75
    """
    
    # === PASO 1: EXTRAER DATOS DEL CV ===
    
    cv_hard_skills = extract_hard_skills_from_gemini(gemini_output)
    cv_soft_skills = extract_soft_skills_from_gemini(gemini_output)
    cv_education = extract_education_from_gemini(gemini_output)
    cv_experience = extract_experience_from_gemini(gemini_output)
    cv_languages = extract_languages_from_gemini(gemini_output)
    
    # === PASO 2: EXTRAER REQUISITOS INSTITUCIONALES ===
    
    requirements = institutional_config.get('requirements', {})
    weights = institutional_config.get('weights', {})
    
    required_skills = requirements.get('required_skills', [])
    preferred_skills = requirements.get('preferred_skills', [])
    required_soft_skills = requirements.get('required_soft_skills', [])
    min_experience_years = requirements.get('min_experience_years', 0.0)
    required_education_level = requirements.get('required_education_level', 'Licenciatura')
    required_languages = requirements.get('required_languages', [])
    
    # === PASO 3: CALCULAR SCORES INDIVIDUALES ===
    
    hard_skills_result = calculate_hard_skills_score(
        cv_skills=cv_hard_skills,
        required_skills=required_skills,
        preferred_skills=preferred_skills
    )
    
    soft_skills_result = calculate_soft_skills_score(
        cv_soft_skills=cv_soft_skills,
        required_soft_skills=required_soft_skills
    )
    
    education_result = calculate_education_score(
        cv_education=cv_education,
        required_education_level=required_education_level
    )
    
    experience_result = calculate_experience_score_from_cv(
        cv_experience=cv_experience,
        min_required_years=min_experience_years
    )
    
    languages_result = calculate_languages_score_from_cv(
        cv_languages=cv_languages,
        required_languages=required_languages
    )
    
    # === PASO 4: EXTRAER SCORES BASE [0-1] ===
    
    cv_scores = {
        'hard_skills_score': hard_skills_result['score'],
        'soft_skills_score': soft_skills_result['score'],
        'experience_score': experience_result['score'],
        'education_score': education_result['score'],
        'languages_score': languages_result['score']
    }
    
    # === PASO 5: EXTRAER PARÁMETROS INSTITUCIONALES ===
    
    institutional_params = {
        'weight_hard_skills': weights.get('hard_skills', 0.3),
        'weight_soft_skills': weights.get('soft_skills', 0.2),
        'weight_experience': weights.get('experience', 0.25),
        'weight_education': weights.get('education', 0.15),
        'weight_languages': weights.get('languages', 0.10)
    }
    
    # Validar que sumen 1.0 (tolerancia de 0.01)
    total_weight = sum(institutional_params.values())
    if abs(total_weight - 1.0) > 0.01:
        raise ValueError(f"Los pesos institucionales deben sumar 1.0 (actual: {total_weight})")
    
    # === PASO 6: CONSTRUIR FEATURE VECTOR ===
    
    # Features base (5)
    feature_vector = [
        cv_scores['hard_skills_score'],      # 0
        cv_scores['soft_skills_score'],      # 1
        cv_scores['experience_score'],       # 2
        cv_scores['education_score'],        # 3
        cv_scores['languages_score'],        # 4
    ]
    
    # Parámetros institucionales (5)
    feature_vector.extend([
        institutional_params['weight_hard_skills'],    # 5
        institutional_params['weight_soft_skills'],    # 6
        institutional_params['weight_experience'],     # 7
        institutional_params['weight_education'],      # 8
        institutional_params['weight_languages']       # 9
    ])
    
    # Features de interacción (productos cruzados) (5)
    feature_vector.extend([
        cv_scores['hard_skills_score'] * institutional_params['weight_hard_skills'],  # 10
        cv_scores['soft_skills_score'] * institutional_params['weight_soft_skills'],  # 11
        cv_scores['experience_score'] * institutional_params['weight_experience'],    # 12
        cv_scores['education_score'] * institutional_params['weight_education'],      # 13
        cv_scores['languages_score'] * institutional_params['weight_languages']       # 14
    ])
    
    # Context features (3)
    feature_vector.extend([
        experience_result.get('total_years', 0.0),                    # 15
        min_experience_years,                                          # 16
        experience_result.get('total_years', 0.0) - min_experience_years  # 17 (delta)
    ])
    
    # === PASO 7: CONSTRUIR METADATA ===
    
    metadata = {
        'hard_skills_details': hard_skills_result,
        'soft_skills_details': soft_skills_result,
        'education_details': education_result,
        'experience_details': experience_result,
        'languages_details': languages_result,
        'total_features': len(feature_vector),
        'feature_names': get_feature_names()
    }
    
    return {
        'cv_scores': cv_scores,
        'institutional_params': institutional_params,
        'feature_vector': feature_vector,
        'feature_vector_array': np.array(feature_vector).reshape(1, -1),  # Para sklearn
        'metadata': metadata
    }


def get_feature_names() -> List[str]:
    """
    Retorna nombres descriptivos de cada feature en el vector
    Útil para explicabilidad y debugging
    
    Returns:
        Lista de nombres de features
    """
    return [
        # CV Scores base (5)
        'hard_skills_score',
        'soft_skills_score',
        'experience_score',
        'education_score',
        'languages_score',
        
        # Institutional weights (5)
        'inst_weight_hard',
        'inst_weight_soft',
        'inst_weight_exp',
        'inst_weight_edu',
        'inst_weight_lang',
        
        # Interaction features (5)
        'interaction_hard',
        'interaction_soft',
        'interaction_exp',
        'interaction_edu',
        'interaction_lang',
        
        # Context features (3)
        'total_experience_years',
        'min_required_years',
        'experience_delta'
    ]


def validate_gemini_output(gemini_output: Dict) -> bool:
    """
    Valida que el output de Gemini tenga la estructura mínima requerida
    
    Args:
        gemini_output: Output de Gemini
    
    Returns:
        True si es válido, False si no
    """
    required_keys = ['hard_skills', 'soft_skills', 'education', 'experience']
    
    for key in required_keys:
        if key not in gemini_output:
            return False
    
    return True
