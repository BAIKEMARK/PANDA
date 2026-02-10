from sqlalchemy.orm import Session
from typing import List, Optional, Set
from sqlalchemy import and_

from backend.app.models.organization import Role, Permission, RolePermission, UserOrganization
from backend.app.models.user import User


class PermissionService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_permissions(self, user_id: str, org_id: Optional[str] = None) -> Set[str]:
        if self.is_super_admin(user_id) or self._is_admin_user(user_id):
            return self._get_all_permission_codes()
        
        query = self.db.query(Permission.code).join(
            RolePermission, Permission.id == RolePermission.permission_id
        ).join(
            Role, RolePermission.role_id == Role.id
        ).join(
            UserOrganization, Role.id == UserOrganization.role_id
        ).filter(
            UserOrganization.user_id == user_id,
            UserOrganization.status == 'active'
        )
        
        if org_id:
            query = query.filter(UserOrganization.org_id == org_id)
        
        return {perm[0] for perm in query.all()}

    def has_permission(self, user_id: str, permission_code: str, org_id: Optional[str] = None) -> bool:
        if self.is_super_admin(user_id) or self._is_admin_user(user_id):
            return True
        
        permissions = self.get_user_permissions(user_id, org_id)
        return permission_code in permissions

    def is_super_admin(self, user_id: str) -> bool:
        user_org = self.db.query(UserOrganization).join(
            Role, UserOrganization.role_id == Role.id
        ).filter(
            UserOrganization.user_id == user_id,
            UserOrganization.status == 'active',
            Role.code == 'super_admin'
        ).first()
        
        return user_org is not None

    def user_belongs_to_org(self, user_id: str, org_id: str) -> bool:
        if self.is_super_admin(user_id) or self._is_admin_user(user_id):
            return True
        user_org = self.db.query(UserOrganization).filter(
            UserOrganization.user_id == user_id,
            UserOrganization.org_id == org_id,
            UserOrganization.status == 'active'
        ).first()
        
        return user_org is not None

    def get_user_orgs(self, user_id: str) -> List[str]:
        if self.is_super_admin(user_id) or self._is_admin_user(user_id):
            from backend.app.models.organization import Organization
            orgs = self.db.query(Organization.id).all()
            return [org[0] for org in orgs]
        
        user_orgs = self.db.query(UserOrganization.org_id).filter(
            UserOrganization.user_id == user_id,
            UserOrganization.status == 'active'
        ).all()
        
        return [org[0] for org in user_orgs]

    def _get_all_permission_codes(self) -> Set[str]:
        perms = self.db.query(Permission.code).all()
        return {perm[0] for perm in perms}

    def _is_admin_user(self, user_id: str) -> bool:
        """兼容旧数据：user.role 为基础角色枚举时，视为管理员."""
        user = self.db.query(User).filter(User.id == user_id).first()
        return bool(user and user.role in ("admin", "instructor"))
