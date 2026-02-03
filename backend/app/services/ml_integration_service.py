"""
ML Integration Service - Fase 6
Servicio que integra el modulo ML con el backend FastAPI
"""

import os
import base64
import io
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

import pdfplumber

from app.db.client import supabase
from app.core.llm_extractor import extract_skills_with_llm
from app.scoring.feature_engineering import FeatureExtractor, extract_features
from app.ml.models import MatchPredictor, InstitutionalMatchModel

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLIntegrationService:
    """
    Servicio de integracion ML

    Singleton que maneja:
    - Carga y cache del modelo ML
    - Extraccion de CV con Gemini
    - Cache de perfiles institucionales
    - Persistencia de evaluaciones
    """

    _instance = None
    _predictor = None
    _profile_cache = {}
    _cache_timestamp = None
    _cache_ttl = timedelta(minutes=5)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa el servicio"""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._load_model()

    def _load_model(self) -> bool:
        """Carga el modelo ML"""
        try:
            # Ruta del modelo
            base_path = Path(__file__).parent.parent
            model_path = base_path / 'ml' / 'trained_models' / 'ridge_v1.joblib'

            if not model_path.exists():
                logger.warning(f"Modelo no encontrado en: {model_path}")
                return False

            self._predictor = MatchPredictor(str(model_path))
            logger.info(f"Modelo ML cargado desde: {model_path}")
            return True

        except Exception as e:
            logger.error(f"Error cargando modelo ML: {e}")
            return False

    @property
    def is_ready(self) -> bool:
        """Verifica si el servicio esta listo"""
        return self._predictor is not None and self._predictor.model is not None

    def get_model_info(self) -> Dict:
        """Retorna informacion del modelo"""
        if not self.is_ready:
            return {
                'status': 'not_loaded',
                'is_ready': False,
                'model_type': 'Ridge Regression',
                'n_features': 18,
                'model_version': 'v1'
            }

        info = self._predictor.get_model_info()
        info['is_ready'] = True
        info['model_version'] = 'v1'
        info['n_features'] = 18
        return info

    def extract_cv_from_base64(self, pdf_base64: str) -> str:
        """
        Extrae texto de un PDF en base64

        Args:
            pdf_base64: PDF codificado en base64

        Returns:
            Texto extraido del PDF

        Raises:
            ValueError: Si el PDF es invalido o no se puede leer
        """
        try:
            # Decodificar base64
            pdf_bytes = base64.b64decode(pdf_base64)

            # Extraer texto con pdfplumber
            text = ""
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            if not text.strip():
                raise ValueError("No se pudo extraer texto del PDF")

            return text

        except Exception as e:
            logger.error(f"Error extrayendo PDF: {e}")
            raise ValueError(f"PDF invalido: {str(e)}")

    def extract_cv_with_gemini(self, pdf_base64: str) -> Dict:
        """
        Extrae informacion estructurada del CV usando Gemini

        Args:
            pdf_base64: PDF codificado en base64

        Returns:
            Dict con estructura del CV

        Raises:
            ValueError: Si Gemini falla o retorna error
        """
        # Extraer texto del PDF
        text = self.extract_cv_from_base64(pdf_base64)

        # Llamar a Gemini
        logger.info("Extrayendo CV con Gemini...")
        result = extract_skills_with_llm(text)

        if 'error' in result and result['error']:
            raise ValueError(f"Error de Gemini: {result['error']}")

        # Validar estructura minima
        required_keys = ['hard_skills', 'soft_skills', 'education', 'experience']
        for key in required_keys:
            if key not in result:
                result[key] = []

        if 'personal_info' not in result:
            result['personal_info'] = {'languages': [], 'summary': ''}

        logger.info(f"CV extraido: {len(result.get('hard_skills', []))} hard skills")
        return result

    def load_institutional_profile(self, profile_id: str) -> Optional[Dict]:
        """
        Carga un perfil institucional desde Supabase

        Args:
            profile_id: ID del perfil

        Returns:
            Dict con el perfil o None si no existe
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            response = supabase.table("institutional_profiles") \
                .select("*") \
                .eq("id", profile_id) \
                .eq("is_active", True) \
                .execute()

            if not response.data:
                return None

            profile = response.data[0]

            # Convertir a formato esperado por el extractor
            return self._format_profile_for_ml(profile)

        except Exception as e:
            logger.error(f"Error cargando perfil {profile_id}: {e}")
            raise

    def load_all_active_profiles(self) -> List[Dict]:
        """
        Carga todos los perfiles institucionales activos

        Returns:
            Lista de perfiles formateados para ML
        """
        # Verificar cache
        if self._is_cache_valid():
            return list(self._profile_cache.values())

        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            response = supabase.table("institutional_profiles") \
                .select("*") \
                .eq("is_active", True) \
                .execute()

            profiles = []
            self._profile_cache = {}

            for profile in response.data:
                formatted = self._format_profile_for_ml(profile)
                profiles.append(formatted)
                self._profile_cache[profile['id']] = formatted

            self._cache_timestamp = datetime.utcnow()
            logger.info(f"Cargados {len(profiles)} perfiles institucionales")

            return profiles

        except Exception as e:
            logger.error(f"Error cargando perfiles: {e}")
            raise

    def _format_profile_for_ml(self, profile: Dict) -> Dict:
        """Formatea un perfil de BD para uso en ML"""
        weights = profile.get('weights', {})
        requirements = profile.get('requirements', {})
        thresholds = profile.get('thresholds', {'apto': 0.70, 'considerado': 0.50})

        return {
            'id': profile['id'],
            'institution_name': profile['institution_name'],
            'sector': profile['sector'],
            'description': profile.get('description', ''),
            'weights': {
                'hard_skills': weights.get('hard_skills', 0.30),
                'soft_skills': weights.get('soft_skills', 0.20),
                'experience': weights.get('experience', 0.25),
                'education': weights.get('education', 0.15),
                'languages': weights.get('languages', 0.10)
            },
            'requirements': {
                'min_experience_years': requirements.get('min_experience_years', 0),
                'required_skills': requirements.get('required_skills', []),
                'preferred_skills': requirements.get('preferred_skills', []),
                'required_education_level': requirements.get('required_education_level', 'Licenciatura'),
                'required_languages': requirements.get('required_languages', [])
            },
            'thresholds': thresholds
        }

    def _is_cache_valid(self) -> bool:
        """Verifica si el cache de perfiles es valido"""
        if not self._cache_timestamp or not self._profile_cache:
            return False
        return datetime.utcnow() - self._cache_timestamp < self._cache_ttl

    def invalidate_cache(self):
        """Invalida el cache de perfiles"""
        self._profile_cache = {}
        self._cache_timestamp = None

    def evaluate_cv(
        self,
        gemini_output: Dict,
        institutional_config: Dict
    ) -> Dict:
        """
        Evalua un CV contra un perfil institucional

        Args:
            gemini_output: Output de Gemini (CV estructurado)
            institutional_config: Configuracion institucional

        Returns:
            Dict con prediccion completa
        """
        # NOTA: Se ha cambiado a usar score heuristico directo para evitar
        # problemas de saturacion (0 o 100%) del modelo ML actual.
        # Esto garantiza granularidad en los resultados.
        
        # Extraer features
        extractor = FeatureExtractor()
        features = extractor.extract_features(gemini_output, institutional_config)

        # Calcular score heuristico (suma ponderada)
        heuristic_score = extractor.calculate_weighted_score(features)
        
        # Clasificar
        classification = extractor.classify(
            heuristic_score, 
            institutional_config.get('thresholds')
        )
        
        # Obtener scores individuales para explicacion
        cv_scores = features['cv_scores']
        
        # Generar fortalezas (scores mas altos)
        sorted_scores = sorted(cv_scores.items(), key=lambda x: x[1], reverse=True)
        top_strengths = [
            {'feature': k, 'contribution': v}
            for k, v in sorted_scores[:3]
        ]
        
        # Generar debilidades (scores mas bajos)
        bottom_scores = sorted(cv_scores.items(), key=lambda x: x[1])
        top_weaknesses = [
            {'feature': k, 'contribution': v}
            for k, v in bottom_scores[:3]
        ]

        # Formatear respuesta compatible con lo esperado
        return {
            'match_score': heuristic_score,
            'classification': classification,
            'cv_scores': cv_scores,
            'top_strengths': top_strengths,
            'top_weaknesses': top_weaknesses,
            'feature_contributions': cv_scores # Usar scores como proxy de contribuciones
        }

    def get_recommendations(
        self,
        gemini_output: Dict,
        top_n: int = 5
    ) -> List[Dict]:
        """
        Obtiene recomendaciones de instituciones para un CV

        Args:
            gemini_output: Output de Gemini
            top_n: Numero de recomendaciones

        Returns:
            Lista de recomendaciones ordenadas por score
        """
        if not self.is_ready:
            raise ValueError("Modelo ML no esta cargado")

        # Cargar todos los perfiles activos
        profiles = self.load_all_active_profiles()

        if not profiles:
            return []

        # Evaluar contra cada perfil
        recommendations = []

        for profile in profiles:
            try:
                result = self.evaluate_cv(gemini_output, profile)

                # Determinar fortaleza y debilidad principal
                strengths = result.get('top_strengths', [])
                weaknesses = result.get('top_weaknesses', [])

                main_strength = strengths[0]['feature'] if strengths else 'N/A'
                main_weakness = weaknesses[0]['feature'] if weaknesses else 'N/A'

                # Mapear nombres de features a descripciones legibles
                feature_names = {
                    'hard_skills_score': 'Habilidades tecnicas',
                    'soft_skills_score': 'Habilidades blandas',
                    'experience_score': 'Experiencia laboral',
                    'education_score': 'Formacion academica',
                    'languages_score': 'Idiomas',
                    'interaction_hard': 'Alineacion de skills',
                    'interaction_exp': 'Alineacion de experiencia',
                    'total_experience_years': 'Anos de experiencia'
                }

                recommendations.append({
                    'institution_id': profile['id'],
                    'institution_name': profile['institution_name'],
                    'sector': profile['sector'],
                    'match_score': result['match_score'],
                    'classification': result['classification'],
                    'main_strength': feature_names.get(main_strength, main_strength),
                    'main_weakness': feature_names.get(main_weakness, main_weakness),
                    'cv_scores': result['cv_scores']
                })

            except Exception as e:
                logger.warning(f"Error evaluando perfil {profile['id']}: {e}")
                continue

        # Ordenar por score descendente
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)

        # Agregar ranking
        for i, rec in enumerate(recommendations[:top_n], 1):
            rec['rank'] = i

        return recommendations[:top_n]

    def save_evaluation(
        self,
        user_id: str,
        profile_id: str,
        evaluation_result: Dict,
        gemini_extraction: Dict
    ) -> Optional[str]:
        """
        Guarda una evaluacion en la base de datos

        Args:
            user_id: ID del usuario
            profile_id: ID del perfil institucional
            evaluation_result: Resultado de la evaluacion
            gemini_extraction: Datos extraidos por Gemini

        Returns:
            ID de la evaluacion creada o None si falla
        """
        if not supabase:
            logger.warning("Base de datos no configurada, no se guarda evaluacion")
            return None

        try:
            data = {
                'user_id': user_id,
                'institutional_profile_id': profile_id,
                'match_score': evaluation_result['match_score'],
                'classification': evaluation_result['classification'],
                'cv_scores': evaluation_result['cv_scores'],
                'explanation': {
                    'top_strengths': evaluation_result.get('top_strengths', []),
                    'top_weaknesses': evaluation_result.get('top_weaknesses', [])
                },
                'gemini_extraction': gemini_extraction
            }

            response = supabase.table("cv_evaluations").insert(data).execute()

            if response.data:
                evaluation_id = response.data[0]['id']
                logger.info(f"Evaluacion guardada: {evaluation_id}")
                return evaluation_id

            return None

        except Exception as e:
            logger.error(f"Error guardando evaluacion: {e}")
            return None

    def get_user_evaluations(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        Obtiene historial de evaluaciones de un usuario

        Args:
            user_id: ID del usuario
            limit: Numero maximo de resultados

        Returns:
            Lista de evaluaciones
        """
        if not supabase:
            return []

        try:
            response = supabase.table("cv_evaluations") \
                .select("*, institutional_profiles(institution_name, sector)") \
                .eq("user_id", user_id) \
                .order("evaluated_at", desc=True) \
                .limit(limit) \
                .execute()

            return response.data or []

        except Exception as e:
            logger.error(f"Error obteniendo evaluaciones: {e}")
            return []

    def extract_cv_summary(self, gemini_output: Dict) -> Dict:
        """
        Extrae un resumen del CV procesado

        Args:
            gemini_output: Output de Gemini

        Returns:
            Dict con resumen del CV
        """
        # Calcular anos de experiencia totales
        total_years = 0
        for exp in gemini_output.get('experience', []):
            duration = exp.get('duration', '')
            # Intentar extraer anos
            import re
            years_match = re.search(r'(\d+)\s*(ano|year|anos|years)', duration.lower())
            if years_match:
                total_years += int(years_match.group(1))

        # Obtener nivel educativo mas alto
        education_order = ['Doctorado', 'Maestria', 'Ingenieria', 'Licenciatura', 'Tecnico', 'Bachillerato']
        education_level = 'No especificado'
        for edu in gemini_output.get('education', []):
            degree = edu.get('degree', '')
            for level in education_order:
                if level.lower() in degree.lower():
                    education_level = level
                    break

        return {
            'name': gemini_output.get('personal_info', {}).get('name', ''),
            'education_level': education_level,
            'total_experience_years': total_years,
            'top_skills': gemini_output.get('hard_skills', [])[:5]
        }


# Singleton instance
_ml_service_instance = None


def get_ml_service() -> MLIntegrationService:
    """
    Obtiene la instancia singleton del servicio ML

    Returns:
        Instancia de MLIntegrationService
    """
    global _ml_service_instance
    if _ml_service_instance is None:
        _ml_service_instance = MLIntegrationService()
    return _ml_service_instance
