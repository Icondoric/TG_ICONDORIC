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


# ============================================================
# PERFIL PROFESIONAL SCHEMAS (Usuario)
# ============================================================

class EducacionItem(BaseModel):
    """Item de educacion del perfil"""
    degree: str = Field(description="Titulo obtenido")
    institution: str = Field(description="Institucion educativa")
    year: Optional[str] = Field(default=None, description="Ano de graduacion")
    field: Optional[str] = Field(default=None, description="Area de estudio")


class ExperienciaItem(BaseModel):
    """Item de experiencia laboral"""
    role: str = Field(description="Cargo/Puesto")
    company: str = Field(description="Empresa")
    duration: Optional[str] = Field(default=None, description="Duracion (ej: '2021-2023')")
    description: Optional[str] = Field(default=None, description="Descripcion de responsabilidades")


class PerfilProfesionalResponse(BaseModel):
    """Response del perfil profesional del usuario"""
    id: str
    usuario_id: str

    # Datos extraidos de Gemini
    gemini_extraction: Dict[str, Any] = Field(default={})

    # Campos normalizados
    hard_skills: List[str] = Field(default=[])
    soft_skills: List[str] = Field(default=[])
    education_level: Optional[str] = None
    experience_years: float = 0
    languages: List[str] = Field(default=[])

    # Metadatos del CV
    cv_filename: Optional[str] = None
    cv_uploaded_at: Optional[datetime] = None

    # Estado del perfil
    is_complete: bool = False
    completeness_score: float = 0

    # Timestamps
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "uuid-perfil",
                "usuario_id": "uuid-usuario",
                "gemini_extraction": {
                    "personal_info": {"summary": "Ingeniero de software..."},
                    "hard_skills": ["Python", "React", "SQL"],
                    "soft_skills": ["Liderazgo", "Trabajo en equipo"],
                    "education": [{"degree": "Ingenieria", "institution": "EMI"}],
                    "experience": [{"role": "Developer", "company": "Tech Co"}]
                },
                "hard_skills": ["Python", "React", "SQL"],
                "soft_skills": ["Liderazgo", "Trabajo en equipo"],
                "education_level": "Licenciatura",
                "experience_years": 2.5,
                "languages": ["Espanol", "Ingles"],
                "cv_filename": "cv_juan_perez.pdf",
                "cv_uploaded_at": "2026-01-31T10:00:00Z",
                "is_complete": True,
                "completeness_score": 0.85,
                "created_at": "2026-01-31T09:00:00Z",
                "updated_at": "2026-01-31T10:00:00Z"
            }
        }


class PerfilProfesionalUpdate(BaseModel):
    """Request para actualizar perfil manualmente"""
    hard_skills: Optional[List[str]] = None
    soft_skills: Optional[List[str]] = None
    education_level: Optional[str] = None
    experience_years: Optional[float] = Field(default=None, ge=0)
    languages: Optional[List[str]] = None

    @field_validator('education_level')
    @classmethod
    def validate_education_level(cls, v):
        if v is None:
            return v
        valid_levels = [
            'Bachillerato', 'Tecnico', 'Licenciatura',
            'Ingenieria', 'Maestria', 'Doctorado'
        ]
        if v not in valid_levels:
            raise ValueError(f"Nivel educativo invalido. Opciones: {valid_levels}")
        return v


class PerfilCompletenessResponse(BaseModel):
    """Response de completitud del perfil"""
    score: float = Field(ge=0, le=1, description="Score de completitud (0-1)")
    percentage: int = Field(ge=0, le=100, description="Porcentaje de completitud")
    is_complete: bool
    missing_fields: List[str] = Field(default=[], description="Campos faltantes o incompletos")
    recommendations: List[str] = Field(default=[], description="Recomendaciones para completar")

    class Config:
        json_schema_extra = {
            "example": {
                "score": 0.75,
                "percentage": 75,
                "is_complete": False,
                "missing_fields": ["languages", "soft_skills"],
                "recommendations": [
                    "Agrega al menos 2 habilidades blandas",
                    "Especifica los idiomas que dominas"
                ]
            }
        }


class CVUploadResponse(BaseModel):
    """Response al subir CV"""
    message: str
    perfil: PerfilProfesionalResponse
    extraction_summary: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "message": "CV procesado y perfil actualizado exitosamente",
                "perfil": {},
                "extraction_summary": {
                    "hard_skills_count": 8,
                    "soft_skills_count": 4,
                    "education_items": 2,
                    "experience_items": 3
                }
            }
        }


# ============================================================
# OFERTAS LABORALES SCHEMAS
# ============================================================

