"""
认证与用户 API 路由
合并原 auth.py 和 users.py
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.modules.auth.schemas.user import (
    TokenResponse, UserResponse, UserCreate, UserUpdate, PasswordChange, UserLogin
)
from backend.app.modules.auth.services.user_service import UserService
from backend.app.modules.auth.services.auth_service import AuthService
from backend.app.core.common.exceptions import NotFoundException, ConflictException

router = APIRouter()
auth_router = APIRouter(prefix="/auth", tags=["认证"])
users_router = APIRouter(prefix="/users", tags=["用户"])

# OAuth2 密码模式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


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
        user=UserResponse.model_validate(user)
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """获取当前登录用户（依赖注入）"""
    auth_service = AuthService(db)
    return auth_service.get_current_user(token)


@auth_router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
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
    service = UserService(db)
    try:
        db_user = service.create_user(user_data)
        return db_user
    except ConflictException as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    service = UserService(db)
    users = service.get_users(skip=skip, limit=limit)
    return users


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """获取单个用户"""
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise NotFoundException("用户不存在")
    return user


@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    service = UserService(db)
    user = service.update_user(user_id, user_data)
    if not user:
        raise NotFoundException("用户不存在")
    return user


@users_router.put("/{user_id}/password")
async def change_password(
    user_id: str,
    password_data: PasswordChange,
    db: Session = Depends(get_db)
):
    """修改用户密码"""
    from backend.app.core.security import verify_password, get_password_hash

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
    db: Session = Depends(get_db)
):
    """删除用户"""
    service = UserService(db)
    success = service.delete_user(user_id)
    if not success:
        raise NotFoundException("用户不存在")
    return None
