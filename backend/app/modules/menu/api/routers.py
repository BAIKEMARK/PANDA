"""
菜单 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.modules.menu.schemas.menu import (
    MenuCreate, MenuUpdate, MenuResponse, MenuTreeNode,
    RoleMenuPermissionCreate, RoleMenuPermissionUpdate, RoleMenuPermissionResponse
)
from backend.app.modules.menu.services.menu_service import MenuService
from backend.app.common.exceptions import NotFoundException

router = APIRouter(prefix="/menus", tags=["菜单管理"])


# ==================== 菜单管理 ====================

@router.get("/", response_model=List[MenuResponse])
async def get_menus(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取所有菜单列表"""
    service = MenuService(db)
    return service.get_all_menus(skip, limit)


@router.get("/tree", response_model=List[MenuTreeNode])
async def get_menu_tree(db: Session = Depends(get_db)):
    """获取菜单树形结构（仅返回启用的菜单）"""
    service = MenuService(db)
    return service.get_menu_tree()


@router.get("/user", response_model=List[MenuResponse])
async def get_user_menus(
    role: str = Query(..., description="用户角色 (student/instructor/admin)"),
    db: Session = Depends(get_db)
):
    """
    根据用户角色获取可访问的菜单树

    前端调用示例：
    GET /api/menus/user?role=student
    """
    if role not in ['student', 'instructor', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的角色，必须是 student、instructor 或 admin"
        )

    service = MenuService(db)
    return service.get_user_menus(role)


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(
    menu_id: str,
    db: Session = Depends(get_db)
):
    """获取菜单详情"""
    service = MenuService(db)
    menu = service.get_menu_by_id(menu_id)
    if not menu:
        raise NotFoundException("菜单不存在")
    return menu


@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_data: MenuCreate,
    db: Session = Depends(get_db)
):
    """创建新菜单"""
    service = MenuService(db)
    return service.create_menu(menu_data)


@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: str,
    menu_data: MenuUpdate,
    db: Session = Depends(get_db)
):
    """更新菜单"""
    service = MenuService(db)
    menu = service.update_menu(menu_id, menu_data)
    if not menu:
        raise NotFoundException("菜单不存在")
    return menu


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(
    menu_id: str,
    db: Session = Depends(get_db)
):
    """删除菜单（会级联删除子菜单和权限）"""
    service = MenuService(db)
    success = service.delete_menu(menu_id)
    if not success:
        raise NotFoundException("菜单不存在")
    return None


# ==================== 权限管理 ====================

@router.get("/permissions/{role}", response_model=List[RoleMenuPermissionResponse])
async def get_role_permissions(
    role: str,
    db: Session = Depends(get_db)
):
    """获取指定角色的所有菜单权限"""
    if role not in ['student', 'instructor', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的角色"
        )

    service = MenuService(db)
    return service.get_role_permissions(role)


@router.post("/permissions", response_model=RoleMenuPermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_data: RoleMenuPermissionCreate,
    db: Session = Depends(get_db)
):
    """创建角色菜单权限"""
    service = MenuService(db)
    return service.create_permission(permission_data)


@router.put("/permissions/{permission_id}", response_model=RoleMenuPermissionResponse)
async def update_permission(
    permission_id: str,
    permission_data: RoleMenuPermissionUpdate,
    db: Session = Depends(get_db)
):
    """更新角色菜单权限"""
    service = MenuService(db)
    permission = service.update_permission(permission_id, permission_data)
    if not permission:
        raise NotFoundException("权限不存在")
    return permission


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    permission_id: str,
    db: Session = Depends(get_db)
):
    """删除角色菜单权限"""
    service = MenuService(db)
    success = service.delete_permission(permission_id)
    if not success:
        raise NotFoundException("权限不存在")
    return None


@router.delete("/permissions/{role}/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission_by_role_menu(
    role: str,
    menu_id: str,
    db: Session = Depends(get_db)
):
    """根据角色和菜单删除权限"""
    service = MenuService(db)
    success = service.delete_permission_by_role_menu(role, menu_id)
    if not success:
        raise NotFoundException("权限不存在")
    return None