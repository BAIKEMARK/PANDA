"""
危机检测器
监控患者状态指标，在达到阈值时触发危机事件
"""
from typing import Optional, Dict
from datetime import datetime

from backend.app.modules.agent.models.patient_state import PatientState, CrisisEvent
from backend.app.modules.agent.core.state_update_engine import state_update_engine


class CrisisDetector:
    """
    危机检测器 - 基于阈值自动触发

    监控四项核心指标：
    - mood_score: 心情指数（低于阈值触发情绪危机）
    - satisfaction_score: 满意度（低于阈值触发信任危机）
    - depression_level: 抑郁程度（高于阈值触发抑郁危机）
    - rapport_score: 信任度（低于阈值触发关系破裂危机）
    """

    def __init__(self):
        """初始化危机检测器"""
        self.engine = state_update_engine
        self.thresholds = self.engine.get_crisis_thresholds()

    def detect_crisis(self, state: PatientState) -> Optional[CrisisEvent]:
        """
        检测是否存在危机

        Args:
            state: 患者当前状态

        Returns:
            CrisisEvent对象，如果没有危机返回None
        """
        # 按优先级检测各种危机
        # 1. 心情过低危机
        if state.mood_score <= self.thresholds.get('mood_too_low', 15):
            return CrisisEvent(
                crisis_type="mood_crisis",
                severity=self._calculate_severity(state.mood_score, 15, is_lower_better=True),
                current_value=state.mood_score,
                threshold=self.thresholds['mood_too_low'],
                message=self.engine.get_crisis_response('mood_crisis')
            )

        # 2. 满意度过低危机
        if state.satisfaction_score <= self.thresholds.get('satisfaction_too_low', 10):
            return CrisisEvent(
                crisis_type="satisfaction_crisis",
                severity=self._calculate_severity(state.satisfaction_score, 10, is_lower_better=True),
                current_value=state.satisfaction_score,
                threshold=self.thresholds['satisfaction_too_low'],
                message=self.engine.get_crisis_response('satisfaction_crisis')
            )

        # 3. 抑郁程度过高危机
        if state.depression_level >= self.thresholds.get('depression_too_high', 85):
            return CrisisEvent(
                crisis_type="depression_crisis",
                severity=self._calculate_severity(state.depression_level, 85, is_lower_better=False),
                current_value=state.depression_level,
                threshold=self.thresholds['depression_too_high'],
                message=self.engine.get_crisis_response('depression_crisis')
            )

        # 4. 信任度破裂危机
        if state.rapport_score <= self.thresholds.get('rapport_broken', 10):
            return CrisisEvent(
                crisis_type="rapport_crisis",
                severity=self._calculate_severity(state.rapport_score, 10, is_lower_better=True),
                current_value=state.rapport_score,
                threshold=self.thresholds['rapport_broken'],
                message=self.engine.get_crisis_response('rapport_crisis')
            )

        return None

    def should_trigger_crisis(self, state: PatientState) -> bool:
        """
        快速检查是否应该触发危机

        Args:
            state: 患者当前状态

        Returns:
            是否触发危机
        """
        return self.detect_crisis(state) is not None

    def check_multiple_crisis(self, state: PatientState) -> list[CrisisEvent]:
        """
        检测所有可能的危机（用于复合危机场景）

        Args:
            state: 患者当前状态

        Returns:
            CrisisEvent列表
        """
        crises = []

        if state.mood_score <= self.thresholds.get('mood_too_low', 15):
            crises.append(CrisisEvent(
                crisis_type="mood_crisis",
                severity=self._calculate_severity(state.mood_score, 15, is_lower_better=True),
                current_value=state.mood_score,
                threshold=self.thresholds['mood_too_low'],
                message=self.engine.get_crisis_response('mood_crisis')
            ))

        if state.satisfaction_score <= self.thresholds.get('satisfaction_too_low', 10):
            crises.append(CrisisEvent(
                crisis_type="satisfaction_crisis",
                severity=self._calculate_severity(state.satisfaction_score, 10, is_lower_better=True),
                current_value=state.satisfaction_score,
                threshold=self.thresholds['satisfaction_too_low'],
                message=self.engine.get_crisis_response('satisfaction_crisis')
            ))

        if state.depression_level >= self.thresholds.get('depression_too_high', 85):
            crises.append(CrisisEvent(
                crisis_type="depression_crisis",
                severity=self._calculate_severity(state.depression_level, 85, is_lower_better=False),
                current_value=state.depression_level,
                threshold=self.thresholds['depression_too_high'],
                message=self.engine.get_crisis_response('depression_crisis')
            ))

        if state.rapport_score <= self.thresholds.get('rapport_broken', 10):
            crises.append(CrisisEvent(
                crisis_type="rapport_crisis",
                severity=self._calculate_severity(state.rapport_score, 10, is_lower_better=True),
                current_value=state.rapport_score,
                threshold=self.thresholds['rapport_broken'],
                message=self.engine.get_crisis_response('rapport_crisis')
            ))

        return crises

    def _calculate_severity(
        self,
        current_value: int,
        threshold: int,
        is_lower_better: bool
    ) -> str:
        """
        计算危机严重程度

        Args:
            current_value: 当前值
            threshold: 阈值
            is_lower_better: 是否越低越好

        Returns:
            严重程度: low/medium/high/critical
        """
        if is_lower_better:
            # 值越低越危险
            distance = threshold - current_value
        else:
            # 值越高越危险
            distance = current_value - threshold

        if distance <= 5:
            return "low"
        elif distance <= 10:
            return "medium"
        elif distance <= 20:
            return "high"
        else:
            return "critical"

    def get_crisis_guidance(self, crisis: CrisisEvent) -> str:
        """
        获取危机应对建议

        Args:
            crisis: 危机事件

        Returns:
            应对建议文本
        """
        guidance_map = {
            "mood_crisis": "患者情绪极度低落，需要立即停止追问，提供情感支持和安全感。",
            "satisfaction_crisis": "患者感到被忽视或误解，需要主动倾听，确认患者的感受。",
            "depression_crisis": "患者抑郁程度严重，可能存在自伤风险，需要立即进行安全评估。",
            "rapport_crisis": "医患关系破裂，需要暂停当前话题，重新建立信任关系。"
        }

        return guidance_map.get(crisis.crisis_type, "需要专业的危机干预技巧。")

    def is_near_crisis(self, state: PatientState, buffer: int = 10) -> Dict[str, bool]:
        """
        检查各项指标是否接近危机阈值（预警功能）

        Args:
            state: 患者当前状态
            buffer: 预警缓冲区大小

        Returns:
            各指标的预警状态
        """
        thresholds = self.thresholds

        return {
            "mood_near_crisis": state.mood_score <= thresholds.get('mood_too_low', 15) + buffer,
            "satisfaction_near_crisis": state.satisfaction_score <= thresholds.get('satisfaction_too_low', 10) + buffer,
            "depression_near_crisis": state.depression_level >= thresholds.get('depression_too_high', 85) - buffer,
            "rapport_near_crisis": state.rapport_score <= thresholds.get('rapport_broken', 10) + buffer
        }


# 创建全局实例
crisis_detector = CrisisDetector()
