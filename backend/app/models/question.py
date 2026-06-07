from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, JSON, Text
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class QuestionBank(Base):
    __tablename__ = "question_bank"

    id = Column(CHAR(36), primary_key=True, comment="题目ID")
    org_id = Column(CHAR(36), index=True, comment="机构ID")
    scope = Column(SQLEnum("private", "platform", "shared", name="question_scope"), default="private", comment="发布范围")
    question_type = Column(SQLEnum("single", "multiple", "judge", name="question_type"), nullable=False, comment="题型")
    question_text = Column(Text, nullable=False, comment="题干")
    options = Column(JSON, nullable=False, comment="选项")
    correct_answer = Column(JSON, nullable=False, comment="正确答案")
    explanation = Column(Text, comment="解析")
    difficulty = Column(SQLEnum("easy", "medium", "hard", name="difficulty"), default="medium", comment="难度")
    knowledge_tags = Column(JSON, comment="知识点标签")
    chapter_id = Column(CHAR(36), comment="章节归属")
    status = Column(SQLEnum("draft", "active", "disabled", name="question_status"), default="draft", comment="状态")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
