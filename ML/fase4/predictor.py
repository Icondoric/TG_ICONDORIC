"""
Predictor
Interfaz de alto nivel para predicción con explicabilidad
"""

import numpy as np
from typing import Dict, List
from pathlib import Path

from .ridge_model import InstitutionalMatchModel


class MatchPredictor:
    """
    Predictor de matching con explicabilidad
    
    Carga modelo entrenado y provee interfaz simple para predicción
    """
    
    def __init__(self, model_path: str = None):
        """
        Args:
            model_path: Ruta del modelo entrenado (.joblib)
        """
        if model_path is None:
            # Ruta por defecto
            current_dir = Path(__file__).parent.parent
            model_path = current_dir / 'trained_models' / 'ridge_v1.joblib'
        
        self.model_path = Path(model_path)
        self.model = None
        
        # Cargar modelo si existe
        if self.model_path.exists():
            self.load_model()
    
    def load_model(self):
        """Carga el modelo desde disco"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {self.model_path}")
        
        self.model = InstitutionalMatchModel.load(str(self.model_path))
        print(f"✅ Modelo cargado desde: {self.model_path}")
    
    def predict_from_features(self, features: Dict) -> Dict:
        """
        Predice desde un dict de features extraídos
        
        Este método espera que ya tengas el output de feature_extractor.extract_features()
        
        Args:
            features: Dict con 'feature_vector' y 'cv_scores'
        
        Returns:
            Dict con predicción y explicación
        
        Example:
            >>> from app.ml.feature_engineering import extract_features
            >>> features = extract_features(gemini_output, institutional_config)
            >>> result = predictor.predict_from_features(features)
            >>> result['match_score']
            0.78
        """
        if self.model is None:
            raise ValueError("Modelo no cargado. Llamar load_model() primero.")
        
        # Extraer feature vector
        feature_vector = np.array(features['feature_vector'])
        
        # Predecir con explicación
        prediction = self.model.predict_single(feature_vector)
        
        # Añadir información adicional de los CV scores
        prediction['cv_scores'] = features.get('cv_scores', {})
        prediction['institutional_params'] = features.get('institutional_params', {})
        
        return prediction
    
    def predict_from_cv_and_config(
        self,
        gemini_output: Dict,
        institutional_config: Dict
    ) -> Dict:
        """
        Predice desde CV procesado y configuración institucional
        
        Args:
            gemini_output: Output de Gemini (CV estructurado)
            institutional_config: Configuración de la institución
        
        Returns:
            Dict con predicción completa y explicación
        
        Example:
            >>> result = predictor.predict_from_cv_and_config(
            ...     gemini_output={"hard_skills": ["Python"], ...},
            ...     institutional_config={"weights": {...}, ...}
            ... )
            >>> result['match_score']
            0.78
        """
        # Importar aquí para evitar dependencias circulares
        from app.ml.feature_engineering import extract_features
        
        # Extraer features
        features = extract_features(gemini_output, institutional_config)
        
        # Predecir
        prediction = self.predict_from_features(features)
        
        # Añadir metadata
        prediction['metadata'] = features.get('metadata', {})
        
        return prediction
    
    def batch_predict(
        self,
        feature_vectors: List[np.ndarray]
    ) -> List[Dict]:
        """
        Predice para múltiples ejemplos
        
        Args:
            feature_vectors: Lista de vectores de features
        
        Returns:
            Lista de predicciones
        """
        if self.model is None:
            raise ValueError("Modelo no cargado.")
        
        predictions = []
        for feature_vector in feature_vectors:
            pred = self.model.predict_single(feature_vector)
            predictions.append(pred)
        
        return predictions
    
    def explain_prediction(self, prediction: Dict) -> str:
        """
        Genera explicación legible de una predicción
        
        Args:
            prediction: Dict de predicción
        
        Returns:
            String con explicación
        """
        explanation = "\n" + "="*60 + "\n"
        explanation += "EXPLICACIÓN DE LA PREDICCIÓN\n"
        explanation += "="*60 + "\n"
        
        # Score y clasificación
        score = prediction['match_score']
        classification = prediction['classification']
        
        explanation += f"\n📊 Resultado:\n"
        explanation += f"   Match Score: {score:.3f} ({score*100:.1f}%)\n"
        explanation += f"   Clasificación: {classification}\n"
        
        # Interpretación
        if classification == 'APTO':
            interpretation = "✅ Alta correspondencia entre perfil y requisitos"
        elif classification == 'CONSIDERADO':
            interpretation = "⚠️ Correspondencia media, revisar detalles"
        else:
            interpretation = "❌ Baja correspondencia, perfil no se ajusta"
        
        explanation += f"   Interpretación: {interpretation}\n"
        
        # Fortalezas
        if 'top_strengths' in prediction:
            explanation += f"\n💪 Principales Fortalezas:\n"
            for i, (feature, contribution) in enumerate(prediction['top_strengths'], 1):
                explanation += f"   {i}. {feature}: +{contribution:.4f}\n"
        
        # Debilidades
        if 'top_weaknesses' in prediction:
            explanation += f"\n⚠️ Áreas de Mejora:\n"
            for i, (feature, contribution) in enumerate(prediction['top_weaknesses'], 1):
                explanation += f"   {i}. {feature}: {contribution:.4f}\n"
        
        # CV Scores
        if 'cv_scores' in prediction:
            explanation += f"\n📋 Evaluación por Dimensión:\n"
            scores = prediction['cv_scores']
            for dim, score_val in scores.items():
                bar = '█' * int(score_val * 20)
                explanation += f"   {dim:25s}: {score_val:.2f} {bar}\n"
        
        explanation += "\n" + "="*60 + "\n"
        
        return explanation
    
    def get_recommendations(
        self,
        cv_profile: Dict,
        institutional_configs: List[Dict],
        top_n: int = 5
    ) -> List[Dict]:
        """
        Genera recomendaciones ordenadas por score
        
        Evalúa el CV contra múltiples instituciones y retorna ranking
        
        Args:
            cv_profile: Perfil del candidato (output de Gemini)
            institutional_configs: Lista de configuraciones institucionales
            top_n: Número de recomendaciones a retornar
        
        Returns:
            Lista de predicciones ordenadas por score
        
        Example:
            >>> recommendations = predictor.get_recommendations(
            ...     cv_profile=gemini_output,
            ...     institutional_configs=[config1, config2, config3]
            ... )
            >>> print(f"Mejor match: {recommendations[0]['institution_name']}")
        """
        predictions = []
        
        for config in institutional_configs:
            try:
                # Predecir para esta institución
                pred = self.predict_from_cv_and_config(cv_profile, config)
                
                # Añadir información de la institución
                pred['institution_id'] = config.get('id', 'unknown')
                pred['institution_name'] = config.get('institution_name', 'Unknown')
                pred['sector'] = config.get('sector', 'N/A')
                
                predictions.append(pred)
            
            except Exception as e:
                print(f"⚠️ Error procesando {config.get('institution_name', 'unknown')}: {e}")
                continue
        
        # Ordenar por score (mayor a menor)
        predictions.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Retornar top N
        return predictions[:top_n]
    
    def get_model_info(self) -> Dict:
        """
        Retorna información del modelo cargado
        
        Returns:
            Dict con metadata del modelo
        """
        if self.model is None:
            return {'status': 'not_loaded'}
        
        return {
            'status': 'loaded',
            'model_type': 'Ridge Regression',
            'alpha': self.model.alpha,
            'normalize': self.model.normalize,
            'is_trained': self.model.is_trained,
            'training_metrics': self.model.training_metrics,
            'feature_count': len(self.model.feature_names) if self.model.feature_names else None,
            'intercept': self.model.get_intercept()
        }


# === EJEMPLO DE USO ===

if __name__ == "__main__":
    # Ejemplo de uso del predictor
    
    # 1. Crear predictor
    predictor = MatchPredictor()
    
    # 2. Ejemplo de CV (simplificado)
    gemini_output_example = {
        "hard_skills": ["Python", "React", "SQL"],
        "soft_skills": ["Liderazgo", "Trabajo en equipo"],
        "education": [{"degree": "Ingeniería de Sistemas", "institution": "EMI"}],
        "experience": [{"role": "Developer", "duration": "2 años"}],
        "personal_info": {"languages": ["Español (Nativo)", "Inglés (B2)"]}
    }
    
    # 3. Configuración institucional de ejemplo
    institutional_config_example = {
        "weights": {
            "hard_skills": 0.45,
            "soft_skills": 0.15,
            "experience": 0.20,
            "education": 0.10,
            "languages": 0.10
        },
        "requirements": {
            "min_experience_years": 1.0,
            "required_skills": ["Python", "SQL"],
            "preferred_skills": ["React"],
            "required_education_level": "Licenciatura",
            "required_languages": ["Inglés"]
        }
    }
    
    # 4. Predecir
    try:
        prediction = predictor.predict_from_cv_and_config(
            gemini_output_example,
            institutional_config_example
        )
        
        # 5. Mostrar explicación
        print(predictor.explain_prediction(prediction))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Asegúrate de que el modelo esté entrenado y guardado")
