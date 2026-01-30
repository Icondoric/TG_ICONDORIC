"""
Calculadora de score de experiencia laboral
Utiliza función logarítmica para reflejar rendimientos decrecientes
"""

import math
from typing import Dict


def calculate_experience_score(
    years: float, 
    min_required: float, 
    max_ideal: float = 5.0
) -> Dict[str, float]:
    """
    Calcula score de experiencia con curva logarítmica adaptativa
    
    La función refleja el principio económico de rendimientos decrecientes:
    - Los primeros años de experiencia aportan mayor valor marginal
    - Después de cierto punto (max_ideal), la experiencia adicional no suma
    - Se penaliza proporcionalmente si no se cumple el mínimo requerido
    
    Args:
        years: Años de experiencia del candidato (puede incluir decimales)
        min_required: Mínimo de años requerido por la institución
        max_ideal: Años donde se alcanza el score máximo (default: 5.0)
    
    Returns:
        Dict con:
            - score: Valor entre 0 y 1
            - meets_minimum: Boolean indicando si cumple mínimo
            - delta: Diferencia entre años del candidato y mínimo requerido
            - classification: Texto descriptivo
    
    Examples:
        >>> calculate_experience_score(2.0, min_required=1.0)
        {
            'score': 0.731,
            'meets_minimum': True,
            'delta': 1.0,
            'classification': 'Por encima del mínimo'
        }
        
        >>> calculate_experience_score(1.0, min_required=3.0)
        {
            'score': 0.167,
            'meets_minimum': False,
            'delta': -2.0,
            'classification': 'No cumple mínimo requerido'
        }
        
        >>> calculate_experience_score(10.0, min_required=1.0, max_ideal=5.0)
        {
            'score': 1.0,
            'meets_minimum': True,
            'delta': 9.0,
            'classification': 'Experiencia máxima'
        }
    """
    # Validación de entrada
    if min_required < 0:
        raise ValueError("min_required debe ser >= 0")
    if max_ideal <= min_required:
        raise ValueError("max_ideal debe ser mayor que min_required")
    
    # Caso 1: Sin experiencia o experiencia negativa (inválido)
    if years <= 0:
        return {
            'score': 0.0,
            'meets_minimum': False,
            'delta': round(-min_required, 2),
            'classification': 'Sin experiencia',
            'years': 0.0,
            'min_required': min_required
        }
    
    # Caso 2: No cumple mínimo requerido (penalización lineal)
    if years < min_required:
        # Score proporcional: (años actuales / mínimo requerido) * 0.5
        # Máximo alcanzable: 0.5 (porque no cumple el mínimo)
        score = (years / min_required) * 0.5
        
        return {
            'score': round(score, 3),
            'meets_minimum': False,
            'delta': round(years - min_required, 2),
            'classification': 'No cumple mínimo requerido',
            'years': years,
            'min_required': min_required
        }
    
    # Caso 3: Cumple o supera el máximo ideal
    if years >= max_ideal:
        return {
            'score': 1.0,
            'meets_minimum': True,
            'delta': round(years - min_required, 2),
            'classification': 'Experiencia máxima',
            'years': years,
            'min_required': min_required
        }
    
    # Caso 4: Entre mínimo y máximo ideal (curva logarítmica)
    # Fórmula: score = 0.5 + 0.5 * normalized
    # Donde normalized = (log(years+1) - log(min+1)) / (log(max+1) - log(min+1))
    
    log_years = math.log(years + 1)
    log_min = math.log(min_required + 1)
    log_max = math.log(max_ideal + 1)
    
    # Normalización logarítmica al rango [0, 1]
    normalized = (log_years - log_min) / (log_max - log_min)
    
    # Desplazar de [0, 1] a [0.5, 1.0]
    # Esto garantiza que cumplir exactamente el mínimo da 0.5
    score = 0.5 + 0.5 * normalized
    
    # Clasificación descriptiva
    if score >= 0.9:
        classification = 'Experiencia excelente'
    elif score >= 0.75:
        classification = 'Experiencia muy buena'
    elif score >= 0.60:
        classification = 'Experiencia buena'
    else:
        classification = 'Por encima del mínimo'
    
    return {
        'score': round(min(1.0, score), 3),
        'meets_minimum': True,
        'delta': round(years - min_required, 2),
        'classification': classification,
        'years': years,
        'min_required': min_required
    }


def parse_experience_duration(duration_str: str) -> float:
    """
    Parsea una duración textual a años decimales
    
    Args:
        duration_str: String como "2 años", "1.5 años", "6 meses", "2021-2023"
    
    Returns:
        Años en formato decimal
    
    Examples:
        >>> parse_experience_duration("2 años")
        2.0
        >>> parse_experience_duration("6 meses")
        0.5
        >>> parse_experience_duration("2021 - 2023")
        2.0
    """
    import re
    
    if not duration_str:
        return 0.0
    
    duration_str = duration_str.lower().strip()
    
    # Caso 1: Formato "X años"
    match_years = re.search(r'(\d+\.?\d*)\s*a[ñn]os?', duration_str)
    if match_years:
        return float(match_years.group(1))
    
    # Caso 2: Formato "X meses"
    match_months = re.search(r'(\d+)\s*mes(?:es)?', duration_str)
    if match_months:
        return round(float(match_months.group(1)) / 12, 2)
    
    # Caso 3: Formato "YYYY - YYYY" o "YYYY-YYYY"
    match_range = re.search(r'(\d{4})\s*-\s*(\d{4}|presente|actual)', duration_str)
    if match_range:
        start_year = int(match_range.group(1))
        end_year_str = match_range.group(2)
        
        if end_year_str in ['presente', 'actual']:
            from datetime import datetime
            end_year = datetime.now().year
        else:
            end_year = int(end_year_str)
        
        return float(end_year - start_year)
    
    # Caso 4: Número decimal directo
    match_number = re.search(r'(\d+\.?\d*)', duration_str)
    if match_number:
        return float(match_number.group(1))
    
    # Default: 0
    return 0.0


def calculate_total_experience(experience_list: list) -> float:
    """
    Calcula años totales de experiencia desde una lista de experiencias
    
    Args:
        experience_list: Lista de dicts con campo 'duration'
    
    Returns:
        Total de años de experiencia
    
    Examples:
        >>> experiences = [
        ...     {'duration': '2 años'},
        ...     {'duration': '6 meses'}
        ... ]
        >>> calculate_total_experience(experiences)
        2.5
    """
    total_years = 0.0
    
    for exp in experience_list:
        if isinstance(exp, dict) and 'duration' in exp:
            years = parse_experience_duration(exp['duration'])
            total_years += years
        elif isinstance(exp, str):
            years = parse_experience_duration(exp)
            total_years += years
    
    return round(total_years, 2)
