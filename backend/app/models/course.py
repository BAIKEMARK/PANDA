"""
Course ORM Model
课程数据库模型
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class Course(Base):
    """课程表"""
    __tablename__ = "courses"

    id = Column(CHAR(36), primary_key=True, comment="课程ID")
    org_id = Column(CHAR(36), index=True, comment="机构ID")
    scope = Column(SQLEnum("private", "platform", "shared", name="course_scope"), default="private", comment="发布范围")
    version = Column(String(50), default="1.0.0", comment="版本号")
    version_notes = Column(Text, comment="版本说明")
    status = Column(SQLEnum("draft", "pending", "published", "archived", name="course_status"), default="draft", comment="状态")
    published_at = Column(DateTime, comment="发布时间")
    published_by = Column(CHAR(36), comment="发布人")
    created_by = Column(CHAR(36), index=True, comment="创建人")
    title = Column(String(255), nullable=False, comment="课程标题")
    content_url = Column(Text, comment="课件PDF URL")
    video_url = Column(Text, comment="视频URL")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    level = Column(SQLEnum("L1", "L2", "L3", "L4", name="level"), default="L1", comment="THP层级")
    description = Column(Text, comment="课程描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
