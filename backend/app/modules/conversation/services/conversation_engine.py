"""
对话编排引擎 - 解耦跨模块依赖
通过依赖注入和接口实现模块间通信
"""
import logging
from typing import Dict, List, TYPE_CHECKING
from sqlalchemy.orm import Session

from backend.app.modules.conversation.repositories.chat_repository import ChatRepository
from backend.app.core.services.event_bus import event_bus, Events
from backend.app.interfaces.scenario_interface import ScenarioInterface
from backend.app.core.config.logging import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from backend.app.core.services.skill_config import SkillConfigManager


class ConversationEngine:
    """对话编排引擎 - 所有对话通过Agent进行"""

    def __init__(
        self,
        db: Session,
        scenario_interface: ScenarioInterface,
        agent_orchestrator: 'AgentOrchestrator'
    ):
        self.db = db
        self.repository = ChatRepository(db)
        self.scenario_interface = scenario_interface
        self.event_bus = event_bus
        self.agent_orchestrator = agent_orchestrator  # 必需的Agent编排器

    async def generate_ai_response(
        self,
        session_id: str,
        user_message: str,
        user_id: str
    ) -> Dict:
        """
        生成患者Agent回复（所有对话都通过Agent进行）

        Args:
            session_id: 会话ID
            user_message: 护士/用户消息
            user_id: 用户ID

        Returns:
            包含回复和状态信息的字典
        """
        try:
            logger.debug(f"generate_ai_response 开始: session_id={session_id}")

            # 1. 获取会话信息
            session = self.repository.get_chat_session(session_id)
            if not session:
                raise ValueError(f"会话不存在: {session_id}")
            logger.debug(f"会话信息获取成功: scenario_id={session['scenario_id']}")

            # 2. 通过接口获取场景配置
            scenario_config = self.scenario_interface.get_scenario_config(session["scenario_id"])
            if not scenario_config:
                raise ValueError(f"场景不存在: {session['scenario_id']}")
            logger.debug(f"场景配置获取成功: title={scenario_config.title}")

            # 3. 获取对话历史
            messages_history = self.repository.get_session_messages(session_id)
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in messages_history
            ]
            logger.debug(f"对话历史获取成功: {len(conversation_history)} 条")

            # 4. 调用Agent编排器（唯一对话方式）
            result = await self.agent_orchestrator.process_turn(
                session_id=session_id,
                user_input=user_message,
                scenario_title=scenario_config.title,
                patient_background=scenario_config.patient_background,
                conversation_history=conversation_history
            )
            logger.debug("Agent编排器返回成功")

            return result

        except Exception as e:
            logger.exception(f"generate_ai_response 错误: {e}")
            raise

    def end_session(self, session_id: str, final_score: int = None) -> Dict:
        """
        结束会话并发布事件

        Args:
            session_id: 会话ID
            final_score: 最终得分

        Returns:
            会话信息
        """
        # 更新会话状态
        from backend.app.modules.conversation.schemas.chat import SessionStatus

        session = self.repository.update_session_status(
            session_id,
            SessionStatus.COMPLETED,
            final_score
        )

        if not session:
            raise ValueError(f"会话不存在: {session_id}")

        # 通过事件总线发布事件（而非直接import mentor_agent）
        self.event_bus.publish(
            Events.CHAT_SESSION_ENDED,
            {"session_id": session_id}
        )

        return {
            "id": session.id,
            "status": session.status,
            "end_time": session.end_time,
            "final_score": session.final_score
        }
