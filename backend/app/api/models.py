from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    rol: str # "estudiante", "titulado", "administrador"
    nombre_completo: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    rol: str
    nombre_completo: str | None = None
    email: str | None = None
