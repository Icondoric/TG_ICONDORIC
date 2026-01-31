"""
Feature Extractor
Orquesta todos los scorers para generar el vector de features completo
"""

from typing import Dict, List

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

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
    y la configuracion institucional

    Este es el CORE del Feature Engineering. Combina los 5 scorers
    y genera el vector de features listo para el modelo ML.

    Args:
        gemini_output: Output de Gemini con estructura JSON del CV
        institutional_config: Configuracion de la institucion (pesos, requisitos)

    Returns:
        Dict con:
            - cv_scores: Scores individuales del CV [0-1]
            - institutional_params: Parametros de la institucion
            - feature_vector: Vector numerico completo para ML
            - metadata: Informacion adicional

    Example:
        >>> gemini_output = {
        ...     'hard_skills': ['Python', 'React', 'SQL'],
        ...     'soft_skills': ['Liderazgo', 'Trabajo en equipo'],
        ...     'education': [{'degree': 'Ingenieria', 'institution': 'EMI'}],
        ...     'experience': [{'role': 'Developer', 'duration': '2 anios'}],
        ...     'personal_info': {'languages': ['Espanol (Nativo)', 'Ingles (B2)']}
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
        ...         'required_languages': ['Ingles']
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

    # === PASO 5: EXTRAER PARAMETROS INSTITUCIONALES ===

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

    # Parametros institucionales (5)
    feature_vector.extend([
        institutional_params['weight_hard_skills'],    # 5
        institutional_params['weight_soft_skills'],    # 6
        institutional_params['weight_experience'],     # 7
        institutional_params['weight_education'],      # 8
        institutional_params['weight_languages']       # 9
    ])

    # Features de interaccion (productos cruzados) (5)
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

    result = {
        'cv_scores': cv_scores,
        'institutional_params': institutional_params,
        'feature_vector': feature_vector,
        'metadata': metadata
    }

    # Agregar numpy array si esta disponible
    if NUMPY_AVAILABLE:
        result['feature_vector_array'] = np.array(feature_vector).reshape(1, -1)

    return result


def get_feature_names() -> List[str]:
    """
    Retorna nombres descriptivos de cada feature en el vector
    Util para explicabilidad y debugging

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
    Valida que el output de Gemini tenga la estructura minima requerida

    Args:
        gemini_output: Output de Gemini

    Returns:
        True si es valido, False si no
    """
    required_keys = ['hard_skills', 'soft_skills', 'education', 'experience']

    for key in required_keys:
        if key not in gemini_output:
            return False

    return True


def calculate_final_score(feature_result: Dict) -> float:
    """
    Calcula el score final ponderado del candidato

    Args:
        feature_result: Resultado de extract_features()

    Returns:
        Score final entre 0 y 1
    """
    cv_scores = feature_result['cv_scores']
    weights = feature_result['institutional_params']

    final_score = (
        cv_scores['hard_skills_score'] * weights['weight_hard_skills'] +
        cv_scores['soft_skills_score'] * weights['weight_soft_skills'] +
        cv_scores['experience_score'] * weights['weight_experience'] +
        cv_scores['education_score'] * weights['weight_education'] +
        cv_scores['languages_score'] * weights['weight_languages']
    )

    return round(final_score, 3)


def classify_candidate(final_score: float, thresholds: Dict) -> str:
    """
    Clasifica al candidato segun los umbrales institucionales

    Args:
        final_score: Score final del candidato
        thresholds: Dict con 'apto' y 'considerado'

    Returns:
        Clasificacion: 'APTO', 'CONSIDERADO' o 'NO_APTO'
    """
    apto_threshold = thresholds.get('apto', 0.70)
    considerado_threshold = thresholds.get('considerado', 0.50)

    if final_score >= apto_threshold:
        return 'APTO'
    elif final_score >= considerado_threshold:
        return 'CONSIDERADO'
    else:
        return 'NO_APTO'
