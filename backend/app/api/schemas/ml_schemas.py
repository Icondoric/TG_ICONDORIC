"""
ML Schemas - Fase 6
Modelos Pydantic para endpoints de Machine Learning
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Dict, Optional, Any
from datetime import datetime


# ============================================================
# INSTITUTIONAL PROFILE SCHEMAS
# ============================================================

class InstitutionalWeights(BaseModel):
    """Pesos de las dimensiones del CV"""
    hard_skills: float = Field(ge=0, le=1, description="Peso de habilidades tecnicas")
    soft_skills: float = Field(ge=0, le=1, description="Peso de habilidades blandas")
    experience: float = Field(ge=0, le=1, description="Peso de experiencia")
    education: float = Field(ge=0, le=1, description="Peso de educacion")
    languages: float = Field(ge=0, le=1, description="Peso de idiomas")

    @model_validator(mode='after')
    def weights_sum_to_one(self):
        """Valida que los pesos sumen aproximadamente 1.0"""
        total = (
            self.hard_skills +
            self.soft_skills +
            self.experience +
            self.education +
            self.languages
        )
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Los pesos deben sumar 1.0 (actual: {total:.3f})")
        return self


class InstitutionalRequirements(BaseModel):
    """Requisitos de la institucion"""
    min_experience_years: float = Field(ge=0, default=0, description="Anos minimos de experiencia")
    required_skills: List[str] = Field(default=[], description="Habilidades requeridas")
    preferred_skills: List[str] = Field(default=[], description="Habilidades preferidas")
    required_education_level: str = Field(default="Licenciatura", description="Nivel educativo requerido")
    required_languages: List[str] = Field(default=[], description="Idiomas requeridos")

    @field_validator('required_education_level')
    @classmethod
    def validate_education_level(cls, v):
        valid_levels = [
            'Bachillerato', 'Tecnico', 'Licenciatura',
            'Ingenieria', 'Maestria', 'Doctorado'
        ]
        if v not in valid_levels:
            raise ValueError(f"Nivel educativo invalido. Opciones: {valid_levels}")
        return v


class InstitutionalThresholds(BaseModel):
    """Umbrales de clasificacion"""
    apto: float = Field(default=0.70, ge=0, le=1, description="Umbral para APTO")
    considerado: float = Field(default=0.50, ge=0, le=1, description="Umbral para CONSIDERADO")

    @model_validator(mode='after')
    def validate_thresholds_order(self):
        """Valida que apto > considerado"""
        if self.apto <= self.considerado:
            raise ValueError("El umbral 'apto' debe ser mayor que 'considerado'")
        return self


class InstitutionalProfileCreate(BaseModel):
    """Request para crear perfil institucional"""
    institution_name: str = Field(min_length=2, max_length=200, description="Nombre de la institucion")
    sector: str = Field(min_length=2, max_length=100, description="Sector de la institucion")
    description: Optional[str] = Field(default=None, max_length=1000, description="Descripcion")
    weights: InstitutionalWeights
    requirements: InstitutionalRequirements
    thresholds: Optional[InstitutionalThresholds] = None

    class Config:
        json_schema_extra = {
            "example": {
                "institution_name": "TechBolivia Startup",
                "sector": "Tecnologia",
                "description": "Empresa de desarrollo de software",
                "weights": {
                    "hard_skills": 0.40,
                    "soft_skills": 0.15,
                    "experience": 0.25,
                    "education": 0.10,
                    "languages": 0.10
                },
                "requirements": {
                    "min_experience_years": 1.0,
                    "required_skills": ["Python", "SQL"],
                    "preferred_skills": ["Docker", "AWS"],
                    "required_education_level": "Licenciatura",
                    "required_languages": ["Ingles"]
                },
                "thresholds": {
                    "apto": 0.70,
                    "considerado": 0.50
                }
            }
        }


class InstitutionalProfileUpdate(BaseModel):
    """Request para actualizar perfil institucional"""
    institution_name: Optional[str] = Field(default=None, min_length=2, max_length=200)
    sector: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    weights: Optional[InstitutionalWeights] = None
    requirements: Optional[InstitutionalRequirements] = None
    thresholds: Optional[InstitutionalThresholds] = None
    is_active: Optional[bool] = None


class InstitutionalProfileResponse(BaseModel):
    """Response de perfil institucional"""
    id: str
    institution_name: str
    sector: str
    description: Optional[str] = None
    weights: Dict[str, float]
    requirements: Dict[str, Any]
    thresholds: Dict[str, float]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None


class InstitutionalProfileListResponse(BaseModel):
    """Response de lista de perfiles"""
    profiles: List[InstitutionalProfileResponse]
    total: int


# ============================================================
# CV EVALUATION SCHEMAS
# ============================================================

class CVScores(BaseModel):
    """Scores individuales del CV"""
    hard_skills_score: float = Field(ge=0, le=1)
    soft_skills_score: float = Field(ge=0, le=1)
    experience_score: float = Field(ge=0, le=1)
    education_score: float = Field(ge=0, le=1)
    languages_score: float = Field(ge=0, le=1)


class FeatureContribution(BaseModel):
    """Contribucion de un feature a la prediccion"""
    feature: str
    contribution: float


class CVEvaluationRequest(BaseModel):
    """Request para evaluar CV"""
    cv_file: str = Field(description="Archivo PDF en base64")
    institutional_profile_id: str = Field(description="ID del perfil institucional")

    class Config:
        json_schema_extra = {
            "example": {
                "cv_file": "JVBERi0xLjQKJ...",
                "institutional_profile_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class CVEvaluationResponse(BaseModel):
    """Response de evaluacion de CV"""
    match_score: float = Field(ge=0, le=1, description="Score de matching")
    classification: str = Field(description="APTO, CONSIDERADO o NO_APTO")
    cv_scores: CVScores
    top_strengths: List[FeatureContribution]
    top_weaknesses: List[FeatureContribution]
    institutional_profile: Dict[str, Any]
    gemini_extraction: Dict[str, Any]
    evaluation_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "match_score": 0.78,
                "classification": "APTO",
                "cv_scores": {
                    "hard_skills_score": 0.82,
                    "soft_skills_score": 0.65,
                    "experience_score": 0.75,
                    "education_score": 0.80,
                    "languages_score": 0.70
                },
                "top_strengths": [
                    {"feature": "hard_skills_score", "contribution": 0.31},
                    {"feature": "experience_score", "contribution": 0.26}
                ],
                "top_weaknesses": [
                    {"feature": "languages_score", "contribution": -0.05}
                ],
                "institutional_profile": {
                    "name": "TechBolivia Startup",
                    "sector": "Tecnologia"
                },
                "gemini_extraction": {
                    "hard_skills": ["Python", "React"],
                    "soft_skills": ["Liderazgo"]
                }
            }
        }


# ============================================================
# RECOMMENDATIONS SCHEMAS
# ============================================================

class CVSummary(BaseModel):
    """Resumen del CV procesado"""
    name: Optional[str] = None
    education_level: Optional[str] = None
    total_experience_years: float = 0
    top_skills: List[str] = []


class RecommendationsRequest(BaseModel):
    """Request para obtener recomendaciones"""
    cv_file: str = Field(description="Archivo PDF en base64")
    top_n: int = Field(default=5, ge=1, le=20, description="Numero de recomendaciones")

    class Config:
        json_schema_extra = {
            "example": {
                "cv_file": "JVBERi0xLjQKJ...",
                "top_n": 5
            }
        }


class RecommendationItem(BaseModel):
    """Un item de recomendacion"""
    rank: int
    institution_id: str
    institution_name: str
    sector: str
    match_score: float
    classification: str
    main_strength: str
    main_weakness: str


class RecommendationsResponse(BaseModel):
    """Response de recomendaciones"""
    recommendations: List[RecommendationItem]
    total_evaluated: int
    cv_summary: CVSummary

    class Config:
        json_schema_extra = {
            "example": {
                "recommendations": [
                    {
                        "rank": 1,
                        "institution_id": "uuid-1",
                        "institution_name": "TechBolivia",
                        "sector": "Tecnologia",
                        "match_score": 0.85,
                        "classification": "APTO",
                        "main_strength": "Hard skills tecnicos",
                        "main_weakness": "Experiencia"
                    }
                ],
                "total_evaluated": 15,
                "cv_summary": {
                    "name": "Juan Perez",
                    "education_level": "Ingenieria",
                    "total_experience_years": 3.5,
                    "top_skills": ["Python", "React"]
                }
            }
        }


# ============================================================
# MODEL INFO SCHEMAS
# ============================================================

class TrainingMetrics(BaseModel):
    """Metricas de entrenamiento del modelo"""
    r2_score: float
    mae: float
    rmse: float
    accuracy: Optional[float] = None


class ModelInfoResponse(BaseModel):
    """Informacion del modelo ML"""
    status: str = Field(description="loaded o not_loaded")
    model_type: str = Field(default="Ridge Regression")
    alpha: Optional[float] = None
    training_metrics: Optional[TrainingMetrics] = None
    n_features: int = 18
    model_version: str = "v1"
    is_ready: bool

    class Config:
        json_schema_extra = {
            "example": {
                "status": "loaded",
                "model_type": "Ridge Regression",
                "alpha": 0.01,
                "training_metrics": {
                    "r2_score": 0.7996,
                    "mae": 0.0736,
                    "rmse": 0.0918,
                    "accuracy": 0.771
                },
                "n_features": 18,
                "model_version": "v1",
                "is_ready": True
            }
        }


# ============================================================
# ERROR SCHEMAS
# ============================================================

class ErrorResponse(BaseModel):
    """Formato de error estandar"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Perfil institucional no encontrado",
                "error_code": "PROFILE_NOT_FOUND",
                "timestamp": "2025-01-31T10:30:00Z"
            }
        }
