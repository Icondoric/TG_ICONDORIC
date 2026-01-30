"""
Models Module
Contiene el modelo Ridge y utilidades de entrenamiento/predicción
"""

from .ridge_model import InstitutionalMatchModel
from .model_trainer import ModelTrainer
from .predictor import MatchPredictor

__all__ = [
    'InstitutionalMatchModel',
    'ModelTrainer',
    'MatchPredictor'
]
