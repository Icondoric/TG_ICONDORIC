"""
Education Scorer
Wrapper para get_education_score con logica adicional de evaluacion
"""

from typing import Dict, List

# Importar desde nuestros modulos de Fase 1
from app.scoring.education_levels import get_education_score, EDUCATION_LEVELS


def calculate_education_score(
    cv_education: List[Dict],
    required_education_level: str
) -> Dict:
    """
    Calcula score de educacion comparando nivel del CV con requerido

    Args:
        cv_education: Lista de educacion del CV (desde Gemini)
        required_education_level: Nivel minimo requerido

    Returns:
        Dict con score y detalles

    Examples:
        >>> calculate_education_score(
        ...     cv_education=[{
        ...         'degree': 'Ingenieria de Sistemas',
        ...         'institution': 'EMI',
        ...         'year': '2023'
        ...     }],
        ...     required_education_level='Licenciatura'
        ... )
        {
            'score': 1.0,
            'cv_level': 'Ingenieria de Sistemas',
            'cv_score': 0.75,
            'required_score': 0.75,
            'meets_requirement': True
        }
    """
    if not cv_education:
        return {
            'score': 0.0,
            'cv_level': 'Sin especificar',
            'cv_score': 0.0,
            'required_score': get_education_score(required_education_level),
            'meets_requirement': False,
            'highest_degree': None
        }

    # Obtener el nivel mas alto del CV
    highest_degree = max(
        cv_education,
        key=lambda x: get_education_score(x.get('degree', ''))
    )

    degree_name = highest_degree.get('degree', '')
    cv_score = get_education_score(degree_name)
    required_score = get_education_score(required_education_level)

    # Determinar si cumple requisito
    meets_requirement = cv_score >= required_score

    # Calcular score normalizado
    if meets_requirement:
        # Si cumple o supera, score = 1.0 (perfecto)
        final_score = 1.0
    else:
        # Si no cumple, score proporcional
        final_score = cv_score / required_score if required_score > 0 else 0.0

    return {
        'score': round(final_score, 3),
        'cv_level': degree_name,
        'cv_score': cv_score,
        'required_score': required_score,
        'meets_requirement': meets_requirement,
        'highest_degree': highest_degree
    }


def extract_education_from_gemini(gemini_output: Dict) -> List[Dict]:
    """
    Extrae educacion desde el output de Gemini

    Args:
        gemini_output: Dict con estructura de Gemini

    Returns:
        Lista de educacion
    """
    if not gemini_output or 'education' not in gemini_output:
        return []

    return gemini_output.get('education', [])
