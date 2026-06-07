"""
状态分析数据模型
定义LLM输出的状态变化结构
"""
from typing import Optional
from pydantic import BaseModel, Field


class StateAnalysis(BaseModel):
    """
    状态分析结果

    由LLM分析护士/学员的回复，计算患者状态的变化
    """

    mood_delta: Optional[int] = Field(
        default=None,
        description="心情变化值 (-20 到 +20)",
        ge=-20, le=20
    )

    satisfaction_delta: Optional[int] = Field(
        default=None,
        description="满意度变化值 (-20 到 +20)",
        ge=-20, le=20
    )

    depression_delta: Optional[int] = Field(
        default=None,
        description="抑郁程度变化值 (-15 到 +15)",
        ge=-15, le=15
    )

    rapport_delta: Optional[int] = Field(
        default=None,
        description="信任度变化值 (-20 到 +20)",
        ge=-20, le=20
    )

    # ========== 危机检测 ==========
    suicide_risk: Optional[bool] = Field(
        default=None,
        description="是否有自杀倾向。如果为true，前端应显示报警按钮"
    )

    patient_leaving: Optional[bool] = Field(
        default=None,
        description="患者是否明确表示要离开（如'我先走了'）。如果为true，将强制结束对话"
    )