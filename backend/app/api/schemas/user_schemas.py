from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserUpdateRequest(BaseModel):
    """Request model for updating user account information"""
    nombre_completo: Optional[str] = None
    email: Optional[EmailStr] = None

class PasswordChangeRequest(BaseModel):
    """Request model for changing password"""
    current_password: str
    new_password: str

class UserAccountResponse(BaseModel):
    """Response model for user account information"""
    id: str
    email: str
    nombre_completo: Optional[str] = None
    rol: str
    created_at: str
    
    class Config:
        from_attributes = True
