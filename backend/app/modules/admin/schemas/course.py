from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CourseResponse(BaseModel):
    id: str
    title: str
    content_url: Optional[str]
    video_url: Optional[str]
    sort_order: int
    level: str
    description: Optional[str]
    org_id: Optional[str]
    scope: str
    version: str
    version_notes: Optional[str]
    status: str
    published_at: Optional[datetime]
    published_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="课程标题")
    content_url: Optional[str] = Field(None, description="课件PDF URL")
    video_url: Optional[str] = Field(None, description="视频URL")
    sort_order: int = Field(0, description="排序顺序")
    level: str = Field("L1", description="THP层级")
    description: Optional[str] = Field(None, description="课程描述")
    org_id: Optional[str] = Field(None, description="机构ID")
    scope: str = Field("private", description="发布范围")
    version: str = Field("1.0.0", description="版本号")
    version_notes: Optional[str] = Field(None, description="版本说明")


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    content_url: Optional[str] = None
    video_url: Optional[str] = None
    sort_order: Optional[int] = None
    level: Optional[str] = None
    description: Optional[str] = None
    org_id: Optional[str] = None
    scope: Optional[str] = None
    version: Optional[str] = None
    version_notes: Optional[str] = None
    status: Optional[str] = None


class CourseListResponse(BaseModel):
    courses: List[CourseResponse]
    total: int
    skip: int
    limit: int
