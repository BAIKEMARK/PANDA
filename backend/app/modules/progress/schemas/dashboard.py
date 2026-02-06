"""
Dashboard Schemas
学习仪表盘相关的数据模型
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from backend.app.modules.progress.schemas.progress import UserProgressResponse


class RadarChartData(BaseModel):
    """雷达图数据点"""
    subject: str  # 维度名称 (如 "风险识别")
    A: int        # 得分
    fullMark: int = 100 # 满分


class ScenarioHistoryItem(BaseModel):
    """情景模拟历史记录"""
    session_id: str
    scenario_name: str
    total_score: Optional[int] = None
    level_assessment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStatsResponse(BaseModel):
    """仪表盘统计数据响应"""
    # 基础统计
    total_courses: int       # 总课程数 (已开始)
    completed_courses: int   # 已完成课程数
    total_scenarios: int     # 已完成模拟数
    avg_score: float         # 综合平均分
    
    # 图表数据
    radar_data: List[RadarChartData] # 五维能力雷达图
    
    # 近期活动
    recent_activities: List[UserProgressResponse]
    
    # 情景模拟历史
    scenario_history: List[ScenarioHistoryItem] = []

