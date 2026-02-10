"""
用户数据访问层（Repository）
用户CRUD操作
"""
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from backend.app.models.user import User
from backend.app.modules.auth.schemas.user import UserCreate, UserUpdate


class UserRepository:
    """用户数据访问仓库"""

    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: str) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user_data: UserCreate) -> User:
        """创建新用户"""
        from backend.app.core.security import get_password_hash

        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            password_hash=hashed_password,
            name=user_data.name,
            role=user_data.role,
            org_id=user_data.org_id,
            phone=user_data.phone,
            department=user_data.department,
            title=user_data.title,
            employee_id=user_data.employee_id
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, db_user: User, user_data: UserUpdate) -> User:
        """更新用户"""
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_user, field, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_password(self, db_user: User, new_password_hash: str) -> User:
        """更新用户密码"""
        db_user.password_hash = new_password_hash
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: str) -> Optional[User]:
        """删除用户"""
        db_user = self.get_user(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
