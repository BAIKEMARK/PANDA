"""
Chat API Router
对话API路由 - Controller层
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from schemas.chat import ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse
from services.chat_service import ChatService
from common.exceptions import NotFoundException
from models.chat import ChatMessage

router = APIRouter(prefix="/chat", tags=["对话"])


@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    session_data: ChatSessionCreate,
    user_id: str = "user-001",  # TODO: 从JWT token获取
    db: Session = Depends(get_db)
):
    """
    创建新的对话会话

    - **scenario_id**: 场景ID
    """
    service = ChatService(db)
    session = service.create_session(session_data, user_id)
    return session


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """获取对话会话详情"""
    service = ChatService(db)
    session = service.get_session(session_id)
    if not session:
        raise NotFoundException("会话不存在")
    return session


@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    session_id: str,
    db: Session = Depends(get_db)
):
    """获取会话的所有消息"""
    service = ChatService(db)
    # 先检查会话是否存在
    session = service.get_session(session_id)
    if not session:
        raise NotFoundException("会话不存在")

    messages = service.get_session_messages(session_id)
    return messages


@router.post("/messages", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
async def create_chat_message(
    message_data: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """
    发送消息

    - **session_id**: 会话ID
    - **role**: 角色 (user/assistant/system)
    - **content**: 消息内容
    - **metadata**: 元数据（可选）
    """
    service = ChatService(db)
    # 验证会话存在
    session = service.get_session(message_data.session_id)
    if not session:
        raise NotFoundException("会话不存在")

    message = service.create_message(message_data)
    return message


@router.put("/sessions/{session_id}/end", response_model=ChatSessionResponse)
async def end_chat_session(
    session_id: str,
    final_score: int = None,
    db: Session = Depends(get_db)
):
    """结束对话会话"""
    service = ChatService(db)
    session = service.end_session(session_id, final_score)
    if not session:
        raise NotFoundException("会话不存在")
    return session
