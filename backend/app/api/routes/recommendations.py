"""
Recommendations Routes - Sistema de Recomendaciones v2
Endpoints para obtener recomendaciones basadas en perfil guardado
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_current_user
from app.api.schemas.ml_schemas import (
    MisRecomendacionesResponse,
    RecomendacionesRequestFromProfile,
    OfertaLaboralResponse
)
from app.services.recommendation_service import get_recommendation_service
from app.services.profile_service import get_profile_service

# Configurar logging
logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("", response_model=MisRecomendacionesResponse)
async def get_my_recommendations(
    top_n: int = Query(10, ge=1, le=50, description="Numero de recomendaciones"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: 'pasantia' o 'empleo'"),
    sector: Optional[str] = Query(None, description="Filtrar por sector"),
    recalcular: bool = Query(False, description="Forzar recalculo"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene recomendaciones personalizadas basadas en el perfil guardado.

    El sistema automaticamente filtra por tipo segun el rol:
    - Estudiante: Solo pasantias
    - Titulado: Solo empleos

    Retorna:
    - Lista de ofertas ordenadas por match score
    - Detalle de scores por dimension
    - Fortalezas y debilidades
    - Estado del perfil

    Nota: Requiere tener un perfil completo (>=70% completitud)
    """
    recommendation_service = get_recommendation_service()

    try:
        result = recommendation_service.get_recommendations_for_user(
            user_id=current_user['user_id'],
            user_role=current_user['role'],
            top_n=top_n,
            tipo=tipo,
            sector=sector,
            recalcular=recalcular
        )

        # Formatear recomendaciones
        recomendaciones_formatted = []
        for rec in result['recomendaciones']:
            oferta = rec.get('oferta', {})

            recomendaciones_formatted.append({
                'id': rec.get('id', ''),
                'oferta_id': rec['oferta_id'],
                'oferta': {
                    'id': oferta.get('id', ''),
                    'institutional_profile_id': oferta.get('institutional_profile_id'),
                    'institution_name': oferta.get('institution_name'),
                    'sector': oferta.get('sector'),
                    'titulo': oferta.get('titulo', ''),
                    'descripcion': oferta.get('descripcion'),
                    'tipo': oferta.get('tipo', ''),
                    'modalidad': oferta.get('modalidad'),
                    'ubicacion': oferta.get('ubicacion'),
                    'requisitos_especificos': oferta.get('requisitos_especificos', {}),
                    'is_active': oferta.get('is_active', True),
                    'fecha_inicio': oferta.get('fecha_inicio'),
                    'fecha_cierre': oferta.get('fecha_cierre'),
                    'cupos_disponibles': oferta.get('cupos_disponibles', 1),
                    'created_by': oferta.get('created_by'),
                    'created_at': oferta.get('created_at'),
                    'updated_at': oferta.get('updated_at')
                },
                'match_score': rec['match_score'],
                'clasificacion': rec['clasificacion'],
                'scores_detalle': rec.get('scores_detalle', {}),
                'fortalezas': rec.get('fortalezas', []),
                'debilidades': rec.get('debilidades', []),
                'fue_vista': rec.get('fue_vista', False),
                'vista_at': rec.get('vista_at'),
                'created_at': rec.get('created_at')
            })

        return MisRecomendacionesResponse(
            recomendaciones=recomendaciones_formatted,
            total=result['total'],
            nuevas=result['nuevas'],
            perfil_summary=result['perfil_summary']
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error obteniendo recomendaciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_recommendation_history(
    limit: int = Query(20, ge=1, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginacion"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene el historial de recomendaciones del usuario.

    Incluye todas las recomendaciones generadas previamente,
    con indicador de si fueron vistas o no.
    """
    recommendation_service = get_recommendation_service()

    try:
        result = recommendation_service.get_recommendation_history(
            user_id=current_user['user_id'],
            limit=limit,
            offset=offset
        )

        return result

    except Exception as e:
        logger.error(f"Error obteniendo historial: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{recommendation_id}/viewed")
async def mark_recommendation_viewed(
    recommendation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Marca una recomendacion como vista.

    Esto permite al sistema saber cuales recomendaciones
    el usuario ya ha revisado.
    """
    recommendation_service = get_recommendation_service()

    try:
        success = recommendation_service.mark_as_viewed(
            user_id=current_user['user_id'],
            recommendation_id=recommendation_id
        )

        if success:
            return {"message": "Recomendacion marcada como vista"}
        else:
            raise HTTPException(
                status_code=404,
                detail="Recomendacion no encontrada"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marcando como vista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check-eligibility")
async def check_recommendation_eligibility(
    current_user: dict = Depends(get_current_user)
):
    """
    Verifica si el usuario puede recibir recomendaciones.

    Requiere:
    - Perfil completo (>=70% completitud)
    - Rol de estudiante o titulado

    Retorna informacion sobre el estado del perfil
    y que falta para poder recibir recomendaciones.
    """
    profile_service = get_profile_service()

    try:
        profile = profile_service.get_profile(current_user['user_id'])

        if not profile:
            return {
                'eligible': False,
                'reason': 'No tienes un perfil creado',
                'action_required': 'Sube tu CV para crear tu perfil',
                'profile_exists': False,
                'completeness_score': 0
            }

        completeness = profile_service.calculate_completeness(profile)

        # Verificar rol
        if current_user['role'] not in ['estudiante', 'titulado']:
            return {
                'eligible': False,
                'reason': 'Solo estudiantes y titulados pueden recibir recomendaciones',
                'action_required': None,
                'profile_exists': True,
                'completeness_score': completeness['score']
            }

        # Verificar completitud
        if not completeness['is_complete']:
            return {
                'eligible': False,
                'reason': 'Tu perfil no esta completo',
                'action_required': 'Completa tu perfil al menos al 70%',
                'profile_exists': True,
                'completeness_score': completeness['score'],
                'missing_fields': completeness['missing_fields'],
                'recommendations': completeness['recommendations']
            }

        # Determinar tipo de ofertas
        offer_type = 'pasantias' if current_user['role'] == 'estudiante' else 'empleos'

        return {
            'eligible': True,
            'reason': None,
            'action_required': None,
            'profile_exists': True,
            'completeness_score': completeness['score'],
            'offer_type': offer_type,
            'message': f'Puedes recibir recomendaciones de {offer_type}'
        }

    except Exception as e:
        logger.error(f"Error verificando elegibilidad: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_my_recommendation_stats(
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene estadisticas de recomendaciones del usuario.

    Incluye:
    - Total de recomendaciones recibidas
    - Recomendaciones no vistas
    - Promedio de match score
    - Distribucion por clasificacion
    """
    recommendation_service = get_recommendation_service()

    try:
        history = recommendation_service.get_recommendation_history(
            user_id=current_user['user_id'],
            limit=1000,
            offset=0
        )

        recomendaciones = history['recomendaciones']

        if not recomendaciones:
            return {
                'total': 0,
                'nuevas': 0,
                'vistas': 0,
                'promedio_score': 0,
                'distribucion': {
                    'APTO': 0,
                    'CONSIDERADO': 0,
                    'NO_APTO': 0
                }
            }

        # Calcular estadisticas
        total = len(recomendaciones)
        nuevas = sum(1 for r in recomendaciones if not r.get('fue_vista', True))
        vistas = total - nuevas
        promedio_score = sum(r['match_score'] for r in recomendaciones) / total

        # Distribucion
        distribucion = {'APTO': 0, 'CONSIDERADO': 0, 'NO_APTO': 0}
        for rec in recomendaciones:
            clasificacion = rec.get('clasificacion', 'NO_APTO')
            if clasificacion in distribucion:
                distribucion[clasificacion] += 1

        return {
            'total': total,
            'nuevas': nuevas,
            'vistas': vistas,
            'promedio_score': round(promedio_score, 3),
            'distribucion': distribucion
        }

    except Exception as e:
        logger.error(f"Error obteniendo estadisticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
