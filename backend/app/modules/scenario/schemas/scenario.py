"""
场景相关的 Pydantic 模型
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ScenarioBase(BaseModel):
    """场景基础模型"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    system_prompt: str = Field(..., min_length=1)
    patient_background: Optional[str] = None
    knowledge_tags: Optional[str] = None
    difficulty: int = Field(default=1, ge=1, le=5)
    time_period: Optional[str] = None


class ScenarioCreate(ScenarioBase):
    """场景创建模型"""
    pass


class ScenarioUpdate(BaseModel):
    """场景更新模型"""
    title: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    patient_background: Optional[str] = None
    knowledge_tags: Optional[str] = None
    difficulty: Optional[int] = None
    time_period: Optional[str] = None


class ScenarioResponse(ScenarioBase):
    """场景响应模型"""
    id: str
    created_at: datetime
    status: str  # draft, pending, published, archived

    class Config:
        from_attributes = True
