"""
Chat CRUD Operations
对话CRUD操作
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from backend.app.models.chat import ChatSession, ChatMessage
from backend.app.schemas.chat import ChatSessionCreate, ChatMessageCreate
from backend.app.common.constants import SessionStatus


def get_chat_session(db: Session, session_id: str) -> Optional[dict]:
    """获取对话会话（包含场景信息）"""
    from backend.app.models.scenario import Scenario
    
    result = db.query(ChatSession, Scenario.title, Scenario.patient_background)\
        .outerjoin(Scenario, ChatSession.scenario_id == Scenario.id)\
        .filter(ChatSession.id == session_id)\
        .first()
    
    if not result:
        return None
    
    session, scenario_title, patient_background = result
    # 返回包含场景信息的字典
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


def get_user_sessions(db: Session, user_id: str) -> List[ChatSession]:
    """获取用户的所有会话"""
    return db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.start_time.desc()).all()


def create_chat_session(db: Session, session_data: ChatSessionCreate, user_id: str) -> ChatSession:
    """创建新会话"""
    db_session = ChatSession(
        id=str(uuid.uuid4()),
        user_id=user_id,
        scenario_id=session_data.scenario_id,
        status=SessionStatus.ACTIVE.value,
        start_time=datetime.utcnow()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def update_session_status(db: Session, session_id: str, status: SessionStatus, final_score: int = None) -> Optional[ChatSession]:
    """更新会话状态"""
    # 直接查询 ChatSession 对象，而不是使用 get_chat_session（它返回字典）
    db_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if db_session:
        db_session.status = status.value
        if status == SessionStatus.COMPLETED:
            db_session.end_time = datetime.utcnow()
            db_session.final_score = final_score
        db.commit()
        db.refresh(db_session)
    return db_session


def get_session_messages(db: Session, session_id: str) -> List[ChatMessage]:
    """获取会话的所有消息"""
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()


def create_message(db: Session, message_data: ChatMessageCreate) -> ChatMessage:
    """创建新消息"""
    db_message = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=message_data.session_id,
        role=message_data.role.value,
        content=message_data.content,
        meta_data=message_data.meta_data,
        created_at=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
