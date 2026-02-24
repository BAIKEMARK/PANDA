"""
对话 API 路由
"""
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.modules.conversation.schemas.chat import (
    ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse,
    MessageRole, SessionStatus
)
from backend.app.modules.conversation.services.chat_service import ChatService
from backend.app.modules.conversation.services.conversation_engine import ConversationEngine
from backend.app.core.common.exceptions import NotFoundException
from backend.app.core.config.logging import get_logger
from backend.app.core.dependencies import get_current_user_with_fallback

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["对话"])


@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: ChatSessionCreate,
    user_id: str = Depends(get_current_user_with_fallback),
    db: Session = Depends(get_db)
):
    """创建新的对话会话"""
    service = ChatService(db)
    session = service.create_session(session_data, user_id)
    
    # 清除 Dashboard 缓存
    try:
        from backend.app.modules.progress.services.dashboard_service import DashboardService
        DashboardService.clear_dashboard_cache(user_id)
    except Exception:
        pass
        
    return session


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
    user_id: str = Depends(get_current_user_with_fallback),
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
    from backend.app.modules.conversation.agent.core.agent_orchestrator import AgentOrchestrator

    scenario_service = ScenarioService(db)  # 实现ScenarioInterface
    agent_orchestrator = AgentOrchestrator(db)  # Agent编排器

    engine = ConversationEngine(
        db=db,
        scenario_interface=scenario_service,
        agent_orchestrator=agent_orchestrator
    )

    try:
        result = await engine.generate_ai_response(
            session_id=message_data.session_id,
            user_message=message_data.content,
            user_id=user_id
        )

        # 3. 保存AI回复
        # 构建meta_data，包含危机信息和患者离开标记
        message_meta = {
            **result.get("crisis_alert", {}),
            "force_end": result.get("force_end", False),
            "patient_leaving": result.get("patient_leaving", False),
            "reason": result.get("reason"),
        }

        assistant_message_data = ChatMessageCreate(
            session_id=message_data.session_id,
            role=MessageRole.ASSISTANT,
            content=result["response"],
            meta_data=message_meta if any(v is not None and v != False for v in message_meta.values()) else None
        )
        assistant_message = service.create_message(assistant_message_data)

        return assistant_message

    except Exception as e:
        logger.exception(f"AI 生成失败: {e}")
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
    结束会话

    流程：
    1. 更新会话状态为已结束
    2. 发布会话结束事件，触发评估Agent生成报告
    3. 返回会话信息
    """
    service = ChatService(db)

    # 检查会话是否存在
    session = service.get_session(session_id)
    if not session:
        raise NotFoundException(f"会话不存在: {session_id}")

    # 使用服务层更新会话状态（会发布事件，触发评估Agent）
    service.end_session(session_id, final_score)

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


@router.post("/sessions/{session_id}/alert", response_model=ChatSessionResponse)
async def alert_suicide_risk(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    用户点击自杀倾向报警按钮

    流程：
    1. 记录报警时间
    2. 标记 suicide_risk_alerted = true
    3. 自动结束对话
    4. 触发评估报告生成
    """
    from backend.app.modules.conversation.repositories.chat_repository import ChatRepository

    service = ChatService(db)

    # 检查会话是否存在
    session = service.get_session(session_id)
    if not session:
        raise NotFoundException(f"会话不存在: {session_id}")

    # 记录报警
    repository = ChatRepository(db)
    repository.alert_suicide_risk(session_id)

    # 自动结束对话
    service.end_session(session_id, final_score=0)

    return service.get_session(session_id)
