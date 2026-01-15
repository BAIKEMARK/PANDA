"""
Chat ORM Models
对话相关数据库模型
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from db.database import Base


class ChatSession(Base):
    """对话会话表"""
    __tablename__ = "chat_sessions"

    id = Column(CHAR(36), primary_key=True, comment="会话ID")
    user_id = Column(CHAR(36), nullable=False, index=True, comment="用户ID")
    scenario_id = Column(CHAR(36), nullable=False, comment="场景ID")
    status = Column(SQLEnum("active", "completed", "abandoned", name="status"), default="active", comment="会话状态")
    start_time = Column(DateTime, default=datetime.utcnow, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    final_score = Column(Integer, comment="最终得分")
    meta_data = Column(JSON, comment="会话元数据")


class ChatMessage(Base):
    """对话消息表"""
    __tablename__ = "chat_messages"

    id = Column(CHAR(36), primary_key=True, comment="消息ID")
    session_id = Column(CHAR(36), nullable=False, index=True, comment="会话ID")
    role = Column(SQLEnum("user", "assistant", "system", name="role"), nullable=False, comment="角色")
    content = Column(Text, nullable=False, comment="消息内容")
    meta_data = Column(JSON, comment="消息元数据")
    created_at = Column(DateTime, default=datetime.utcnow, index=True, comment="创建时间")
