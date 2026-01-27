"""
学习进度服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.models.progress import UserProgress
from backend.app.modules.progress.schemas.progress import UserProgressCreate, UserProgressUpdate
from backend.app.modules.progress.repositories.progress_repository import ProgressRepository


class ProgressService:
    """学习进度服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ProgressRepository(db)

    def get_user_progress(self, user_id: str, course_id: str) -> Optional[UserProgress]:
        """获取用户特定课程的学习进度"""
        return self.repository.get_user_progress(user_id, course_id)

    def get_user_all_progress(self, user_id: str) -> List[UserProgress]:
        """获取用户所有课程的学习进度"""
        return self.repository.get_user_all_progress(user_id)

    def start_course(self, user_id: str, course_data: UserProgressCreate) -> UserProgress:
        """开始学习课程"""
        # 检查是否已有进度记录
        existing = self.get_user_progress(user_id, course_data.course_id)
        if existing:
            return existing

        # 创建新的进度记录
        return self.repository.create_progress(user_id, course_data.course_id)

    def update_progress(self, user_id: str, course_id: str, progress_data: UserProgressUpdate) -> Optional[UserProgress]:
        """更新学习进度"""
        progress = self.get_user_progress(user_id, course_id)
        if not progress:
            return None

        if progress_data.is_completed is not None:
            return self.repository.update_progress(progress, progress_data.is_completed)

        return progress

    def delete_progress(self, progress_id: str) -> bool:
        """删除学习进度"""
        return self.repository.delete_progress(progress_id)
