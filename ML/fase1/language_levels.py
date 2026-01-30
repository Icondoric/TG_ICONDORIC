"""
Configuración de niveles de idiomas para evaluación de perfiles
Basado en el Marco Común Europeo de Referencia (CEFR)
"""

LANGUAGE_LEVELS = {
    "Básico": 0.30,
    "A1": 0.35,
    "A2": 0.45,
    "Intermedio": 0.55,
    "B1": 0.60,
    "B2": 0.75,
    "Avanzado": 0.85,
    "C1": 0.90,
    "C2": 0.95,
    "Nativo": 1.00,
    "Materno": 1.00,
    "Fluido": 0.80  # Término común sin nivel específico
}


def get_language_score(language_description: str) -> float:
    """
    Extrae el score de un idioma desde su descripción
    
    Args:
        language_description: Descripción del idioma (ej: "Inglés (B2)", "Español Nativo")
    
    Returns:
        Score numérico entre 0 y 1
    
    Examples:
        >>> get_language_score("Inglés (B2)")
        0.75
        >>> get_language_score("Español (Nativo)")
        1.0
        >>> get_language_score("Francés Intermedio")
        0.55
    """
    if not language_description:
        return 0.5  # Default: intermedio
    
    desc_upper = language_description.upper()
    
    # Buscar niveles CEFR (más específicos primero)
    if "C2" in desc_upper:
        return LANGUAGE_LEVELS["C2"]
    if "C1" in desc_upper:
        return LANGUAGE_LEVELS["C1"]
    if "B2" in desc_upper:
        return LANGUAGE_LEVELS["B2"]
    if "B1" in desc_upper:
        return LANGUAGE_LEVELS["B1"]
    if "A2" in desc_upper:
        return LANGUAGE_LEVELS["A2"]
    if "A1" in desc_upper:
        return LANGUAGE_LEVELS["A1"]
    
    # Buscar términos descriptivos
    desc_lower = language_description.lower()
    
    if "nativ" in desc_lower or "matern" in desc_lower:
        return LANGUAGE_LEVELS["Nativo"]
    
    if "avanzad" in desc_lower or "advanced" in desc_lower:
        return LANGUAGE_LEVELS["Avanzado"]
    
    if "fluid" in desc_lower:
        return LANGUAGE_LEVELS["Fluido"]
    
    if "intermedi" in desc_lower or "intermediate" in desc_lower:
        return LANGUAGE_LEVELS["Intermedio"]
    
    if "básic" in desc_lower or "basic" in desc_lower or "basico" in desc_lower:
        return LANGUAGE_LEVELS["Básico"]
    
    # Default: asumir intermedio si no se especifica
    return 0.5


def parse_language_entry(language_str: str) -> dict:
    """
    Parsea una entrada de idioma completa
    
    Args:
        language_str: String del idioma (ej: "Inglés (B2)")
    
    Returns:
        Dict con language_name y score
    
    Examples:
        >>> parse_language_entry("Inglés (B2)")
        {'language': 'Inglés', 'level': 'B2', 'score': 0.75}
    """
    import re
    
    # Extraer nivel entre paréntesis si existe
    match = re.search(r'\(([^)]+)\)', language_str)
    level = match.group(1) if match else ""
    
    # Extraer nombre del idioma (antes del paréntesis)
    language_name = re.sub(r'\([^)]+\)', '', language_str).strip()
    
    # Si no hay nombre, usar todo el string
    if not language_name:
        language_name = language_str
    
    score = get_language_score(language_str)
    
    return {
        'language': language_name,
        'level': level if level else "Sin especificar",
        'score': score
    }


def calculate_languages_score(cv_languages: list, required_languages: list) -> dict:
    """
    Calcula el score de idiomas comparando CV con requisitos
    
    Args:
        cv_languages: Lista de idiomas del CV (ej: ["Español (Nativo)", "Inglés (B2)"])
        required_languages: Lista de idiomas requeridos (ej: ["Inglés", "Francés"])
    
    Returns:
        Dict con score global y detalles
    
    Examples:
        >>> calculate_languages_score(
        ...     ["Español (Nativo)", "Inglés (B2)"],
        ...     ["Inglés"]
        ... )
        {'score': 0.75, 'matched': ['Inglés'], 'missing': []}
    """
    if not required_languages:
        return {
            'score': 1.0,  # Si no hay requisitos, score perfecto
            'matched': [],
            'missing': [],
            'details': []
        }
    
    # Parsear idiomas del CV
    cv_parsed = []
    for lang_str in cv_languages:
        parsed = parse_language_entry(lang_str)
        cv_parsed.append(parsed)
    
    # Verificar cada idioma requerido
    scores = []
    matched = []
    missing = []
    details = []
    
    for req_lang in required_languages:
        req_lang_lower = req_lang.lower().strip()
        
        # Buscar coincidencia en CV
        found = False
        for cv_lang in cv_parsed:
            if req_lang_lower in cv_lang['language'].lower():
                scores.append(cv_lang['score'])
                matched.append(cv_lang['language'])
                details.append({
                    'language': req_lang,
                    'found': True,
                    'level': cv_lang['level'],
                    'score': cv_lang['score']
                })
                found = True
                break
        
        if not found:
            scores.append(0.0)
            missing.append(req_lang)
            details.append({
                'language': req_lang,
                'found': False,
                'level': 'N/A',
                'score': 0.0
            })
    
    # Score global = promedio de scores
    global_score = sum(scores) / len(scores) if scores else 1.0
    
    return {
        'score': round(global_score, 3),
        'matched': matched,
        'missing': missing,
        'details': details
    }
