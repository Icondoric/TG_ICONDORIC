"""
API Dependencies - Fase 6
Dependencias de autenticacion y verificacion para endpoints
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Dict, List, Optional

from app.core.config import settings
from app.services.ml_integration_service import get_ml_service, MLIntegrationService

# Permisos por rol fijo. Formato: { moduleId: [submoduleId, ...] }
FIXED_ROLE_MODULES: Dict[str, Dict[str, List[str]]] = {
    "administrador": {
        "gestion_usuarios":         ["lista_usuarios", "nuevo_usuario"],
        "digitalizacion_perfiles":  ["subir_cv", "mi_perfil", "editar_perfil", "buscar_perfiles"],
        "oferta_laboral":           ["ver_ofertas", "nueva_oferta"],
        "perfiles_institucionales": ["ver_perfiles", "nuevo_perfil"],
        "evaluacion_perfiles":      ["correspondencia", "historial", "ranking_candidatos"],
        "informes_reportes":        ["resumen_general", "reporte_usuarios", "reporte_ofertas", "reporte_perfiles"],
    },
    "operador": {
        "gestion_usuarios":         ["lista_usuarios", "nuevo_usuario"],
        "digitalizacion_perfiles":  ["buscar_perfiles"],
        "oferta_laboral":           ["ver_ofertas", "nueva_oferta"],
        "perfiles_institucionales": ["ver_perfiles", "nuevo_perfil"],
        "informes_reportes":        ["resumen_general", "reporte_usuarios", "reporte_ofertas", "reporte_perfiles"],
    },
    "estudiante": {
        "digitalizacion_perfiles": ["subir_cv", "mi_perfil", "editar_perfil"],
        "evaluacion_perfiles":     ["correspondencia", "historial"],
    },
    "titulado": {
        "digitalizacion_perfiles": ["subir_cv", "mi_perfil", "editar_perfil"],
        "evaluacion_perfiles":     ["correspondencia", "historial"],
    },
}

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Obtiene el usuario actual desde el token JWT
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return {"user_id": user_id, "role": role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[dict]:
    """
    Obtiene el usuario actual si hay token, sino retorna None
    """
    if credentials is None:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None


def _is_custom_role(role: str) -> bool:
    """True si el rol no es ninguno de los 4 roles fijos del sistema."""
    return role not in ("administrador", "operador", "estudiante", "titulado")


async def verify_admin_role(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Verifica rol de administrador.
    También acepta roles personalizados válidos (creados en Gestión de Sistema).
    """
    role = current_user.get("role")
    if role == "administrador":
        return current_user
    if _is_custom_role(role) and _get_role_perms(role) is not None:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acceso denegado. Se requiere rol de administrador o rol personalizado con acceso."
    )


async def verify_operator_access(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Verifica rol de operador o administrador.
    También acepta roles personalizados válidos (creados en Gestión de Sistema).
    """
    role = current_user.get("role")
    if role in ("operador", "administrador"):
        return current_user
    if _is_custom_role(role) and _get_role_perms(role) is not None:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acceso denegado. Se requiere rol de operador, administrador o rol personalizado con acceso."
    )


async def verify_ml_model_loaded(
    ml_service: MLIntegrationService = Depends(get_ml_service)
) -> MLIntegrationService:
    """Verifica que el modelo ML este cargado"""
    if not ml_service.is_ready:
        ml_service._load_model()

        if not ml_service.is_ready:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo ML no disponible. Intente mas tarde."
            )

    return ml_service


def get_ml_service_dependency() -> MLIntegrationService:
    """Dependency injection para el servicio ML"""
    return get_ml_service()


def _get_role_perms(role: str) -> Optional[Dict[str, List[str]]]:
    """
    Retorna el dict de permisos {moduleId: [submoduleId]} para un rol.
    Para roles fijos usa FIXED_ROLE_MODULES.
    Para roles personalizados consulta la BD (síncrono via supabase client).
    Retorna None si el rol no existe.
    """
    if role in FIXED_ROLE_MODULES:
        return FIXED_ROLE_MODULES[role]

    from app.db.client import supabase
    if not supabase:
        return None
    result = supabase.table("roles_personalizados").select("modulos_permitidos").eq("nombre", role).execute()
    return result.data[0]["modulos_permitidos"] if result.data else None


def require_module_access(module_id: str, submodule_id: Optional[str] = None):
    """
    Factory que retorna una dependencia FastAPI que verifica acceso
    a un módulo y opcionalmente a un sub-módulo específico.
    Soporta roles fijos y roles personalizados.
    """
    async def _check(current_user: dict = Depends(get_current_user)) -> dict:
        role = current_user.get("role")
        perms = _get_role_perms(role)

        if perms is None or module_id not in perms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado al módulo '{module_id}'"
            )

        if submodule_id and submodule_id not in perms[module_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado al submódulo '{submodule_id}'"
            )

        return current_user

    return _check
