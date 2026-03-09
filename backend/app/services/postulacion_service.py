"""
Postulacion Service - Correspondencia entre Perfiles
Servicio para gestionar postulaciones explícitas de usuarios a ofertas laborales.

Diferencia con recomendaciones:
- Recomendaciones: el sistema evalúa automáticamente todas las ofertas.
- Postulaciones: el usuario elige una oferta específica y se postula.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from app.db.client import supabase
from app.services.profile_service import get_profile_service
from app.services.oferta_service import get_oferta_service
from app.services.ml_integration_service import get_ml_service

logger = logging.getLogger(__name__)


class PostulacionService:
    """
    Servicio para gestionar postulaciones a ofertas laborales.

    Funcionalidades:
    - Postular usuario a oferta (evalúa CV con ML y almacena resultado)
    - Listar postulaciones del usuario
    - Listar ofertas disponibles para el usuario según su rol
    - Respeta configuración propia de la oferta (weights/thresholds/requirements de v3)
    """

    _instance = None

    FEATURE_NAMES = {
        'hard_skills_score': 'Habilidades tecnicas',
        'soft_skills_score': 'Habilidades blandas',
        'experience_score': 'Experiencia laboral',
        'education_score': 'Formacion academica',
        'languages_score': 'Idiomas',
        'interaction_hard': 'Alineacion de skills',
        'interaction_exp': 'Alineacion de experiencia',
        'total_experience_years': 'Anos de experiencia'
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def postular(self, user_id: str, user_role: str, oferta_id: str) -> Dict:
        """
        Registra la postulación de un usuario a una oferta.

        Evalúa el CV del usuario contra la oferta usando ML y almacena
        el resultado en la tabla postulaciones.

        Args:
            user_id: ID del usuario
            user_role: Rol del usuario ('estudiante' o 'titulado')
            oferta_id: ID de la oferta

        Returns:
            Dict con resultado de evaluación y datos de la postulación
        """
        profile_service = get_profile_service()
        oferta_service = get_oferta_service()
        ml_service = get_ml_service()

        if not ml_service.is_ready:
            raise ValueError("Modelo ML no disponible")

        # Obtener perfil del usuario
        profile = profile_service.get_profile(user_id)
        if not profile:
            raise ValueError("Debes subir tu CV primero para postular")

        completeness = profile_service.calculate_completeness(profile)
        if not completeness['is_complete']:
            raise ValueError(
                f"Tu perfil no está completo ({int(completeness['score'] * 100)}%). "
                "Necesitas al menos 70% para postular."
            )

        # Obtener oferta
        oferta = oferta_service.get_oferta(oferta_id)
        if not oferta:
            raise ValueError("Oferta no encontrada")

        if not oferta.get('is_active'):
            raise ValueError("Esta oferta ya no está disponible")

        # Validar compatibilidad de rol con tipo de oferta
        oferta_tipo = oferta.get('tipo', '')
        if user_role == 'estudiante' and oferta_tipo != 'pasantia':
            raise ValueError("Los estudiantes solo pueden postular a pasantías")
        if user_role == 'titulado' and oferta_tipo != 'empleo':
            raise ValueError("Los titulados solo pueden postular a empleos")

        # Obtener datos del perfil para ML
        gemini_output = profile_service.get_profile_for_recommendations(user_id)
        if not gemini_output:
            raise ValueError("No se pudo obtener los datos del perfil para evaluación")

        # Evaluar CV contra la oferta
        eval_result = self._evaluate_oferta(gemini_output, oferta)

        # Guardar postulación
        saved = self._save_postulacion(user_id, oferta_id, eval_result)

        return {
            **saved,
            'oferta': oferta
        }

    def _evaluate_oferta(self, gemini_output: Dict, oferta: Dict) -> Dict:
        """
        Evalúa un CV contra una oferta.

        Prioridad de configuración:
        1. Config propia de la oferta (weights/thresholds/requirements de v3)
        2. Config del perfil institucional asociado
        3. Config genérica por defecto

        Args:
            gemini_output: Perfil extraído del CV
            oferta: Datos de la oferta

        Returns:
            Dict con resultado de evaluación
        """
        ml_service = get_ml_service()

        # Cargar perfil institucional como base
        if oferta.get('institutional_profile_id'):
            profile = ml_service.load_institutional_profile(
                oferta['institutional_profile_id']
            )
            if not profile:
                profile = self._create_generic_profile(oferta)
        else:
            profile = self._create_generic_profile(oferta)

        # Override con config propia de la oferta (migration v3)
        # Nivel educativo mínimo, pesos y umbrales vienen ahora de la oferta
        if oferta.get('weights'):
            profile['weights'] = oferta['weights']
        if oferta.get('thresholds'):
            profile['thresholds'] = oferta['thresholds']
        if oferta.get('requirements'):
            profile['requirements'] = {
                **profile['requirements'],
                **oferta['requirements']
            }

        # Merge requisitos_especificos (campos adicionales de la oferta)
        if oferta.get('requisitos_especificos'):
            profile['requirements'] = {
                **profile['requirements'],
                **oferta['requisitos_especificos']
            }

        result = ml_service.evaluate_cv(gemini_output, profile)

        return {
            'match_score': result['match_score'],
            'clasificacion': result['classification'],
            'scores_detalle': result['cv_scores'],
            'fortalezas': [
                self.FEATURE_NAMES.get(s['feature'], s['feature'])
                for s in result.get('top_strengths', [])[:3]
            ],
            'debilidades': [
                self.FEATURE_NAMES.get(w['feature'], w['feature'])
                for w in result.get('top_weaknesses', [])[:3]
            ],
            'match_details': result.get('match_details')
        }

    def _create_generic_profile(self, oferta: Dict) -> Dict:
        """Crea un perfil genérico para ofertas sin perfil institucional."""
        requisitos = oferta.get('requisitos_especificos', {}) or {}
        return {
            'id': 'generic',
            'institution_name': oferta.get('institution_name', 'Empresa'),
            'sector': oferta.get('sector', 'General'),
            'weights': {
                'hard_skills': 0.30,
                'soft_skills': 0.20,
                'experience': 0.25,
                'education': 0.15,
                'languages': 0.10
            },
            'requirements': {
                'min_experience_years': requisitos.get('min_experience_years', 0),
                'required_skills': requisitos.get('required_skills', []),
                'preferred_skills': requisitos.get('preferred_skills', []),
                'required_soft_skills': requisitos.get('required_soft_skills', []),
                'required_education_level': requisitos.get('required_education_level', 'Licenciatura'),
                'required_languages': requisitos.get('required_languages', [])
            },
            'thresholds': {'apto': 0.70, 'considerado': 0.50}
        }

    def _save_postulacion(self, user_id: str, oferta_id: str, eval_result: Dict) -> Dict:
        """
        Guarda la postulación en la base de datos.
        Usa upsert para evitar duplicados (un usuario puede re-postular
        y actualizar su evaluación si su CV cambió).

        Returns:
            Dict con resultado más id y metadata de BD
        """
        if not supabase:
            return eval_result

        try:
            data = {
                'usuario_id': user_id,
                'oferta_id': oferta_id,
                'match_score': eval_result['match_score'],
                'clasificacion': eval_result['clasificacion'],
                'scores_detalle': eval_result['scores_detalle'],
                'fortalezas': eval_result['fortalezas'],
                'debilidades': eval_result['debilidades'],
                'match_details': eval_result.get('match_details'),
                'estado': 'pendiente',
                'updated_at': datetime.utcnow().isoformat()
            }

            response = supabase.table("postulaciones") \
                .upsert(data, on_conflict="usuario_id,oferta_id") \
                .execute()

            if response.data:
                row = response.data[0]
                return {
                    **eval_result,
                    'id': row['id'],
                    'estado': row['estado'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }

            return eval_result

        except Exception as e:
            logger.error(f"Error guardando postulacion {oferta_id}: {e}")
            return eval_result

    def get_my_postulaciones(self, user_id: str) -> List[Dict]:
        """
        Obtiene todas las postulaciones del usuario con datos de la oferta.

        Args:
            user_id: ID del usuario

        Returns:
            Lista de postulaciones con oferta enriquecida
        """
        if not supabase:
            return []

        try:
            response = supabase.table("postulaciones") \
                .select(
                    "*, convocatorias_laborales(*, institutional_profiles(institution_name, sector))"
                ) \
                .eq("usuario_id", user_id) \
                .order("created_at", desc=True) \
                .execute()

            result = []
            for p in response.data or []:
                oferta_data = p.pop('convocatorias_laborales', {}) or {}
                inst_profile = oferta_data.pop('institutional_profiles', None) or {}
                result.append({
                    **p,
                    'oferta': {
                        **oferta_data,
                        'institution_name': inst_profile.get('institution_name'),
                        'sector': inst_profile.get('sector')
                    }
                })

            return result

        except Exception as e:
            logger.error(f"Error obteniendo postulaciones de usuario {user_id}: {e}")
            return []

    def get_ofertas_disponibles(self, user_role: str) -> List[Dict]:
        """
        Lista ofertas activas disponibles para el usuario según su rol.
        - Estudiante: solo pasantías
        - Titulado: solo empleos
        - Admin/Operador: todas

        Args:
            user_role: Rol del usuario

        Returns:
            Lista de ofertas activas
        """
        oferta_service = get_oferta_service()

        if user_role == 'estudiante':
            tipo = 'pasantia'
        elif user_role == 'titulado':
            tipo = 'empleo'
        else:
            tipo = None  # Admin ve todo

        result = oferta_service.list_ofertas(
            tipo=tipo,
            is_active=True,
            include_expired=False,
            page_size=100
        )

        return result['ofertas']


# Singleton instance
_postulacion_service_instance = None


def get_postulacion_service() -> PostulacionService:
    """Obtiene la instancia singleton del servicio de postulaciones."""
    global _postulacion_service_instance
    if _postulacion_service_instance is None:
        _postulacion_service_instance = PostulacionService()
    return _postulacion_service_instance
