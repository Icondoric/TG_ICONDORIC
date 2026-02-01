"""
Profile Service - Sistema de Recomendaciones v2
Servicio para gestionar perfiles profesionales de usuarios
"""

import logging
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.db.client import supabase
from app.services.ml_integration_service import get_ml_service

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProfileService:
    """
    Servicio para gestionar perfiles profesionales de usuarios.

    Funcionalidades:
    - Actualizar perfil desde extraccion de CV (Gemini)
    - Calcular completitud del perfil
    - Edicion manual de campos
    - Consulta de perfil
    """

    _instance = None

    # Mapeo de niveles educativos a valores numericos
    EDUCATION_LEVELS = {
        'bachillerato': 1,
        'tecnico': 2,
        'tecnico superior': 2,
        'licenciatura': 3,
        'ingenieria': 3,
        'maestria': 4,
        'magister': 4,
        'doctorado': 5,
        'phd': 5
    }

    # Pesos para calculo de completitud
    COMPLETENESS_WEIGHTS = {
        'hard_skills': 0.25,
        'soft_skills': 0.15,
        'education': 0.20,
        'experience': 0.25,
        'languages': 0.10,
        'summary': 0.05
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_profile(self, user_id: str) -> Optional[Dict]:
        """
        Obtiene el perfil profesional de un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            Dict con el perfil o None si no existe
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            response = supabase.table("perfiles_profesionales") \
                .select("*") \
                .eq("usuario_id", user_id) \
                .execute()

            if not response.data:
                return None

            return response.data[0]

        except Exception as e:
            logger.error(f"Error obteniendo perfil de usuario {user_id}: {e}")
            raise

    def get_or_create_profile(self, user_id: str) -> Dict:
        """
        Obtiene el perfil del usuario o crea uno vacio si no existe.

        Args:
            user_id: ID del usuario

        Returns:
            Dict con el perfil
        """
        profile = self.get_profile(user_id)

        if profile:
            return profile

        # Crear perfil vacio
        try:
            data = {
                'usuario_id': user_id,
                'gemini_extraction': {},
                'hard_skills': [],
                'soft_skills': [],
                'education_level': None,
                'experience_years': 0,
                'languages': [],
                'is_complete': False,
                'completeness_score': 0
            }

            response = supabase.table("perfiles_profesionales") \
                .insert(data) \
                .execute()

            if response.data:
                logger.info(f"Perfil creado para usuario {user_id}")
                return response.data[0]

            raise ValueError("No se pudo crear el perfil")

        except Exception as e:
            logger.error(f"Error creando perfil: {e}")
            raise

    def update_profile_from_cv(
        self,
        user_id: str,
        gemini_output: Dict,
        cv_filename: str = None
    ) -> Dict:
        """
        Actualiza el perfil del usuario con los datos extraidos del CV.

        Args:
            user_id: ID del usuario
            gemini_output: Salida de Gemini con datos del CV
            cv_filename: Nombre del archivo CV

        Returns:
            Dict con el perfil actualizado
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        # Asegurar que existe el perfil
        self.get_or_create_profile(user_id)

        # Extraer y normalizar datos
        hard_skills = gemini_output.get('hard_skills', [])
        soft_skills = gemini_output.get('soft_skills', [])
        education = gemini_output.get('education', [])
        experience = gemini_output.get('experience', [])
        personal_info = gemini_output.get('personal_info', {})

        # Determinar nivel educativo mas alto
        education_level = self._extract_highest_education(education)

        # Calcular anos de experiencia
        experience_years = self._calculate_experience_years(experience)

        # Extraer idiomas
        languages = personal_info.get('languages', [])
        if isinstance(languages, str):
            languages = [l.strip() for l in languages.split(',')]

        # Preparar datos para actualizar
        update_data = {
            'gemini_extraction': gemini_output,
            'hard_skills': hard_skills if isinstance(hard_skills, list) else [],
            'soft_skills': soft_skills if isinstance(soft_skills, list) else [],
            'education_level': education_level,
            'experience_years': experience_years,
            'languages': languages if isinstance(languages, list) else [],
            'cv_filename': cv_filename,
            'cv_uploaded_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }

        # Calcular completitud
        completeness = self.calculate_completeness(update_data)
        update_data['completeness_score'] = completeness['score']
        update_data['is_complete'] = completeness['is_complete']

        try:
            response = supabase.table("perfiles_profesionales") \
                .update(update_data) \
                .eq("usuario_id", user_id) \
                .execute()

            if response.data:
                logger.info(f"Perfil actualizado para usuario {user_id}")
                return response.data[0]

            raise ValueError("No se pudo actualizar el perfil")

        except Exception as e:
            logger.error(f"Error actualizando perfil: {e}")
            raise

    def update_profile_manual(
        self,
        user_id: str,
        updates: Dict
    ) -> Dict:
        """
        Actualiza campos del perfil manualmente.

        Args:
            user_id: ID del usuario
            updates: Dict con campos a actualizar

        Returns:
            Dict con el perfil actualizado
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        # Obtener perfil actual
        profile = self.get_profile(user_id)
        if not profile:
            raise ValueError("Perfil no encontrado")

        # Campos permitidos para edicion manual
        allowed_fields = ['hard_skills', 'soft_skills', 'education_level',
                         'experience_years', 'languages']

        update_data = {'updated_at': datetime.utcnow().isoformat()}

        for field in allowed_fields:
            if field in updates and updates[field] is not None:
                update_data[field] = updates[field]

        # Recalcular completitud con los nuevos datos
        merged_profile = {**profile, **update_data}
        completeness = self.calculate_completeness(merged_profile)
        update_data['completeness_score'] = completeness['score']
        update_data['is_complete'] = completeness['is_complete']

        try:
            response = supabase.table("perfiles_profesionales") \
                .update(update_data) \
                .eq("usuario_id", user_id) \
                .execute()

            if response.data:
                logger.info(f"Perfil actualizado manualmente: {user_id}")
                return response.data[0]

            raise ValueError("No se pudo actualizar el perfil")

        except Exception as e:
            logger.error(f"Error en actualizacion manual: {e}")
            raise

    def calculate_completeness(self, profile: Dict) -> Dict:
        """
        Calcula el score de completitud del perfil.

        Args:
            profile: Dict con datos del perfil

        Returns:
            Dict con score, porcentaje, campos faltantes y recomendaciones
        """
        score = 0.0
        missing_fields = []
        recommendations = []

        # Hard skills (25%)
        hard_skills = profile.get('hard_skills', [])
        if hard_skills and len(hard_skills) >= 3:
            score += self.COMPLETENESS_WEIGHTS['hard_skills']
        else:
            missing_fields.append('hard_skills')
            count = len(hard_skills) if hard_skills else 0
            recommendations.append(f"Agrega al menos {3 - count} habilidades tecnicas mas")

        # Soft skills (15%)
        soft_skills = profile.get('soft_skills', [])
        if soft_skills and len(soft_skills) >= 2:
            score += self.COMPLETENESS_WEIGHTS['soft_skills']
        else:
            missing_fields.append('soft_skills')
            count = len(soft_skills) if soft_skills else 0
            recommendations.append(f"Agrega al menos {2 - count} habilidades blandas mas")

        # Educacion (20%)
        education_level = profile.get('education_level')
        gemini_edu = profile.get('gemini_extraction', {}).get('education', [])
        if education_level or (gemini_edu and len(gemini_edu) >= 1):
            score += self.COMPLETENESS_WEIGHTS['education']
        else:
            missing_fields.append('education')
            recommendations.append("Sube tu CV para registrar tu formacion academica")

        # Experiencia (25%)
        experience_years = profile.get('experience_years', 0)
        gemini_exp = profile.get('gemini_extraction', {}).get('experience', [])
        if experience_years > 0 or (gemini_exp and len(gemini_exp) >= 1):
            score += self.COMPLETENESS_WEIGHTS['experience']
        else:
            missing_fields.append('experience')
            recommendations.append("Agrega tu experiencia laboral o pasantias")

        # Idiomas (10%)
        languages = profile.get('languages', [])
        if languages and len(languages) >= 1:
            score += self.COMPLETENESS_WEIGHTS['languages']
        else:
            missing_fields.append('languages')
            recommendations.append("Especifica los idiomas que dominas")

        # Resumen/Summary (5%)
        summary = profile.get('gemini_extraction', {}).get('personal_info', {}).get('summary', '')
        if summary and len(summary) > 20:
            score += self.COMPLETENESS_WEIGHTS['summary']
        else:
            missing_fields.append('summary')
            recommendations.append("Tu CV deberia incluir un resumen profesional")

        # Determinar si esta completo (umbral 70%)
        is_complete = score >= 0.70

        return {
            'score': round(score, 2),
            'percentage': int(score * 100),
            'is_complete': is_complete,
            'missing_fields': missing_fields,
            'recommendations': recommendations
        }

    def _extract_highest_education(self, education_list: List[Dict]) -> Optional[str]:
        """
        Extrae el nivel educativo mas alto de la lista de educacion.

        Args:
            education_list: Lista de items de educacion

        Returns:
            Nombre del nivel educativo mas alto
        """
        if not education_list:
            return None

        highest_level = 0
        highest_name = None

        for edu in education_list:
            degree = edu.get('degree', '').lower()

            for level_name, level_value in self.EDUCATION_LEVELS.items():
                if level_name in degree:
                    if level_value > highest_level:
                        highest_level = level_value
                        # Capitalizar correctamente
                        highest_name = level_name.title()
                    break

        return highest_name

    def _calculate_experience_years(self, experience_list: List[Dict]) -> float:
        """
        Calcula el total de anos de experiencia.

        Args:
            experience_list: Lista de items de experiencia

        Returns:
            Total de anos de experiencia
        """
        if not experience_list:
            return 0.0

        total_years = 0.0

        for exp in experience_list:
            duration = exp.get('duration', '')

            # Patron: "X anos" o "X years"
            years_match = re.search(r'(\d+(?:\.\d+)?)\s*(anos?|years?)', duration.lower())
            if years_match:
                total_years += float(years_match.group(1))
                continue

            # Patron: "X meses" o "X months"
            months_match = re.search(r'(\d+)\s*(meses?|months?)', duration.lower())
            if months_match:
                total_years += float(months_match.group(1)) / 12
                continue

            # Patron: "2020 - 2023" o "2020-2023"
            range_match = re.search(r'(\d{4})\s*[-–]\s*(\d{4}|presente|actual|present)', duration.lower())
            if range_match:
                start_year = int(range_match.group(1))
                end_str = range_match.group(2)

                if end_str in ['presente', 'actual', 'present']:
                    end_year = datetime.now().year
                else:
                    end_year = int(end_str)

                years_diff = end_year - start_year
                if years_diff > 0:
                    total_years += years_diff

        return round(total_years, 1)

    def get_profile_for_recommendations(self, user_id: str) -> Optional[Dict]:
        """
        Obtiene el perfil en formato adecuado para el sistema de recomendaciones.

        Args:
            user_id: ID del usuario

        Returns:
            Dict con formato de gemini_output para ML
        """
        profile = self.get_profile(user_id)

        if not profile:
            return None

        # Si tiene extraccion de Gemini, usarla directamente
        gemini_extraction = profile.get('gemini_extraction', {})
        if gemini_extraction:
            return gemini_extraction

        # Construir formato compatible desde campos normalizados
        return {
            'hard_skills': profile.get('hard_skills', []),
            'soft_skills': profile.get('soft_skills', []),
            'education': [],
            'experience': [],
            'personal_info': {
                'languages': profile.get('languages', []),
                'summary': ''
            }
        }

    def delete_profile(self, user_id: str) -> bool:
        """
        Elimina el perfil de un usuario (y sus datos de CV).

        Args:
            user_id: ID del usuario

        Returns:
            True si se elimino correctamente
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            # Resetear a perfil vacio en lugar de eliminar
            update_data = {
                'gemini_extraction': {},
                'hard_skills': [],
                'soft_skills': [],
                'education_level': None,
                'experience_years': 0,
                'languages': [],
                'cv_filename': None,
                'cv_uploaded_at': None,
                'is_complete': False,
                'completeness_score': 0,
                'updated_at': datetime.utcnow().isoformat()
            }

            response = supabase.table("perfiles_profesionales") \
                .update(update_data) \
                .eq("usuario_id", user_id) \
                .execute()

            if response.data:
                logger.info(f"Perfil limpiado para usuario {user_id}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error eliminando perfil: {e}")
            raise


# Singleton instance
_profile_service_instance = None


def get_profile_service() -> ProfileService:
    """
    Obtiene la instancia singleton del servicio de perfiles.

    Returns:
        Instancia de ProfileService
    """
    global _profile_service_instance
    if _profile_service_instance is None:
        _profile_service_instance = ProfileService()
    return _profile_service_instance
