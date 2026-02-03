"""
Agent状态API路由
提供患者状态查询接口
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.modules.agent.core.agent_orchestrator import AgentOrchestrator
from backend.app.modules.agent.models.patient_state import PatientState

router = APIRouter(prefix="/agent", tags=["Agent状态"])


# ==================== Request/Response Models ====================

class PatientStateResponse(BaseModel):
    """患者状态响应"""
    session_id: str = Field(description="会话ID")
    mood_score: int = Field(description="心情指数 (0-100)")
    satisfaction_score: int = Field(description="满意度 (0-100)")
    depression_level: int = Field(description="抑郁程度 (0-100)")
    rapport_score: int = Field(description="信任度 (0-100)")
    message_count: int = Field(description="对话轮次")


class CrisisCheckResponse(BaseModel):
    """危机检测响应"""
    has_crisis: bool = Field(description="是否存在危机")
    crisis_type: Optional[str] = Field(default=None, description="危机类型")
    severity: Optional[str] = Field(default=None, description="严重程度")
    current_value: Optional[int] = Field(default=None, description="当前值")
    threshold: Optional[int] = Field(default=None, description="阈值")
    message: Optional[str] = Field(default=None, description="危机响应")


class NearCrisisWarningResponse(BaseModel):
    """危机预警响应"""
    mood_near_crisis: bool = Field(description="心情是否接近危机")
    satisfaction_near_crisis: bool = Field(description="满意度是否接近危机")
    depression_near_crisis: bool = Field(description="抑郁程度是否接近危机")
    rapport_near_crisis: bool = Field(description="信任度是否接近危机")


# ==================== API Endpoints ====================

def get_agent_orchestrator(db: Session = Depends(get_db)) -> AgentOrchestrator:
    """依赖注入：获取AgentOrchestrator实例"""
    return AgentOrchestrator(db)


@router.get("/sessions/{session_id}/state", response_model=PatientStateResponse)
async def get_patient_state(
    session_id: str,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    """
    获取患者当前状态

    Args:
        session_id: 会话ID

    Returns:
        患者当前状态
    """
    state = orchestrator.get_state(session_id)

    if state is None:
        raise HTTPException(status_code=404, detail="会话状态不存在")

    return PatientStateResponse(
        session_id=session_id,
        mood_score=state.mood_score,
        satisfaction_score=state.satisfaction_score,
        depression_level=state.depression_level,
        rapport_score=state.rapport_score,
        message_count=state.message_count
    )


@router.get("/sessions/{session_id}/crisis", response_model=CrisisCheckResponse)
async def check_crisis(
    session_id: str,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    """
    检查会话是否存在危机

    Args:
        session_id: 会话ID

    Returns:
        危机状态信息
    """
    crisis = orchestrator.check_crisis(session_id)

    if crisis is None:
        return CrisisCheckResponse(has_crisis=False)

    return CrisisCheckResponse(
        has_crisis=True,
        crisis_type=crisis.get("crisis_type"),
        severity=crisis.get("severity"),
        current_value=crisis.get("current_value"),
        threshold=crisis.get("threshold"),
        message=crisis.get("message")
    )


@router.get("/sessions/{session_id}/near-crisis", response_model=NearCrisisWarningResponse)
async def get_near_crisis_warning(
    session_id: str,
    buffer: int = 10,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    """
    获取危机预警信息

    Args:
        session_id: 会话ID
        buffer: 预警缓冲区大小（默认10）

    Returns:
        预警状态信息
    """
    warnings = orchestrator.get_near_crisis_warning(session_id, buffer)

    return NearCrisisWarningResponse(**warnings)
