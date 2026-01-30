"""
患者状态数据模型
定义患者动态指标的数据结构
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class PatientState(BaseModel):
    """患者动态状态模型"""

    # 四项核心指标 (0-100)
    mood_score: int = Field(default=50, description="心情指数 (0-100)")
    satisfaction_score: int = Field(default=50, description="满意度 (0-100)")
    depression_level: int = Field(default=50, description="抑郁程度 (0-100)")
    rapport_score: int = Field(default=50, description="信任度 (0-100)")

    # 会话元数据
    message_count: int = Field(default=0, description="对话轮次")


class PatientStateUpdate(BaseModel):
    """状态更新请求"""

    mood_score_delta: Optional[int] = Field(default=None, description="心情变化值")
    satisfaction_score_delta: Optional[int] = Field(default=None, description="满意度变化值")
    depression_level_delta: Optional[int] = Field(default=None, description="抑郁程度变化值")
    rapport_score_delta: Optional[int] = Field(default=None, description="信任度变化值")

    trigger: str = Field(default="user_input", description="触发原因")


class CrisisEvent(BaseModel):
    """危机事件模型"""

    crisis_type: str = Field(description="危机类型: mood_crisis/satisfaction_crisis/depression_crisis/rapport_crisis")
    severity: str = Field(description="严重程度: low/medium/high/critical")
    current_value: int = Field(description="触发时的当前值")
    threshold: int = Field(description="触发的阈值")
    timestamp: datetime = Field(default_factory=datetime.now)
    message: str = Field(description="危机描述信息")

