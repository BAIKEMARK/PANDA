"""
User Service
用户服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import List, Optional

import crud.crud_user as crud_user
from schemas.user import UserCreate, UserUpdate
from models.user import User
from common.exceptions import ConflictException


class UserService:
    """用户服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """创建新用户"""
        # 检查邮箱是否已存在
        existing_user = crud_user.get_user_by_email(self.db, email=user_data.email)
        if existing_user:
            raise ConflictException("邮箱已被注册")

        # 调用CRUD创建用户
        return crud_user.create_user(self.db, user_data)

    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户"""
        return crud_user.get_user(self.db, user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return crud_user.get_user_by_email(self.db, email)

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        return crud_user.get_users(self.db, skip=skip, limit=limit)

    def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """更新用户"""
        db_user = self.get_user(user_id)
        if not db_user:
            return None
        return crud_user.update_user(self.db, db_user, user_data)

    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        db_user = crud_user.delete_user(self.db, user_id)
        return db_user is not None
