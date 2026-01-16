"""
User Progress ORM Model
学习进度数据库模型
"""
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from db.database import Base


class UserProgress(Base):
    """学习进度表"""
    __tablename__ = "user_progress"

    id = Column(CHAR(36), primary_key=True, comment="进度ID")
    user_id = Column(CHAR(36), nullable=False, index=True, comment="用户ID")
    course_id = Column(CHAR(36), nullable=False, index=True, comment="课程ID")
    is_completed = Column(Boolean, default=False, comment="是否完成")
    completed_at = Column(DateTime, comment="完成时间")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