class OfertaLaboralCreate(BaseModel):
    """Request para crear oferta laboral"""
    institutional_profile_id: Optional[str] = Field(default=None, description="ID del perfil institucional base")
    titulo: str = Field(min_length=5, max_length=200, description="Titulo de la oferta")
    descripcion: Optional[str] = Field(default=None, max_length=2000, description="Descripcion detallada")
    tipo: str = Field(description="Tipo: 'pasantia' o 'empleo'")
    modalidad: Optional[str] = Field(default=None, description="Modalidad: 'presencial', 'remoto', 'hibrido'")
    ubicacion: Optional[str] = Field(default=None, max_length=200, description="Ubicacion geografica")
    requisitos_especificos: Optional[Dict[str, Any]] = Field(default=None, description="Requisitos adicionales")
    fecha_inicio: Optional[str] = Field(default=None, description="Fecha inicio (YYYY-MM-DD)")
    fecha_cierre: Optional[str] = Field(default=None, description="Fecha cierre (YYYY-MM-DD)")
    cupos_disponibles: int = Field(default=1, ge=1, description="Numero de cupos")

    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        if v not in ['pasantia', 'empleo']:
            raise ValueError("Tipo debe ser 'pasantia' o 'empleo'")
        return v

    @field_validator('modalidad')
    @classmethod
    def validate_modalidad(cls, v):
        if v is not None and v not in ['presencial', 'remoto', 'hibrido']:
            raise ValueError("Modalidad debe ser 'presencial', 'remoto' o 'hibrido'")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "institutional_profile_id": "uuid-perfil-institucional",
                "titulo": "Pasantia en Desarrollo Web",
                "descripcion": "Buscamos estudiantes para desarrollo de aplicaciones web...",
                "tipo": "pasantia",
                "modalidad": "hibrido",
                "ubicacion": "La Paz, Bolivia",
                "fecha_inicio": "2026-02-01",
                "fecha_cierre": "2026-04-30",
                "cupos_disponibles": 3
            }
        }


class OfertaLaboralUpdate(BaseModel):
    """Request para actualizar oferta laboral"""
    institutional_profile_id: Optional[str] = None
    titulo: Optional[str] = Field(default=None, min_length=5, max_length=200)
    descripcion: Optional[str] = Field(default=None, max_length=2000)
    tipo: Optional[str] = None
    modalidad: Optional[str] = None
    ubicacion: Optional[str] = Field(default=None, max_length=200)
    requisitos_especificos: Optional[Dict[str, Any]] = None
    fecha_inicio: Optional[str] = None
    fecha_cierre: Optional[str] = None
    cupos_disponibles: Optional[int] = Field(default=None, ge=1)
    is_active: Optional[bool] = None

    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        if v is not None and v not in ['pasantia', 'empleo']:
            raise ValueError("Tipo debe ser 'pasantia' o 'empleo'")
        return v

    @field_validator('modalidad')
    @classmethod
    def validate_modalidad(cls, v):
        if v is not None and v not in ['presencial', 'remoto', 'hibrido']:
            raise ValueError("Modalidad debe ser 'presencial', 'remoto' o 'hibrido'")
        return v


class OfertaLaboralResponse(BaseModel):
    """Response de oferta laboral"""
    id: str
    institutional_profile_id: Optional[str] = None
    institution_name: Optional[str] = None  # Joined from institutional_profiles
    sector: Optional[str] = None  # Joined from institutional_profiles

    titulo: str
    descripcion: Optional[str] = None
    tipo: str
    modalidad: Optional[str] = None
    ubicacion: Optional[str] = None
    requisitos_especificos: Dict[str, Any] = Field(default={})

    is_active: bool
    fecha_inicio: Optional[str] = None
    fecha_cierre: Optional[str] = None
    cupos_disponibles: int

    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "uuid-oferta",
                "institutional_profile_id": "uuid-perfil",
                "institution_name": "AGETIC",
                "sector": "Gobierno - Tecnologia",
                "titulo": "Pasantia en Desarrollo Web",
                "descripcion": "Buscamos estudiantes...",
                "tipo": "pasantia",
                "modalidad": "hibrido",
                "ubicacion": "La Paz, Bolivia",
                "requisitos_especificos": {},
                "is_active": True,
                "fecha_inicio": "2026-02-01",
                "fecha_cierre": "2026-04-30",
                "cupos_disponibles": 3,
                "created_at": "2026-01-31T10:00:00Z",
                "updated_at": "2026-01-31T10:00:00Z"
            }
        }


class OfertaLaboralListResponse(BaseModel):
    """Response de lista de ofertas"""
    ofertas: List[OfertaLaboralResponse]
    total: int
    page: int = 1
    page_size: int = 20


# ============================================================
# RECOMENDACIONES MEJORADAS SCHEMAS
# ============================================================

