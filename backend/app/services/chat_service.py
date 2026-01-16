"""
Chat Service
对话服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import List, Optional

import crud.crud_chat as crud_chat
from schemas.chat import ChatSessionCreate, ChatMessageCreate
from models.chat import ChatSession, ChatMessage
from common.constants import SessionStatus
from common.exceptions import NotFoundException


class ChatService:
    """对话服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_session(self, session_data: ChatSessionCreate, user_id: str) -> ChatSession:
        """创建新会话"""
        return crud_chat.create_chat_session(self.db, session_data, user_id)

    def get_session(self, session_id: str) -> Optional[dict]:
        """获取会话（包含场景信息）"""
        return crud_chat.get_chat_session(self.db, session_id)

    def get_user_sessions(self, user_id: str) -> List[ChatSession]:
        """获取用户的所有会话"""
        return crud_chat.get_user_sessions(self.db, user_id)

    def create_message(self, message_data: ChatMessageCreate) -> ChatMessage:
        """创建新消息"""
        return crud_chat.create_message(self.db, message_data)

    def get_session_messages(self, session_id: str) -> List[ChatMessage]:
        """获取会话的所有消息"""
        return crud_chat.get_session_messages(self.db, session_id)

    def end_session(self, session_id: str, final_score: Optional[int] = None) -> Optional[ChatSession]:
        """结束会话"""
        return crud_chat.update_session_status(
            self.db,
            session_id,
            SessionStatus.COMPLETED,
            final_score
        )
