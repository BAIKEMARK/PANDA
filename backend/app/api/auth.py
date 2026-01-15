"""
Auth API Router
认证API路由 - Controller层
处理用户登录、登出等认证操作
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from db.database import get_db
from schemas.user import UserResponse
from services.user_service import UserService
from core.security import verify_password, create_access_token
from core.config import settings

router = APIRouter(prefix="/auth", tags=["认证"])


class LoginRequest(BaseModel):
    """登录请求"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    用户登录

    - **email**: 用户邮箱
    - **password**: 密码

    返回JWT访问令牌和用户信息
    """
    service = UserService(db)

    # 查找用户
    user = service.get_user_by_email(login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )

    # 验证密码
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )

    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.id})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.from_orm(user)
    )


@router.post("/logout")
async def logout():
    """
    用户登出

    注意：JWT是无状态的，客户端只需删除本地token即可
    """
    return {"message": "登出成功"}
