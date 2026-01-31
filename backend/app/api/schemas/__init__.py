"""
API Schemas
Modelos Pydantic para validacion de requests y responses
"""

from .ml_schemas import (
    # Weights and Requirements
    InstitutionalWeights,
    InstitutionalRequirements,
    InstitutionalThresholds,
    # Profile CRUD
    InstitutionalProfileCreate,
    InstitutionalProfileUpdate,
    InstitutionalProfileResponse,
    InstitutionalProfileListResponse,
    # CV Evaluation
    CVEvaluationRequest,
    CVEvaluationResponse,
    CVScores,
    FeatureContribution,
    # Recommendations
    RecommendationsRequest,
    RecommendationItem,
    RecommendationsResponse,
    CVSummary,
    # Model Info
    ModelInfoResponse,
)

__all__ = [
    "InstitutionalWeights",
    "InstitutionalRequirements",
    "InstitutionalThresholds",
    "InstitutionalProfileCreate",
    "InstitutionalProfileUpdate",
    "InstitutionalProfileResponse",
    "InstitutionalProfileListResponse",
    "CVEvaluationRequest",
    "CVEvaluationResponse",
    "CVScores",
    "FeatureContribution",
    "RecommendationsRequest",
    "RecommendationItem",
    "RecommendationsResponse",
    "CVSummary",
    "ModelInfoResponse",
]
