"""
ML Service - Servicio de Machine Learning Integrado
====================================================

Archivo recopilatorio que integra todas las fases del sistema ML:
- Fase 1: Feature Engineering (scorers individuales)
- Fase 2: Extraccion de Features (feature extractor)
- Fase 3: Dataset Sintetico (generador)
- Fase 4: Modelo Ridge (entrenamiento y prediccion)

Este modulo provee una interfaz unificada para:
1. Extraer features de un CV procesado por Gemini
2. Predecir el match score con una configuracion institucional
3. Obtener explicaciones detalladas de las predicciones
4. Generar recomendaciones para multiples instituciones

Uso basico:
    >>> from app.ml_service import MLService
    >>> service = MLService()
    >>> result = service.predict(gemini_output, institutional_config)
    >>> print(result['match_score'])
    0.78

Autor: Sistema ATG
Fecha: Enero 2025
"""

from typing import Dict, List, Optional
from pathlib import Path

# Importar componentes de Feature Engineering (Fase 1-2)
from app.scoring.feature_engineering import (
    FeatureExtractor,
    extract_features,
    get_feature_names,
    validate_gemini_output,
    calculate_final_score,
    classify_candidate
)

# Importar componentes de ML (Fase 3-4)
from app.ml import (
    InstitutionalMatchModel,
    ModelTrainer,
    MatchPredictor,
    SyntheticDatasetGenerator,
    InstitutionalConfigLoader
)


class MLService:
    """
    Servicio principal de Machine Learning

    Integra todas las fases del sistema ML en una interfaz unificada.
    Maneja la carga del modelo, extraccion de features y prediccion.
    """

    def __init__(self, model_path: str = None):
        """
        Inicializa el servicio ML

        Args:
            model_path: Ruta al modelo entrenado (.joblib)
                       Si no se especifica, usa la ruta por defecto
        """
        # Configurar ruta del modelo
        if model_path is None:
            base_dir = Path(__file__).parent / 'ml' / 'trained_models'
            model_path = base_dir / 'ridge_v1.joblib'

        self.model_path = Path(model_path)

        # Inicializar componentes
        self.feature_extractor = FeatureExtractor()
        self.predictor = None

        # Cargar modelo si existe
        if self.model_path.exists():
            self._load_model()

    def _load_model(self):
        """Carga el modelo desde disco"""
        try:
            self.predictor = MatchPredictor(str(self.model_path))
            print(f"MLService: Modelo cargado desde {self.model_path}")
        except Exception as e:
            print(f"MLService: Error cargando modelo: {e}")
            self.predictor = None

    def is_ready(self) -> bool:
        """
        Verifica si el servicio esta listo para predicciones

        Returns:
            True si el modelo esta cargado y listo
        """
        return self.predictor is not None and self.predictor.model is not None

    def predict(
        self,
        gemini_output: Dict,
        institutional_config: Dict
    ) -> Dict:
        """
        Realiza una prediccion completa de match score

        Args:
            gemini_output: CV procesado por Gemini (estructura JSON)
            institutional_config: Configuracion de la institucion

        Returns:
            Dict con:
                - match_score: Score de matching [0-1]
                - classification: APTO, CONSIDERADO o NO_APTO
                - cv_scores: Scores individuales por dimension
                - feature_contributions: Contribucion de cada feature
                - top_strengths: Top 3 fortalezas
                - top_weaknesses: Top 3 debilidades
                - explanation: Explicacion legible (opcional)

        Raises:
            ValueError: Si el modelo no esta cargado
            ValueError: Si el input es invalido

        Example:
            >>> service = MLService()
            >>> result = service.predict(gemini_output, config)
            >>> print(f"Score: {result['match_score']:.2f}")
            Score: 0.78
        """
        if not self.is_ready():
            raise ValueError("Modelo no cargado. Entrena el modelo primero.")

        # Validar input
        if not validate_gemini_output(gemini_output):
            raise ValueError("Output de Gemini invalido. Faltan campos requeridos.")

        # Extraer features
        features = self.feature_extractor.extract_features(
            gemini_output,
            institutional_config
        )

        # Predecir
        prediction = self.predictor.predict_from_features(features)

        return prediction

    def predict_with_explanation(
        self,
        gemini_output: Dict,
        institutional_config: Dict
    ) -> Dict:
        """
        Realiza prediccion con explicacion detallada incluida

        Args:
            gemini_output: CV procesado por Gemini
            institutional_config: Configuracion institucional

        Returns:
            Dict con prediccion y campo 'explanation' con texto legible
        """
        prediction = self.predict(gemini_output, institutional_config)
        prediction['explanation'] = self.predictor.explain_prediction(prediction)
        return prediction

    def get_recommendations(
        self,
        gemini_output: Dict,
        institutional_configs: List[Dict],
        top_n: int = 5
    ) -> List[Dict]:
        """
        Genera recomendaciones ordenadas para multiples instituciones

        Args:
            gemini_output: CV procesado por Gemini
            institutional_configs: Lista de configuraciones institucionales
            top_n: Numero de recomendaciones a retornar

        Returns:
            Lista de predicciones ordenadas por score (mayor a menor)

        Example:
            >>> configs = [config1, config2, config3]
            >>> recs = service.get_recommendations(cv, configs, top_n=3)
            >>> print(f"Mejor match: {recs[0]['institution_name']}")
        """
        if not self.is_ready():
            raise ValueError("Modelo no cargado.")

        return self.predictor.get_recommendations(
            gemini_output,
            institutional_configs,
            top_n
        )

    def extract_features_only(
        self,
        gemini_output: Dict,
        institutional_config: Dict
    ) -> Dict:
        """
        Extrae features sin realizar prediccion

        Util para debugging o para usar con otros modelos

        Args:
            gemini_output: CV procesado por Gemini
            institutional_config: Configuracion institucional

        Returns:
            Dict con feature_vector, cv_scores, institutional_params
        """
        return self.feature_extractor.extract_features(
            gemini_output,
            institutional_config
        )

    def calculate_simple_score(
        self,
        gemini_output: Dict,
        institutional_config: Dict
    ) -> float:
        """
        Calcula score ponderado simple (sin ML)

        Usa solo los pesos institucionales sin el modelo Ridge.
        Util como baseline o cuando el modelo no esta disponible.

        Args:
            gemini_output: CV procesado por Gemini
            institutional_config: Configuracion institucional

        Returns:
            Score ponderado [0-1]
        """
        features = self.feature_extractor.extract_features(
            gemini_output,
            institutional_config
        )
        return calculate_final_score(features)

    def get_model_info(self) -> Dict:
        """
        Retorna informacion del modelo cargado

        Returns:
            Dict con metadata del modelo o estado
        """
        if not self.is_ready():
            return {
                'status': 'not_loaded',
                'model_path': str(self.model_path),
                'exists': self.model_path.exists()
            }

        info = self.predictor.get_model_info()
        info['model_path'] = str(self.model_path)
        return info

    def get_feature_names(self) -> List[str]:
        """
        Retorna nombres de los features del modelo

        Returns:
            Lista de 18 nombres de features
        """
        return get_feature_names()


