"""
Chat API Router
对话API路由 - Controller层
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.schemas.chat import ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse
from backend.app.services.chat_service import ChatService
from backend.app.common.exceptions import NotFoundException
from backend.app.common.constants import MessageRole

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
    发送消息并获取AI回复

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

    # 1. 保存用户消息
    user_message = service.create_message(message_data)

    # 2. 获取场景配置以获取系统提示词
    from crud.crud_scenario import get_scenario
    scenario = get_scenario(db, session.scenario_id)

    # 3. 构建AI对话历史
    messages_history = service.get_session_messages(message_data.session_id)

    # 4. 调用AI生成回复
    try:
        from utils.google_search import search_with_ai
        system_prompt = scenario.system_prompt if scenario else "你是一位围产期抑郁管理专家。"

        # 构建对话上下文
        conversation_context = f"系统提示：{system_prompt}\n\n"
        conversation_context += f"患者背景：{scenario.patient_background if scenario else '暂无'}\n\n"
        conversation_context += "对话历史：\n"

        for msg in messages_history:
            role_name = "用户" if msg.role == "user" else "专家"
            conversation_context += f"{role_name}: {msg.content}\n"

        conversation_context += f"\n用户最新消息: {message_data.content}\n"
        conversation_context += "请以专家的身份回复："

        # 调用AI生成回复（阻塞式）
        ai_response = search_with_ai(conversation_context)

        # 5. 保存AI回复
        assistant_message_data = ChatMessageCreate(
            session_id=message_data.session_id,
            role=MessageRole.ASSISTANT,
            content=ai_response,
            meta_data=None
        )
        assistant_message = service.create_message(assistant_message_data)

        return assistant_message

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI生成回复失败: {str(e)}"
        )


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
