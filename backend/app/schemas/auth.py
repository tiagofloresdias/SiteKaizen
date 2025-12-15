"""
Schemas Pydantic para Autenticação
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class Token(BaseModel):
    """Schema de resposta de token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Dados do token"""
    user_id: Optional[str] = None
    username: Optional[str] = None


class UserLogin(BaseModel):
    """Schema de login"""
    username: str
    password: str


class UserCreate(BaseModel):
    """Schema de criação de usuário"""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    is_admin: bool = False


class UserResponse(BaseModel):
    """Schema de resposta de usuário"""
    id: UUID
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema de atualização de usuário"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = None

