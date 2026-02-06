"""
菜单服务层
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Set
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

    def _norm_id(self, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip()

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
        menu_dict = {self._norm_id(m.id): MenuResponse.model_validate(m) for m in all_menus}

        # 先清空 children，避免后续排序覆盖
        for menu in menu_dict.values():
            menu.children = []

        # 构建树形结构
        root_menus = []
        for menu in menu_dict.values():
            parent_id = self._norm_id(menu.parent_id)
            if parent_id is None:
                # 顶级菜单
                root_menus.append(menu)
            elif parent_id in menu_dict:
                # 子菜单
                parent = menu_dict[parent_id]
                parent.children.append(menu)

        # 按sort_order排序
        root_menus.sort(key=lambda x: x.sort_order)
        for menu in menu_dict.values():
            if menu.children:
                menu.children.sort(key=lambda x: x.sort_order)

        return root_menus

    def get_user_menus(self, menu_roles: List[str], permission_codes: List[str]) -> List[MenuResponse]:
        """
        根据用户角色获取可访问的菜单树

        Args:
            menu_roles: 用户角色列表（如 super_admin、org_admin、trainer 等业务角色）
            permission_codes: 用户权限编码列表

        Returns:
            菜单树形结构
        """
        # 角色规范化：将业务角色映射到菜单权限使用的基础角色枚举
        # role_menu_permissions.role 目前仅支持: student / instructor / admin
        base_role_mapping = {
            "super_admin": "admin",
            "org_admin": "admin",
            "content_editor": "instructor",
            "trainer": "instructor",
            "auditor": "student",
        }
        roles: List[str] = []
        for r in menu_roles:
            if not r:
                continue
            roles.append(r)
            # 补充映射后的基础角色，避免菜单权限表查不到
            mapped = base_role_mapping.get(r)
            if mapped and mapped not in roles:
                roles.append(mapped)

        accessible_menus: List[Menu] = []
        for role in set(roles):
            accessible_menus.extend(self.permission_repo.get_menus_by_role(role))
        if "admin" in roles and not accessible_menus:
            accessible_menus = self.menu_repo.get_enabled_menus()
        if not accessible_menus:
            return []

        all_menus = self.menu_repo.get_enabled_menus()
        menu_dict = {self._norm_id(m.id): MenuResponse.model_validate(m) for m in all_menus}

        # 先清空 children，避免后续排序覆盖
        for menu in menu_dict.values():
            menu.children = []

        accessible_ids: Set[str] = set()
        for menu in accessible_menus:
            menu_id = self._norm_id(menu.id)
            if not menu_id:
                continue
            accessible_ids.add(menu_id)
            parent_id = self._norm_id(menu.parent_id)
            while parent_id and parent_id in menu_dict:
                accessible_ids.add(parent_id)
                parent_id = self._norm_id(menu_dict[parent_id].parent_id)

        # 构建树形结构
        root_menus = []
        for menu in menu_dict.values():
            menu_id = self._norm_id(menu.id)
            if not menu_id or menu_id not in accessible_ids:
                continue
            parent_id = self._norm_id(menu.parent_id)
            menu.permission_codes = self._get_menu_permission_codes(menu.path, permission_codes)
            if parent_id is None or parent_id not in accessible_ids:
                # 顶级菜单
                root_menus.append(menu)
            elif parent_id in menu_dict:
                parent = menu_dict[parent_id]
                parent.children.append(menu)

        # 按sort_order排序
        root_menus.sort(key=lambda x: x.sort_order)
        for menu in menu_dict.values():
            if menu.children:
                menu.children.sort(key=lambda x: x.sort_order)

        return root_menus

    def _get_menu_permission_codes(self, path: Optional[str], permission_codes: List[str]) -> List[str]:
        if not path:
            return []
        mapping = {
            "/admin/organizations": "org:",
            "/admin/users": "user:",
            "/admin/classes": "class:",
            "/admin/questions": "question:",
            "/admin/certificates": "certificate:",
            "/courses": "course:",
            "/scenarios": "scenario:",
            "/evaluation": "evaluation:",
        }
        for prefix, perm_prefix in mapping.items():
            if path.startswith(prefix):
                return [code for code in permission_codes if code.startswith(perm_prefix)]
        return []

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