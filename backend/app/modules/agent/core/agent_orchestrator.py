"""
Agent编排器
协调PatientAgent、StateUpdateEngine和CrisisDetector
"""
from typing import Optional, Dict
from sqlalchemy.orm import Session

from backend.app.modules.agent.chains.patient_agent_chain import patient_agent_chain
from backend.app.modules.agent.core.state_update_engine import state_update_engine
from backend.app.modules.agent.core.crisis_detector import crisis_detector
from backend.app.modules.agent.services.patient_state_service import PatientStateService
from backend.app.modules.agent.models.patient_state import PatientState, CrisisEvent


class AgentOrchestrator:
    """
    Agent编排器 - 协调PatientAgent和CrisisDetector

    负责完整的Agent交互流程：
    1. 获取当前患者状态
    2. 调用PatientAgent生成回复
    3. 计算状态更新
    4. 检测危机
    5. 持久化状态变更
    """

    def __init__(self, db: Session):
        """初始化Agent编排器"""
        self.patient_chain = patient_agent_chain
        self.state_engine = state_update_engine
        self.crisis_detector = crisis_detector
        self.state_service = PatientStateService(db)

    async def process_turn(
        self,
        session_id: str,
        user_input: str,
        scenario_title: str = "围产期抑郁场景",
        patient_background: str = "见对话历史",
        conversation_history: Optional[list] = None
    ) -> Dict:
        """
        处理一轮对话

        Args:
            session_id: 会话ID
            user_input: 用户/护士输入
            scenario_title: 场景标题
            patient_background: 患者背景
            conversation_history: 对话历史

        Returns:
            包含回复和状态信息的字典
        """
        if conversation_history is None:
            conversation_history = []

        # 1. 获取当前状态
        current_state = self.state_service.get_state(session_id)
        if current_state is None:
            current_state = PatientState()

        # 2. 检测是否处于危机状态
        crisis = self.crisis_detector.detect_crisis(current_state)

        # 3. 如果有危机，优先返回危机响应
        if crisis:
            # 危机情况下仍需更新状态
            state_update = self.state_engine.calculate_state_update(
                current_state=current_state.model_dump(),
                user_input=user_input
            )
            self._apply_state_update(session_id, current_state, state_update)

            return {
                "response": crisis.message,
                "state": self.state_service.get_state(session_id).model_dump(),
                "crisis": crisis.model_dump(),
                "is_crisis": True
            }

        # 4. 调用PatientAgent生成回复
        agent_response = await self.patient_chain.ainvoke(
            scenario_title=scenario_title,
            patient_background=patient_background,
            current_state=current_state.model_dump(),
            conversation_history=conversation_history,
            user_input=user_input
        )

        # 5. 计算状态更新
        state_update = self.state_engine.calculate_state_update(
            current_state=current_state.model_dump(),
            user_input=user_input,
            agent_response=agent_response
        )

        # 6. 应用状态更新
        new_state = self._apply_state_update(session_id, current_state, state_update)

        # 7. 增加消息计数
        new_count = self.state_service.increment_message_count(session_id)
        if new_state:
            new_state.message_count = new_count

        # 8. 检测新的危机（更新后）
        new_crisis = None
        if new_state:
            new_crisis = self.crisis_detector.detect_crisis(new_state)

        return {
            "response": agent_response,
            "state": new_state.model_dump() if new_state else current_state.model_dump(),
            "state_update": state_update.model_dump(),
            "crisis": new_crisis.model_dump() if new_crisis else None,
            "is_crisis": new_crisis is not None,
            "meta_data": {
                "session_id": session_id,
                "message_count": new_count,
                "agent_type": "patient_agent"
            }
        }

    def _apply_state_update(
        self,
        session_id: str,
        current_state: PatientState,
        state_update
    ) -> PatientState:
        """应用状态更新"""
        new_mood = current_state.mood_score
        new_satisfaction = current_state.satisfaction_score
        new_depression = current_state.depression_level
        new_rapport = current_state.rapport_score

        if state_update.mood_score_delta is not None:
            new_mood = max(0, min(100, current_state.mood_score + state_update.mood_score_delta))
        if state_update.satisfaction_score_delta is not None:
            new_satisfaction = max(0, min(100, current_state.satisfaction_score + state_update.satisfaction_score_delta))
        if state_update.depression_level_delta is not None:
            new_depression = max(0, min(100, current_state.depression_level + state_update.depression_level_delta))
        if state_update.rapport_score_delta is not None:
            new_rapport = max(0, min(100, current_state.rapport_score + state_update.rapport_score_delta))

        return self.state_service.update_state(
            session_id=session_id,
            mood_score=new_mood,
            satisfaction_score=new_satisfaction,
            depression_level=new_depression,
            rapport_score=new_rapport
        )

    def get_state(self, session_id: str) -> Optional[PatientState]:
        """
        获取患者当前状态

        Args:
            session_id: 会话ID

        Returns:
            PatientState对象
        """
        return self.state_service.get_state(session_id)

    def check_crisis(self, session_id: str) -> Optional[Dict]:
        """
        检查当前会话是否存在危机

        Args:
            session_id: 会话ID

        Returns:
            危机事件字典
        """
        state = self.state_service.get_state(session_id)
        if state is None:
            return None

        crisis = self.crisis_detector.detect_crisis(state)
        return crisis.model_dump() if crisis else None

    def get_near_crisis_warning(self, session_id: str, buffer: int = 10) -> Dict:
        """
        获取危机预警信息

        Args:
            session_id: 会话ID
            buffer: 预警缓冲区大小

        Returns:
            预警状态字典
        """
        state = self.state_service.get_state(session_id)
        if state is None:
            return {}

        return self.crisis_detector.is_near_crisis(state, buffer)
