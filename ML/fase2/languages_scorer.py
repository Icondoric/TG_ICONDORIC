"""
Languages Scorer
Wrapper para calculate_languages_score con extracción desde Gemini
"""

from typing import Dict, List
from app.ml.config.language_levels import calculate_languages_score


def calculate_languages_score_from_cv(
    cv_languages: List[str],
    required_languages: List[str]
) -> Dict:
    """
    Calcula score de idiomas comparando CV con requisitos
    
    Args:
        cv_languages: Lista de idiomas del CV (ej: ["Español (Nativo)", "Inglés (B2)"])
        required_languages: Lista de idiomas requeridos (ej: ["Inglés"])
    
    Returns:
        Dict con score y detalles
    
    Examples:
        >>> calculate_languages_score_from_cv(
        ...     cv_languages=["Español (Nativo)", "Inglés (B2)"],
        ...     required_languages=["Inglés"]
        ... )
        {
            'score': 0.75,
            'matched': ['Inglés'],
            'missing': [],
            'details': [...]
        }
    """
    # Usar la función del módulo config
    result = calculate_languages_score(cv_languages, required_languages)
    
    # Añadir información adicional
    result['total_cv_languages'] = len(cv_languages)
    result['total_required_languages'] = len(required_languages)
    
    return result


def extract_languages_from_gemini(gemini_output: Dict) -> List[str]:
    """
    Extrae idiomas desde el output de Gemini
    
    Args:
        gemini_output: Dict con estructura de Gemini
    
    Returns:
        Lista de idiomas
    """
    if not gemini_output:
        return []
    
    # Intenta extraer de personal_info.languages o directamente de languages
    if 'personal_info' in gemini_output and 'languages' in gemini_output['personal_info']:
        return gemini_output['personal_info']['languages']
    
    if 'languages' in gemini_output:
        return gemini_output['languages']
    
    return []
