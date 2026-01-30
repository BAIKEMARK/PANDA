"""
患者状态服务
协调Redis和MySQL的混合存储，提供统一的状态管理接口
"""
from typing import Optional

from sqlalchemy.orm import Session

from backend.app.modules.agent.repositories.patient_state_repository import PatientStateRepository
from backend.app.shared.infrastructure.redis_state_manager import redis_state_manager
from backend.app.modules.agent.models.patient_state import PatientState


class PatientStateService:
    """
    患者状态服务 - Repository模式

    负责：
    - Redis实时状态管理（快速读写）
    - MySQL状态持久化（会话级别）
    """

    def __init__(self, db: Session):
        self.state_repo = PatientStateRepository(db)
        self.redis_manager = redis_state_manager

    def get_state(self, session_id: str) -> Optional[PatientState]:
        """
        获取患者当前状态

        Args:
            session_id: 会话ID

        Returns:
            PatientState对象
        """
        # 优先从Redis获取
        redis_state = self.redis_manager.get_patient_state(session_id)

        if redis_state:
            return redis_state

        # Redis无数据，从MySQL获取并同步到Redis
        db_state = self.state_repo.get_state(session_id)

        if db_state:
            # 同步到Redis
            self.redis_manager.update_patient_state(session_id, {
                'mood_score': db_state.mood_score,
                'satisfaction_score': db_state.satisfaction_score,
                'depression_level': db_state.depression_level,
                'rapport_score': db_state.rapport_score,
                'message_count': db_state.message_count
            })

            return PatientState(
                mood_score=db_state.mood_score,
                satisfaction_score=db_state.satisfaction_score,
                depression_level=db_state.depression_level,
                rapport_score=db_state.rapport_score,
                message_count=db_state.message_count
            )

        # 都没有数据，返回默认状态
        return None

    def update_state(
        self,
        session_id: str,
        mood_score: int = None,
        satisfaction_score: int = None,
        depression_level: int = None,
        rapport_score: int = None,
        message_count: int = None
    ) -> PatientState:
        """
        更新患者状态（Redis + MySQL）

        Args:
            session_id: 会话ID
            mood_score: 心情指数
            satisfaction_score: 满意度
            depression_level: 抑郁程度
            rapport_score: 信任度
            message_count: 对话轮次

        Returns:
            更新后的PatientState对象
        """
        # 1. 获取或创建MySQL记录
        db_state = self.state_repo.get_or_create_state(session_id)

        # 2. 更新MySQL
        updated_db_state = self.state_repo.update_state(
            session_id=session_id,
            mood_score=mood_score,
            satisfaction_score=satisfaction_score,
            depression_level=depression_level,
            rapport_score=rapport_score,
            message_count=message_count
        )

        # 3. 更新Redis
        redis_updates = {}
        if mood_score is not None:
            redis_updates['mood_score'] = mood_score
        if satisfaction_score is not None:
            redis_updates['satisfaction_score'] = satisfaction_score
        if depression_level is not None:
            redis_updates['depression_level'] = depression_level
        if rapport_score is not None:
            redis_updates['rapport_score'] = rapport_score
        if message_count is not None:
            redis_updates['message_count'] = message_count

        redis_state = self.redis_manager.update_patient_state(session_id, redis_updates)

        return redis_state if redis_state else PatientState(
            mood_score=updated_db_state.mood_score,
            satisfaction_score=updated_db_state.satisfaction_score,
            depression_level=updated_db_state.depression_level,
            rapport_score=updated_db_state.rapport_score,
            message_count=updated_db_state.message_count
        )

    def increment_message_count(self, session_id: str) -> int:
        """
        增加消息计数

        Args:
            session_id: 会话ID

        Returns:
            新的消息计数
        """
        # 获取当前状态
        current = self.get_state(session_id)
        if not current:
            current = PatientState()

        new_count = current.message_count + 1

        # 同时更新Redis和MySQL
        self.redis_manager.increment_message_count(session_id)
        db_state = self.state_repo.get_state(session_id)
        if db_state:
            self.state_repo.update_state(session_id, message_count=new_count)

        return new_count

    def delete_session(self, session_id: str) -> bool:
        """
        删除会话数据（Redis + MySQL）

        Args:
            session_id: 会话ID

        Returns:
            是否成功
        """
        redis_ok = self.redis_manager.delete_session(session_id)
        mysql_ok = self.state_repo.delete_state(session_id)
        return redis_ok and mysql_ok
