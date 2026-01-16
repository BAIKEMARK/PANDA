"""
Scenario ORM Model
场景数据库模型
"""
from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class Scenario(Base):
    """场景表"""
    __tablename__ = "scenarios"

    id = Column(CHAR(36), primary_key=True, comment="场景ID")
    title = Column(String(255), nullable=False, comment="场景标题")
    description = Column(Text, comment="场景描述")
    system_prompt = Column(Text, nullable=False, comment="AI系统提示词")
    patient_background = Column(Text, comment="患者背景信息")
    knowledge_tags = Column(String(500), comment="知识点标签")
    difficulty = Column(Integer, default=1, comment="难度等级")
    time_period = Column(String(50), comment="时间节点")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
