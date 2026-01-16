"""
Evaluation Report ORM Model
评估报告数据库模型
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, JSON
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class EvaluationReport(Base):
    """评估报告表"""
    __tablename__ = "evaluation_reports"

    id = Column(CHAR(36), primary_key=True, comment="报告ID")
    session_id = Column(CHAR(36), nullable=False, index=True, comment="会话ID")
    scores = Column(JSON, comment="评分详情(empathy/skill/safety等)")
    total_score = Column(Integer, comment="总分")
    ai_feedback = Column(Text, comment="AI反馈建议")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
