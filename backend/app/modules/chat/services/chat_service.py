"""
对话服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.models.chat import ChatSession, ChatMessage
from backend.app.modules.chat.schemas.chat import (
    ChatSessionCreate, ChatMessageCreate, SessionStatus, MessageRole
)
from backend.app.modules.chat.repositories.chat_repository import ChatRepository
from backend.app.common.exceptions import NotFoundException


class ChatService:
    """对话服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ChatRepository(db)

    def create_session(self, session_data: ChatSessionCreate, user_id: str = "user-001") -> ChatSession:
        """创建新会话"""
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
        """结束会话"""
        session = self.repository.update_session_status(
            session_id,
            SessionStatus.COMPLETED,
            final_score
        )
        if not session:
            raise NotFoundException("会话不存在")
        return session
