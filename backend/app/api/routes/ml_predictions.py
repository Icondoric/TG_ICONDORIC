"""
ML Predictions Endpoints - Fase 6
Endpoints para prediccion y recomendaciones ML
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.api.schemas.ml_schemas import (
    CVEvaluationRequest,
    CVEvaluationResponse,
    RecommendationsRequest,
    RecommendationsResponse,
    RecommendationItem,
    CVSummary,
    CVScores,
    ModelInfoResponse,
    TrainingMetrics
)
from app.api.dependencies import (
    get_current_user,
    get_current_user_optional,
    verify_ml_model_loaded,
    get_ml_service_dependency
)
from app.services.ml_integration_service import MLIntegrationService

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/evaluate-cv",
    response_model=CVEvaluationResponse,
    summary="Evaluar CV contra perfil institucional",
    description="""
    Evalua un CV (PDF en base64) contra un perfil institucional especifico.

    El proceso:
    1. Extrae texto del PDF
    2. Usa Gemini para estructurar la informacion
    3. Calcula scores por dimension
    4. Predice match score con modelo Ridge
    5. Retorna resultado con explicacion
    """
)
async def evaluate_cv(
    request: CVEvaluationRequest,
    current_user: Optional[dict] = Depends(get_current_user_optional),
    ml_service: MLIntegrationService = Depends(verify_ml_model_loaded)
):
    """
    Evalua un CV contra un perfil institucional
    """
    try:
        # 1. Extraer CV con Gemini
        logger.info(f"Procesando CV para perfil: {request.institutional_profile_id}")
        gemini_output = ml_service.extract_cv_with_gemini(request.cv_file)

        # 2. Cargar perfil institucional
        profile = ml_service.load_institutional_profile(request.institutional_profile_id)

        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perfil institucional no encontrado: {request.institutional_profile_id}"
            )

        # 3. Evaluar CV
        evaluation = ml_service.evaluate_cv(gemini_output, profile)

        # 4. Guardar evaluacion si hay usuario autenticado
        evaluation_id = None
        if current_user:
            evaluation_id = ml_service.save_evaluation(
                user_id=current_user['user_id'],
                profile_id=request.institutional_profile_id,
                evaluation_result=evaluation,
                gemini_extraction=gemini_output
            )

        # 5. Construir respuesta
        return CVEvaluationResponse(
            match_score=evaluation['match_score'],
            classification=evaluation['classification'],
            cv_scores=CVScores(**evaluation['cv_scores']),
            top_strengths=evaluation['top_strengths'],
            top_weaknesses=evaluation['top_weaknesses'],
            institutional_profile={
                'id': profile['id'],
                'name': profile['institution_name'],
                'sector': profile['sector']
            },
            gemini_extraction=gemini_output,
            evaluation_id=evaluation_id
        )

    except ValueError as e:
        logger.error(f"Error de validacion: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error evaluando CV: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando CV: {str(e)}"
        )


@router.post(
    "/get-recommendations",
    response_model=RecommendationsResponse,
    summary="Obtener recomendaciones de instituciones",
    description="""
    Evalua un CV contra todos los perfiles institucionales activos
    y retorna las mejores coincidencias ordenadas por score.
    """
)
async def get_recommendations(
    request: RecommendationsRequest,
    current_user: Optional[dict] = Depends(get_current_user_optional),
    ml_service: MLIntegrationService = Depends(verify_ml_model_loaded)
):
    """
    Obtiene recomendaciones de instituciones para un CV
    """
    try:
        # 1. Extraer CV con Gemini
        logger.info(f"Generando recomendaciones (top {request.top_n})")
        gemini_output = ml_service.extract_cv_with_gemini(request.cv_file)

        # 2. Obtener recomendaciones
        recommendations = ml_service.get_recommendations(
            gemini_output=gemini_output,
            top_n=request.top_n
        )

        if not recommendations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay perfiles institucionales activos"
            )

        # 3. Extraer resumen del CV
        cv_summary = ml_service.extract_cv_summary(gemini_output)

        # 4. Contar total de perfiles evaluados
        all_profiles = ml_service.load_all_active_profiles()
        total_evaluated = len(all_profiles)

        # 5. Construir respuesta
        recommendation_items = [
            RecommendationItem(
                rank=rec['rank'],
                institution_id=rec['institution_id'],
                institution_name=rec['institution_name'],
                sector=rec['sector'],
                match_score=rec['match_score'],
                classification=rec['classification'],
                main_strength=rec['main_strength'],
                main_weakness=rec['main_weakness']
            )
            for rec in recommendations
        ]

        return RecommendationsResponse(
            recommendations=recommendation_items,
            total_evaluated=total_evaluated,
            cv_summary=CVSummary(**cv_summary)
        )

    except ValueError as e:
        logger.error(f"Error de validacion: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generando recomendaciones: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando CV: {str(e)}"
        )


@router.get(
    "/model-info",
    response_model=ModelInfoResponse,
    summary="Informacion del modelo ML",
    description="Retorna informacion del modelo ML cargado"
)
async def get_model_info(
    ml_service: MLIntegrationService = Depends(get_ml_service_dependency)
):
    """
    Obtiene informacion del modelo ML
    """
    info = ml_service.get_model_info()

    # Construir respuesta
    training_metrics = None
    if info.get('training_metrics'):
        metrics = info['training_metrics']
        training_metrics = TrainingMetrics(
            r2_score=metrics.get('r2_score', 0),
            mae=metrics.get('mae', 0),
            rmse=metrics.get('rmse', 0),
            accuracy=metrics.get('classification_accuracy')
        )

    return ModelInfoResponse(
        status=info.get('status', 'not_loaded'),
        model_type=info.get('model_type', 'Ridge Regression'),
        alpha=info.get('alpha'),
        training_metrics=training_metrics,
        n_features=info.get('n_features', 18),
        model_version=info.get('model_version', 'v1'),
        is_ready=info.get('is_ready', False)
    )


@router.get(
    "/user-evaluations",
    summary="Historial de evaluaciones del usuario",
    description="Retorna las ultimas evaluaciones del usuario autenticado"
)
async def get_user_evaluations(
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    ml_service: MLIntegrationService = Depends(get_ml_service_dependency)
):
    """
    Obtiene el historial de evaluaciones del usuario
    """
    evaluations = ml_service.get_user_evaluations(
        user_id=current_user['user_id'],
        limit=limit
    )

    return {
        "evaluations": evaluations,
        "total": len(evaluations)
    }
