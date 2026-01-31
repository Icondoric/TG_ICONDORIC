"""
API Dependencies - Fase 6
Dependencias de autenticacion y verificacion para endpoints
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional

from app.core.config import settings
from app.services.ml_integration_service import get_ml_service, MLIntegrationService

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Obtiene el usuario actual desde el token JWT

    Args:
        credentials: Token de autenticacion

    Returns:
        Dict con user_id y role

    Raises:
        HTTPException 401: Si el token es invalido
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

    Util para endpoints que funcionan con o sin autenticacion
    """
    if credentials is None:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None


async def verify_admin_role(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Verifica que el usuario tenga rol de administrador

    Args:
        current_user: Usuario actual

    Returns:
        Dict con user_id y role

    Raises:
        HTTPException 403: Si no es administrador
    """
    if current_user.get("role") != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requiere rol de administrador."
        )
    return current_user


async def verify_ml_model_loaded(
    ml_service: MLIntegrationService = Depends(get_ml_service)
) -> MLIntegrationService:
    """
    Verifica que el modelo ML este cargado

    Args:
        ml_service: Servicio ML

    Returns:
        Servicio ML verificado

    Raises:
        HTTPException 503: Si el modelo no esta disponible
    """
    if not ml_service.is_ready:
        # Intentar recargar
        ml_service._load_model()

        if not ml_service.is_ready:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo ML no disponible. Intente mas tarde."
            )

    return ml_service


def get_ml_service_dependency() -> MLIntegrationService:
    """
    Dependency injection para el servicio ML
    """
    return get_ml_service()
