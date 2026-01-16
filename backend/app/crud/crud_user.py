"""
User CRUD Operations
用户CRUD操作
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
import uuid

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: str) -> Optional[User]:
    """根据ID获取用户"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """根据邮箱获取用户"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """获取用户列表"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """创建新用户"""
    from backend.app.core.security import get_password_hash

    hashed_password = get_password_hash(user.password)
    db_user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        password_hash=hashed_password,
        name=user.name,
        role=user.role.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    """更新用户"""
    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str) -> Optional[User]:
    """删除用户"""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
