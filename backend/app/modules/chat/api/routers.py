"""
对话 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.modules.chat.schemas.chat import (
    ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse,
    MessageRole, SessionStatus
)
from backend.app.modules.chat.services.chat_service import ChatService
from backend.app.modules.chat.services.conversation_engine import ConversationEngine
from backend.app.common.exceptions import NotFoundException

router = APIRouter(prefix="/chat", tags=["对话"])


@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: ChatSessionCreate,
    db: Session = Depends(get_db)
):
    """创建新的对话会话"""
    service = ChatService(db)
    return service.create_session(session_data)


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """获取会话详情"""
    service = ChatService(db)
    session = service.get_session(session_id)
    if not session:
        raise NotFoundException(f"会话不存在: {session_id}")
    return session


@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_session_messages(
    session_id: str,
    db: Session = Depends(get_db)
):
    """获取会话的所有消息"""
    service = ChatService(db)
    messages = service.get_session_messages(session_id)
    return messages


@router.post("/messages", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message_data: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """
    发送消息并获取 AI 回复

    流程：
    1. 保存用户消息
    2. 使用 ConversationEngine 生成 AI 回复
    3. 保存 AI 回复
    """
    service = ChatService(db)

    # 1. 保存用户消息
    user_message = service.create_message(message_data)

    # 2. 使用对话编排引擎生成AI回复（依赖注入方式）
    from backend.app.modules.scenario.services.scenario_service import ScenarioService
    from backend.app.shared.infrastructure.ai_service import ai_service

    scenario_service = ScenarioService(db)  # 实现ScenarioInterface

    engine = ConversationEngine(
        db=db,
        ai_service=ai_service,
        scenario_interface=scenario_service
    )

    try:
        result = engine.generate_ai_response(
            session_id=message_data.session_id,
            user_message=message_data.content
        )

        # 3. 保存AI回复
        assistant_message_data = ChatMessageCreate(
            session_id=message_data.session_id,
            role=MessageRole.ASSISTANT,
            content=result["response"],
            meta_data=None
        )
        assistant_message = service.create_message(assistant_message_data)

        return assistant_message

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI 生成失败: {str(e)}"
        )


@router.put("/sessions/{session_id}/end", response_model=ChatSessionResponse)
async def end_session(
    session_id: str,
    final_score: int = 0,
    db: Session = Depends(get_db)
):
    """
    结束会话并发布事件

    流程：
    1. 更新会话状态为已结束
    2. 通过 EventBus 发布会话结束事件
    3. MentorAgent 订阅该事件并自动生成评估报告
    """
    service = ChatService(db)

    # 检查会话是否存在
    session = service.get_session(session_id)
    if not session:
        raise NotFoundException(f"会话不存在: {session_id}")

    # 使用服务层更新会话状态
    service.end_session(session_id, final_score)

    # 使用对话编排引擎发布会话结束事件
    from backend.app.modules.scenario.services.scenario_service import ScenarioService
    from backend.app.shared.infrastructure.ai_service import ai_service

    scenario_service = ScenarioService(db)

    engine = ConversationEngine(
        db=db,
        ai_service=ai_service,
        scenario_interface=scenario_service
    )

    try:
        # 通过事件总线发布会话结束事件
        engine.end_session(session_id, final_score)
    except Exception as e:
        # 事件发布失败不影响会话结束，但记录错误
        print(f"[WARN] 事件发布失败: {e}")

    return service.get_session(session_id)


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """删除会话及其所有消息"""
    service = ChatService(db)
    service.delete_session(session_id)
    return None
