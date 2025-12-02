"""
Schemas de Usuario (Pydantic)
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


# ========== Base ==========
class UserBase(BaseModel):
    """Schema base de usuario"""
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=100)
    role: UserRole = UserRole.VIEWER
    is_active: bool = True


# ========== Create ==========
class UserCreate(UserBase):
    """Schema para crear usuario"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


# ========== Update ==========
class UserUpdate(BaseModel):
    """Schema para actualizar usuario"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6)


# ========== Response ==========
class UserResponse(UserBase):
    """Schema de respuesta de usuario"""
    id: int
    username: str
    is_superuser: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ========== Login ==========
class UserLogin(BaseModel):
    """Schema para login"""
    username: str
    password: str


class Token(BaseModel):
    """Schema de token de acceso"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema de datos del token"""
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None