# === FUNCIONES DE UTILIDAD ===

def create_ml_service(model_path: str = None) -> MLService:
    """
    Funcion factory para crear el servicio ML

    Args:
        model_path: Ruta opcional al modelo

    Returns:
        Instancia de MLService
    """
    return MLService(model_path)


def quick_predict(
    gemini_output: Dict,
    institutional_config: Dict,
    model_path: str = None
) -> Dict:
    """
    Funcion de conveniencia para prediccion rapida

    Crea el servicio, predice y retorna resultado en una sola llamada.

    Args:
        gemini_output: CV procesado por Gemini
        institutional_config: Configuracion institucional
        model_path: Ruta opcional al modelo

    Returns:
        Dict con prediccion

    Example:
        >>> result = quick_predict(cv_data, config)
        >>> print(result['match_score'])
    """
    service = MLService(model_path)
    return service.predict(gemini_output, institutional_config)


# === INFORMACION DEL MODULO ===

__version__ = "1.0.0"
__author__ = "Sistema ATG"
__description__ = "Servicio ML integrado para matching de CVs"

__all__ = [
    # Clase principal
    "MLService",
    # Funciones de utilidad
    "create_ml_service",
    "quick_predict",
    # Re-exportar componentes clave
    "FeatureExtractor",
    "MatchPredictor",
    "InstitutionalMatchModel",
    "ModelTrainer",
    "SyntheticDatasetGenerator",
    # Funciones de feature engineering
    "extract_features",
    "get_feature_names",
    "validate_gemini_output",
    "calculate_final_score",
    "classify_candidate",
]


# === EJEMPLO DE USO ===

if __name__ == "__main__":
    # Ejemplo de uso del servicio

    print("="*70)
    print("ML SERVICE - EJEMPLO DE USO")
    print("="*70)

    # 1. Crear servicio
    service = MLService()

    # 2. Verificar estado
    print(f"\nServicio listo: {service.is_ready()}")

    if service.is_ready():
        # 3. Mostrar info del modelo
        info = service.get_model_info()
        print(f"\nInformacion del modelo:")
        for key, value in info.items():
            print(f"   {key}: {value}")

        # 4. Mostrar nombres de features
        print(f"\nFeatures del modelo ({len(service.get_feature_names())}):")
        for i, name in enumerate(service.get_feature_names(), 1):
            print(f"   {i:2d}. {name}")

        # 5. Ejemplo de prediccion (requiere datos reales)
        print("\n" + "="*70)
        print("Para predicciones, usa:")
        print("   result = service.predict(gemini_output, institutional_config)")
        print("="*70)

    else:
        print("\nModelo no cargado. Ejecuta el script de entrenamiento:")
        print("   python -m app.ml.scripts.train_model")
