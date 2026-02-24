"""
Dashboard Service
学习仪表盘服务 - 负责聚合统计数据
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from backend.app.models.progress import UserProgress
from backend.app.models.evaluation import EvaluationReport
from backend.app.models.chat import ChatSession
from backend.app.models.scenario import Scenario
from backend.app.modules.progress.schemas.dashboard import DashboardStatsResponse, RadarChartData, ScenarioHistoryItem
from backend.app.modules.progress.schemas.progress import UserProgressResponse
from backend.app.core.config.settings import settings
from backend.app.core.services.redis_cache import redis_cache


class DashboardService:
    """仪表盘服务类"""

    CACHE_KEY_PREFIX = "dashboard:"

    def __init__(self, db: Session):
        self.db = db

    def get_user_dashboard_stats(self, user_id: str) -> DashboardStatsResponse:
        """获取用户仪表盘聚合统计数据"""

        cache_key = f"{self.CACHE_KEY_PREFIX}{user_id}"
        if settings.CACHE_ENABLED:
            cached = redis_cache.get_json(cache_key)
            if cached:
                return DashboardStatsResponse.model_validate(cached)
        
        # 1. 课程统计
        total_courses = self.db.query(func.count(UserProgress.id)).filter(
            UserProgress.user_id == user_id
        ).scalar() or 0
        
        completed_courses = self.db.query(func.count(UserProgress.id)).filter(
            UserProgress.user_id == user_id,
            UserProgress.is_completed == True
        ).scalar() or 0

        # 2. 模拟训练统计 (需要关联 ChatSession)
        # 获取该用户所有相关的 session_id
        session_ids = [
            sid for (sid,) in self.db.query(ChatSession.id).filter(
                ChatSession.user_id == user_id
            ).all()
        ]
        
        # 如果没有会话，直接返回默认值
        if not session_ids:
            return DashboardStatsResponse(
                total_courses=total_courses,
                completed_courses=completed_courses,
                total_scenarios=0,
                avg_score=0,
                radar_data=[],
                recent_activities=[UserProgressResponse.model_validate(p) for p in self.db.query(UserProgress).filter(
                    UserProgress.user_id == user_id
                ).order_by(UserProgress.created_at.desc()).limit(5).all()],
                scenario_history=[]
            )

        total_scenarios = self.db.query(EvaluationReport).filter(
            EvaluationReport.session_id.in_(session_ids),
            EvaluationReport.status == 'completed'
        ).count()
        
        # 3. 计算雷达图各项平均分
        radar_stats = self.db.query(
            func.avg(EvaluationReport.radar_a_risk_identification).label('risk'),
            func.avg(EvaluationReport.radar_b_communication).label('comm'),
            func.avg(EvaluationReport.radar_c_skill_application).label('skill'),
            func.avg(EvaluationReport.radar_d_safety_management).label('safety'),
            func.avg(EvaluationReport.radar_e_self_efficacy).label('self')
        ).filter(
            EvaluationReport.session_id.in_(session_ids),
            EvaluationReport.status == 'completed'
        ).first()

        # 构建雷达数据 (处理 None 的情况)
        def get_avg(val):
            return int(val) if val is not None else 0

        radar_data = [
            RadarChartData(subject="风险识别", A=get_avg(radar_stats.risk)),
            RadarChartData(subject="沟通支持", A=get_avg(radar_stats.comm)),
            RadarChartData(subject="技能应用", A=get_avg(radar_stats.skill)),
            RadarChartData(subject="安全管理", A=get_avg(radar_stats.safety)),
            RadarChartData(subject="自我效能", A=get_avg(radar_stats.self)),
        ]
        
        # 4. 计算综合平均分
        avg_score = self.db.query(func.avg(EvaluationReport.total_score)).filter(
            EvaluationReport.session_id.in_(session_ids),
            EvaluationReport.status == 'completed'
        ).scalar()
        
        if avg_score is None:
            avg_score = 0
            
        # 5. 近期活动 (UserProgress 前5条，按最近更新排序)
        recent_progress = self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id
        ).order_by(
            UserProgress.created_at.desc() # 或者 completed_at? 创建时间比较稳妥表示最近开始的
        ).limit(5).all()
        
        recent_activities = [UserProgressResponse.model_validate(p) for p in recent_progress]
        
        # 6. 情景模拟历史 (基于 ChatSession 获取)
        recent_sessions = self.db.query(ChatSession).filter(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.start_time.desc()).limit(10).all()
        
        scenario_history = []
        if recent_sessions:
            recent_session_ids = [s.id for s in recent_sessions]
            
            # Map session to scenario
            scenario_ids = list(set([s.scenario_id for s in recent_sessions]))
            scenarios = self.db.query(Scenario).filter(Scenario.id.in_(scenario_ids)).all()
            scenario_name_map = {s.id: s.title for s in scenarios}
            
            # Fetch evaluations for these sessions
            evaluations = self.db.query(EvaluationReport).filter(
                EvaluationReport.session_id.in_(recent_session_ids)
            ).all()
            eval_map = {e.session_id: e for e in evaluations}
            
            for session in recent_sessions:
                e = eval_map.get(session.id)
                # Determine status
                if e:
                    status = e.status
                    total_score = e.total_score
                    level_assessment = e.level_assessment
                else:
                    if session.status == 'completed':
                        status = 'generating'
                    else:
                        status = session.status  # 'active' or 'abandoned'
                    total_score = None
                    level_assessment = None

                scenario_history.append(
                    ScenarioHistoryItem(
                        session_id=session.id,
                        scenario_name=scenario_name_map.get(session.scenario_id, '未知场景'),
                        total_score=total_score,
                        level_assessment=level_assessment,
                        status=status,
                        created_at=session.start_time
                    )
                )

        response = DashboardStatsResponse(
            total_courses=total_courses,
            completed_courses=completed_courses,
            total_scenarios=total_scenarios,
            avg_score=round(avg_score, 1),
            radar_data=radar_data,
            recent_activities=recent_activities,
            scenario_history=scenario_history
        )
        if settings.CACHE_ENABLED:
            redis_cache.set_json(
                cache_key,
                response.model_dump(mode="json"),
                ttl_seconds=settings.CACHE_DEFAULT_TTL
            )
        return response

    @classmethod
    def clear_dashboard_cache(cls, user_id: str):
        if settings.CACHE_ENABLED:
            try:
                redis_cache.delete(f"{cls.CACHE_KEY_PREFIX}{user_id}")
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to clear dashboard cache: {e}")
