"""
对话编排引擎 - 解耦跨模块依赖
通过依赖注入和接口实现模块间通信
"""
from typing import Dict, List, TYPE_CHECKING
from sqlalchemy.orm import Session

from backend.app.modules.chat.repositories.chat_repository import ChatRepository
from backend.app.shared.infrastructure.ai_service import AIService
from backend.app.shared.infrastructure.skill_config import skill_config_manager
from backend.app.shared.infrastructure.event_bus import event_bus, Events
from backend.app.interfaces.scenario_interface import ScenarioInterface

if TYPE_CHECKING:
    from backend.app.shared.infrastructure.skill_config import SkillConfigManager


class ConversationEngine:
    """对话编排引擎 - 解耦跨模块依赖"""

    def __init__(
        self,
        db: Session,
        ai_service: AIService,
        scenario_interface: ScenarioInterface
    ):
        self.db = db
        self.repository = ChatRepository(db)
        self.ai_service = ai_service
        self.skill_config = skill_config_manager
        self.scenario_interface = scenario_interface
        self.event_bus = event_bus  # 使用全局单例

    def generate_ai_response(
        self,
        session_id: str,
        user_message: str,
        user_id: str = "user-001"
    ) -> Dict:
        """
        生成AI回复（解除原有耦合）

        Args:
            session_id: 会话ID
            user_message: 用户消息
            user_id: 用户ID

        Returns:
            包含AI回复的字典
        """
        # 1. 获取会话信息
        session = self.repository.get_chat_session(session_id)
        if not session:
            raise ValueError(f"会话不存在: {session_id}")

        # 2. 通过接口获取场景配置（而非直接import crud_scenario）
        scenario_config = self.scenario_interface.get_scenario_config(session["scenario_id"])
        if not scenario_config:
            raise ValueError(f"场景不存在: {session['scenario_id']}")

        # 3. 从shared获取技能提示词（而非直接import skill_manager）
        skill_prompt = ""
        if self.skill_config.is_enabled():
            skill_prompt = self.skill_config.get_skill_prompt()

        # 4. 构建对话上下文
        messages_history = self.repository.get_session_messages(session_id)

        # 5. 调用shared的AI服务（基于LangChain）
        conversation_context = self._build_context(
            scenario_config,
            skill_prompt,
            messages_history,
            user_message
        )

        ai_response = self.ai_service.generate_conversation_response(
            system_prompt=conversation_context["system_prompt"],
            user_message=user_message,
            conversation_history=conversation_context["history"]
        )

        return {"response": ai_response}

    def _build_context(
        self,
        scenario_config,
        skill_prompt: str,
        messages_history: List,
        user_message: str
    ) -> Dict:
        """构建对话上下文"""
        # 构建系统提示词
        system_prompt = f"【系统提示】\n{scenario_config.system_prompt}\n\n"

        # 如果启用了全局技能，添加技能提示
        if skill_prompt:
            system_prompt += f"【全局技能指导】\n{skill_prompt}\n\n"

        system_prompt += f"【患者背景】\n{scenario_config.patient_background}\n\n"

        # 构建历史消息
        history = []
        for msg in messages_history:
            history.append({
                "role": msg.role,
                "content": msg.content
            })

        return {
            "system_prompt": system_prompt,
            "history": history
        }

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
        from backend.app.modules.chat.schemas.chat import SessionStatus

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
