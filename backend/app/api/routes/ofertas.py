"""
Ofertas Routes - Sistema de Recomendaciones v2
Endpoints para gestionar ofertas laborales (admin)
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import verify_admin_role
from app.api.schemas.ml_schemas import (
    OfertaLaboralCreate,
    OfertaLaboralUpdate,
    OfertaLaboralResponse,
    OfertaLaboralListResponse
)
from app.services.oferta_service import get_oferta_service

# Configurar logging
logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/api/admin/ofertas", tags=["Admin - Ofertas"])


@router.get("", response_model=OfertaLaboralListResponse)
async def list_ofertas(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: 'pasantia' o 'empleo'"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    sector: Optional[str] = Query(None, description="Filtrar por sector"),
    include_expired: bool = Query(False, description="Incluir ofertas expiradas"),
    page: int = Query(1, ge=1, description="Numero de pagina"),
    page_size: int = Query(20, ge=1, le=100, description="Tamano de pagina"),
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Lista todas las ofertas laborales con filtros.

    Solo accesible para administradores.
    """
    oferta_service = get_oferta_service()

    try:
        result = oferta_service.list_ofertas(
            tipo=tipo,
            is_active=is_active,
            sector=sector,
            include_expired=include_expired,
            page=page,
            page_size=page_size
        )

        ofertas_response = [
            OfertaLaboralResponse(
                id=o['id'],
                institutional_profile_id=o.get('institutional_profile_id'),
                institution_name=o.get('institution_name'),
                sector=o.get('sector'),
                titulo=o['titulo'],
                descripcion=o.get('descripcion'),
                tipo=o['tipo'],
                modalidad=o.get('modalidad'),
                ubicacion=o.get('ubicacion'),
                requisitos_especificos=o.get('requisitos_especificos', {}),
                is_active=o['is_active'],
                fecha_inicio=o.get('fecha_inicio'),
                fecha_cierre=o.get('fecha_cierre'),
                cupos_disponibles=o.get('cupos_disponibles', 1),
                created_by=o.get('created_by'),
                created_at=o['created_at'],
                updated_at=o['updated_at']
            )
            for o in result['ofertas']
        ]

        return OfertaLaboralListResponse(
            ofertas=ofertas_response,
            total=result['total'],
            page=result['page'],
            page_size=result['page_size']
        )

    except Exception as e:
        logger.error(f"Error listando ofertas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{oferta_id}", response_model=OfertaLaboralResponse)
