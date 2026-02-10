"""
患者状态数据访问层（Repository）
处理患者状态的MySQL持久化（会话级别，每次对话更新）
"""
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from backend.app.models.patient_state import PatientStateORM
from backend.app.core.config.logging import get_logger

logger = get_logger(__name__)


class PatientStateRepository:
    """患者状态数据访问仓库"""

    def __init__(self, db: Session):
        self.db = db

    def get_state(self, session_id: str) -> Optional[PatientStateORM]:
        """
        获取患者当前状态

        Args:
            session_id: 会话ID

        Returns:
            PatientStateORM对象，不存在返回None
        """
        return self.db.query(PatientStateORM).filter(
            PatientStateORM.session_id == session_id
        ).first()

    def create_state(self, session_id: str) -> PatientStateORM:
        """
        创建新状态记录

        Args:
            session_id: 会话ID

        Returns:
            PatientStateORM对象
        """
        db_state = PatientStateORM(
            session_id=session_id,
            mood_score=50,
            satisfaction_score=50,
            depression_level=50,
            rapport_score=50,
            message_count=0
        )
        self.db.add(db_state)
        self.db.commit()
        self.db.refresh(db_state)
        return db_state

    def update_state(
        self,
        session_id: str,
        mood_score: int = None,
        satisfaction_score: int = None,
        depression_level: int = None,
        rapport_score: int = None,
        message_count: int = None
    ) -> Optional[PatientStateORM]:
        """
        更新患者状态

        Args:
            session_id: 会话ID
            mood_score: 心情指数
            satisfaction_score: 满意度
            depression_level: 抑郁程度
            rapport_score: 信任度
            message_count: 对话轮次

        Returns:
            更新后的PatientStateORM对象
        """
        db_state = self.get_state(session_id)
        if not db_state:
            return None

        if mood_score is not None:
            db_state.mood_score = mood_score
        if satisfaction_score is not None:
            db_state.satisfaction_score = satisfaction_score
        if depression_level is not None:
            db_state.depression_level = depression_level
        if rapport_score is not None:
            db_state.rapport_score = rapport_score
        if message_count is not None:
            db_state.message_count = message_count

        db_state.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(db_state)
        return db_state

    def get_or_create_state(self, session_id: str) -> PatientStateORM:
        """
        获取或创建状态记录

        Args:
            session_id: 会话ID

        Returns:
            PatientStateORM对象
        """
        db_state = self.get_state(session_id)
        if not db_state:
            db_state = self.create_state(session_id)
        return db_state

    def delete_state(self, session_id: str) -> bool:
        """
        删除状态记录

        Args:
            session_id: 会话ID

        Returns:
            是否成功
        """
        try:
            self.db.query(PatientStateORM).filter(
                PatientStateORM.session_id == session_id
            ).delete()
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"删除状态失败: {e}")
            return False
