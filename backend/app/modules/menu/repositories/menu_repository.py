"""
菜单数据访问层
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.models.menu import Menu, RoleMenuPermission


class MenuRepository:
    """菜单数据访问类"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Menu]:
        """获取所有菜单"""
        return self.db.query(Menu).offset(skip).limit(limit).all()

    def get_by_id(self, menu_id: str) -> Optional[Menu]:
        """根据ID获取菜单"""
        return self.db.query(Menu).filter(Menu.id == menu_id).first()

    def get_by_parent_id(self, parent_id: Optional[str]) -> List[Menu]:
        """根据父菜单ID获取子菜单"""
        if parent_id is None:
            return self.db.query(Menu).filter(Menu.parent_id.is_(None)).all()
        return self.db.query(Menu).filter(Menu.parent_id == parent_id).all()

    def get_enabled_menus(self) -> List[Menu]:
        """获取所有启用的菜单"""
        return self.db.query(Menu).filter(Menu.is_enabled == True).all()

    def get_visible_menus(self) -> List[Menu]:
        """获取所有可见的菜单"""
        return self.db.query(Menu).filter(
            Menu.is_visible == True,
            Menu.is_enabled == True
        ).all()

    def create(self, menu_data: dict) -> Menu:
        """创建菜单"""
        db_menu = Menu(**menu_data)
        self.db.add(db_menu)
        self.db.commit()
        self.db.refresh(db_menu)
        return db_menu

    def update(self, menu_id: str, menu_data: dict) -> Optional[Menu]:
        """更新菜单"""
        db_menu = self.get_by_id(menu_id)
        if not db_menu:
            return None
        for key, value in menu_data.items():
            if hasattr(db_menu, key) and value is not None:
                setattr(db_menu, key, value)
        self.db.commit()
        self.db.refresh(db_menu)
        return db_menu

    def delete(self, menu_id: str) -> bool:
        """删除菜单"""
        db_menu = self.get_by_id(menu_id)
        if not db_menu:
            return False
        self.db.delete(db_menu)
        self.db.commit()
        return True


class RoleMenuPermissionRepository:
    """角色菜单权限数据访问类"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_role(self, role: str) -> List[RoleMenuPermission]:
        """根据角色获取所有权限"""
        return self.db.query(RoleMenuPermission).filter(
            RoleMenuPermission.role == role
        ).all()

    def get_by_menu(self, menu_id: str) -> List[RoleMenuPermission]:
        """根据菜单获取所有角色权限"""
        return self.db.query(RoleMenuPermission).filter(
            RoleMenuPermission.menu_id == menu_id
        ).all()

    def get_by_role_and_menu(self, role: str, menu_id: str) -> Optional[RoleMenuPermission]:
        """根据角色和菜单获取权限"""
        return self.db.query(RoleMenuPermission).filter(
            RoleMenuPermission.role == role,
            RoleMenuPermission.menu_id == menu_id
        ).first()

    def get_menus_by_role(self, role: str) -> List[Menu]:
        """根据角色获取可访问的菜单"""
        return self.db.query(Menu).join(
            RoleMenuPermission,
            Menu.id == RoleMenuPermission.menu_id
        ).filter(
            RoleMenuPermission.role == role,
            RoleMenuPermission.can_view == True,
            Menu.is_enabled == True,
            Menu.is_visible == True
        ).order_by(Menu.sort_order).all()

    def create(self, permission_data: dict) -> RoleMenuPermission:
        """创建权限"""
        db_permission = RoleMenuPermission(**permission_data)
        self.db.add(db_permission)
        self.db.commit()
        self.db.refresh(db_permission)
        return db_permission

    def update(self, permission_id: str, permission_data: dict) -> Optional[RoleMenuPermission]:
        """更新权限"""
        db_permission = self.db.query(RoleMenuPermission).filter(
            RoleMenuPermission.id == permission_id
        ).first()
        if not db_permission:
            return None
        for key, value in permission_data.items():
            if hasattr(db_permission, key) and value is not None:
                setattr(db_permission, key, value)
        self.db.commit()
        self.db.refresh(db_permission)
        return db_permission

    def delete(self, permission_id: str) -> bool:
        """删除权限"""
        db_permission = self.db.query(RoleMenuPermission).filter(
            RoleMenuPermission.id == permission_id
        ).first()
        if not db_permission:
            return False
        self.db.delete(db_permission)
        self.db.commit()
        return True

    def delete_by_role_and_menu(self, role: str, menu_id: str) -> bool:
        """根据角色和菜单删除权限"""
        db_permission = self.get_by_role_and_menu(role, menu_id)
        if not db_permission:
            return False
        self.db.delete(db_permission)
        self.db.commit()
        return True