"""
Agent编排器
协调StateUpdateChain和PatientAgentChain
"""
from typing import Dict, Optional
from sqlalchemy.orm import Session

from backend.app.modules.conversation.agent.chains.patient_agent_chain import patient_agent_chain
from backend.app.modules.conversation.agent.chains.state_update_chain import state_update_chain
from backend.app.modules.conversation.agent.services.patient_state_service import PatientStateService
from backend.app.modules.conversation.agent.models.patient_state import PatientState
from backend.app.modules.conversation.agent.models.state_analysis import StateAnalysis
from backend.app.modules.conversation.repositories.chat_repository import ChatRepository


class AgentOrchestrator:
    """
    Agent编排器 - 协调状态分析和患者回复生成

    工作流：
    1. 获取当前患者状态
    2. 调用StateUpdateChain分析状态变化
    3. 应用状态更新
    4. 调用PatientAgentChain生成患者回复
    5. 处理患者离开检测（如果有）
    6. 持久化状态变更
    """

    def __init__(self, db: Session):
        """初始化Agent编排器"""
        self.state_update_chain = state_update_chain
        self.patient_chain = patient_agent_chain
        self.state_service = PatientStateService(db)
        self.chat_repository = ChatRepository(db)

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

        try:
            # 1. 获取当前状态
            current_state = self.state_service.get_state(session_id)
            if current_state is None:
                current_state = PatientState()

            # 2. 调用StateUpdateChain分析状态变化
            state_analysis: StateAnalysis = await self.state_update_chain.ainvoke(
                nurse_input=user_input,
                current_state=current_state.model_dump(),
                conversation_history=conversation_history
            )

            # 3. 处理自杀倾向检测（数据库操作使用事务）
            if state_analysis.suicide_risk is True:
                try:
                    self.chat_repository.update_suicide_risk(session_id, True)
                    self.db.commit()
                except Exception as e:
                    self.db.rollback()
                    # 记录错误但不中断流程
                    print(f"[ERROR] 更新自杀风险标记失败: {e}")

            # 4. 应用状态更新，计算新状态
            new_state = self._apply_state_update(current_state, state_analysis)

            # 5. 保存新状态到Redis
            self.state_service.update_state(
                session_id=session_id,
                mood_score=new_state.mood_score,
                satisfaction_score=new_state.satisfaction_score,
                depression_level=new_state.depression_level,
                rapport_score=new_state.rapport_score
            )

            # 6. 增加消息计数
            new_count = self.state_service.increment_message_count(session_id)
            new_state.message_count = new_count

            # 7. 调用PatientAgentChain生成患者回复（基于新状态）
            agent_response = await self.patient_chain.ainvoke(
                scenario_title=scenario_title,
                patient_background=patient_background,
                current_state=new_state.model_dump(),
                conversation_history=conversation_history,
                user_input=user_input
            )

            # 8. 检查是否患者离开 - 在生成回复后再处理
            if state_analysis.patient_leaving is True:
                # 患者说完告别话后，但不自动结束会话
                # 让用户自己决定是评估还是继续对话
                # 返回回复 + 离开标记
                return {
                    "response": agent_response,  # 返回告别消息
                    "state": new_state.model_dump(),
                    "force_end": False,  # 不强制结束，让用户选择
                    "patient_leaving": True,  # 标记患者想离开
                    "message": "患者表示要离开"
                }

            # 9. 返回正常结果
            return {
                "response": agent_response,
                "state": new_state.model_dump(),
                "state_delta": {
                    "mood_delta": state_analysis.mood_delta,
                    "satisfaction_delta": state_analysis.satisfaction_delta,
                    "depression_delta": state_analysis.depression_delta,
                    "rapport_delta": state_analysis.rapport_delta,
                },
                "crisis_alert": {
                    "suicide_risk": state_analysis.suicide_risk,
                },
                "meta_data": {
                    "session_id": session_id,
                    "message_count": new_count,
                    "agent_type": "patient_agent"
                }
            }
        
        except Exception as e:
            # 发生异常时回滚数据库事务
            self.db.rollback()
            print(f"[ERROR] 处理对话轮次失败: {e}")
            raise

    def _apply_state_update(
        self,
        current_state: PatientState,
        state_analysis: StateAnalysis
    ) -> PatientState:
        """
        应用状态更新

        Args:
            current_state: 当前状态
            state_analysis: 状态分析结果

        Returns:
            更新后的新状态
        """
        new_mood = current_state.mood_score
        new_satisfaction = current_state.satisfaction_score
        new_depression = current_state.depression_level
        new_rapport = current_state.rapport_score

        # 应用变化，确保在0-100范围内
        if state_analysis.mood_delta is not None:
            new_mood = max(0, min(100, current_state.mood_score + state_analysis.mood_delta))
        if state_analysis.satisfaction_delta is not None:
            new_satisfaction = max(0, min(100, current_state.satisfaction_score + state_analysis.satisfaction_delta))
        if state_analysis.depression_delta is not None:
            new_depression = max(0, min(100, current_state.depression_level + state_analysis.depression_delta))
        if state_analysis.rapport_delta is not None:
            new_rapport = max(0, min(100, current_state.rapport_score + state_analysis.rapport_delta))

        return PatientState(
            mood_score=new_mood,
            satisfaction_score=new_satisfaction,
            depression_level=new_depression,
            rapport_score=new_rapport,
            message_count=current_state.message_count
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
