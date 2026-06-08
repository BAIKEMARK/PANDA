"""
认证与用户 API 路由
合并原 auth.py 和 users.py
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.modules.auth.schemas.user import (
    TokenResponse, UserResponse, UserCreate, UserUpdate, PasswordChange, UserLogin
)
from backend.app.modules.auth.services.user_service import UserService
from backend.app.modules.auth.services.auth_service import AuthService
from backend.app.core.common.exceptions import NotFoundException, ConflictException
from backend.app.core.dependencies import get_current_user, get_current_user_required
from backend.app.core.config.logging import get_logger
from fastapi import Request

logger = get_logger(__name__)
router = APIRouter()
auth_router = APIRouter(prefix="/auth", tags=["认证"])
users_router = APIRouter(prefix="/users", tags=["用户"])


def _is_user_admin(user) -> bool:
    return bool(user and user.role in ("admin", "instructor"))


# ==================== 认证路由 ====================

@auth_router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    用户登录

    - **email**: 用户邮箱
    - **password**: 密码

    返回JWT访问令牌和用户信息
    """
    auth_service = AuthService(db)

    # 验证用户
    user = auth_service.authenticate(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )

    # 创建访问令牌
    access_token = auth_service.login(login_data.email, login_data.password)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(auth_service.enrich_user(user))
    )


@auth_router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user_required)):
    """
    获取当前登录用户信息

    需要在请求头中携带有效的JWT Token
    """
    return current_user


@auth_router.post("/logout")
async def logout():
    """
    用户登出

    注意：JWT是无状态的，客户端只需删除本地token即可
    """
    return {"message": "登出成功"}


# ==================== 用户路由 ====================

@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    用户注册

    - **email**: 用户邮箱
    - **name**: 用户姓名
    - **password**: 密码
    - **role**: 角色 (student/instructor/admin)
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(f"用户注册请求 | request_id={request_id} | email={user_data.email} | name={user_data.name}")
    
    service = UserService(db)
    auth_service = AuthService(db)
    
    try:
        logger.debug(f"开始创建用户 | request_id={request_id} | email={user_data.email}")
        db_user = service.create_user(user_data)
        logger.debug(f"用户创建完成，开始丰富用户信息 | request_id={request_id} | user_id={db_user.id}")
        
        try:
            enriched_user = auth_service.enrich_user(db_user)
            logger.debug(f"用户信息丰富完成 | request_id={request_id} | roles={getattr(enriched_user, 'roles', [])} | org_ids={getattr(enriched_user, 'org_ids', [])}")
        except Exception as enrich_error:
            logger.warning(f"丰富用户信息失败，使用基础信息 | request_id={request_id} | error={str(enrich_error)}")
            enriched_user = db_user
            enriched_user.roles = [db_user.role] if db_user.role else []
            enriched_user.org_ids = []
            enriched_user.permission_codes = []
        
        try:
            response_data = UserResponse.model_validate(enriched_user)
            logger.info(f"用户注册成功 | request_id={request_id} | user_id={enriched_user.id} | email={enriched_user.email}")
            return response_data
        except Exception as validate_error:
            logger.error(f"用户响应序列化失败 | request_id={request_id} | error={str(validate_error)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"响应序列化失败: {str(validate_error)}")
    except ConflictException as e:
        logger.warning(f"用户注册失败-冲突 | request_id={request_id} | error={str(e)} | email={user_data.email}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"用户注册失败-异常 | request_id={request_id} | error={str(e)} | email={user_data.email}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"注册失败: {str(e)}")


@users_router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    if not _is_user_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    service = UserService(db)
    users = service.get_users(skip=skip, limit=limit)
    return users


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """获取单个用户"""
    if current_user.id != user_id and not _is_user_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise NotFoundException("用户不存在")
    return user


@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    if current_user.id != user_id and not _is_user_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    service = UserService(db)
    user = service.update_user(user_id, user_data)
    if not user:
        raise NotFoundException("用户不存在")
    return user


@users_router.put("/{user_id}/password")
async def change_password(
    user_id: str,
    password_data: PasswordChange,
    current_user = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """修改用户密码"""
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能修改本人密码")
    from backend.app.core.config.security import verify_password, get_password_hash

    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise NotFoundException("用户不存在")

    # 验证旧密码
    if not verify_password(password_data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="当前密码错误")

    # 更新密码
    user.password_hash = get_password_hash(password_data.new_password)
    db.commit()

    return {"message": "密码修改成功"}


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """删除用户"""
    if not _is_user_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    service = UserService(db)
    success = service.delete_user(user_id)
    if not success:
        raise NotFoundException("用户不存在")
    return None
