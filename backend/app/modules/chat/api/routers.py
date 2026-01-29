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
from backend.app.shared.infrastructure.ai_service import AIService

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
    # 返回完整会话信息（包含场景信息）
    session_info = service.get_session(session.id)
    return session_info


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

    # 2. 使用对话编排引擎生成AI回复（依赖注入方式）
    from backend.app.modules.scenario.services.scenario_service import ScenarioService

    scenario_service = ScenarioService(db)  # 实现ScenarioInterface
    ai_service = AIService()

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
            detail=f"AI生成回复失败: {str(e)}"
        )


@router.put("/sessions/{session_id}/end", response_model=ChatSessionResponse)
async def end_chat_session(
    session_id: str,
    final_score: int = None,
    db: Session = Depends(get_db)
):
    """
    结束对话会话并生成评估报告

    结束会话后会自动通过事件总线触发评估报告生成。
    """
    service = ChatService(db)
    session = service.end_session(session_id, final_score)
    if not session:
        raise NotFoundException("会话不存在")

    # 使用对话编排引擎发布事件（事件驱动）
    from backend.app.modules.chat.services.conversation_engine import ConversationEngine
    from backend.app.shared.infrastructure.ai_service import AIService
    from backend.app.modules.scenario.services.scenario_service import ScenarioService

    scenario_service = ScenarioService(db)
    ai_service = AIService()

    engine = ConversationEngine(
        db=db,
        ai_service=ai_service,
        scenario_interface=scenario_service
    )

    try:
        # 通过事件总线发布会话结束事件
        engine.end_session(session_id, final_score)
        print(f"✅ 会话 {session_id} 已结束，已发布事件")
    except Exception as e:
        # 事件发布失败不影响会话结束
        print(f"⚠️  会话 {session_id} 事件发布失败: {e}")
        print(f"   会话已正常结束，但未触发评估报告")

    return service.get_session(session_id)
