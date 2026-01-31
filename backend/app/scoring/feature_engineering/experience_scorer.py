"""
Experience Scorer
Wrapper para calculate_experience_score con extraccion desde Gemini
"""

from typing import Dict, List

# Importar desde nuestros modulos de Fase 1
from app.scoring.experience_calculator import (
    calculate_experience_score,
    calculate_total_experience
)


def calculate_experience_score_from_cv(
    cv_experience: List[Dict],
    min_required_years: float
) -> Dict:
    """
    Calcula score de experiencia desde lista de experiencias del CV

    Args:
        cv_experience: Lista de experiencias (desde Gemini)
        min_required_years: Anios minimos requeridos

    Returns:
        Dict con score y detalles

    Examples:
        >>> calculate_experience_score_from_cv(
        ...     cv_experience=[
        ...         {'role': 'Developer', 'duration': '2 anios'},
        ...         {'role': 'Intern', 'duration': '6 meses'}
        ...     ],
        ...     min_required_years=1.0
        ... )
        {
            'score': 0.85,
            'total_years': 2.5,
            'meets_minimum': True,
            'delta': 1.5,
            'classification': 'Experiencia muy buena'
        }
    """
    # Calcular anios totales de experiencia
    total_years = calculate_total_experience(cv_experience)

    # Calcular score usando la funcion logaritmica
    result = calculate_experience_score(
        years=total_years,
        min_required=min_required_years,
        max_ideal=5.0
    )

    # Aniadir informacion adicional
    result['total_years'] = total_years
    result['experience_count'] = len(cv_experience)
    result['experiences'] = cv_experience

    return result


def extract_experience_from_gemini(gemini_output: Dict) -> List[Dict]:
    """
    Extrae experiencia desde el output de Gemini

    Args:
        gemini_output: Dict con estructura de Gemini

    Returns:
        Lista de experiencias
    """
    if not gemini_output or 'experience' not in gemini_output:
        return []

    return gemini_output.get('experience', [])
