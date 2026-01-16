"""
Course Schemas
课程相关的 Pydantic 模型
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from backend.app.common.constants import CourseLevel


class CourseBase(BaseModel):
    """课程基础模型"""
    title: str = Field(..., min_length=1, max_length=255)
    content_url: Optional[str] = None
    sort_order: int = 0
    level: CourseLevel = CourseLevel.L1
    description: Optional[str] = None


class CourseCreate(CourseBase):
    """课程创建模型"""
    pass


class CourseUpdate(BaseModel):
    """课程更新模型"""
    title: Optional[str] = None
    content_url: Optional[str] = None
    sort_order: Optional[int] = None
    level: Optional[CourseLevel] = None
    description: Optional[str] = None


class CourseResponse(CourseBase):
    """课程响应模型"""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
