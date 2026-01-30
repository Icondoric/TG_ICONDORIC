"""
Módulo de Machine Learning para evaluación de perfiles profesionales
Incluye feature engineering, modelos predictivos y evaluación
"""

__version__ = "1.0.0"
__author__ = "Ivan Condori Choquehuanca"

from .feature_engineering.feature_extractor import extract_features
from .models.predictor import predict_match_score

__all__ = [
    'extract_features',
    'predict_match_score'
]
