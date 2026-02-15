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
