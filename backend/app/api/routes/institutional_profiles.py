"""
Institutional Profiles CRUD Endpoints - Fase 6
Endpoints administrativos para gestion de perfiles institucionales
"""

import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.db.client import supabase
from app.api.schemas.ml_schemas import (
    InstitutionalProfileCreate,
    InstitutionalProfileUpdate,
    InstitutionalProfileResponse,
    InstitutionalProfileListResponse
)
from app.api.dependencies import verify_admin_role, get_ml_service_dependency
from app.services.ml_integration_service import MLIntegrationService

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()


def check_database():
    """Verifica que la base de datos este disponible"""
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos no configurada"
        )


@router.get(
    "/institutional-profiles",
    response_model=InstitutionalProfileListResponse,
    summary="Listar perfiles institucionales",
    description="Lista todos los perfiles institucionales (solo admin)"
)
async def list_institutional_profiles(
    include_inactive: bool = False,
    sector: str = None,
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Lista todos los perfiles institucionales
    """
    check_database()

    try:
        query = supabase.table("institutional_profiles").select("*")

        if not include_inactive:
            query = query.eq("is_active", True)

        if sector:
            query = query.eq("sector", sector)

        query = query.order("created_at", desc=True)
        response = query.execute()

        profiles = [
            InstitutionalProfileResponse(
                id=str(p['id']),
                institution_name=p['institution_name'],
                sector=p['sector'],
                description=p.get('description'),
                weights=p.get('weights', {}),
                requirements=p.get('requirements', {}),
                thresholds=p.get('thresholds', {'apto': 0.70, 'considerado': 0.50}),
                is_active=p.get('is_active', True),
                created_at=p['created_at'],
                updated_at=p['updated_at'],
                created_by=str(p.get('created_by')) if p.get('created_by') else None
            )
            for p in response.data
        ]

        return InstitutionalProfileListResponse(
            profiles=profiles,
            total=len(profiles)
        )

    except Exception as e:
        logger.error(f"Error listando perfiles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo perfiles: {str(e)}"
        )


@router.get(
    "/institutional-profiles/{profile_id}",
    response_model=InstitutionalProfileResponse,
    summary="Obtener perfil institucional",
    description="Obtiene un perfil institucional por ID (solo admin)"
)
async def get_institutional_profile(
    profile_id: str,
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Obtiene un perfil institucional especifico
    """
    check_database()

    try:
        response = supabase.table("institutional_profiles") \
            .select("*") \
            .eq("id", profile_id) \
            .execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perfil no encontrado: {profile_id}"
            )

        p = response.data[0]

        return InstitutionalProfileResponse(
            id=str(p['id']),
            institution_name=p['institution_name'],
            sector=p['sector'],
            description=p.get('description'),
            weights=p.get('weights', {}),
            requirements=p.get('requirements', {}),
            thresholds=p.get('thresholds', {'apto': 0.70, 'considerado': 0.50}),
            is_active=p.get('is_active', True),
            created_at=p['created_at'],
            updated_at=p['updated_at'],
            created_by=str(p.get('created_by')) if p.get('created_by') else None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo perfil {profile_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo perfil: {str(e)}"
        )


@router.post(
    "/institutional-profiles",
    response_model=InstitutionalProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear perfil institucional",
    description="Crea un nuevo perfil institucional (solo admin)"
)
async def create_institutional_profile(
    profile: InstitutionalProfileCreate,
    admin_user: dict = Depends(verify_admin_role),
    ml_service: MLIntegrationService = Depends(get_ml_service_dependency)
):
    """
    Crea un nuevo perfil institucional
    """
    check_database()

    try:
        # Verificar que el nombre no exista
        existing = supabase.table("institutional_profiles") \
            .select("id") \
            .eq("institution_name", profile.institution_name) \
            .execute()

        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un perfil con el nombre: {profile.institution_name}"
            )

        # Preparar datos
        now = datetime.utcnow().isoformat()
        data = {
            'institution_name': profile.institution_name,
            'sector': profile.sector,
            'description': profile.description,
            'weights': profile.weights.model_dump(),
            'requirements': profile.requirements.model_dump(),
            'thresholds': profile.thresholds.model_dump() if profile.thresholds else {
                'apto': 0.70,
                'considerado': 0.50
            },
            'is_active': True,
            'created_at': now,
            'updated_at': now,
            'created_by': admin_user['user_id']
        }

        # Insertar
        response = supabase.table("institutional_profiles").insert(data).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creando perfil"
            )

        # Invalidar cache
        ml_service.invalidate_cache()

        p = response.data[0]
        logger.info(f"Perfil creado: {p['id']} - {profile.institution_name}")

        return InstitutionalProfileResponse(
            id=str(p['id']),
            institution_name=p['institution_name'],
            sector=p['sector'],
            description=p.get('description'),
            weights=p.get('weights', {}),
            requirements=p.get('requirements', {}),
            thresholds=p.get('thresholds', {'apto': 0.70, 'considerado': 0.50}),
            is_active=p.get('is_active', True),
            created_at=p['created_at'],
            updated_at=p['updated_at'],
            created_by=str(p.get('created_by')) if p.get('created_by') else None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creando perfil: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creando perfil: {str(e)}"
        )


