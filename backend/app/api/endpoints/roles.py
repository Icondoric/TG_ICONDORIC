from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user, verify_admin_role
from app.api.schemas.role_schemas import RoleCreateRequest, RoleUpdateRequest, RoleResponse
from app.db.client import supabase

router = APIRouter()


@router.get("/", response_model=list[RoleResponse])
async def list_roles(
    current_user: dict = Depends(verify_admin_role)
):
    """Listar todos los roles personalizados."""
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        response = supabase.table("roles_personalizados").select("*").order("created_at", desc=False).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando roles: {str(e)}")


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreateRequest,
    current_user: dict = Depends(verify_admin_role)
):
    """Crear un nuevo rol personalizado."""
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        # Check name uniqueness
        check = supabase.table("roles_personalizados").select("id").eq("nombre", role_data.nombre).execute()
        if check.data:
            raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")

        new_role = {
            "nombre": role_data.nombre,
            "descripcion": role_data.descripcion,
            "modulos_permitidos": role_data.modulos_permitidos,
        }
        response = supabase.table("roles_personalizados").insert(new_role).execute()
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando rol: {str(e)}")


@router.get("/by-name/{role_name}")
async def get_role_by_name(
    role_name: str,
    current_user: dict = Depends(get_current_user)
):
    """Obtener módulos permitidos de un rol por nombre (para cualquier usuario autenticado)."""
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        response = supabase.table("roles_personalizados").select("modulos_permitidos").eq("nombre", role_name).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return {"modulos_permitidos": response.data[0]["modulos_permitidos"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo rol: {str(e)}")


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: str,
    current_user: dict = Depends(verify_admin_role)
):
    """Obtener detalle de un rol personalizado."""
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        response = supabase.table("roles_personalizados").select("*").eq("id", role_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo rol: {str(e)}")


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: str,
    role_data: RoleUpdateRequest,
    current_user: dict = Depends(verify_admin_role)
):
    """Editar un rol personalizado."""
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")

    data = role_data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    try:
        # If renaming, check uniqueness
        if "nombre" in data:
            check = supabase.table("roles_personalizados").select("id").eq("nombre", data["nombre"]).neq("id", role_id).execute()
            if check.data:
                raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")

        response = supabase.table("roles_personalizados").update(data).eq("id", role_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando rol: {str(e)}")


@router.delete("/{role_id}")
async def delete_role(
    role_id: str,
    current_user: dict = Depends(verify_admin_role)
):
    """Eliminar un rol personalizado."""
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")

    try:
        response = supabase.table("roles_personalizados").delete().eq("id", role_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return {"message": "Rol eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando rol: {str(e)}")
