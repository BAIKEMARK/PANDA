from functools import wraps
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.modules.auth.services.auth_service import AuthService
from backend.app.db.database import get_db
from backend.app.modules.admin.services.permission_service import PermissionService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user_dependency(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    auth_service = AuthService(db)
    return auth_service.get_current_user(token)


def require_permission(permission_code: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user_dependency), db: Session = Depends(get_db), **kwargs):
            permission_service = PermissionService(db)
            user_orgs = permission_service.get_user_orgs(current_user.id)
            org_id = kwargs.get('org_id') or current_user.org_id
            
            if not permission_service.has_permission(current_user.id, permission_code, org_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"权限不足: {permission_code}"
                )
            
            return await func(*args, current_user=current_user, db=db, **kwargs)
        return wrapper
    return decorator


def check_permission(permission_code: str, current_user: User, db: Session, org_id: Optional[str] = None) -> bool:
    permission_service = PermissionService(db)
    if not org_id:
        org_id = current_user.org_id
    return permission_service.has_permission(current_user.id, permission_code, org_id)


def require_org_access(org_id_param: str = "org_id"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user_dependency), db: Session = Depends(get_db), **kwargs):
            org_id = kwargs.get(org_id_param)
            if not org_id:
                org_id = current_user.org_id
            
            if not org_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="未指定机构"
                )
            
            permission_service = PermissionService(db)
            
            if not permission_service.is_super_admin(current_user.id):
                if not permission_service.user_belongs_to_org(current_user.id, org_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="无权访问该机构"
                    )
            
            kwargs[org_id_param] = org_id
            return await func(*args, current_user=current_user, db=db, **kwargs)
        return wrapper
    return decorator