@router.put(
    "/institutional-profiles/{profile_id}",
    response_model=InstitutionalProfileResponse,
    summary="Actualizar perfil institucional",
    description="Actualiza un perfil institucional existente (solo admin)"
)
async def update_institutional_profile(
    profile_id: str,
    profile: InstitutionalProfileUpdate,
    admin_user: dict = Depends(verify_admin_role),
    ml_service: MLIntegrationService = Depends(get_ml_service_dependency)
):
    """
    Actualiza un perfil institucional existente
    """
    check_database()

    try:
        # Verificar que existe
        existing = supabase.table("institutional_profiles") \
            .select("*") \
            .eq("id", profile_id) \
            .execute()

        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perfil no encontrado: {profile_id}"
            )

        # Verificar nombre unico si se esta cambiando
        if profile.institution_name:
            name_check = supabase.table("institutional_profiles") \
                .select("id") \
                .eq("institution_name", profile.institution_name) \
                .neq("id", profile_id) \
                .execute()

            if name_check.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro perfil con el nombre: {profile.institution_name}"
                )

        # Preparar datos a actualizar
        update_data = {'updated_at': datetime.utcnow().isoformat()}

        if profile.institution_name is not None:
            update_data['institution_name'] = profile.institution_name
        if profile.sector is not None:
            update_data['sector'] = profile.sector
        if profile.description is not None:
            update_data['description'] = profile.description
        if profile.weights is not None:
            update_data['weights'] = profile.weights.model_dump()
        if profile.requirements is not None:
            update_data['requirements'] = profile.requirements.model_dump()
        if profile.thresholds is not None:
            update_data['thresholds'] = profile.thresholds.model_dump()
        if profile.is_active is not None:
            update_data['is_active'] = profile.is_active

        # Actualizar
        response = supabase.table("institutional_profiles") \
            .update(update_data) \
            .eq("id", profile_id) \
            .execute()

        # Invalidar cache
        ml_service.invalidate_cache()

        p = response.data[0]
        logger.info(f"Perfil actualizado: {profile_id}")

        return InstitutionalProfileResponse(
            id=str(p['id']),
            institution_name=p['institution_name'],
            sector=p['sector'],
            description=p.get('description'),
            weights=p.get('weights', {}),
            requirements=p.get('requirements', {}),
            thresholds=p.get('thresholds', {'apto': 0.70, 'considerado': 0.50}),
            is_active=p.get('is_active', True),
            created_at=p['created_at'],
            updated_at=p['updated_at'],
            created_by=str(p.get('created_by')) if p.get('created_by') else None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando perfil {profile_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error actualizando perfil: {str(e)}"
        )


@router.delete(
    "/institutional-profiles/{profile_id}",
    summary="Eliminar perfil institucional (soft delete)",
    description="Desactiva un perfil institucional (solo admin)"
)
async def delete_institutional_profile(
    profile_id: str,
    admin_user: dict = Depends(verify_admin_role),
    ml_service: MLIntegrationService = Depends(get_ml_service_dependency)
):
    """
    Desactiva (soft delete) un perfil institucional
    """
    check_database()

    try:
        # Verificar que existe
        existing = supabase.table("institutional_profiles") \
            .select("id, institution_name") \
            .eq("id", profile_id) \
            .execute()

        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perfil no encontrado: {profile_id}"
            )

        # Soft delete
        response = supabase.table("institutional_profiles") \
            .update({
                'is_active': False,
                'updated_at': datetime.utcnow().isoformat()
            }) \
            .eq("id", profile_id) \
            .execute()

        # Invalidar cache
        ml_service.invalidate_cache()

        logger.info(f"Perfil desactivado: {profile_id}")

        return {
            "message": "Perfil desactivado exitosamente",
            "profile_id": profile_id,
            "institution_name": existing.data[0]['institution_name']
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando perfil {profile_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error eliminando perfil: {str(e)}"
        )


@router.post(
    "/institutional-profiles/{profile_id}/activate",
    summary="Reactivar perfil institucional",
    description="Reactiva un perfil institucional desactivado (solo admin)"
)
async def activate_institutional_profile(
    profile_id: str,
    admin_user: dict = Depends(verify_admin_role),
    ml_service: MLIntegrationService = Depends(get_ml_service_dependency)
):
    """
    Reactiva un perfil institucional
    """
    check_database()

    try:
        # Verificar que existe
        existing = supabase.table("institutional_profiles") \
            .select("id, institution_name, is_active") \
            .eq("id", profile_id) \
            .execute()

        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perfil no encontrado: {profile_id}"
            )

        if existing.data[0].get('is_active'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El perfil ya esta activo"
            )

        # Reactivar
        response = supabase.table("institutional_profiles") \
            .update({
                'is_active': True,
                'updated_at': datetime.utcnow().isoformat()
            }) \
            .eq("id", profile_id) \
            .execute()

        # Invalidar cache
        ml_service.invalidate_cache()

        logger.info(f"Perfil reactivado: {profile_id}")

        return {
            "message": "Perfil reactivado exitosamente",
            "profile_id": profile_id,
            "institution_name": existing.data[0]['institution_name']
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activando perfil {profile_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error activando perfil: {str(e)}"
        )


@router.get(
    "/sectors",
    summary="Listar sectores disponibles",
    description="Lista todos los sectores de perfiles institucionales"
)
async def list_sectors(
    admin_user: dict = Depends(verify_admin_role)
):
    """
    Lista los sectores unicos de los perfiles
    """
    check_database()

    try:
        response = supabase.table("institutional_profiles") \
            .select("sector") \
            .eq("is_active", True) \
            .execute()

        sectors = list(set(p['sector'] for p in response.data))
        sectors.sort()

        return {
            "sectors": sectors,
            "total": len(sectors)
        }

    except Exception as e:
        logger.error(f"Error listando sectores: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo sectores: {str(e)}"
        )
