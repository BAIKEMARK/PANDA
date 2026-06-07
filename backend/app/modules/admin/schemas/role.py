from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PermissionResponse(BaseModel):
    id: str
    code: str
    name: str
    module: str
    action: str
    description: Optional[str]

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    code: str = Field(..., description="角色代码")
    name: str = Field(..., description="角色名称")
    description: Optional[str] = Field(None, description="角色说明")
    scope: str = Field("org", description="作用域")


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scope: Optional[str] = None


class RoleResponse(BaseModel):
    id: str
    code: str
    name: str
    description: Optional[str]
    scope: str
    created_at: datetime
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True


class RolePermissionAssign(BaseModel):
    permission_ids: List[str] = Field(..., description="权限ID列表")
