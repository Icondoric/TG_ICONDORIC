from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from datetime import datetime

from app.api.dependencies import get_current_user, verify_admin_role
from app.db.client import supabase
from app.api.schemas.ml_schemas import (
    UsuariosListResponse, 
    UsuarioAdminResponse, 
    PerfilProfesionalResponse
)
from app.services.profile_service import get_profile_service

router = APIRouter()

@router.get("/", response_model=UsuariosListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: Optional[str] = None,
    search: Optional[str] = None,
    current_user: dict = Depends(verify_admin_role)
):
    """
    Listar usuarios con paginacion y filtros.
    Solo para administradores.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        # Construct query
        query = supabase.table("usuarios").select("*", count="exact")
        
        # Apply filters
        if role:
            query = query.eq("rol", role)
        
        if search:
            # Search by email or full name
            query = query.or_(f"email.ilike.%{search}%,nombre_completo.ilike.%{search}%")
            
        # Pagination
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        query = query.range(start, end).order("created_at", desc=True)
        
        # Execute
        response = query.execute()
        
        users_data = []
        for user in response.data:
            # Check profile status for each user
            # Optimization: Try to batch fetch profiles later if performance is an issue
            # For now, fetching one by one is simpler but slower
            
            # Get profile info lightly
            profile_query = supabase.table("perfiles_profesionales") \
                .select("id, is_complete, completeness_score, cv_uploaded_at") \
                .eq("usuario_id", user['id']) \
                .execute()
            
            has_profile = False
            is_complete = False
            completeness_score = 0
            cv_uploaded_at = None
            
            if profile_query.data:
                p_data = profile_query.data[0]
                has_profile = True
                is_complete = p_data.get('is_complete', False)
                completeness_score = p_data.get('completeness_score', 0)
                cv_uploaded_at = p_data.get('cv_uploaded_at')

            users_data.append(UsuarioAdminResponse(
                id=user['id'],
                email=user['email'],
                nombre_completo=user.get('nombre_completo'),
                rol=user['rol'],
                created_at=user['created_at'],
                tiene_perfil=has_profile,
                perfil_completo=is_complete,
                completeness_score=float(completeness_score),
                cv_uploaded_at=cv_uploaded_at
            ))
            
        return UsuariosListResponse(
            usuarios=users_data,
            total=response.count,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        print(f"Error listing users: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing users: {str(e)}")

@router.get("/{user_id}", response_model=UsuarioAdminResponse)
async def get_user_detail(
    user_id: str,
    current_user: dict = Depends(verify_admin_role)
):
    """
    Obtener detalle de un usuario.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        # Get user
        response = supabase.table("usuarios").select("*").eq("id", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
            
        user = response.data[0]
        
        # Get profile status
        profile_query = supabase.table("perfiles_profesionales") \
            .select("id, is_complete, completeness_score, cv_uploaded_at") \
            .eq("usuario_id", user['id']) \
            .execute()
            
        has_profile = False
        is_complete = False
        completeness_score = 0
        cv_uploaded_at = None
        
        if profile_query.data:
            p_data = profile_query.data[0]
            has_profile = True
            is_complete = p_data.get('is_complete', False)
            completeness_score = p_data.get('completeness_score', 0)
            cv_uploaded_at = p_data.get('cv_uploaded_at')

        return UsuarioAdminResponse(
            id=user['id'],
            email=user['email'],
            nombre_completo=user.get('nombre_completo'),
            rol=user['rol'],
            created_at=user['created_at'],
            tiene_perfil=has_profile,
            perfil_completo=is_complete,
            completeness_score=float(completeness_score),
            cv_uploaded_at=cv_uploaded_at
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting user: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting user: {str(e)}")

@router.get("/{user_id}/profile", response_model=PerfilProfesionalResponse)
async def get_user_profile_full(
    user_id: str,
    current_user: dict = Depends(verify_admin_role)
):
    """
    Obtener el perfil profesional completo de un usuario (para ver aptitudes).
    """
    profile_service = get_profile_service()
    
    try:
        profile = profile_service.get_profile(user_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found for this user")
            
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
        print(f"Error getting user profile: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting user profile: {str(e)}")

@router.put("/{user_id}")
async def update_user(
    user_id: str,
    user_update: dict,
    current_user: dict = Depends(verify_admin_role)
):
    """
    Actualizar datos básicos de usuario (rol, nombre).
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")

    # Filter allowed fields
    allowed_fields = ['rol', 'nombre_completo']
    data = {k: v for k, v in user_update.items() if k in allowed_fields}
    
    if not data:
         raise HTTPException(status_code=400, detail="No valid fields to update")

    try:
        response = supabase.table("usuarios").update(data).eq("id", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
            
        return {"message": "User updated successfully", "user": response.data[0]}
        
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(verify_admin_role)
):
    """
    Eliminar usuario (Caution: Physical delete).
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")
        
    if user_id == current_user['user_id']:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    try:
        # Supabase should handle cascade usually, but let's be safe
        # Delete profile first
        supabase.table("perfiles_profesionales").delete().eq("usuario_id", user_id).execute()
        
        # Delete user
        response = supabase.table("usuarios").delete().eq("id", user_id).execute()
        
        if not response.data:
             raise HTTPException(status_code=404, detail="User not found")
             
        return {"message": "User deleted successfully"}
        
    except Exception as e:
        print(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
