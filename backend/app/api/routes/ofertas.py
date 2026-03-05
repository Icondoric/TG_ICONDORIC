"""
Ofertas Routes - Sistema de Recomendaciones v2
Endpoints para gestionar ofertas laborales (admin)
"""

import base64
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File

from app.api.dependencies import verify_admin_role, verify_operator_access
from app.api.schemas.ml_schemas import (
    OfertaLaboralCreate,
    OfertaLaboralUpdate,
    OfertaLaboralResponse,
    OfertaLaboralListResponse
)
from app.services.oferta_service import get_oferta_service
from app.services.ml_integration_service import get_ml_service
from app.db.client import supabase

# Configurar logging
logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/api/admin/ofertas", tags=["Admin - Ofertas"])


def _oferta_to_response(o: dict) -> OfertaLaboralResponse:
    """Convierte un dict de oferta al schema de respuesta."""
    return OfertaLaboralResponse(
        id=o['id'],
        institutional_profile_id=o.get('institutional_profile_id'),
        institution_name=o.get('institution_name'),
        sector=o.get('sector'),
        titulo=o['titulo'],
        descripcion=o.get('descripcion'),
        tipo=o['tipo'],
        modalidad=o.get('modalidad'),
        ubicacion=o.get('ubicacion'),
        area=o.get('area'),
        contact_phone=o.get('contact_phone'),
        contact_email=o.get('contact_email'),
        requisitos_especificos=o.get('requisitos_especificos', {}),
        weights=o.get('weights'),
        thresholds=o.get('thresholds'),
        requirements=o.get('requirements'),
        is_active=o['is_active'],
        fecha_inicio=o.get('fecha_inicio'),
        fecha_cierre=o.get('fecha_cierre'),
        cupos_disponibles=o.get('cupos_disponibles', 1),
        created_by=o.get('created_by'),
        created_at=o['created_at'],
        updated_at=o['updated_at']
    )


@router.post("/analyze-pdf")
async def analyze_oferta_pdf(
    file: UploadFile = File(..., description="PDF de la convocatoria laboral"),
    admin_user: dict = Depends(verify_operator_access)
):
    """
    Analiza un PDF de convocatoria laboral con Gemini y retorna los campos extraídos
    para pre-rellenar el formulario de Nueva Oferta.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="El archivo excede el tamaño máximo de 10MB")

    ml_service = get_ml_service()
    try:
        pdf_base64 = base64.b64encode(contents).decode('utf-8')
        logger.info(f"Analizando PDF de oferta: {file.filename}")
        extraction = await ml_service.extract_oferta_with_gemini(pdf_base64)
        return extraction
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error analizando PDF de oferta: {e}")
        raise HTTPException(status_code=500, detail=f"Error procesando el PDF: {str(e)}")


@router.get("/contact-suggestions")
async def get_contact_suggestions(
    institution_id: str = Query(..., description="ID del perfil institucional"),
    admin_user: dict = Depends(verify_operator_access)
):
    """
    Retorna sugerencias de contacto para una institucion.

    Busca el ultimo telefono, correo y area usados en las ofertas de esa
    institucion para pre-rellenar el formulario de nueva oferta.
    """
    oferta_service = get_oferta_service()

    try:
        suggestions = oferta_service.get_contact_suggestions(institution_id)
        return suggestions
    except Exception as e:
        logger.error(f"Error obteniendo sugerencias de contacto: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=OfertaLaboralListResponse)
async def list_ofertas(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: 'pasantia' o 'empleo'"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    sector: Optional[str] = Query(None, description="Filtrar por sector"),
    include_expired: bool = Query(False, description="Incluir ofertas expiradas"),
    page: int = Query(1, ge=1, description="Numero de pagina"),
    page_size: int = Query(20, ge=1, le=100, description="Tamano de pagina"),
    admin_user: dict = Depends(verify_operator_access)
):
    """
    Lista todas las ofertas laborales con filtros.

    Solo accesible para operadores y administradores.
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

        ofertas_response = [_oferta_to_response(o) for o in result['ofertas']]

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
    admin_user: dict = Depends(verify_operator_access)
):
    """
    Obtiene una oferta por ID.

    Solo accesible para operadores y administradores.
    """
    oferta_service = get_oferta_service()

    try:
        oferta = oferta_service.get_oferta(oferta_id)

        if not oferta:
            raise HTTPException(
                status_code=404,
                detail="Oferta no encontrada"
            )

        return _oferta_to_response(oferta)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo oferta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=OfertaLaboralResponse, status_code=201)
async def create_oferta(
    data: OfertaLaboralCreate,
    admin_user: dict = Depends(verify_operator_access)
):
    """
    Crea una nueva oferta laboral.

    Solo accesible para operadores y administradores.

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

        return _oferta_to_response(oferta)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creando oferta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{oferta_id}", response_model=OfertaLaboralResponse)
async def update_oferta(
    oferta_id: str,
    data: OfertaLaboralUpdate,
    admin_user: dict = Depends(verify_operator_access)
):
    """
    Actualiza una oferta existente.

    Solo accesible para operadores y administradores.
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

        return _oferta_to_response(oferta)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error actualizando oferta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{oferta_id}")
async def delete_oferta(
    oferta_id: str,
    admin_user: dict = Depends(verify_operator_access)
):
    """
    Desactiva una oferta (soft delete).

    Solo accesible para operadores y administradores.
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


@router.delete("/{oferta_id}/permanent")
async def permanent_delete_oferta(
    oferta_id: str,
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Elimina permanentemente una oferta laboral.
    Esta accion no se puede deshacer.
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Base de datos no configurada")

    try:
        existing = supabase.table("ofertas_laborales") \
            .select("id, titulo") \
            .eq("id", oferta_id) \
            .execute()

        if not existing.data:
            raise HTTPException(status_code=404, detail="Oferta no encontrada")

        titulo = existing.data[0]['titulo']

        supabase.table("ofertas_laborales") \
            .delete() \
            .eq("id", oferta_id) \
            .execute()

        logger.info(f"Oferta eliminada permanentemente: {oferta_id} - {titulo}")

        return {
            "message": "Oferta eliminada permanentemente",
            "oferta_id": oferta_id,
            "titulo": titulo
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando oferta permanentemente {oferta_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{oferta_id}/activate", response_model=OfertaLaboralResponse)
async def activate_oferta(
    oferta_id: str,
    admin_user: dict = Depends(verify_operator_access)
):
    """
    Reactiva una oferta desactivada.

    Solo accesible para operadores y administradores.
    """
    oferta_service = get_oferta_service()

    try:
        oferta = oferta_service.activate_oferta(oferta_id)

        return _oferta_to_response(oferta)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error reactivando oferta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
async def get_ofertas_stats(
    admin_user: dict = Depends(verify_operator_access)
):
    """
    Obtiene estadisticas de ofertas.

    Solo accesible para operadores y administradores.
    """
    oferta_service = get_oferta_service()

    try:
        stats = oferta_service.get_statistics()
        return stats

    except Exception as e:
        logger.error(f"Error obteniendo estadisticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
