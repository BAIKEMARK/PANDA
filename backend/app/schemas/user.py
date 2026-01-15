"""
User Schemas
用户相关的 Pydantic 模型
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

from common.constants import UserRole


class UserBase(BaseModel):
    """用户基础模型"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.STUDENT


class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """用户登录模型"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """用户更新模型"""
    name: Optional[str] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    """用户响应模型"""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT Token响应模型"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
