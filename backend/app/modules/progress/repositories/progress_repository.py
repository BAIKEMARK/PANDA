"""
学习进度数据访问层（Repository）
学习进度CRUD操作
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from backend.app.models.progress import UserProgress


class ProgressRepository:
    """学习进度数据访问仓库"""

    def __init__(self, db: Session):
        self.db = db

    def get_user_progress(self, user_id: str, course_id: str) -> Optional[UserProgress]:
        """获取用户特定课程的学习进度"""
        return self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.course_id == course_id
        ).first()

    def get_user_all_progress(self, user_id: str) -> List[UserProgress]:
        """获取用户所有课程的学习进度"""
        return self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id
        ).all()

    def create_progress(self, user_id: str, course_id: str) -> UserProgress:
        """创建学习进度"""
        progress = UserProgress(
            id=str(uuid.uuid4()),
            user_id=user_id,
            course_id=course_id,
            is_completed=False
        )
        self.db.add(progress)
        self.db.commit()
        self.db.refresh(progress)
        return progress

    def update_progress(self, progress: UserProgress, is_completed: bool) -> UserProgress:
        """更新学习进度"""
        progress.is_completed = is_completed
        if is_completed:
            progress.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(progress)
        return progress

    def delete_progress(self, progress_id: str) -> bool:
        """删除学习进度"""
        progress = self.db.query(UserProgress).filter(
            UserProgress.id == progress_id
        ).first()
        if progress:
            self.db.delete(progress)
            self.db.commit()
            return True
        return False
