"""
Scenario ORM Model
场景数据库模型
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class Scenario(Base):
    """场景表"""
    __tablename__ = "scenarios"

    id = Column(CHAR(36), primary_key=True, comment="场景ID")
    org_id = Column(CHAR(36), index=True, comment="机构ID")
    scope = Column(SQLEnum("private", "platform", "shared", name="scenario_scope"), default="private", comment="发布范围")
    version = Column(String(50), default="1.0.0", comment="版本号")
    version_notes = Column(Text, comment="版本说明")
    status = Column(SQLEnum("draft", "pending", "published", "archived", name="scenario_status"), default="draft", comment="状态")
    published_at = Column(DateTime, comment="发布时间")
    published_by = Column(CHAR(36), comment="发布人")
    created_by = Column(CHAR(36), index=True, comment="创建人")
    title = Column(String(255), nullable=False, comment="场景标题")
    description = Column(Text, comment="场景描述")
    system_prompt = Column(Text, nullable=False, comment="AI系统提示词")
    patient_background = Column(Text, comment="患者背景信息")
    knowledge_tags = Column(String(500), comment="知识点标签")
    difficulty = Column(Integer, default=1, comment="难度等级")
    time_period = Column(String(50), comment="时间节点")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")