"""
Postulaciones Routes - Correspondencia entre Perfiles
Endpoints para que estudiantes y titulados postulen a ofertas laborales.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.services.postulacion_service import get_postulacion_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/postulaciones", tags=["Postulaciones"])


@router.get("/ofertas")
async def get_ofertas_disponibles(
    current_user: dict = Depends(get_current_user)
):
    """
    Lista las ofertas disponibles para el usuario según su rol.

    - Estudiante: pasantías activas
    - Titulado: empleos activos
    - Admin/Operador: todas las ofertas activas
    """
    service = get_postulacion_service()
    try:
        ofertas = service.get_ofertas_disponibles(current_user['role'])
        return {'ofertas': ofertas, 'total': len(ofertas)}
    except Exception as e:
        logger.error(f"Error listando ofertas para postulacion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{oferta_id}")
async def postular_a_oferta(
    oferta_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Postula al usuario a una oferta específica.

    Evalúa el CV del usuario contra la oferta usando el modelo ML
    y almacena el resultado en la tabla postulaciones.

    Retorna:
    - match_score: puntaje de compatibilidad (0-1)
    - clasificacion: APTO / CONSIDERADO / NO_APTO
    - scores_detalle: desglose por dimensión
    - fortalezas / debilidades identificadas
    - datos de la oferta
    """
    service = get_postulacion_service()
    try:
        result = service.postular(
            user_id=current_user['user_id'],
            user_role=current_user['role'],
            oferta_id=oferta_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error postulando a oferta {oferta_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def get_my_postulaciones(
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene todas las postulaciones del usuario actual.

    Incluye los datos de la oferta y el resultado de evaluación ML.
    """
    service = get_postulacion_service()
    try:
        postulaciones = service.get_my_postulaciones(current_user['user_id'])
        return {
            'postulaciones': postulaciones,
            'total': len(postulaciones)
        }
    except Exception as e:
        logger.error(f"Error obteniendo postulaciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))