async def get_oferta(
    oferta_id: str,
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Obtiene una oferta por ID.

    Solo accesible para administradores.
    """
    oferta_service = get_oferta_service()

    try:
        oferta = oferta_service.get_oferta(oferta_id)

        if not oferta:
            raise HTTPException(
                status_code=404,
                detail="Oferta no encontrada"
            )

        return OfertaLaboralResponse(
            id=oferta['id'],
            institutional_profile_id=oferta.get('institutional_profile_id'),
            institution_name=oferta.get('institution_name'),
            sector=oferta.get('sector'),
            titulo=oferta['titulo'],
            descripcion=oferta.get('descripcion'),
            tipo=oferta['tipo'],
            modalidad=oferta.get('modalidad'),
            ubicacion=oferta.get('ubicacion'),
            requisitos_especificos=oferta.get('requisitos_especificos', {}),
            is_active=oferta['is_active'],
            fecha_inicio=oferta.get('fecha_inicio'),
            fecha_cierre=oferta.get('fecha_cierre'),
            cupos_disponibles=oferta.get('cupos_disponibles', 1),
            created_by=oferta.get('created_by'),
            created_at=oferta['created_at'],
            updated_at=oferta['updated_at']
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo oferta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=OfertaLaboralResponse, status_code=201)
async def create_oferta(
    data: OfertaLaboralCreate,
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Crea una nueva oferta laboral.

    Solo accesible para administradores.

    Campos requeridos:
    - titulo: Titulo de la oferta
    - tipo: 'pasantia' o 'empleo'

    Campos opcionales:
    - institutional_profile_id: Vincular a un perfil institucional
    - descripcion: Descripcion detallada
    - modalidad: 'presencial', 'remoto', 'hibrido'
    - ubicacion: Ubicacion geografica
    - fecha_inicio, fecha_cierre: Vigencia
    - cupos_disponibles: Numero de vacantes
    """
    oferta_service = get_oferta_service()

    try:
        oferta = oferta_service.create_oferta(
            data.model_dump(),
            created_by=admin_user['user_id']
        )

        return OfertaLaboralResponse(
            id=oferta['id'],
            institutional_profile_id=oferta.get('institutional_profile_id'),
            institution_name=oferta.get('institution_name'),
            sector=oferta.get('sector'),
            titulo=oferta['titulo'],
            descripcion=oferta.get('descripcion'),
            tipo=oferta['tipo'],
            modalidad=oferta.get('modalidad'),
            ubicacion=oferta.get('ubicacion'),
            requisitos_especificos=oferta.get('requisitos_especificos', {}),
            is_active=oferta['is_active'],
            fecha_inicio=oferta.get('fecha_inicio'),
            fecha_cierre=oferta.get('fecha_cierre'),
            cupos_disponibles=oferta.get('cupos_disponibles', 1),
            created_by=oferta.get('created_by'),
            created_at=oferta['created_at'],
            updated_at=oferta['updated_at']
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creando oferta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{oferta_id}", response_model=OfertaLaboralResponse)
async def update_oferta(
    oferta_id: str,
    data: OfertaLaboralUpdate,
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Actualiza una oferta existente.

    Solo accesible para administradores.
    """
    oferta_service = get_oferta_service()

    try:
        update_dict = data.model_dump(exclude_none=True)

        if not update_dict:
            raise HTTPException(
                status_code=400,
                detail="No se proporcionaron campos para actualizar"
            )

        oferta = oferta_service.update_oferta(oferta_id, update_dict)

        return OfertaLaboralResponse(
            id=oferta['id'],
            institutional_profile_id=oferta.get('institutional_profile_id'),
            institution_name=oferta.get('institution_name'),
            sector=oferta.get('sector'),
            titulo=oferta['titulo'],
            descripcion=oferta.get('descripcion'),
            tipo=oferta['tipo'],
            modalidad=oferta.get('modalidad'),
            ubicacion=oferta.get('ubicacion'),
            requisitos_especificos=oferta.get('requisitos_especificos', {}),
            is_active=oferta['is_active'],
            fecha_inicio=oferta.get('fecha_inicio'),
            fecha_cierre=oferta.get('fecha_cierre'),
            cupos_disponibles=oferta.get('cupos_disponibles', 1),
            created_by=oferta.get('created_by'),
            created_at=oferta['created_at'],
            updated_at=oferta['updated_at']
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error actualizando oferta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{oferta_id}")
async def delete_oferta(
    oferta_id: str,
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Desactiva una oferta (soft delete).

    Solo accesible para administradores.
    La oferta no se elimina, solo se marca como inactiva.
    """
    oferta_service = get_oferta_service()

    try:
        success = oferta_service.delete_oferta(oferta_id)

        if success:
            return {
                "message": "Oferta desactivada exitosamente",
                "oferta_id": oferta_id
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="Oferta no encontrada"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error desactivando oferta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{oferta_id}/activate", response_model=OfertaLaboralResponse)
async def activate_oferta(
    oferta_id: str,
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Reactiva una oferta desactivada.

    Solo accesible para administradores.
    """
    oferta_service = get_oferta_service()

    try:
        oferta = oferta_service.activate_oferta(oferta_id)

        return OfertaLaboralResponse(
            id=oferta['id'],
            institutional_profile_id=oferta.get('institutional_profile_id'),
            institution_name=oferta.get('institution_name'),
            sector=oferta.get('sector'),
            titulo=oferta['titulo'],
            descripcion=oferta.get('descripcion'),
            tipo=oferta['tipo'],
            modalidad=oferta.get('modalidad'),
            ubicacion=oferta.get('ubicacion'),
            requisitos_especificos=oferta.get('requisitos_especificos', {}),
            is_active=oferta['is_active'],
            fecha_inicio=oferta.get('fecha_inicio'),
            fecha_cierre=oferta.get('fecha_cierre'),
            cupos_disponibles=oferta.get('cupos_disponibles', 1),
            created_by=oferta.get('created_by'),
            created_at=oferta['created_at'],
            updated_at=oferta['updated_at']
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error reactivando oferta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
async def get_ofertas_stats(
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Obtiene estadisticas de ofertas.

    Solo accesible para administradores.
    """
    oferta_service = get_oferta_service()

    try:
        stats = oferta_service.get_statistics()
        return stats

    except Exception as e:
        logger.error(f"Error obteniendo estadisticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
