"""
菜单服务层
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.modules.menu.repositories.menu_repository import (
    MenuRepository,
    RoleMenuPermissionRepository
)
from backend.app.modules.menu.schemas.menu import (
    MenuCreate,
    MenuUpdate,
    MenuResponse,
    RoleMenuPermissionCreate,
    RoleMenuPermissionUpdate,
    RoleMenuPermissionResponse
)
from backend.app.models.menu import Menu
import uuid


class MenuService:
    """菜单服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.menu_repo = MenuRepository(db)
        self.permission_repo = RoleMenuPermissionRepository(db)

    # ==================== 菜单管理 ====================

    def get_all_menus(self, skip: int = 0, limit: int = 100) -> List[MenuResponse]:
        """获取所有菜单"""
        menus = self.menu_repo.get_all(skip, limit)
        return [MenuResponse.model_validate(m) for m in menus]

    def get_menu_by_id(self, menu_id: str) -> Optional[MenuResponse]:
        """根据ID获取菜单"""
        menu = self.menu_repo.get_by_id(menu_id)
        if not menu:
            return None
        return MenuResponse.model_validate(menu)

    def get_menu_tree(self) -> List[MenuResponse]:
        """获取菜单树形结构"""
        # 获取所有启用的菜单
        all_menus = self.menu_repo.get_enabled_menus()

        # 构建菜单字典
        menu_dict = {m.id: MenuResponse.model_validate(m) for m in all_menus}

        # 构建树形结构
        root_menus = []
        for menu in menu_dict.values():
            if menu.parent_id is None:
                # 顶级菜单
                menu.children = []
                root_menus.append(menu)
            elif menu.parent_id in menu_dict:
                # 子菜单
                parent = menu_dict[menu.parent_id]
                if not parent.children:
                    parent.children = []
                parent.children.append(menu)

        # 按sort_order排序
        root_menus.sort(key=lambda x: x.sort_order)
        for menu in menu_dict.values():
            if menu.children:
                menu.children.sort(key=lambda x: x.sort_order)

        return root_menus

    def get_user_menus(self, role: str) -> List[MenuResponse]:
        """
        根据用户角色获取可访问的菜单树

        Args:
            role: 用户角色 (student/instructor/admin)

        Returns:
            菜单树形结构
        """
        # 获取角色可访问的菜单
        accessible_menus = self.permission_repo.get_menus_by_role(role)

        # 构建菜单字典
        menu_dict = {m.id: MenuResponse.model_validate(m) for m in accessible_menus}

        # 构建树形结构
        root_menus = []
        for menu in menu_dict.values():
            if menu.parent_id is None:
                # 顶级菜单
                menu.children = []
                root_menus.append(menu)
            elif menu.parent_id in menu_dict:
                # 子菜单（父菜单也在可访问列表中）
                parent = menu_dict[menu.parent_id]
                if not parent.children:
                    parent.children = []
                parent.children.append(menu)

        # 按sort_order排序
        root_menus.sort(key=lambda x: x.sort_order)
        for menu in menu_dict.values():
            if menu.children:
                menu.children.sort(key=lambda x: x.sort_order)

        return root_menus

    def create_menu(self, menu_data: MenuCreate) -> MenuResponse:
        """创建菜单"""
        data = menu_data.model_dump()
        data['id'] = data.get('id', str(uuid.uuid4()))
        menu = self.menu_repo.create(data)
        return MenuResponse.model_validate(menu)

    def update_menu(self, menu_id: str, menu_data: MenuUpdate) -> Optional[MenuResponse]:
        """更新菜单"""
        update_data = menu_data.model_dump(exclude_unset=True)
        menu = self.menu_repo.update(menu_id, update_data)
        if not menu:
            return None
        return MenuResponse.model_validate(menu)

    def delete_menu(self, menu_id: str) -> bool:
        """删除菜单"""
        return self.menu_repo.delete(menu_id)

    # ==================== 权限管理 ====================

    def get_role_permissions(self, role: str) -> List[RoleMenuPermissionResponse]:
        """获取角色的所有权限"""
        permissions = self.permission_repo.get_by_role(role)
        return [RoleMenuPermissionResponse.model_validate(p) for p in permissions]

    def create_permission(self, permission_data: RoleMenuPermissionCreate) -> RoleMenuPermissionResponse:
        """创建权限"""
        data = permission_data.model_dump()
        data['id'] = data.get('id', str(uuid.uuid4()))
        permission = self.permission_repo.create(data)
        return RoleMenuPermissionResponse.model_validate(permission)

    def update_permission(self, permission_id: str, permission_data: RoleMenuPermissionUpdate) -> Optional[RoleMenuPermissionResponse]:
        """更新权限"""
        update_data = permission_data.model_dump(exclude_unset=True)
        permission = self.permission_repo.update(permission_id, update_data)
        if not permission:
            return None
        return RoleMenuPermissionResponse.model_validate(permission)

    def delete_permission(self, permission_id: str) -> bool:
        """删除权限"""
        return self.permission_repo.delete(permission_id)

    def delete_permission_by_role_menu(self, role: str, menu_id: str) -> bool:
        """根据角色和菜单删除权限"""
        return self.permission_repo.delete_by_role_and_menu(role, menu_id)