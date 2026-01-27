"""
评估报告相关的 Pydantic 模型 - THP五维评分系统
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from datetime import datetime


class RadarChart(BaseModel):
    """雷达图数据 - THP五维评分"""
    A_risk_identification: int = Field(..., ge=0, le=100, description="A类-风险识别能力")
    B_communication: int = Field(..., ge=0, le=100, description="B类-沟通支持能力")
    C_skill_application: int = Field(..., ge=0, le=100, description="C类-THP技能应用")
    D_safety_management: int = Field(..., ge=0, le=100, description="D类-安全管理能力")
    E_self_efficacy: int = Field(..., ge=0, le=100, description="E类-自我效能感")


class StateAnalysis(BaseModel):
    """状态变化分析"""
    mood_change: int = Field(default=0, description="心情变化")
    rapport_change: int = Field(default=0, description="信任关系变化")
    depression_change: int = Field(default=0, description="抑郁程度变化")
    overall_performance: str = Field(default="", description="整体表现评价")


class FeedbackItem(BaseModel):
    """详细反馈项"""
    dimension: str = Field(..., description="评估维度")
    status: str = Field(..., description="通过/失败")
    dialogue_ref_id: Optional[int] = Field(None, description="对话轮次引用")
    user_input: Optional[str] = Field(None, description="用户输入")
    patient_state_snapshot: Optional[Union[str, Dict[str, Any]]] = Field(None, description="患者状态快照")
    critique: str = Field(..., description="批评意见")
    expert_suggestion: str = Field(..., description="专家建议")


class EvaluationReportResponse(BaseModel):
    """评估报告响应模型"""
    id: str
    session_id: str
    total_score: Optional[int] = None
    level_assessment: Optional[str] = None
    radar_chart: Optional[RadarChart] = None
    state_analysis: Optional[StateAnalysis] = None
    detailed_feedback: Optional[List[FeedbackItem]] = None
    technical_guidance: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def from_orm_model(cls, report: 'EvaluationReport') -> 'EvaluationReportResponse':
        """从 ORM 模型转换为响应模型"""
        # 构建雷达图数据
        radar_chart = None
        if all([
            report.radar_a_risk_identification is not None,
            report.radar_b_communication is not None,
            report.radar_c_skill_application is not None,
            report.radar_d_safety_management is not None,
            report.radar_e_self_efficacy is not None,
        ]):
            radar_chart = RadarChart(
                A_risk_identification=report.radar_a_risk_identification,
                B_communication=report.radar_b_communication,
                C_skill_application=report.radar_c_skill_application,
                D_safety_management=report.radar_d_safety_management,
                E_self_efficacy=report.radar_e_self_efficacy,
            )

        # 处理状态分析数据
        state_analysis = None
        if report.state_analysis:
            if isinstance(report.state_analysis, dict):
                try:
                    state_analysis = StateAnalysis(**report.state_analysis)
                except Exception:
                    state_analysis = report.state_analysis
            else:
                state_analysis = report.state_analysis

        # 处理详细反馈数据
        detailed_feedback = None
        if report.detailed_feedback:
            if isinstance(report.detailed_feedback, list):
                valid_feedback_items = []
                for item in report.detailed_feedback:
                    if isinstance(item, dict):
                        try:
                            valid_feedback_items.append(FeedbackItem(**item))
                        except Exception as e:
                            print(f"⚠️  跳过无效的反馈项: {e}")
                    else:
                        valid_feedback_items.append(item)
                detailed_feedback = valid_feedback_items if valid_feedback_items else None
            else:
                detailed_feedback = report.detailed_feedback

        return cls(
            id=report.id,
            session_id=report.session_id,
            total_score=report.total_score,
            level_assessment=report.level_assessment,
            radar_chart=radar_chart,
            state_analysis=state_analysis,
            detailed_feedback=detailed_feedback,
            technical_guidance=report.technical_guidance,
            meta_data=report.meta_data,
            created_at=report.created_at,
            updated_at=report.updated_at,
        )

    class Config:
        from_attributes = True
