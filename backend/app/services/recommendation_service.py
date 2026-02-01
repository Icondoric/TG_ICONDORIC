"""
Recommendation Service - Sistema de Recomendaciones v2
Servicio para generar recomendaciones basadas en perfil guardado
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.db.client import supabase
from app.services.profile_service import get_profile_service
from app.services.oferta_service import get_oferta_service
from app.services.ml_integration_service import get_ml_service
from app.scoring.feature_engineering import FeatureExtractor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RecommendationService:
    """
    Servicio para generar recomendaciones de ofertas laborales.

    Funcionalidades:
    - Generar recomendaciones basadas en perfil guardado
    - Filtrar por tipo segun rol del usuario
    - Guardar y consultar historial de recomendaciones
    - Marcar recomendaciones como vistas
    """

    _instance = None

    # Mapeo de nombres de features a descripciones legibles
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

    def get_recommendations_for_user(
        self,
        user_id: str,
        user_role: str,
        top_n: int = 10,
        tipo: str = None,
        sector: str = None,
        recalcular: bool = False
    ) -> Dict:
        """
        Genera recomendaciones para un usuario basadas en su perfil guardado.

        Args:
            user_id: ID del usuario
            user_role: Rol del usuario ('estudiante' o 'titulado')
            top_n: Numero maximo de recomendaciones
            tipo: Filtrar por tipo (opcional, si no se especifica usa el rol)
            sector: Filtrar por sector
            recalcular: Forzar recalculo de recomendaciones

        Returns:
            Dict con recomendaciones y metadata
        """
        profile_service = get_profile_service()
        oferta_service = get_oferta_service()
        ml_service = get_ml_service()

        # Verificar que el modelo ML esta listo
        if not ml_service.is_ready:
            raise ValueError("Modelo ML no disponible")

        # Obtener perfil del usuario
        profile = profile_service.get_profile(user_id)
        if not profile:
            raise ValueError("Perfil no encontrado. Sube tu CV primero.")

        # Verificar completitud del perfil
        completeness = profile_service.calculate_completeness(profile)
        if not completeness['is_complete']:
            return {
                'recomendaciones': [],
                'total': 0,
                'nuevas': 0,
                'perfil_summary': {
                    'completeness_score': completeness['score'],
                    'is_complete': False,
                    'missing_fields': completeness['missing_fields'],
                    'message': 'Completa tu perfil para recibir recomendaciones'
                }
            }

        # Determinar tipo de ofertas segun rol
        if tipo is None:
            if user_role == 'estudiante':
                tipo = 'pasantia'
            elif user_role == 'titulado':
                tipo = 'empleo'

        # Obtener ofertas activas
        ofertas_result = oferta_service.list_ofertas(
            tipo=tipo,
            is_active=True,
            sector=sector,
            include_expired=False,
            page_size=100  # Maximo de ofertas a evaluar
        )

        ofertas = ofertas_result['ofertas']

        if not ofertas:
            return {
                'recomendaciones': [],
                'total': 0,
                'nuevas': 0,
                'perfil_summary': self._get_profile_summary(profile, completeness)
            }

        # Obtener perfil en formato Gemini para ML
        gemini_output = profile_service.get_profile_for_recommendations(user_id)

        # Si no hay recalculo, intentar obtener recomendaciones existentes
        if not recalcular:
            existing = self._get_existing_recommendations(user_id, [o['id'] for o in ofertas])
            if existing and len(existing) >= min(top_n, len(ofertas)):
                return self._format_recommendations_response(
                    existing[:top_n],
                    profile,
                    completeness
                )

        # Evaluar cada oferta
        recommendations = []

        for oferta in ofertas:
            try:
                result = self._evaluate_oferta(gemini_output, oferta)

                if result:
                    recommendations.append({
                        'oferta_id': oferta['id'],
                        'oferta': oferta,
                        **result
                    })

            except Exception as e:
                logger.warning(f"Error evaluando oferta {oferta['id']}: {e}")
                continue

        # Ordenar por score descendente
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)

        # Tomar top N
        top_recommendations = recommendations[:top_n]

        # Guardar recomendaciones
        saved = self._save_recommendations(user_id, top_recommendations)

        return self._format_recommendations_response(
            saved,
            profile,
            completeness
        )

    def _evaluate_oferta(
        self,
        gemini_output: Dict,
        oferta: Dict
    ) -> Optional[Dict]:
        """
        Evalua una oferta contra el perfil del usuario.

        Args:
            gemini_output: Perfil en formato Gemini
            oferta: Datos de la oferta

        Returns:
            Dict con resultado de evaluacion o None
        """
        ml_service = get_ml_service()

        # Si la oferta tiene perfil institucional, usarlo
        if oferta.get('institutional_profile_id'):
            profile = ml_service.load_institutional_profile(
                oferta['institutional_profile_id']
            )

            if profile:
                # Merge requisitos especificos de la oferta
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
                    'fortalezas': self._extract_fortalezas(result),
                    'debilidades': self._extract_debilidades(result)
                }

        # Si no tiene perfil institucional, crear uno generico
        generic_profile = self._create_generic_profile(oferta)
        result = ml_service.evaluate_cv(gemini_output, generic_profile)

        return {
            'match_score': result['match_score'],
            'clasificacion': result['classification'],
            'scores_detalle': result['cv_scores'],
            'fortalezas': self._extract_fortalezas(result),
            'debilidades': self._extract_debilidades(result)
        }

    def _create_generic_profile(self, oferta: Dict) -> Dict:
        """Crea un perfil institucional generico para ofertas sin perfil asociado."""
        requisitos = oferta.get('requisitos_especificos', {})

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
                'required_education_level': requisitos.get('required_education_level', 'Licenciatura'),
                'required_languages': requisitos.get('required_languages', [])
            },
            'thresholds': {'apto': 0.70, 'considerado': 0.50}
        }

    def _extract_fortalezas(self, result: Dict) -> List[str]:
        """Extrae descripciones legibles de fortalezas."""
        strengths = result.get('top_strengths', [])
        return [
            self.FEATURE_NAMES.get(s['feature'], s['feature'])
            for s in strengths[:3]
        ]

    def _extract_debilidades(self, result: Dict) -> List[str]:
        """Extrae descripciones legibles de debilidades."""
        weaknesses = result.get('top_weaknesses', [])
        return [
            self.FEATURE_NAMES.get(w['feature'], w['feature'])
            for w in weaknesses[:3]
        ]

    def _save_recommendations(
        self,
        user_id: str,
        recommendations: List[Dict]
    ) -> List[Dict]:
        """
        Guarda las recomendaciones en la base de datos.

        Args:
            user_id: ID del usuario
            recommendations: Lista de recomendaciones

        Returns:
            Lista de recomendaciones guardadas con IDs
        """
        if not supabase:
            return recommendations

        saved = []

        for rec in recommendations:
            try:
                data = {
                    'usuario_id': user_id,
                    'oferta_id': rec['oferta_id'],
                    'match_score': rec['match_score'],
                    'clasificacion': rec['clasificacion'],
                    'scores_detalle': rec['scores_detalle'],
                    'fortalezas': rec['fortalezas'],
                    'debilidades': rec['debilidades'],
                    'fue_vista': False
                }

                # Upsert para evitar duplicados
                response = supabase.table("recomendaciones") \
                    .upsert(data, on_conflict="usuario_id,oferta_id") \
                    .execute()

                if response.data:
                    saved.append({
                        **rec,
                        'id': response.data[0]['id'],
                        'fue_vista': response.data[0]['fue_vista'],
                        'created_at': response.data[0]['created_at']
                    })

            except Exception as e:
                logger.warning(f"Error guardando recomendacion: {e}")
                saved.append(rec)

        return saved

    def _get_existing_recommendations(
        self,
        user_id: str,
        oferta_ids: List[str]
    ) -> List[Dict]:
        """
        Obtiene recomendaciones existentes para las ofertas dadas.

        Args:
            user_id: ID del usuario
            oferta_ids: Lista de IDs de ofertas

        Returns:
            Lista de recomendaciones existentes
        """
        if not supabase:
            return []

        try:
            response = supabase.table("recomendaciones") \
                .select("*, ofertas_laborales(*, institutional_profiles(institution_name, sector))") \
                .eq("usuario_id", user_id) \
                .in_("oferta_id", oferta_ids) \
                .order("match_score", desc=True) \
                .execute()

            if not response.data:
                return []

            # Formatear respuesta
            result = []
            for rec in response.data:
                oferta_data = rec.pop('ofertas_laborales', {}) or {}
                inst_profile = oferta_data.pop('institutional_profiles', None) or {}

                result.append({
                    'id': rec['id'],
                    'oferta_id': rec['oferta_id'],
                    'oferta': {
                        **oferta_data,
                        'institution_name': inst_profile.get('institution_name'),
                        'sector': inst_profile.get('sector')
                    },
                    'match_score': rec['match_score'],
                    'clasificacion': rec['clasificacion'],
                    'scores_detalle': rec.get('scores_detalle', {}),
                    'fortalezas': rec.get('fortalezas', []),
                    'debilidades': rec.get('debilidades', []),
                    'fue_vista': rec['fue_vista'],
                    'vista_at': rec.get('vista_at'),
                    'created_at': rec['created_at']
                })

            return result

        except Exception as e:
            logger.error(f"Error obteniendo recomendaciones existentes: {e}")
            return []

    def get_recommendation_history(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> Dict:
        """
        Obtiene el historial de recomendaciones del usuario.

        Args:
            user_id: ID del usuario
            limit: Limite de resultados
            offset: Offset para paginacion

        Returns:
            Dict con recomendaciones y metadata
        """
        if not supabase:
            return {'recomendaciones': [], 'total': 0, 'nuevas': 0}

        try:
            # Obtener recomendaciones
            response = supabase.table("recomendaciones") \
                .select("*, ofertas_laborales(*, institutional_profiles(institution_name, sector))", count="exact") \
                .eq("usuario_id", user_id) \
                .order("created_at", desc=True) \
                .range(offset, offset + limit - 1) \
                .execute()

            # Contar no vistas
            nuevas_response = supabase.table("recomendaciones") \
                .select("id", count="exact") \
                .eq("usuario_id", user_id) \
                .eq("fue_vista", False) \
                .execute()

            # Formatear
            recomendaciones = []
            for rec in response.data or []:
                oferta_data = rec.pop('ofertas_laborales', {}) or {}
                inst_profile = oferta_data.pop('institutional_profiles', None) or {}

                recomendaciones.append({
                    'id': rec['id'],
                    'oferta_id': rec['oferta_id'],
                    'oferta': {
                        **oferta_data,
                        'institution_name': inst_profile.get('institution_name'),
                        'sector': inst_profile.get('sector')
                    },
                    'match_score': rec['match_score'],
                    'clasificacion': rec['clasificacion'],
                    'scores_detalle': rec.get('scores_detalle', {}),
                    'fortalezas': rec.get('fortalezas', []),
                    'debilidades': rec.get('debilidades', []),
                    'fue_vista': rec['fue_vista'],
                    'vista_at': rec.get('vista_at'),
                    'created_at': rec['created_at']
                })

            return {
                'recomendaciones': recomendaciones,
                'total': response.count or 0,
                'nuevas': nuevas_response.count or 0
            }

        except Exception as e:
            logger.error(f"Error obteniendo historial: {e}")
            return {'recomendaciones': [], 'total': 0, 'nuevas': 0}

    def mark_as_viewed(self, user_id: str, recommendation_id: str) -> bool:
        """
        Marca una recomendacion como vista.

        Args:
            user_id: ID del usuario
            recommendation_id: ID de la recomendacion

        Returns:
            True si se actualizo correctamente
        """
        if not supabase:
            return False

        try:
            response = supabase.table("recomendaciones") \
                .update({
                    'fue_vista': True,
                    'vista_at': datetime.utcnow().isoformat()
                }) \
                .eq("id", recommendation_id) \
                .eq("usuario_id", user_id) \
                .execute()

            return bool(response.data)

        except Exception as e:
            logger.error(f"Error marcando como vista: {e}")
            return False

    def _get_profile_summary(self, profile: Dict, completeness: Dict) -> Dict:
        """Genera resumen del perfil para incluir en respuesta."""
        return {
            'completeness_score': completeness['score'],
            'is_complete': completeness['is_complete'],
            'top_skills': profile.get('hard_skills', [])[:5],
            'experience_years': profile.get('experience_years', 0),
            'education_level': profile.get('education_level'),
            'languages': profile.get('languages', [])
        }

    def _format_recommendations_response(
        self,
        recommendations: List[Dict],
        profile: Dict,
        completeness: Dict
    ) -> Dict:
        """Formatea la respuesta de recomendaciones."""
        nuevas = sum(1 for r in recommendations if not r.get('fue_vista', True))

        return {
            'recomendaciones': recommendations,
            'total': len(recommendations),
            'nuevas': nuevas,
            'perfil_summary': self._get_profile_summary(profile, completeness)
        }


# Singleton instance
_recommendation_service_instance = None


def get_recommendation_service() -> RecommendationService:
    """
    Obtiene la instancia singleton del servicio de recomendaciones.

    Returns:
        Instancia de RecommendationService
    """
    global _recommendation_service_instance
    if _recommendation_service_instance is None:
        _recommendation_service_instance = RecommendationService()
    return _recommendation_service_instance
