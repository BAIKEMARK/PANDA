"""
Evaluation Report ORM Model
评估报告数据库模型 - THP五维评分系统
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, JSON, Float, func
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class EvaluationReport(Base):
    """评估报告表"""
    __tablename__ = "evaluation_reports"

    id = Column(CHAR(36), primary_key=True, comment="报告ID")
    session_id = Column(CHAR(36), nullable=False, unique=True, index=True, comment="会话ID")

    # 总体评分
    total_score = Column(Integer, comment="总分 (0-100)")
    level_assessment = Column(String(20), comment="等级评定: 优秀/良好/合格/不合格")

    # 五维雷达图数据
    radar_a_risk_identification = Column(Integer, comment="A类-风险识别能力 (0-100)")
    radar_b_communication = Column(Integer, comment="B类-沟通支持能力 (0-100)")
    radar_c_skill_application = Column(Integer, comment="C类-THP技能应用 (0-100)")
    radar_d_safety_management = Column(Integer, comment="D类-安全管理能力 (0-100)")
    radar_e_self_efficacy = Column(Integer, comment="E类-自我效能感 (0-100)")

    # 状态变化分析
    state_analysis = Column(JSON, comment="状态变化分析数据")

    # 详细反馈 (JSON数组)
    detailed_feedback = Column(JSON, comment="详细反馈列表")

    # 技术指导
    technical_guidance = Column(Text, comment="技术指导建议")

    # 元数据（使用meta_data避免与SQLAlchemy的metadata冲突）
    meta_data = Column(JSON, comment="其他元数据")

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