class RecomendacionDetalladaResponse(BaseModel):
    """Response de recomendacion con detalle completo"""
    id: str
    oferta_id: str

    # Info de la oferta
    oferta: OfertaLaboralResponse

    # Resultado de evaluacion
    match_score: float = Field(ge=0, le=1)
    clasificacion: str

    # Detalles
    scores_detalle: Dict[str, float] = Field(default={})
    fortalezas: List[str] = Field(default=[])
    debilidades: List[str] = Field(default=[])

    # Estado
    fue_vista: bool = False
    vista_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "uuid-recomendacion",
                "oferta_id": "uuid-oferta",
                "oferta": {},
                "match_score": 0.82,
                "clasificacion": "APTO",
                "scores_detalle": {
                    "hard_skills": 0.85,
                    "soft_skills": 0.70,
                    "education": 0.90,
                    "experience": 0.75,
                    "languages": 0.80
                },
                "fortalezas": ["Habilidades tecnicas solidas", "Nivel educativo adecuado"],
                "debilidades": ["Podria mejorar experiencia"],
                "fue_vista": False,
                "created_at": "2026-01-31T10:00:00Z"
            }
        }


class MisRecomendacionesResponse(BaseModel):
    """Response de recomendaciones del usuario"""
    recomendaciones: List[RecomendacionDetalladaResponse]
    total: int
    nuevas: int = Field(description="Recomendaciones no vistas")

    # Resumen del perfil usado
    perfil_summary: Dict[str, Any] = Field(default={})

    class Config:
        json_schema_extra = {
            "example": {
                "recomendaciones": [],
                "total": 5,
                "nuevas": 3,
                "perfil_summary": {
                    "completeness_score": 0.85,
                    "top_skills": ["Python", "React"],
                    "experience_years": 2.5
                }
            }
        }


class RecomendacionesRequestFromProfile(BaseModel):
    """Request para obtener recomendaciones basadas en perfil guardado"""
    top_n: int = Field(default=10, ge=1, le=50, description="Numero maximo de recomendaciones")
    tipo: Optional[str] = Field(default=None, description="Filtrar por tipo: 'pasantia' o 'empleo'")
    sector: Optional[str] = Field(default=None, description="Filtrar por sector")
    recalcular: bool = Field(default=False, description="Forzar recalculo de recomendaciones")

    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        if v is not None and v not in ['pasantia', 'empleo']:
            raise ValueError("Tipo debe ser 'pasantia' o 'empleo'")
        return v


# ============================================================
# ESTADISTICAS ADMIN SCHEMAS
# ============================================================

class EstadisticasGeneralesResponse(BaseModel):
    """Estadisticas generales para admin dashboard"""
    # Usuarios
    total_estudiantes: int = 0
    total_titulados: int = 0
    total_admins: int = 0
    perfiles_completos: int = 0

    # Ofertas
    pasantias_activas: int = 0
    empleos_activos: int = 0
    ofertas_expiradas: int = 0

    # Recomendaciones
    total_recomendaciones: int = 0
    promedio_match_score: float = 0
    distribucion_clasificacion: Dict[str, int] = Field(default={})

    # Perfiles institucionales
    perfiles_institucionales_activos: int = 0

    # Por sector
    ofertas_por_sector: Dict[str, int] = Field(default={})
    matches_por_sector: Dict[str, float] = Field(default={})

    class Config:
        json_schema_extra = {
            "example": {
                "total_estudiantes": 150,
                "total_titulados": 80,
                "total_admins": 3,
                "perfiles_completos": 120,
                "pasantias_activas": 25,
                "empleos_activos": 15,
                "ofertas_expiradas": 5,
                "total_recomendaciones": 500,
                "promedio_match_score": 0.68,
                "distribucion_clasificacion": {
                    "APTO": 150,
                    "CONSIDERADO": 200,
                    "NO_APTO": 150
                },
                "perfiles_institucionales_activos": 10,
                "ofertas_por_sector": {
                    "Tecnologia": 15,
                    "Finanzas": 10,
                    "Gobierno": 8
                }
            }
        }


class UsuarioAdminResponse(BaseModel):
    """Response de usuario para admin"""
    id: str
    email: str
    nombre_completo: Optional[str] = None
    rol: str
    created_at: datetime

    # Estado del perfil
    tiene_perfil: bool = False
    perfil_completo: bool = False
    completeness_score: float = 0
    cv_uploaded_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "uuid-usuario",
                "email": "juan@emi.edu.bo",
                "nombre_completo": "Juan Perez",
                "rol": "estudiante",
                "created_at": "2026-01-15T10:00:00Z",
                "tiene_perfil": True,
                "perfil_completo": True,
                "completeness_score": 0.85,
                "cv_uploaded_at": "2026-01-20T14:30:00Z"
            }
        }


class UsuariosListResponse(BaseModel):
    """Response de lista de usuarios para admin"""
    usuarios: List[UsuarioAdminResponse]
    total: int
    page: int = 1
    page_size: int = 20
