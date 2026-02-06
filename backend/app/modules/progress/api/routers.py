"""
学习进度 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.modules.progress.schemas.progress import (
    UserProgressResponse, UserProgressCreate, UserProgressUpdate
)
from backend.app.modules.progress.schemas.dashboard import DashboardStatsResponse
from backend.app.modules.progress.services.progress_service import ProgressService
from backend.app.modules.progress.services.dashboard_service import DashboardService
from backend.app.core.common.exceptions import NotFoundException
from backend.app.core.dependencies import get_current_user_with_fallback

router = APIRouter(prefix="/progress", tags=["学习进度"])


@router.get("/dashboard", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    user_id: str = Depends(get_current_user_with_fallback),
    db: Session = Depends(get_db)
):
    """获取学习仪表盘统计数据"""
    service = DashboardService(db)
    return service.get_user_dashboard_stats(user_id)


@router.post("/courses/{course_id}/start", response_model=UserProgressResponse, status_code=status.HTTP_201_CREATED)
async def start_course(
    course_id: str,
    user_id: str = Depends(get_current_user_with_fallback),
    db: Session = Depends(get_db)
):
    """
    开始学习课程

    - **course_id**: 课程ID
    """
    service = ProgressService(db)
    course_data = UserProgressCreate(course_id=course_id)
    return service.start_course(user_id, course_data)


@router.get("/courses/{course_id}", response_model=UserProgressResponse)
async def get_course_progress(
    course_id: str,
    user_id: str = Depends(get_current_user_with_fallback),
    db: Session = Depends(get_db)
):
    """获取特定课程的学习进度"""
    service = ProgressService(db)
    progress = service.get_user_progress(user_id, course_id)
    if not progress:
        raise NotFoundException("学习进度不存在")
    return progress


@router.get("/", response_model=List[UserProgressResponse])
async def get_all_progress(
    user_id: str = Depends(get_current_user_with_fallback),
    db: Session = Depends(get_db)
):
    """获取用户所有课程的学习进度"""
    service = ProgressService(db)
    return service.get_user_all_progress(user_id)


@router.put("/courses/{course_id}", response_model=UserProgressResponse)
async def update_progress(
    course_id: str,
    progress_data: UserProgressUpdate,
    user_id: str = Depends(get_current_user_with_fallback),
    db: Session = Depends(get_db)
):
    """更新学习进度"""
    service = ProgressService(db)
    progress = service.update_progress(user_id, course_id, progress_data)
    if not progress:
        raise NotFoundException("学习进度不存在")
    return progress