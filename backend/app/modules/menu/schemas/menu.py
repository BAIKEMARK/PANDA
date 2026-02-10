"""
菜单相关的 Pydantic 模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MenuBase(BaseModel):
    """菜单基础模型"""
    parent_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=100)
    icon: Optional[str] = Field(None, max_length=50)
    path: Optional[str] = Field(None, max_length=200)
    component: Optional[str] = Field(None, max_length=200)
    sort_order: int = 0
    is_visible: bool = True
    is_enabled: bool = True


class MenuCreate(MenuBase):
    """菜单创建模型"""
    id: str = Field(..., min_length=1, max_length=36)


class MenuUpdate(BaseModel):
    """菜单更新模型"""
    parent_id: Optional[str] = None
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    icon: Optional[str] = Field(None, max_length=50)
    path: Optional[str] = Field(None, max_length=200)
    component: Optional[str] = Field(None, max_length=200)
    sort_order: Optional[int] = None
    is_visible: Optional[bool] = None
    is_enabled: Optional[bool] = None


class MenuResponse(MenuBase):
    """菜单响应模型"""
    id: str
    created_at: datetime
    updated_at: datetime
    children: Optional[List['MenuResponse']] = []
    permission_codes: Optional[List[str]] = []

    class Config:
        from_attributes = True


# 递归模型支持
MenuResponse.model_rebuild()


class MenuTreeNode(MenuResponse):
    """菜单树节点（用于构建树形结构）"""
    pass


class RoleMenuPermissionBase(BaseModel):
    """角色菜单权限基础模型"""
    role: str = Field(..., pattern="^(student|instructor|admin)$")
    menu_id: str
    can_view: bool = True


class RoleMenuPermissionCreate(RoleMenuPermissionBase):
    """角色菜单权限创建模型"""
    id: str = Field(..., min_length=1, max_length=36)


class RoleMenuPermissionUpdate(BaseModel):
    """角色菜单权限更新模型"""
    can_view: Optional[bool] = None


class RoleMenuPermissionResponse(RoleMenuPermissionBase):
    """角色菜单权限响应模型"""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
