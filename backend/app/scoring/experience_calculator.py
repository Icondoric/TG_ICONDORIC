"""
Calculadora de score de experiencia laboral
Utiliza funcion logaritmica para reflejar rendimientos decrecientes
"""

import math
import re
from typing import Dict
from datetime import datetime


def calculate_experience_score(
    years: float,
    min_required: float,
    max_ideal: float = 5.0
) -> Dict[str, float]:
    """
    Calcula score de experiencia con curva logaritmica adaptativa

    La funcion refleja el principio economico de rendimientos decrecientes:
    - Los primeros anios de experiencia aportan mayor valor marginal
    - Despues de cierto punto (max_ideal), la experiencia adicional no suma
    - Se penaliza proporcionalmente si no se cumple el minimo requerido

    Args:
        years: Anios de experiencia del candidato (puede incluir decimales)
        min_required: Minimo de anios requerido por la institucion
        max_ideal: Anios donde se alcanza el score maximo (default: 5.0)

    Returns:
        Dict con:
            - score: Valor entre 0 y 1
            - meets_minimum: Boolean indicando si cumple minimo
            - delta: Diferencia entre anios del candidato y minimo requerido
            - classification: Texto descriptivo

    Examples:
        >>> calculate_experience_score(2.0, min_required=1.0)
        {
            'score': 0.731,
            'meets_minimum': True,
            'delta': 1.0,
            'classification': 'Por encima del minimo'
        }
    """
    # Validacion de entrada
    if min_required < 0:
        raise ValueError("min_required debe ser >= 0")
    if max_ideal <= min_required:
        raise ValueError("max_ideal debe ser mayor que min_required")

    # Caso 1: Sin experiencia o experiencia negativa (invalido)
    if years <= 0:
        return {
            'score': 0.0,
            'meets_minimum': False,
            'delta': round(-min_required, 2),
            'classification': 'Sin experiencia',
            'years': 0.0,
            'min_required': min_required
        }

    # Caso 2: No cumple minimo requerido (penalizacion lineal)
    if years < min_required:
        # Score proporcional: (anios actuales / minimo requerido) * 0.5
        # Maximo alcanzable: 0.5 (porque no cumple el minimo)
        score = (years / min_required) * 0.5

        return {
            'score': round(score, 3),
            'meets_minimum': False,
            'delta': round(years - min_required, 2),
            'classification': 'No cumple minimo requerido',
            'years': years,
            'min_required': min_required
        }

    # Caso 3: Cumple o supera el maximo ideal
    if years >= max_ideal:
        return {
            'score': 1.0,
            'meets_minimum': True,
            'delta': round(years - min_required, 2),
            'classification': 'Experiencia maxima',
            'years': years,
            'min_required': min_required
        }

    # Caso 4: Entre minimo y maximo ideal (curva logaritmica)
    # Formula: score = 0.5 + 0.5 * normalized
    # Donde normalized = (log(years+1) - log(min+1)) / (log(max+1) - log(min+1))

    log_years = math.log(years + 1)
    log_min = math.log(min_required + 1)
    log_max = math.log(max_ideal + 1)

    # Normalizacion logaritmica al rango [0, 1]
    normalized = (log_years - log_min) / (log_max - log_min)

    # Desplazar de [0, 1] a [0.5, 1.0]
    # Esto garantiza que cumplir exactamente el minimo da 0.5
    score = 0.5 + 0.5 * normalized

    # Clasificacion descriptiva
    if score >= 0.9:
        classification = 'Experiencia excelente'
    elif score >= 0.75:
        classification = 'Experiencia muy buena'
    elif score >= 0.60:
        classification = 'Experiencia buena'
    else:
        classification = 'Por encima del minimo'

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
    Parsea una duracion textual a anios decimales

    Args:
        duration_str: String como "2 anios", "1.5 anios", "6 meses", "2021-2023"

    Returns:
        Anios en formato decimal

    Examples:
        >>> parse_experience_duration("2 anios")
        2.0
        >>> parse_experience_duration("6 meses")
        0.5
        >>> parse_experience_duration("2021 - 2023")
        2.0
    """
    if not duration_str:
        return 0.0

    duration_str = duration_str.lower().strip()

    # Caso 1: Formato "X anios"
    match_years = re.search(r'(\d+\.?\d*)\s*a[ñn]os?', duration_str)
    if match_years:
        return float(match_years.group(1))

    # Caso 2: Formato "X meses"
    match_months = re.search(r'(\d+)\s*mes(?:es)?', duration_str)
    if match_months:
        return round(float(match_months.group(1)) / 12, 2)

    # Caso 3: Rango de fechas ISO "YYYY-MM-DD - YYYY-MM-DD" (Gemini puede devolver fechas completas)
    match_iso_range = re.search(
        r'(\d{4})-\d{2}-\d{2}\s*[-–]\s*(\d{4})-\d{2}-\d{2}', duration_str
    )
    if match_iso_range:
        start_year = int(match_iso_range.group(1))
        end_year = int(match_iso_range.group(2))
        return float(max(0, end_year - start_year))

    match_iso_open = re.search(
        r'(\d{4})-\d{2}-\d{2}\s*[-–]\s*(presente|actual|present)', duration_str
    )
    if match_iso_open:
        start_year = int(match_iso_open.group(1))
        return float(max(0, datetime.now().year - start_year))

    # Caso 3b: Formato "YYYY - YYYY" o "YYYY-YYYY"
    match_range = re.search(r'(\d{4})\s*[-–]\s*(\d{4}|presente|actual|present)', duration_str)
    if match_range:
        start_year = int(match_range.group(1))
        end_year_str = match_range.group(2)

        if end_year_str in ['presente', 'actual', 'present']:
            end_year = datetime.now().year
        else:
            end_year = int(end_year_str)

        return float(max(0, end_year - start_year))

    # Caso 3c: Año suelto de 4 dígitos (ej: "2025") — se interpreta como
    # inicio en ese año hasta la actualidad. Evita que "2025" se tome como
    # 2025 años de experiencia en el caso 4.
    match_single_year = re.fullmatch(r'\d{4}', duration_str.strip())
    if match_single_year:
        start_year = int(duration_str.strip())
        return float(max(0, datetime.now().year - start_year))

    # Caso 3d: Días ("X días" / "X days") — Gemini puede devolver duraciones en días
    match_days = re.search(r'(\d+)\s*d[íi]as?|(\d+)\s*days?', duration_str)
    if match_days:
        days = float((match_days.group(1) or match_days.group(2)))
        return round(days / 365, 2)

    # Caso 4: Numero decimal directo — con límite de seguridad para valores absurdos
    match_number = re.search(r'(\d+\.?\d*)', duration_str)
    if match_number:
        value = float(match_number.group(1))
        # Si el valor supera 80 años de carrera razonable, ignorar (formato desconocido)
        if value > 80:
            return 0.0
        return value

    # Default: 0
    return 0.0


def calculate_total_experience(experience_list: list) -> float:
    """
    Calcula anios totales de experiencia desde una lista de experiencias

    Args:
        experience_list: Lista de dicts con campo 'duration'

    Returns:
        Total de anios de experiencia

    Examples:
        >>> experiences = [
        ...     {'duration': '2 anios'},
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
