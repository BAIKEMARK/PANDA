"""
全局依赖注入模块
包含可复用的依赖注入函数
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.db.database import get_db
from backend.app.modules.auth.services.auth_service import AuthService
from backend.app.modules.auth.services.user_service import UserService
from backend.app.models.user import User

# OAuth2 密码模式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    获取当前登录用户（依赖注入）

    Args:
        token: JWT 访问令牌（自动从请求头提取）
        db: 数据库会话

    Returns:
        User对象，如果未认证返回None（不抛出异常）

    注意：
        auto_error=False 表示如果未提供token不会抛出异常，
        而是返回 None，便于后续做兼容性处理
    """
    if not token:
        return None

    try:
        auth_service = AuthService(db)
        return auth_service.get_current_user(token)
    except Exception:
        return None


def get_current_user_required(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """
    获取当前登录用户（必须认证）

    与 get_current_user 的区别：
    - 如果未认证会抛出 401 异常
    - 用于需要强制登录的接口

    Args:
        current_user: 当前用户（从 get_current_user 获取）

    Returns:
        User对象

    Raises:
        HTTPException: 未认证时抛出 401 错误
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未认证，请先登录"
        )
    return current_user


def get_current_user_id_required(
    current_user: User = Depends(get_current_user_required)
) -> str:
    """获取当前登录用户ID（必须认证）"""
    return current_user.id


def require_role(*allowed_roles: str):
    """
    角色权限检查依赖工厂函数

    用法:
        @router.get("/admin")
        async def admin_only(
            user: User = Depends(require_role("admin", "instructor"))
        ):
            ...

    Args:
        *allowed_roles: 允许的角色列表

    Returns:
        依赖注入函数
    """
    def role_checker(
        current_user: User = Depends(get_current_user_required)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要以下角色之一: {', '.join(allowed_roles)}"
            )
        return current_user

    return role_checker
