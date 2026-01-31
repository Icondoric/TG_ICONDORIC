"""
Cargador de perfiles institucionales
"""

import json
import os
from typing import Dict, List, Optional

# Directorio de perfiles
PROFILES_DIR = os.path.join(os.path.dirname(__file__), "profiles")


def get_available_profiles() -> List[str]:
    """
    Retorna lista de IDs de perfiles disponibles

    Returns:
        Lista de nombres de perfiles (sin extension .json)

    Example:
        >>> get_available_profiles()
        ['profile_agetic', 'profile_banco_fie', ...]
    """
    profiles = []
    if os.path.exists(PROFILES_DIR):
        for filename in os.listdir(PROFILES_DIR):
            if filename.endswith(".json"):
                profiles.append(filename.replace(".json", ""))
    return sorted(profiles)


def load_profile(profile_id: str) -> Optional[Dict]:
    """
    Carga un perfil institucional por su ID

    Args:
        profile_id: ID del perfil (ej: "profile_agetic")

    Returns:
        Dict con datos del perfil o None si no existe

    Example:
        >>> profile = load_profile("profile_agetic")
        >>> profile["institution_name"]
        'AGETIC - Agencia de Gobierno Electronico y TICs'
    """
    # Agregar extension si no la tiene
    if not profile_id.endswith(".json"):
        filename = f"{profile_id}.json"
    else:
        filename = profile_id

    filepath = os.path.join(PROFILES_DIR, filename)

    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading profile {profile_id}: {e}")
        return None


def load_all_profiles() -> Dict[str, Dict]:
    """
    Carga todos los perfiles institucionales disponibles

    Returns:
        Dict con profile_id como key y datos del perfil como value

    Example:
        >>> profiles = load_all_profiles()
        >>> len(profiles)
        5
    """
    profiles = {}
    for profile_id in get_available_profiles():
        profile_data = load_profile(profile_id)
        if profile_data:
            profiles[profile_id] = profile_data
    return profiles


def validate_profile(profile: Dict) -> Dict[str, any]:
    """
    Valida que un perfil tenga la estructura correcta

    Args:
        profile: Dict con datos del perfil

    Returns:
        Dict con resultado de validacion
    """
    required_fields = ["id", "institution_name", "weights", "requirements", "thresholds"]
    required_weights = ["hard_skills", "soft_skills", "experience", "education", "languages"]

    errors = []

    # Verificar campos requeridos
    for field in required_fields:
        if field not in profile:
            errors.append(f"Campo requerido faltante: {field}")

    # Verificar pesos
    if "weights" in profile:
        weights = profile["weights"]
        for w in required_weights:
            if w not in weights:
                errors.append(f"Peso requerido faltante: {w}")

        # Verificar que los pesos sumen 1.0
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            errors.append(f"Los pesos deben sumar 1.0, suma actual: {total}")

    # Verificar umbrales
    if "thresholds" in profile:
        thresholds = profile["thresholds"]
        if "apto" not in thresholds:
            errors.append("Umbral 'apto' requerido")
        if "considerado" not in thresholds:
            errors.append("Umbral 'considerado' requerido")
        if thresholds.get("apto", 0) <= thresholds.get("considerado", 0):
            errors.append("Umbral 'apto' debe ser mayor que 'considerado'")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "profile_id": profile.get("id", "unknown")
    }
