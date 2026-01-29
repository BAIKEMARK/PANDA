"""
对话数据访问层（Repository）
对话CRUD操作
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import uuid
from datetime import datetime

from backend.app.models.chat import ChatSession, ChatMessage
from backend.app.modules.chat.schemas.chat import ChatSessionCreate, ChatMessageCreate, SessionStatus


class ChatRepository:
    """对话数据访问仓库"""

    def __init__(self, db: Session):
        self.db = db

    def get_chat_session(self, session_id: str) -> Optional[Dict]:
        """获取对话会话（包含场景信息）"""
        from backend.app.models.scenario import Scenario

        result = self.db.query(ChatSession, Scenario.title, Scenario.patient_background)\
            .outerjoin(Scenario, ChatSession.scenario_id == Scenario.id)\
            .filter(ChatSession.id == session_id)\
            .first()

        if not result:
            return None

        session, scenario_title, patient_background = result
        return {
            "id": session.id,
            "user_id": session.user_id,
            "scenario_id": session.scenario_id,
            "scenario_title": scenario_title,
            "patient_background": patient_background,
            "status": session.status,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "final_score": session.final_score,
        }

    def get_user_sessions(self, user_id: str) -> List[ChatSession]:
        """获取用户的所有会话"""
        return self.db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.start_time.desc()).all()

    def create_chat_session(self, session_data: ChatSessionCreate, user_id: str) -> ChatSession:
        """创建新会话"""
        db_session = ChatSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            scenario_id=session_data.scenario_id,
            status=SessionStatus.ACTIVE,
            start_time=datetime.utcnow()
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def update_session_status(self, session_id: str, status: str, final_score: int = None) -> Optional[ChatSession]:
        """更新会话状态"""
        db_session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if db_session:
            db_session.status = status
            if status == SessionStatus.COMPLETED:
                db_session.end_time = datetime.utcnow()
                db_session.final_score = final_score
            self.db.commit()
            self.db.refresh(db_session)
        return db_session

    def get_session_messages(self, session_id: str) -> List[ChatMessage]:
        """获取会话的所有消息"""
        return self.db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()

    def create_message(self, message_data: ChatMessageCreate) -> ChatMessage:
        """创建新消息"""
        db_message = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=message_data.session_id,
            role=message_data.role,
            content=message_data.content,
            meta_data=message_data.meta_data,
            created_at=datetime.utcnow()
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
