"""
Evaluation Schemas
评估报告相关的 Pydantic 模型
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class EvaluationScores(BaseModel):
    """评分详情模型"""
    empathy: int = Field(default=0, ge=0, le=100, description="共情能力")
    skill: int = Field(default=0, ge=0, le=100, description="专业技能")
    safety: int = Field(default=0, ge=0, le=100, description="安全意识")
    communication: int = Field(default=0, ge=0, le=100, description="沟通流畅度")


class EvaluationReportBase(BaseModel):
    """评估报告基础模型"""
    session_id: str
    scores: Optional[Dict[str, Any]] = None
    total_score: Optional[int] = Field(default=None, ge=0, le=100)
    ai_feedback: Optional[str] = None


class EvaluationReportCreate(BaseModel):
    """评估报告创建模型"""
    session_id: str
    scores: Dict[str, Any]
    total_score: int = Field(..., ge=0, le=100)
    ai_feedback: str


class EvaluationReportResponse(EvaluationReportBase):
    """评估报告响应模型"""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
