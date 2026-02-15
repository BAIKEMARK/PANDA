"""
用户相关的 Pydantic 模型
"""
from pydantic import BaseModel, EmailStr, Field, field_serializer
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserRole:
    """用户角色枚举"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class UserBase(BaseModel):
    """用户基础模型"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: str = UserRole.STUDENT
    org_id: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    employee_id: Optional[str] = None


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
    role: Optional[str] = None
    org_id: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    employee_id: Optional[str] = None


class UserResponse(UserBase):
    """用户响应模型"""
    id: str
    created_at: datetime
    roles: List[str] = []
    org_ids: List[str] = []
    organizations: List[Dict[str, Any]] = []  # 机构信息列表 [{id, name, short_name}]
    permission_codes: List[str] = []

    @field_serializer('organizations')
    def serialize_organizations(self, organizations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """确保organizations字段被正确序列化"""
        if not organizations:
            return []
        return organizations

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT Token响应模型"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenResponse(BaseModel):
    """Token响应（用于登录）"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class PasswordChange(BaseModel):
    """修改密码请求"""
    old_password: str
    new_password: str
