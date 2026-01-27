"""
学习进度相关的 Pydantic 模型
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserProgressBase(BaseModel):
    """学习进度基础模型"""
    user_id: str
    course_id: str
    is_completed: bool = False


class UserProgressCreate(BaseModel):
    """学习进度创建模型"""
    course_id: str


class UserProgressUpdate(BaseModel):
    """学习进度更新模型"""
    is_completed: Optional[bool] = None


class UserProgressResponse(UserProgressBase):
    """学习进度响应模型"""
    id: str
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
