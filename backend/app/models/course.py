"""
Course ORM Model
课程数据库模型
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class Course(Base):
    """课程表"""
    __tablename__ = "courses"

    id = Column(CHAR(36), primary_key=True, comment="课程ID")
    title = Column(String(255), nullable=False, comment="课程标题")
    content_url = Column(Text, comment="内容URL")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    level = Column(SQLEnum("L1", "L2", "L3", "L4", name="level"), default="L1", comment="THP层级")
    description = Column(Text, comment="课程描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
