"""
Hard Skills Scorer
Evalúa competencias técnicas usando TF-IDF + Jaccard Similarity
"""

from typing import Dict, List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def calculate_jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """
    Calcula similitud de Jaccard entre dos conjuntos
    
    Jaccard = |A ∩ B| / |A ∪ B|
    
    Args:
        set_a: Conjunto A (ej: skills del CV)
        set_b: Conjunto B (ej: skills requeridos)
    
    Returns:
        Similitud entre 0 y 1
    
    Examples:
        >>> calculate_jaccard_similarity({'Python', 'SQL'}, {'Python', 'Java'})
        0.333
    """
    if not set_a or not set_b:
        return 0.0
    
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    
    return intersection / union if union > 0 else 0.0


def calculate_tfidf_similarity(cv_skills: List[str], required_skills: List[str]) -> float:
    """
    Calcula similitud semántica usando TF-IDF
    Útil para detectar skills relacionados (ej: "Machine Learning" vs "ML")
    
    Args:
        cv_skills: Lista de skills del CV
        required_skills: Lista de skills requeridos
    
    Returns:
        Similitud entre 0 y 1
    """
    if not cv_skills or not required_skills:
        return 0.0
    
    # Unir skills en strings
    cv_text = ' '.join(cv_skills)
    required_text = ' '.join(required_skills)
    
    # Vectorizar con TF-IDF
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),  # Unigramas y bigramas
        max_features=100
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([cv_text, required_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except:
        return 0.0


def normalize_skill(skill: str) -> str:
    """
    Normaliza un skill para mejorar matching
    
    Args:
        skill: Nombre del skill
    
    Returns:
        Skill normalizado
    
    Examples:
        >>> normalize_skill("  Python 3.x  ")
        'python'
        >>> normalize_skill("React.js")
        'react'
    """
    # Convertir a minúsculas
    skill = skill.lower().strip()
    
    # Remover versiones (ej: "Python 3.x" -> "python")
    skill = skill.split()[0]
    
    # Remover extensiones comunes (.js, .py)
    skill = skill.replace('.js', '').replace('.py', '')
    
    # Mapeos comunes
    mappings = {
        'javascript': 'js',
        'typescript': 'ts',
        'reactjs': 'react',
        'vuejs': 'vue',
        'nodejs': 'node',
        'postgresql': 'postgres',
        'fastapi': 'fast api'
    }
    
    return mappings.get(skill, skill)


def calculate_hard_skills_score(
    cv_skills: List[str],
    required_skills: List[str],
    preferred_skills: List[str] = None
) -> Dict:
    """
    Calcula score de hard skills combinando matching exacto y semántico
    
    Estrategia:
    1. Normalizar todos los skills
    2. Matching exacto (Jaccard) con skills requeridos
    3. Matching semántico (TF-IDF) para detectar relacionados
    4. Bonus por skills preferidos
    
    Args:
        cv_skills: Lista de skills del candidato
        required_skills: Lista de skills obligatorios
        preferred_skills: Lista de skills deseables (opcional)
    
    Returns:
        Dict con score y detalles del matching
    
    Examples:
        >>> calculate_hard_skills_score(
        ...     cv_skills=['Python', 'React', 'SQL'],
        ...     required_skills=['Python', 'JavaScript'],
        ...     preferred_skills=['React', 'Docker']
        ... )
        {
            'score': 0.75,
            'required_match_ratio': 0.5,
            'preferred_match_ratio': 0.5,
            'matched_required': ['Python'],
            'matched_preferred': ['React'],
            'missing_required': ['JavaScript'],
            'total_cv_skills': 3
        }
    """
    if preferred_skills is None:
        preferred_skills = []
    
    # Normalizar skills
    cv_normalized = set([normalize_skill(s) for s in cv_skills])
    required_normalized = set([normalize_skill(s) for s in required_skills])
    preferred_normalized = set([normalize_skill(s) for s in preferred_skills]) if preferred_skills else set()
    
    # === MATCHING EXACTO (Jaccard) ===
    
    # Required skills
    required_matched = cv_normalized & required_normalized
    required_missing = required_normalized - cv_normalized
    required_match_ratio = len(required_matched) / len(required_normalized) if required_normalized else 0.0
    
    # Preferred skills
    preferred_matched = cv_normalized & preferred_normalized if preferred_normalized else set()
    preferred_match_ratio = len(preferred_matched) / len(preferred_normalized) if preferred_normalized else 0.0
    
    # === MATCHING SEMÁNTICO (TF-IDF) ===
    semantic_similarity = calculate_tfidf_similarity(cv_skills, required_skills)
    
    # === CÁLCULO DE SCORE FINAL ===
    
    # Pesos de cada componente
    WEIGHT_REQUIRED_EXACT = 0.50   # 50% - Match exacto con requeridos
    WEIGHT_SEMANTIC = 0.25          # 25% - Similitud semántica
    WEIGHT_PREFERRED = 0.15         # 15% - Match con preferidos
    WEIGHT_BREADTH = 0.10           # 10% - Amplitud de skills (bonus por tener más)
    
    # Componente 1: Match exacto con requeridos
    score_required = required_match_ratio
    
    # Componente 2: Similitud semántica (captura relacionados)
    score_semantic = semantic_similarity
    
    # Componente 3: Match con preferidos (bonus)
    score_preferred = preferred_match_ratio
    
    # Componente 4: Amplitud de skills (bonus si tiene muchos skills)
    # Normalizado: tener 10+ skills = 1.0, menos = proporcional
    breadth_score = min(1.0, len(cv_normalized) / 10.0)
    
    # Score final ponderado
    final_score = (
        score_required * WEIGHT_REQUIRED_EXACT +
        score_semantic * WEIGHT_SEMANTIC +
        score_preferred * WEIGHT_PREFERRED +
        breadth_score * WEIGHT_BREADTH
    )
    
    # === PENALIZACIÓN SI NO CUMPLE MÍNIMO ===
    # Si match con requeridos < 50%, penalizar fuertemente
    if required_match_ratio < 0.5:
        final_score *= 0.7  # Penalización del 30%
    
    return {
        'score': round(min(1.0, final_score), 3),
        'required_match_ratio': round(required_match_ratio, 3),
        'preferred_match_ratio': round(preferred_match_ratio, 3),
        'semantic_similarity': round(semantic_similarity, 3),
        'matched_required': list(required_matched),
        'matched_preferred': list(preferred_matched),
        'missing_required': list(required_missing),
        'total_cv_skills': len(cv_normalized),
        'breadth_score': round(breadth_score, 3)
    }


def extract_hard_skills_from_gemini(gemini_output: Dict) -> List[str]:
    """
    Extrae hard skills desde el output de Gemini
    
    Args:
        gemini_output: Dict con estructura de Gemini
    
    Returns:
        Lista de hard skills
    
    Examples:
        >>> extract_hard_skills_from_gemini({
        ...     'hard_skills': ['Python', 'React', 'SQL']
        ... })
        ['Python', 'React', 'SQL']
    """
    if not gemini_output or 'hard_skills' not in gemini_output:
        return []
    
    return gemini_output.get('hard_skills', [])
