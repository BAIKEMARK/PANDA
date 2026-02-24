"""
对话服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.models.chat import ChatSession, ChatMessage
from backend.app.modules.conversation.schemas.chat import (
    ChatSessionCreate, ChatMessageCreate, SessionStatus, MessageRole
)
from backend.app.modules.conversation.repositories.chat_repository import ChatRepository
from backend.app.core.common.exceptions import NotFoundException
from backend.app.core.services.event_bus import event_bus, Events


class ChatService:
    """对话服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ChatRepository(db)

    def create_session(self, session_data: ChatSessionCreate, user_id: str) -> ChatSession:
        """
        创建新会话

        Args:
            session_data: 会话创建数据
            user_id: 用户ID（从JWT token获取）
        """
        return self.repository.create_chat_session(session_data, user_id)

    def get_session(self, session_id: str) -> Optional[dict]:
        """获取对话会话"""
        return self.repository.get_chat_session(session_id)

    def get_session_messages(self, session_id: str) -> List[ChatMessage]:
        """获取会话的所有消息"""
        return self.repository.get_session_messages(session_id)

    def create_message(self, message_data: ChatMessageCreate) -> ChatMessage:
        """创建新消息"""
        return self.repository.create_message(message_data)

    def end_session(self, session_id: str, final_score: int = None) -> Optional[ChatSession]:
        """结束会话并发布会话结束事件（触发评估Agent）"""
        session = self.repository.update_session_status(
            session_id,
            SessionStatus.COMPLETED,
            final_score
        )
        if not session:
            raise NotFoundException("会话不存在")

        # 发布会话结束事件，触发评估Agent生成报告
        event_bus.publish(
            Events.CHAT_SESSION_ENDED,
            {"session_id": session_id}
        )

        return session

    def fork_session(self, session_id: str, user_id: str) -> ChatSession:
        """
        从已完成的会话分叉出一个新会话（继续对话）
        
        1. 创建一个全新的 session（新 ID，同 scenario_id）
        2. 把旧 session 的所有消息复制到新 session
        3. 旧 session 和旧评估报告完全不动
        """
        import uuid
        from datetime import datetime

        # 获取旧会话
        old_session = self.db.query(ChatSession).filter(
            ChatSession.id == session_id
        ).first()
        if not old_session:
            raise NotFoundException("会话不存在")

        # 1. 创建新会话
        new_session_id = str(uuid.uuid4())
        new_session = ChatSession(
            id=new_session_id,
            user_id=user_id,
            scenario_id=old_session.scenario_id,
            status=SessionStatus.ACTIVE,
            start_time=datetime.utcnow(),
            # 继承自杀倾向检测状态
            has_suicide_risk=old_session.has_suicide_risk,
            suicide_risk_first_detected=old_session.suicide_risk_first_detected,
        )
        self.db.add(new_session)

        # 2. 复制旧消息到新会话
        old_messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.asc()).all()

        for msg in old_messages:
            new_msg = ChatMessage(
                id=str(uuid.uuid4()),
                session_id=new_session_id,
                role=msg.role,
                content=msg.content,
                meta_data=msg.meta_data,
                created_at=msg.created_at,  # 保留原始时间戳
            )
            self.db.add(new_msg)

        self.db.commit()
        self.db.refresh(new_session)
        return new_session
