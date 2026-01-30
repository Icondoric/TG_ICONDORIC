"""
Ridge Regression Model
Modelo de regresión lineal con regularización L2
"""

from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
from typing import Dict, Optional
from pathlib import Path


class InstitutionalMatchModel:
    """
    Modelo de matching entre perfiles y configuraciones institucionales
    
    Usa Ridge Regression (regresión lineal con regularización L2) para:
    1. Aprender pesos relativos entre dimensiones del CV
    2. Capturar interacciones entre scores y parámetros institucionales
    3. Generalizar a múltiples instituciones sin reentrenamiento
    
    El modelo NO se reentrena cuando cambian configuraciones institucionales,
    ya que estas son features de entrada, no parámetros del modelo.
    """
    
    def __init__(self, alpha: float = 1.0, normalize: bool = True):
        """
        Args:
            alpha: Parámetro de regularización L2 (mayor = más regularización)
                   - alpha pequeño (0.01-0.1): Más flexible, riesgo de sobreajuste
                   - alpha medio (1.0-10.0): Balance (RECOMENDADO)
                   - alpha grande (100+): Más regularizado, menos flexible
            normalize: Si True, estandariza features antes de entrenar
        """
        self.alpha = alpha
        self.normalize = normalize
        
        # Modelo Ridge
        self.model = Ridge(
            alpha=alpha,
            fit_intercept=True,
            solver='auto',
            random_state=42
        )
        
        # Scaler (opcional)
        self.scaler = StandardScaler() if normalize else None
        
        # Metadata
        self.is_trained = False
        self.feature_names = None
        self.training_metrics = {}
    
    def fit(self, X: np.ndarray, y: np.ndarray, feature_names: list = None):
        """
        Entrena el modelo
        
        Args:
            X: Features (n_samples, n_features)
            y: Target (n_samples,)
            feature_names: Nombres de features (opcional)
        
        Returns:
            self
        """
        # Guardar nombres de features
        if feature_names is not None:
            self.feature_names = feature_names
        
        # Normalizar features si está habilitado
        if self.normalize:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = X
        
        # Entrenar modelo
        self.model.fit(X_scaled, y)
        
        # Marcar como entrenado
        self.is_trained = True
        
        # Calcular métricas de entrenamiento
        y_pred_train = self.predict(X)
        self.training_metrics = self._calculate_metrics(y, y_pred_train)
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predice scores de matching
        
        Args:
            X: Features (n_samples, n_features)
        
        Returns:
            Array de scores predichos [0-1]
        """
        if not self.is_trained:
            raise ValueError("Modelo no ha sido entrenado. Llamar fit() primero.")
        
        # Normalizar si es necesario
        if self.normalize:
            X_scaled = self.scaler.transform(X)
        else:
            X_scaled = X
        
        # Predecir
        y_pred = self.model.predict(X_scaled)
        
        # Clipear a [0, 1]
        y_pred = np.clip(y_pred, 0, 1)
        
        return y_pred
    
    def predict_single(self, feature_vector: np.ndarray) -> Dict:
        """
        Predice para un ÚNICO ejemplo con explicación detallada
        
        Args:
            feature_vector: Vector de features (18 dimensiones)
        
        Returns:
            Dict con score, clasificación y explicación
        """
        if not self.is_trained:
            raise ValueError("Modelo no ha sido entrenado.")
        
        # Asegurar shape correcto
        if feature_vector.ndim == 1:
            feature_vector = feature_vector.reshape(1, -1)
        
        # Predecir
        score = self.predict(feature_vector)[0]
        
        # Clasificar
        classification = self._classify_score(score)
        
        # Calcular contribuciones de features
        contributions = self._calculate_feature_contributions(feature_vector[0])
        
        return {
            'match_score': float(score),
            'classification': classification,
            'feature_contributions': contributions,
            'top_strengths': self._get_top_features(contributions, top=3, positive=True),
            'top_weaknesses': self._get_top_features(contributions, top=3, positive=False)
        }
    
    def get_coefficients(self) -> Dict[str, float]:
        """
        Retorna coeficientes del modelo (pesos aprendidos)
        
        Returns:
            Dict {feature_name: coefficient}
        """
        if not self.is_trained:
            raise ValueError("Modelo no ha sido entrenado.")
        
        if self.feature_names is None:
            feature_names = [f"feature_{i}" for i in range(len(self.model.coef_))]
        else:
            feature_names = self.feature_names
        
        return dict(zip(feature_names, self.model.coef_))
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Calcula importancia de features (coeficientes absolutos normalizados)
        
        Returns:
            Dict {feature_name: importance} ordenado por importancia
        """
        coefficients = self.get_coefficients()
        
        # Importancia = valor absoluto del coeficiente
        importance = {name: abs(coef) for name, coef in coefficients.items()}
        
        # Normalizar a [0, 1]
        total = sum(importance.values())
        if total > 0:
            importance = {name: imp/total for name, imp in importance.items()}
        
        # Ordenar por importancia
        importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
        
        return importance
    
    def get_intercept(self) -> float:
        """Retorna el intercepto (sesgo) del modelo"""
        if not self.is_trained:
            raise ValueError("Modelo no ha sido entrenado.")
        return float(self.model.intercept_)
    
    def _classify_score(self, score: float) -> str:
        """Clasifica un score en categorías"""
        if score >= 0.70:
            return 'APTO'
        elif score >= 0.50:
            return 'CONSIDERADO'
        else:
            return 'NO_APTO'
    
    def _calculate_feature_contributions(self, feature_vector: np.ndarray) -> Dict[str, float]:
        """
        Calcula contribución de cada feature al score final
        
        Contribución = coeficiente × valor_feature
        
        Args:
            feature_vector: Vector de features (1D)
        
        Returns:
            Dict {feature_name: contribution}
        """
        coefficients = self.get_coefficients()
        
        contributions = {}
        for i, (name, coef) in enumerate(coefficients.items()):
            contributions[name] = float(coef * feature_vector[i])
        
        return contributions
    
    def _get_top_features(self, contributions: Dict, top: int = 3, positive: bool = True) -> list:
        """
        Obtiene las top N features con mayor/menor contribución
        
        Args:
            contributions: Dict de contribuciones
            top: Número de features a retornar
            positive: Si True, retorna mayores; si False, retorna menores
        
        Returns:
            Lista de tuplas (feature_name, contribution)
        """
        sorted_contribs = sorted(contributions.items(), key=lambda x: x[1], reverse=positive)
        return sorted_contribs[:top]
    
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calcula métricas de evaluación
        
        Args:
            y_true: Valores reales
            y_pred: Valores predichos
        
        Returns:
            Dict con métricas
        """
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        
        return {
            'r2_score': r2_score(y_true, y_pred),
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mae': mean_absolute_error(y_true, y_pred)
        }
    
    def save(self, filepath: str):
        """
        Guarda el modelo entrenado
        
        Args:
            filepath: Ruta donde guardar el modelo
        """
        if not self.is_trained:
            raise ValueError("No se puede guardar un modelo sin entrenar.")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'alpha': self.alpha,
            'normalize': self.normalize,
            'feature_names': self.feature_names,
            'training_metrics': self.training_metrics,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        print(f"✅ Modelo guardado en: {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'InstitutionalMatchModel':
        """
        Carga un modelo guardado
        
        Args:
            filepath: Ruta del modelo guardado
        
        Returns:
            Instancia de InstitutionalMatchModel
        """
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Modelo no encontrado: {filepath}")
        
        model_data = joblib.load(filepath)
        
        # Crear instancia
        instance = cls(
            alpha=model_data['alpha'],
            normalize=model_data['normalize']
        )
        
        # Restaurar estado
        instance.model = model_data['model']
        instance.scaler = model_data['scaler']
        instance.feature_names = model_data['feature_names']
        instance.training_metrics = model_data['training_metrics']
        instance.is_trained = model_data['is_trained']
        
        print(f"✅ Modelo cargado desde: {filepath}")
        return instance
    
    def summary(self) -> str:
        """
        Genera resumen del modelo
        
        Returns:
            String con información del modelo
        """
        if not self.is_trained:
            return "Modelo no entrenado"
        
        summary = "\n" + "="*60 + "\n"
        summary += "RESUMEN DEL MODELO\n"
        summary += "="*60 + "\n"
        
        summary += f"\nTipo: Ridge Regression\n"
        summary += f"Alpha (regularización): {self.alpha}\n"
        summary += f"Normalización: {'Sí' if self.normalize else 'No'}\n"
        summary += f"Intercepto: {self.get_intercept():.4f}\n"
        
        summary += f"\n📊 Métricas de Entrenamiento:\n"
        for metric, value in self.training_metrics.items():
            summary += f"  {metric:10s}: {value:.4f}\n"
        
        summary += f"\n🔝 Top 5 Features Más Importantes:\n"
        importance = self.get_feature_importance()
        for i, (name, imp) in enumerate(list(importance.items())[:5], 1):
            summary += f"  {i}. {name:30s}: {imp:.4f}\n"
        
        summary += "\n" + "="*60 + "\n"
        
        return summary
