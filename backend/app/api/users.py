"""
Users API Router
用户API路由 - Controller层
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.schemas.user import UserCreate, UserResponse, UserUpdate
from backend.app.services.user_service import UserService
from backend.app.models.user import User
from backend.app.common.exceptions import NotFoundException

router = APIRouter(prefix="/users", tags=["用户"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    service = UserService(db)
    users = service.get_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
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


@router.put("/{user_id}", response_model=UserResponse)
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


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
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
