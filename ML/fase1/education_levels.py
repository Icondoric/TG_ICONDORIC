"""
Configuración de niveles educativos para evaluación de perfiles
Basado en el sistema educativo boliviano y estándares académicos
"""

EDUCATION_LEVELS = {
    "Técnico Medio": 0.25,
    "Técnico Superior": 0.45,
    "Licenciatura": 0.75,
    "Ingeniería": 0.75,      # Mismo nivel que Licenciatura (EMI)
    "Diplomado": 0.80,       # Formación complementaria
    "Especialidad": 0.85,
    "Maestría": 0.92,
    "Doctorado": 1.00
}


def get_education_score(degree_name: str) -> float:
    """
    Retorna score de educación [0-1]
    
    Args:
        degree_name: Nombre del grado (ej: "Licenciatura en Ingeniería de Sistemas")
    
    Returns:
        Score numérico entre 0 y 1
    
    Examples:
        >>> get_education_score("Ingeniería")
        0.75
        >>> get_education_score("Maestría en Ciencias")
        0.92
        >>> get_education_score("Licenciado en Sistemas")
        0.75
    """
    if not degree_name:
        return 0.0
    
    # Búsqueda exacta (case insensitive)
    degree_clean = degree_name.strip()
    for key, value in EDUCATION_LEVELS.items():
        if key.lower() == degree_clean.lower():
            return value
    
    # Búsqueda por coincidencia parcial
    degree_lower = degree_clean.lower()
    
    # Priorizar coincidencias más específicas primero
    if "doctor" in degree_lower or "phd" in degree_lower:
        return EDUCATION_LEVELS["Doctorado"]
    
    if "maestr" in degree_lower or "magister" in degree_lower or "master" in degree_lower:
        return EDUCATION_LEVELS["Maestría"]
    
    if "especial" in degree_lower:
        return EDUCATION_LEVELS["Especialidad"]
    
    if "diplomado" in degree_lower:
        return EDUCATION_LEVELS["Diplomado"]
    
    if "ingenier" in degree_lower:
        return EDUCATION_LEVELS["Ingeniería"]
    
    if "licenciat" in degree_lower or "licenciad" in degree_lower:
        return EDUCATION_LEVELS["Licenciatura"]
    
    if "técnico superior" in degree_lower or "tecnico superior" in degree_lower:
        return EDUCATION_LEVELS["Técnico Superior"]
    
    if "técnico" in degree_lower or "tecnico" in degree_lower:
        return EDUCATION_LEVELS["Técnico Medio"]
    
    # Default: asumir nivel más bajo
    return EDUCATION_LEVELS["Técnico Medio"]


def get_education_level_name(score: float) -> str:
    """
    Retorna el nombre del nivel educativo dado un score
    
    Args:
        score: Score numérico [0-1]
    
    Returns:
        Nombre del nivel educativo
    """
    # Encontrar el nivel más cercano
    closest_level = min(
        EDUCATION_LEVELS.items(),
        key=lambda x: abs(x[1] - score)
    )
    return closest_level[0]
