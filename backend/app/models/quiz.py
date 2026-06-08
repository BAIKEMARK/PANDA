"""
Quiz ORM Models
测验数据库模型
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, JSON, String
from sqlalchemy.dialects.mysql import CHAR

from backend.app.db.database import Base


class Quiz(Base):
    """测验表"""
    __tablename__ = "quizzes"

    id = Column(CHAR(36), primary_key=True, comment="测验ID")
    course_id = Column(CHAR(36), comment="关联课程ID")
    title = Column(String(255), nullable=False, comment="测验标题")
    questions = Column(JSON, nullable=False, comment="题目数据(JSON格式)")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")


class QuizResult(Base):
    """测验结果表"""
    __tablename__ = "quiz_results"

    id = Column(CHAR(36), primary_key=True, comment="测验结果ID")
    user_id = Column(CHAR(36), nullable=False, index=True, comment="用户ID")
    quiz_id = Column(CHAR(36), nullable=False, index=True, comment="测验ID")
    score = Column(Integer, nullable=False, comment="得分")
    answers = Column(JSON, comment="答案记录")
    completed_at = Column(DateTime, default=datetime.utcnow, comment="完成时间")
