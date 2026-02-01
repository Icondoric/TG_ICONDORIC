"""
Profile Routes - Sistema de Recomendaciones v2
Endpoints para gestionar el perfil profesional del usuario
"""

import base64
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse

from app.api.dependencies import get_current_user, get_current_user_optional
from app.api.schemas.ml_schemas import (
    PerfilProfesionalResponse,
    PerfilProfesionalUpdate,
    PerfilCompletenessResponse,
    CVUploadResponse
)
from app.services.profile_service import get_profile_service
from app.services.ml_integration_service import get_ml_service

# Configurar logging
logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("/me", response_model=PerfilProfesionalResponse)
async def get_my_profile(
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene el perfil profesional del usuario autenticado.

    Retorna todos los datos del perfil incluyendo:
    - Datos extraidos del CV (Gemini)
    - Skills normalizados
    - Nivel educativo y experiencia
    - Score de completitud
    """
    profile_service = get_profile_service()

    try:
        profile = profile_service.get_or_create_profile(current_user['user_id'])

        return PerfilProfesionalResponse(
            id=profile['id'],
            usuario_id=profile['usuario_id'],
            gemini_extraction=profile.get('gemini_extraction', {}),
            hard_skills=profile.get('hard_skills', []),
            soft_skills=profile.get('soft_skills', []),
            education_level=profile.get('education_level'),
            experience_years=float(profile.get('experience_years', 0)),
            languages=profile.get('languages', []),
            cv_filename=profile.get('cv_filename'),
            cv_uploaded_at=profile.get('cv_uploaded_at'),
            is_complete=profile.get('is_complete', False),
            completeness_score=float(profile.get('completeness_score', 0)),
            created_at=profile['created_at'],
            updated_at=profile['updated_at']
        )

    except Exception as e:
        logger.error(f"Error obteniendo perfil: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/me", response_model=PerfilProfesionalResponse)
async def update_my_profile(
    updates: PerfilProfesionalUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualiza campos del perfil manualmente.

    Permite editar:
    - hard_skills: Lista de habilidades tecnicas
    - soft_skills: Lista de habilidades blandas
    - education_level: Nivel educativo
    - experience_years: Anos de experiencia
    - languages: Lista de idiomas
    """
    profile_service = get_profile_service()

    try:
        # Convertir a dict excluyendo None
        update_dict = updates.model_dump(exclude_none=True)

        if not update_dict:
            raise HTTPException(
                status_code=400,
                detail="No se proporcionaron campos para actualizar"
            )

        profile = profile_service.update_profile_manual(
            current_user['user_id'],
            update_dict
        )

        return PerfilProfesionalResponse(
            id=profile['id'],
            usuario_id=profile['usuario_id'],
            gemini_extraction=profile.get('gemini_extraction', {}),
            hard_skills=profile.get('hard_skills', []),
            soft_skills=profile.get('soft_skills', []),
            education_level=profile.get('education_level'),
            experience_years=float(profile.get('experience_years', 0)),
            languages=profile.get('languages', []),
            cv_filename=profile.get('cv_filename'),
            cv_uploaded_at=profile.get('cv_uploaded_at'),
            is_complete=profile.get('is_complete', False),
            completeness_score=float(profile.get('completeness_score', 0)),
            created_at=profile['created_at'],
            updated_at=profile['updated_at']
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error actualizando perfil: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/completeness", response_model=PerfilCompletenessResponse)
async def get_profile_completeness(
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene el score de completitud del perfil.

    Retorna:
    - score: Valor de 0 a 1
    - percentage: Porcentaje de completitud
    - is_complete: Si el perfil esta completo (>=70%)
    - missing_fields: Campos faltantes o incompletos
    - recommendations: Sugerencias para completar
    """
    profile_service = get_profile_service()

    try:
        profile = profile_service.get_or_create_profile(current_user['user_id'])
        completeness = profile_service.calculate_completeness(profile)

        return PerfilCompletenessResponse(**completeness)

    except Exception as e:
        logger.error(f"Error calculando completitud: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-cv", response_model=CVUploadResponse)
async def upload_cv(
    file: UploadFile = File(..., description="Archivo PDF del CV"),
    current_user: dict = Depends(get_current_user)
):
    """
    Sube un CV en PDF y actualiza el perfil con los datos extraidos.

    El CV es procesado con Gemini para extraer:
    - Habilidades tecnicas y blandas
    - Formacion academica
    - Experiencia laboral
    - Idiomas
    - Resumen profesional

    Los datos se guardan de forma persistente en el perfil.
    """
    # Validar tipo de archivo
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos PDF"
        )

    # Validar tamano (max 10MB)
    contents = await file.read()
    max_size = 10 * 1024 * 1024  # 10MB
    if len(contents) > max_size:
        raise HTTPException(
            status_code=400,
            detail="El archivo excede el tamano maximo de 10MB"
        )

    ml_service = get_ml_service()
    profile_service = get_profile_service()

    try:
        # Codificar a base64
        pdf_base64 = base64.b64encode(contents).decode('utf-8')

        # Extraer con Gemini
        logger.info(f"Procesando CV: {file.filename}")
        gemini_output = ml_service.extract_cv_with_gemini(pdf_base64)

        # Actualizar perfil
        profile = profile_service.update_profile_from_cv(
            current_user['user_id'],
            gemini_output,
            cv_filename=file.filename
        )

        # Preparar resumen de extraccion
        extraction_summary = {
            'hard_skills_count': len(gemini_output.get('hard_skills', [])),
            'soft_skills_count': len(gemini_output.get('soft_skills', [])),
            'education_items': len(gemini_output.get('education', [])),
            'experience_items': len(gemini_output.get('experience', [])),
            'languages_detected': gemini_output.get('personal_info', {}).get('languages', [])
        }

        perfil_response = PerfilProfesionalResponse(
            id=profile['id'],
            usuario_id=profile['usuario_id'],
            gemini_extraction=profile.get('gemini_extraction', {}),
            hard_skills=profile.get('hard_skills', []),
            soft_skills=profile.get('soft_skills', []),
            education_level=profile.get('education_level'),
            experience_years=float(profile.get('experience_years', 0)),
            languages=profile.get('languages', []),
            cv_filename=profile.get('cv_filename'),
            cv_uploaded_at=profile.get('cv_uploaded_at'),
            is_complete=profile.get('is_complete', False),
            completeness_score=float(profile.get('completeness_score', 0)),
            created_at=profile['created_at'],
            updated_at=profile['updated_at']
        )

        return CVUploadResponse(
            message="CV procesado y perfil actualizado exitosamente",
            perfil=perfil_response,
            extraction_summary=extraction_summary
        )

    except ValueError as e:
        logger.error(f"Error procesando CV: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando el CV: {str(e)}"
        )


@router.delete("/me")
async def delete_my_profile(
    current_user: dict = Depends(get_current_user)
):
    """
    Elimina los datos del perfil (limpia el CV subido).

    El perfil se reinicia a estado vacio pero no se elimina
    la cuenta del usuario.
    """
    profile_service = get_profile_service()

    try:
        success = profile_service.delete_profile(current_user['user_id'])

        if success:
            return {"message": "Perfil limpiado exitosamente"}
        else:
            raise HTTPException(
                status_code=404,
                detail="Perfil no encontrado"
            )

    except Exception as e:
        logger.error(f"Error eliminando perfil: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preview")
async def preview_profile_from_cv(
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene una vista previa del perfil para recomendaciones.

    Retorna el perfil en formato compatible con el sistema ML.
    """
    profile_service = get_profile_service()

    try:
        profile = profile_service.get_profile(current_user['user_id'])

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Perfil no encontrado. Sube tu CV primero."
            )

        ml_format = profile_service.get_profile_for_recommendations(
            current_user['user_id']
        )

        completeness = profile_service.calculate_completeness(profile)

        return {
            "profile_ready": completeness['is_complete'],
            "completeness_score": completeness['score'],
            "missing_fields": completeness['missing_fields'],
            "recommendations_available": completeness['is_complete'],
            "profile_data": {
                "hard_skills": profile.get('hard_skills', []),
                "soft_skills": profile.get('soft_skills', []),
                "education_level": profile.get('education_level'),
                "experience_years": profile.get('experience_years', 0),
                "languages": profile.get('languages', [])
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en preview: {e}")
        raise HTTPException(status_code=500, detail=str(e))
