"""
用户服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.models.user import User
from backend.app.modules.auth.schemas.user import UserCreate, UserUpdate
from backend.app.modules.auth.repositories.user_repository import UserRepository
from backend.app.core.common.exceptions import ConflictException


class UserService:
    """用户服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> User:
        """创建新用户"""
        # 检查邮箱是否已存在
        existing_user = self.repository.get_user_by_email(user_data.email)
        if existing_user:
            raise ConflictException("邮箱已被注册")

        # 调用repository创建用户
        return self.repository.create_user(user_data)

    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户"""
        return self.repository.get_user(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.repository.get_user_by_email(email)

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        return self.repository.get_users(skip=skip, limit=limit)

    def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """更新用户"""
        db_user = self.get_user(user_id)
        if not db_user:
            return None
        return self.repository.update_user(db_user, user_data)

    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        db_user = self.repository.delete_user(user_id)
        return db_user is not None
