"""
Patient State ORM Models
患者状态相关数据库模型
"""
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class PatientStateORM(Base):
    """患者状态表（会话级别）"""
    __tablename__ = "patient_states"

    session_id = Column(CHAR(36), primary_key=True, comment="会话ID")
    mood_score = Column(Integer, default=50, comment="心情指数 (0-100)")
    satisfaction_score = Column(Integer, default=50, comment="满意度 (0-100)")
    depression_level = Column(Integer, default=50, comment="抑郁程度 (0-100)")
    rapport_score = Column(Integer, default=50, comment="信任度 (0-100)")
    message_count = Column(Integer, default=0, comment="对话轮次")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
