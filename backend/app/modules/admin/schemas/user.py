from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class UserOrgAssign(BaseModel):
    org_id: str = Field(..., description="机构ID")
    role_id: str = Field(..., description="角色ID")


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    org_id: Optional[str]
    phone: Optional[str]
    department: Optional[str]
    title: Optional[str]
    employee_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="邮箱")
    name: str = Field(..., description="姓名")
    password: str = Field(..., min_length=6, description="密码")
    role: str = Field("student", description="角色")
    org_id: Optional[str] = Field(None, description="默认机构ID")
    phone: Optional[str] = Field(None, description="手机号")
    department: Optional[str] = Field(None, description="科室")
    title: Optional[str] = Field(None, description="职称")
    employee_id: Optional[str] = Field(None, description="工号")


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    employee_id: Optional[str] = None
    org_id: Optional[str] = None
    role: Optional[str] = None


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    skip: int
    limit: int
