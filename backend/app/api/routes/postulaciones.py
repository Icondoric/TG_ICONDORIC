"""
Postulaciones Routes - Correspondencia entre Perfiles
Endpoints para que estudiantes y titulados postulen a ofertas laborales.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.db.client import supabase
from app.services.postulacion_service import get_postulacion_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/postulaciones", tags=["Postulaciones"])


@router.get("/convocatorias")
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


@router.post("/{oferta_id}/desde-recomendacion")
async def postular_desde_recomendacion(
    oferta_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Registra una postulación copiando los datos de la recomendación existente.
    No re-evalúa el CV — usa el match ya calculado por el sistema.
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

    user_id = current_user['user_id']

    # Buscar recomendación existente para este usuario+oferta
    rec = supabase.table("recomendaciones") \
        .select("*") \
        .eq("usuario_id", user_id) \
        .eq("oferta_id", oferta_id) \
        .limit(1) \
        .execute()

    if not rec.data:
        raise HTTPException(status_code=404, detail="No existe una recomendación para esta oferta")

    r = rec.data[0]

    data = {
        'usuario_id': user_id,
        'oferta_id':  oferta_id,
        'match_score':    r.get('match_score'),
        'clasificacion':  r.get('clasificacion'),
        'scores_detalle': r.get('scores_detalle'),
        'fortalezas':     r.get('fortalezas'),
        'debilidades':    r.get('debilidades'),
        'match_details':  r.get('match_details'),
        'estado':         'pendiente',
        'updated_at':     datetime.utcnow().isoformat(),
    }

    try:
        saved = supabase.table("postulaciones") \
            .upsert(data, on_conflict="usuario_id,oferta_id") \
            .execute()

        row = saved.data[0] if saved.data else {}

        # Obtener datos de la oferta para devolver al frontend
        oferta_row = supabase.table("convocatorias_laborales") \
            .select("*, institutional_profiles(institution_name, sector)") \
            .eq("id", oferta_id) \
            .limit(1) \
            .execute()

        oferta = {}
        if oferta_row.data:
            oferta = oferta_row.data[0]
            inst = oferta.pop("institutional_profiles", None) or {}
            oferta["institution_name"] = inst.get("institution_name")
            oferta["sector"] = inst.get("sector")

        return {
            **data,
            'id':         row.get('id'),
            'created_at': row.get('created_at'),
            'oferta':     oferta,
        }

    except Exception as e:
        logger.error(f"Error guardando postulacion desde recomendacion {oferta_id}: {e}")
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
