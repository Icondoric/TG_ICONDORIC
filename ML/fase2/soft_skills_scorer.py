"""
Soft Skills Scorer
Evalúa habilidades blandas usando matching semántico
"""

from typing import Dict, List, Set


def normalize_soft_skill(skill: str) -> str:
    """
    Normaliza una soft skill para mejor matching
    
    Args:
        skill: Nombre de la soft skill
    
    Returns:
        Skill normalizado
    
    Examples:
        >>> normalize_soft_skill("  Trabajo en Equipo  ")
        'trabajo en equipo'
        >>> normalize_soft_skill("Teamwork")
        'trabajo en equipo'
    """
    skill = skill.lower().strip()
    
    # Mapeo de términos en inglés/español
    mappings = {
        'teamwork': 'trabajo en equipo',
        'leadership': 'liderazgo',
        'communication': 'comunicación',
        'problem solving': 'resolución de problemas',
        'adaptability': 'adaptabilidad',
        'creativity': 'creatividad',
        'critical thinking': 'pensamiento crítico',
        'time management': 'gestión del tiempo',
        'empathy': 'empatía',
        'collaboration': 'colaboración',
        'flexibility': 'flexibilidad',
        'initiative': 'iniciativa',
        'decision making': 'toma de decisiones',
        'conflict resolution': 'resolución de conflictos',
        'emotional intelligence': 'inteligencia emocional'
    }
    
    return mappings.get(skill, skill)


def get_soft_skill_category(skill: str) -> str:
    """
    Clasifica una soft skill en categorías amplias
    Útil para matching semántico
    
    Args:
        skill: Nombre de la soft skill
    
    Returns:
        Categoría de la skill
    
    Examples:
        >>> get_soft_skill_category("liderazgo")
        'interpersonal'
        >>> get_soft_skill_category("pensamiento crítico")
        'cognitivo'
    """
    skill_normalized = normalize_soft_skill(skill)
    
    categories = {
        'interpersonal': [
            'liderazgo', 'trabajo en equipo', 'comunicación', 
            'colaboración', 'empatía', 'inteligencia emocional',
            'resolución de conflictos', 'persuasión'
        ],
        'cognitivo': [
            'pensamiento crítico', 'creatividad', 'resolución de problemas',
            'toma de decisiones', 'análisis', 'innovación'
        ],
        'organizacional': [
            'gestión del tiempo', 'planificación', 'organización',
            'priorización', 'multitasking'
        ],
        'personal': [
            'adaptabilidad', 'flexibilidad', 'iniciativa',
            'autonomía', 'proactividad', 'resiliencia', 'motivación'
        ]
    }
    
    for category, skills_list in categories.items():
        if any(skill_normalized in s or s in skill_normalized for s in skills_list):
            return category
    
    return 'general'


def calculate_soft_skills_score(
    cv_soft_skills: List[str],
    required_soft_skills: List[str]
) -> Dict:
    """
    Calcula score de soft skills usando matching exacto y por categorías
    
    Estrategia:
    1. Normalizar soft skills
    2. Matching exacto (Jaccard)
    3. Matching por categorías (si comparten categoría, cuenta parcialmente)
    4. Score final combinado
    
    Args:
        cv_soft_skills: Lista de soft skills del CV
        required_soft_skills: Lista de soft skills requeridas
    
    Returns:
        Dict con score y detalles
    
    Examples:
        >>> calculate_soft_skills_score(
        ...     cv_soft_skills=['Liderazgo', 'Comunicación', 'Trabajo en equipo'],
        ...     required_soft_skills=['Liderazgo', 'Adaptabilidad']
        ... )
        {
            'score': 0.65,
            'exact_match_ratio': 0.5,
            'category_match_ratio': 0.75,
            'matched_exact': ['liderazgo'],
            'matched_by_category': ['comunicación', 'trabajo en equipo'],
            'missing': ['adaptabilidad']
        }
    """
    if not required_soft_skills:
        return {
            'score': 1.0,  # Si no hay requisitos, score perfecto
            'exact_match_ratio': 1.0,
            'category_match_ratio': 1.0,
            'matched_exact': [],
            'matched_by_category': [],
            'missing': []
        }
    
    if not cv_soft_skills:
        return {
            'score': 0.0,
            'exact_match_ratio': 0.0,
            'category_match_ratio': 0.0,
            'matched_exact': [],
            'matched_by_category': [],
            'missing': [normalize_soft_skill(s) for s in required_soft_skills]
        }
    
    # Normalizar
    cv_normalized = set([normalize_soft_skill(s) for s in cv_soft_skills])
    required_normalized = set([normalize_soft_skill(s) for s in required_soft_skills])
    
    # === MATCHING EXACTO ===
    exact_matched = cv_normalized & required_normalized
    exact_match_ratio = len(exact_matched) / len(required_normalized)
    
    # === MATCHING POR CATEGORÍAS ===
    # Para skills que no hicieron match exacto, ver si comparten categoría
    cv_categories = {skill: get_soft_skill_category(skill) for skill in cv_normalized}
    required_categories = {skill: get_soft_skill_category(skill) for skill in required_normalized}
    
    category_matches = set()
    for req_skill, req_category in required_categories.items():
        if req_skill not in exact_matched:  # Solo si no hubo match exacto
            for cv_skill, cv_category in cv_categories.items():
                if cv_category == req_category:
                    category_matches.add(cv_skill)
                    break
    
    # Ratio de skills requeridas cubiertas (exacto + categoría)
    total_coverage = len(exact_matched) + len(category_matches)
    category_match_ratio = total_coverage / len(required_normalized)
    
    # Skills faltantes
    missing = required_normalized - exact_matched
    
    # === CÁLCULO DE SCORE FINAL ===
    WEIGHT_EXACT = 0.70   # 70% - Match exacto
    WEIGHT_CATEGORY = 0.30  # 30% - Match por categoría
    
    final_score = (
        exact_match_ratio * WEIGHT_EXACT +
        category_match_ratio * WEIGHT_CATEGORY
    )
    
    return {
        'score': round(min(1.0, final_score), 3),
        'exact_match_ratio': round(exact_match_ratio, 3),
        'category_match_ratio': round(category_match_ratio, 3),
        'matched_exact': list(exact_matched),
        'matched_by_category': list(category_matches),
        'missing': list(missing),
        'cv_categories': list(set(cv_categories.values())),
        'required_categories': list(set(required_categories.values()))
    }


def extract_soft_skills_from_gemini(gemini_output: Dict) -> List[str]:
    """
    Extrae soft skills desde el output de Gemini
    
    Args:
        gemini_output: Dict con estructura de Gemini
    
    Returns:
        Lista de soft skills
    """
    if not gemini_output or 'soft_skills' not in gemini_output:
        return []
    
    return gemini_output.get('soft_skills', [])
