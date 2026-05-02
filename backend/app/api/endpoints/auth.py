import logging
from fastapi import APIRouter, HTTPException, status, Depends
from app.db.client import supabase
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.models import UserRegister, UserLogin, Token

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=Token)
async def register(user: UserRegister):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not configured")
        
    if user.rol not in ["estudiante", "titulado", "administrador"]:
        raise HTTPException(status_code=400, detail="Rol inválido")

    # 1. Check if email exists
    try:
        check = supabase.table("usuarios").select("id").eq("email", user.email).execute()
    except Exception as e:
        logger.error(f"Error de base de datos al verificar email: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    if check.data:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # 2. Create user
    hashed_password = get_password_hash(user.password)
    new_user_data = {
        "email": user.email,
        "password_hash": hashed_password,
        "rol": user.rol,
        "nombre_completo": user.nombre_completo
    }
    
    try:
        response = supabase.table("usuarios").insert(new_user_data).execute()
        created_user = response.data[0]
        user_id = created_user["id"]
        
        # 3. Create empty profile
        supabase.table("perfiles_profesionales").insert({"usuario_id": user_id}).execute()
        
        # 4. Generate Token
        access_token = create_access_token(user_id, user.rol)
        
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "user_id": user_id,
            "rol": user.rol,
            "nombre_completo": user.nombre_completo,
            "email": user.email
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {str(e)}")

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    if not supabase:
         raise HTTPException(status_code=500, detail="Database connection not configured")

    # 1. Get user
    try:
        response = supabase.table("usuarios").select("*").eq("email", user.email).execute()
    except Exception as e:
        logger.error(f"Error de base de datos al buscar usuario: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error de conexión con la base de datos: {str(e)}")

    if not response.data:
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")

    db_user = response.data[0]

    # 2. Verify password
    password_hash = db_user.get("password_hash")
    if not password_hash:
        logger.error(f"Usuario {user.email} no tiene password_hash en la base de datos")
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")

    try:
        if not verify_password(user.password, password_hash):
            raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verificando contraseña: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno al verificar credenciales")

    # 3. Generate Token
    try:
        access_token = create_access_token(db_user["id"], db_user["rol"])
    except Exception as e:
        logger.error(f"Error generando token: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error generando token de acceso")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(db_user["id"]),
        "rol": db_user["rol"],
        "nombre_completo": db_user.get("nombre_completo"),
        "email": db_user.get("email")
    }
