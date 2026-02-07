"""
Chat ORM Models
对话相关数据库模型
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum as SQLEnum, JSON, Boolean, Index
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, timezone
from backend.app.db.database import Base


class ChatSession(Base):
    """对话会话表"""
    __tablename__ = "chat_sessions"

    id = Column(CHAR(36), primary_key=True, comment="会话ID")
    user_id = Column(CHAR(36), nullable=False, index=True, comment="用户ID")
    scenario_id = Column(CHAR(36), nullable=False, comment="场景ID")
    status = Column(SQLEnum("active", "completed", "abandoned", name="status"), default="active", comment="会话状态")
    start_time = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        comment="开始时间"
    )
    end_time = Column(DateTime(timezone=True), comment="结束时间")
    final_score = Column(Integer, comment="最终得分")
    meta_data = Column(JSON, comment="会话元数据")

    # ========== 自杀倾向检测 ==========
    has_suicide_risk = Column(Boolean, default=False, comment="会话中是否检测到自杀倾向")
    suicide_risk_alerted = Column(Boolean, default=False, comment="用户是否点击了报警按钮")
    suicide_risk_alert_time = Column(DateTime(timezone=True), comment="报警时间")
    suicide_risk_first_detected = Column(DateTime(timezone=True), comment="首次检测到自杀倾向的时间")
    
    # 复合索引优化
    __table_args__ = (
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_user_start_time', 'user_id', 'start_time'),
    )


class ChatMessage(Base):
    """对话消息表"""
    __tablename__ = "chat_messages"

    id = Column(CHAR(36), primary_key=True, comment="消息ID")
    session_id = Column(CHAR(36), nullable=False, index=True, comment="会话ID")
    role = Column(SQLEnum("user", "assistant", "system", name="role"), nullable=False, comment="角色")
    content = Column(Text, nullable=False, comment="消息内容")
    meta_data = Column(JSON, comment="消息元数据")
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        index=True, 
        comment="创建时间"
    )
    
    # 复合索引优化
    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
        Index('idx_session_role', 'session_id', 'role'),
    )
