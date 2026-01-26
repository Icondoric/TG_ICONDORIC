from fastapi import APIRouter, HTTPException, status, Depends
from app.db.client import supabase
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.models import UserRegister, UserLogin, Token

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserRegister):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not configured")
        
    if user.rol not in ["estudiante", "titulado", "administrador"]:
        raise HTTPException(status_code=400, detail="Rol inválido")

    # 1. Check if email exists
    try:
        # Supabase select
        check = supabase.table("usuarios").select("id").eq("email", user.email).execute()
        if check.data:
            raise HTTPException(status_code=400, detail="Email ya registrado")
    except Exception as e:
         # If table doesn't exist or connection fails
         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

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
        if not response.data:
             raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
        
        db_user = response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar usuario: {str(e)}")
        
    # 2. Verify password
    if not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
        
    # 3. Generate Token
    access_token = create_access_token(db_user["id"], db_user["rol"])
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": db_user["id"],
        "rol": db_user["rol"],
        "nombre_completo": db_user.get("nombre_completo"),
        "email": db_user.get("email")
    }
