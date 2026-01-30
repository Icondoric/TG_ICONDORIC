"""
Education Scorer
Wrapper para get_education_score con lógica adicional de evaluación
"""

from typing import Dict, List
from app.ml.config.education_levels import get_education_score, EDUCATION_LEVELS


def calculate_education_score(
    cv_education: List[Dict],
    required_education_level: str
) -> Dict:
    """
    Calcula score de educación comparando nivel del CV con requerido
    
    Args:
        cv_education: Lista de educación del CV (desde Gemini)
        required_education_level: Nivel mínimo requerido
    
    Returns:
        Dict con score y detalles
    
    Examples:
        >>> calculate_education_score(
        ...     cv_education=[{
        ...         'degree': 'Ingeniería de Sistemas',
        ...         'institution': 'EMI',
        ...         'year': '2023'
        ...     }],
        ...     required_education_level='Licenciatura'
        ... )
        {
            'score': 1.0,
            'cv_level': 'Ingeniería',
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
            'meets_requirement': False
        }
    
    # Obtener el nivel más alto del CV
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
    Extrae educación desde el output de Gemini
    
    Args:
        gemini_output: Dict con estructura de Gemini
    
    Returns:
        Lista de educación
    """
    if not gemini_output or 'education' not in gemini_output:
        return []
    
    return gemini_output.get('education', [])
