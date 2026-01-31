"""
Configuracion de niveles educativos para evaluacion de perfiles
Basado en el sistema educativo boliviano y estandares academicos
"""

EDUCATION_LEVELS = {
    "Tecnico Medio": 0.25,
    "Tecnico Superior": 0.45,
    "Licenciatura": 0.75,
    "Ingenieria": 0.75,      # Mismo nivel que Licenciatura (EMI)
    "Diplomado": 0.80,       # Formacion complementaria
    "Especialidad": 0.85,
    "Maestria": 0.92,
    "Doctorado": 1.00
}


def get_education_score(degree_name: str) -> float:
    """
    Retorna score de educacion [0-1]

    Args:
        degree_name: Nombre del grado (ej: "Licenciatura en Ingenieria de Sistemas")

    Returns:
        Score numerico entre 0 y 1

    Examples:
        >>> get_education_score("Ingenieria")
        0.75
        >>> get_education_score("Maestria en Ciencias")
        0.92
        >>> get_education_score("Licenciado en Sistemas")
        0.75
    """
    if not degree_name:
        return 0.0

    # Busqueda exacta (case insensitive)
    degree_clean = degree_name.strip()
    for key, value in EDUCATION_LEVELS.items():
        if key.lower() == degree_clean.lower():
            return value

    # Busqueda por coincidencia parcial
    degree_lower = degree_clean.lower()

    # Priorizar coincidencias mas especificas primero
    if "doctor" in degree_lower or "phd" in degree_lower:
        return EDUCATION_LEVELS["Doctorado"]

    if "maestr" in degree_lower or "magister" in degree_lower or "master" in degree_lower:
        return EDUCATION_LEVELS["Maestria"]

    if "especial" in degree_lower:
        return EDUCATION_LEVELS["Especialidad"]

    if "diplomado" in degree_lower:
        return EDUCATION_LEVELS["Diplomado"]

    if "ingenier" in degree_lower:
        return EDUCATION_LEVELS["Ingenieria"]

    if "licenciat" in degree_lower or "licenciad" in degree_lower:
        return EDUCATION_LEVELS["Licenciatura"]

    if "tecnico superior" in degree_lower:
        return EDUCATION_LEVELS["Tecnico Superior"]

    if "tecnico" in degree_lower:
        return EDUCATION_LEVELS["Tecnico Medio"]

    # Default: asumir nivel mas bajo
    return EDUCATION_LEVELS["Tecnico Medio"]


def get_education_level_name(score: float) -> str:
    """
    Retorna el nombre del nivel educativo dado un score

    Args:
        score: Score numerico [0-1]

    Returns:
        Nombre del nivel educativo
    """
    # Encontrar el nivel mas cercano
    closest_level = min(
        EDUCATION_LEVELS.items(),
        key=lambda x: abs(x[1] - score)
    )
    return closest_level[0]
