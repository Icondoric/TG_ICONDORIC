"""
Institutional Configurations Loader
Carga y gestiona perfiles institucionales desde archivos JSON
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path


class InstitutionalConfigLoader:
    """
    Carga y gestiona configuraciones de instituciones
    """
    
    def __init__(self, profiles_dir: str = None):
        """
        Args:
            profiles_dir: Directorio donde están los JSONs de perfiles
        """
        if profiles_dir is None:
            # Por defecto, buscar en la carpeta del módulo
            current_dir = Path(__file__).parent
            profiles_dir = current_dir / 'config' / 'institutional_profiles'
        
        self.profiles_dir = Path(profiles_dir)
        self.profiles_cache = {}
    
    def load_profile(self, profile_id: str) -> Optional[Dict]:
        """
        Carga un perfil institucional por ID
        
        Args:
            profile_id: ID del perfil (ej: 'tech_startup', 'gov_health')
        
        Returns:
            Dict con configuración institucional o None si no existe
        
        Examples:
            >>> loader = InstitutionalConfigLoader()
            >>> profile = loader.load_profile('tech_startup')
            >>> profile['weights']['hard_skills']
            0.45
        """
        # Verificar cache
        if profile_id in self.profiles_cache:
            return self.profiles_cache[profile_id]
        
        # Buscar archivo
        json_path = self.profiles_dir / f"{profile_id}.json"
        
        if not json_path.exists():
            print(f"⚠️ Warning: Profile '{profile_id}' no encontrado en {self.profiles_dir}")
            return None
        
        # Cargar JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                profile = json.load(f)
            
            # Validar estructura
            if not self._validate_profile(profile):
                print(f"⚠️ Warning: Profile '{profile_id}' tiene estructura inválida")
                return None
            
            # Guardar en cache
            self.profiles_cache[profile_id] = profile
            
            return profile
        
        except Exception as e:
            print(f"❌ Error cargando profile '{profile_id}': {e}")
            return None
    
    def load_all_profiles(self) -> Dict[str, Dict]:
        """
        Carga todos los perfiles disponibles
        
        Returns:
            Dict con {profile_id: config}
        """
        if not self.profiles_dir.exists():
            print(f"⚠️ Warning: Directorio {self.profiles_dir} no existe")
            return {}
        
        profiles = {}
        
        for json_file in self.profiles_dir.glob("*.json"):
            profile_id = json_file.stem  # Nombre sin extensión
            profile = self.load_profile(profile_id)
            
            if profile:
                profiles[profile_id] = profile
        
        print(f"✅ Cargados {len(profiles)} perfiles institucionales")
        return profiles
    
    def _validate_profile(self, profile: Dict) -> bool:
        """
        Valida que un perfil tenga la estructura correcta
        
        Args:
            profile: Dict del perfil
        
        Returns:
            True si es válido, False si no
        """
        # Verificar keys principales
        required_keys = ['weights', 'requirements']
        for key in required_keys:
            if key not in profile:
                return False
        
        # Verificar pesos
        weights = profile['weights']
        required_weights = ['hard_skills', 'soft_skills', 'experience', 'education', 'languages']
        
        for weight_key in required_weights:
            if weight_key not in weights:
                return False
            
            if not isinstance(weights[weight_key], (int, float)):
                return False
            
            if weights[weight_key] < 0 or weights[weight_key] > 1:
                return False
        
        # Verificar que sumen ~1.0
        total_weight = sum(weights[k] for k in required_weights)
        if abs(total_weight - 1.0) > 0.01:
            print(f"⚠️ Warning: Pesos no suman 1.0 (suman {total_weight})")
            return False
        
        # Verificar requirements
        requirements = profile['requirements']
        if 'min_experience_years' not in requirements:
            return False
        
        return True
    
    def get_profile_summary(self, profile_id: str) -> str:
        """
        Genera un resumen legible de un perfil
        
        Args:
            profile_id: ID del perfil
        
        Returns:
            String con resumen
        """
        profile = self.load_profile(profile_id)
        
        if not profile:
            return f"Profile '{profile_id}' no encontrado"
        
        summary = f"\n{'='*60}\n"
        summary += f"PERFIL INSTITUCIONAL: {profile.get('institution_name', profile_id)}\n"
        summary += f"{'='*60}\n"
        
        # Sector
        summary += f"\nSector: {profile.get('sector', 'N/A')}\n"
        summary += f"Descripción: {profile.get('description', 'N/A')}\n"
        
        # Pesos
        summary += f"\n📊 Distribución de Pesos:\n"
        weights = profile['weights']
        for key, value in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            bar = '█' * int(value * 50)
            summary += f"  {key:20s}: {value:.2f} {bar}\n"
        
        # Requisitos
        requirements = profile['requirements']
        summary += f"\n📋 Requisitos:\n"
        summary += f"  Experiencia mínima: {requirements.get('min_experience_years', 0)} años\n"
        summary += f"  Skills requeridos: {', '.join(requirements.get('required_skills', []))}\n"
        summary += f"  Skills preferidos: {', '.join(requirements.get('preferred_skills', []))}\n"
        summary += f"  Educación mínima: {requirements.get('required_education_level', 'N/A')}\n"
        summary += f"  Idiomas: {', '.join(requirements.get('required_languages', ['Ninguno']))}\n"
        
        # Umbrales
        if 'thresholds' in profile:
            summary += f"\n🎯 Umbrales de Clasificación:\n"
            summary += f"  APTO: ≥ {profile['thresholds'].get('apto', 0.7)}\n"
            summary += f"  CONSIDERADO: ≥ {profile['thresholds'].get('considerado', 0.5)}\n"
        
        summary += f"\n{'='*60}\n"
        
        return summary


def get_random_profile_config() -> Dict:
    """
    Genera una configuración institucional aleatoria
    Útil para generación de dataset sintético
    
    Returns:
        Dict con configuración válida
    """
    import random
    import numpy as np
    
    # Generar pesos aleatorios que sumen 1.0
    weights = np.random.dirichlet([2, 2, 2, 2, 2])
    
    # Skills pool
    skills_pool = [
        'Python', 'JavaScript', 'SQL', 'React', 'FastAPI',
        'Docker', 'Git', 'Excel', 'PowerBI', 'Tableau',
        'Java', 'C++', 'AWS', 'Azure', 'PostgreSQL'
    ]
    
    # Generar requisitos
    n_required = random.randint(2, 5)
    required_skills = random.sample(skills_pool, n_required)
    
    n_preferred = random.randint(1, 4)
    remaining_skills = [s for s in skills_pool if s not in required_skills]
    preferred_skills = random.sample(remaining_skills, min(n_preferred, len(remaining_skills)))
    
    config = {
        'weights': {
            'hard_skills': float(weights[0]),
            'soft_skills': float(weights[1]),
            'experience': float(weights[2]),
            'education': float(weights[3]),
            'languages': float(weights[4])
        },
        'requirements': {
            'min_experience_years': random.uniform(0, 5),
            'required_skills': required_skills,
            'preferred_skills': preferred_skills,
            'required_education_level': random.choice(['Técnico Superior', 'Licenciatura', 'Ingeniería', 'Maestría']),
            'required_languages': random.choice([[], ['Inglés'], ['Inglés', 'Francés']])
        }
    }
    
    return config


# === EJEMPLOS DE USO ===

if __name__ == "__main__":
    # Ejemplo 1: Cargar un perfil específico
    loader = InstitutionalConfigLoader()
    
    profile = loader.load_profile('tech_startup')
    if profile:
        print(loader.get_profile_summary('tech_startup'))
    
    # Ejemplo 2: Cargar todos los perfiles
    all_profiles = loader.load_all_profiles()
    print(f"\nPerfiles cargados: {list(all_profiles.keys())}")
    
    # Ejemplo 3: Generar perfil aleatorio
    random_config = get_random_profile_config()
    print(f"\n🎲 Configuración aleatoria generada:")
    print(f"   Peso hard_skills: {random_config['weights']['hard_skills']:.2f}")
    print(f"   Skills requeridos: {random_config['requirements']['required_skills']}")
