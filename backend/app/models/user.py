"""
User ORM Model
用户数据库模型
"""
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Text
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, comment="用户ID")
    email = Column(String(255), unique=True, nullable=False, index=True, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    name = Column(String(100), nullable=False, comment="姓名")
    role = Column(SQLEnum("student", "instructor", "admin", name="role"), default="student", comment="角色")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
