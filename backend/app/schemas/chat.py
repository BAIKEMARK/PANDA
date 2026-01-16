"""
Chat Schemas
对话相关的 Pydantic 模型
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from backend.app.common.constants import SessionStatus, MessageRole


class ChatSessionCreate(BaseModel):
    """创建会话模型"""
    scenario_id: str


class ChatSessionResponse(BaseModel):
    """会话响应模型"""
    id: str
    user_id: str
    scenario_id: str
    scenario_title: Optional[str] = None
    patient_background: Optional[str] = None
    status: SessionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    final_score: Optional[int] = None

    class Config:
        from_attributes = True


class ChatMessageCreate(BaseModel):
    """消息创建模型"""
    session_id: str
    role: MessageRole
    content: str = Field(..., min_length=1)
    meta_data: Optional[Dict[str, Any]] = None


class ChatMessageResponse(BaseModel):
    """消息响应模型"""
    id: str
    session_id: str
    role: MessageRole
    content: str
    meta_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
