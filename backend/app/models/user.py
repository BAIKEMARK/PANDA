"""
User ORM Model
用户数据库模型
"""
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Text
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, timezone
from backend.app.db.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, comment="用户ID")
    email = Column(String(255), unique=True, nullable=False, index=True, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    name = Column(String(100), nullable=False, comment="姓名")
    # 与 roles.code 对齐，支持动态角色
    role = Column(String(50), default="student", comment="角色代码")
    org_id = Column(CHAR(36), index=True, comment="默认机构ID")
    phone = Column(String(50), comment="手机号")
    department = Column(String(100), comment="科室")
    title = Column(String(100), comment="职称")
    employee_id = Column(String(100), comment="工号")
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        comment="创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        comment="更新时间"
    )
