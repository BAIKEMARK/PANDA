"""
认证服务 - 处理登录、JWT等认证逻辑
"""
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.app.models.user import User
from backend.app.models.organization import Role, UserOrganization
from backend.app.modules.auth.services.user_service import UserService
from backend.app.core.config.security import verify_password, create_access_token, decode_access_token
from backend.app.core.common.exceptions import UnauthorizedException
from backend.app.modules.admin.services.permission_service import PermissionService


class AuthService:
    """认证服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        验证用户凭据

        Args:
            email: 用户邮箱
            password: 密码

        Returns:
            验证成功返回用户对象，失败返回 None
        """
        user = self.user_service.get_user_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    def login(self, email: str, password: str) -> Optional[str]:
        """
        用户登录

        Args:
            email: 用户邮箱
            password: 密码

        Returns:
            成功返回JWT token，失败返回 None
        """
        user = self.authenticate(email, password)
        if not user:
            return None

        return create_access_token(data={"sub": user.id})

    def get_current_user(self, token: str) -> Optional[User]:
        """
        根据JWT token获取当前用户

        Args:
            token: JWT token

        Returns:
            用户对象，无效token返回 None
        """
        payload = decode_access_token(token)
        if payload is None:
            raise UnauthorizedException("无效的认证凭据")

        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException("无效的认证凭据")

        user = self.user_service.get_user(user_id)
        if user is None:
            raise UnauthorizedException("用户不存在")

        return self._enrich_user(user)

    def enrich_user(self, user: User) -> User:
        return self._enrich_user(user)

    def _enrich_user(self, user: User) -> User:
        permission_service = PermissionService(self.db)
        roles = self._get_user_roles(user.id)
        if user.role and user.role not in roles:
            roles.append(user.role)
        user.roles = roles
        user.org_ids = permission_service.get_user_orgs(user.id)
        user.permission_codes = list(permission_service.get_user_permissions(user.id))
        return user

    def _get_user_roles(self, user_id: str) -> List[str]:
        rows = self.db.query(Role.code).join(
            UserOrganization, Role.id == UserOrganization.role_id
        ).filter(
            UserOrganization.user_id == user_id,
            UserOrganization.status == "active"
        ).all()
        return [row[0] for row in rows]
