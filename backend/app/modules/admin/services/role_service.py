from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from backend.app.models.organization import Role, Permission, RolePermission
from backend.app.core.common.exceptions import NotFoundException, ConflictException


class RoleService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, code: str, name: str, description: Optional[str] = None, scope: str = "org") -> Role:
        """
        创建角色。
        默认分配基础“查看”权限（action = 'view'），避免新角色创建后完全无权限可用。
        """
        existing = self.db.query(Role).filter(Role.code == code).first()
        if existing:
            raise ConflictException(f"角色代码已存在: {code}")

        role = Role(
            id=str(uuid4()),
            code=code,
            name=name,
            description=description,
            scope=scope,
        )
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

        # 为新角色分配默认权限：所有 action='view' 的权限
        self._assign_default_permissions(role.id)
        # 刷新 relationship
        self.db.refresh(role)
        return role

    def get(self, role_id: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.id == role_id).first()

    def get_by_code(self, code: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.code == code).first()

    def list(self, scope: Optional[str] = None) -> List[Role]:
        query = self.db.query(Role)
        if scope:
            query = query.filter(Role.scope == scope)
        return query.all()

    def update(self, role_id: str, **kwargs) -> Role:
        role = self.get(role_id)
        if not role:
            raise NotFoundException(f"角色不存在: {role_id}")
        
        for key, value in kwargs.items():
            if hasattr(role, key) and value is not None:
                setattr(role, key, value)
        
        self.db.commit()
        self.db.refresh(role)
        return role

    def delete(self, role_id: str) -> None:
        role = self.get(role_id)
        if not role:
            raise NotFoundException(f"角色不存在: {role_id}")
        self.db.delete(role)
        self.db.commit()

    def assign_permissions(self, role_id: str, permission_ids: List[str]) -> Role:
        role = self.get(role_id)
        if not role:
            raise NotFoundException(f"角色不存在: {role_id}")
        
        self.db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        
        for perm_id in permission_ids:
            perm = self.db.query(Permission).filter(Permission.id == perm_id).first()
            if perm:
                role_perm = RolePermission(role_id=role_id, permission_id=perm_id)
                self.db.add(role_perm)
        
        self.db.commit()
        self.db.refresh(role)
        return role

    def _assign_default_permissions(self, role_id: str) -> None:
        """
        为新建角色分配默认权限：
        - 当前策略：所有 action = 'view' 的权限，保证至少有基础查看能力。
        """
        # 先清空可能存在的旧记录（理论上新角色不会有，但为了幂等）
        self.db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()

        view_perms = (
            self.db.query(Permission)
            .filter(Permission.action == "view")
            .all()
        )

        for perm in view_perms:
            self.db.add(RolePermission(role_id=role_id, permission_id=perm.id))

        self.db.commit()

    def get_permissions(self, role_id: str) -> List[Permission]:
        role = self.get(role_id)
        if not role:
            raise NotFoundException(f"角色不存在: {role_id}")
        
        return role.permissions
