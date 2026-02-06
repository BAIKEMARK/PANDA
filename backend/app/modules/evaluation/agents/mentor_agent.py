"""
Mentor-Agent 服务 - 事件驱动模式
基于THP标准评估护士表现
"""
from typing import Dict, List
from sqlalchemy.orm import Session

from backend.app.models.chat import ChatSession, ChatMessage
from backend.app.models.evaluation import EvaluationReport
from backend.app.models.scenario import Scenario
from backend.app.modules.evaluation.services.evaluation_service import EvaluationService
from backend.app.core.services.ai_service import ai_service
from backend.app.core.services.event_bus import event_bus, Events


class MentorAgent:
    """导师智能体 - 评估报告生成（事件驱动）"""

    def __init__(self, db: Session):
        self.db = db
        self.evaluation_service = EvaluationService(db)
        self.event_bus = event_bus

        # 订阅会话结束事件
        self.event_bus.subscribe(
            Events.CHAT_SESSION_ENDED,
            self._handle_session_ended
        )

    def _handle_session_ended(self, event_data: Dict):
        """处理会话结束事件（自动触发评估）"""
        session_id = event_data.get("session_id")
        if session_id:
            try:
                self.generate_evaluation(session_id)
            except Exception as e:
                print(f"[ERROR] 评估生成失败: {e}")
                # 发布失败事件
                self.event_bus.publish(
                    Events.EVALUATION_FAILED,
                    {"session_id": session_id, "error": str(e)}
                )

    def generate_evaluation(self, session_id: str) -> EvaluationReport:
        """
        生成评估报告（通过 AIService 统一入口）

        Args:
            session_id: 会话ID

        Returns:
            EvaluationReport: 评估报告对象
        """
        # 检查是否已存在评估报告
        existing_report = self.evaluation_service.get_report_by_session(session_id)
        if existing_report:
            return existing_report

        # 获取会话和对话数据
        session, messages, scenario = self._get_session_data(session_id)

        # 构建对话文本
        conversation_text = self._build_conversation_text(messages)

        # 获取 THP 评分标准（统一来源）
        from backend.app.modules.evaluation.prompts.evaluation_prompt import get_thp_rubric_text
        evaluation_criteria = get_thp_rubric_text()

        # 构建危机检测摘要
        crisis_detection_summary = self._build_crisis_detection_summary(session)

        # 通过 AIService 调用（统一入口）
        try:
            evaluation_data = ai_service.generate_evaluation_report(
                conversation_text=conversation_text,
                evaluation_criteria=evaluation_criteria,
                crisis_detection_summary=crisis_detection_summary
            )
        except Exception as e:
            print(f"[ERROR] AI 评估失败: {e}")
            self.event_bus.publish(
                Events.EVALUATION_FAILED,
                {"session_id": session_id, "error": str(e)}
            )
            raise

        # 保存评估报告到数据库
        report = self._save_report(session_id, evaluation_data)

        # 发布评估生成成功事件
        self.event_bus.publish(
            Events.EVALUATION_GENERATED,
            {"session_id": session_id, "report_id": report.id}
        )

        return report

    def _get_session_data(self, session_id: str):
        """获取会话数据"""
        # 获取会话
        session = self.db.query(ChatSession).filter(
            ChatSession.id == session_id
        ).first()

        if not session:
            self.db.rollback()
            session = self.db.query(ChatSession).filter(
                ChatSession.id == session_id
            ).first()
            if not session:
                raise ValueError(f"会话不存在: {session_id}")

        # 获取对话历史
        messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.asc()).all()

        # 获取场景
        scenario = self.db.query(Scenario).filter(
            Scenario.id == session.scenario_id
        ).first()

        return session, messages, scenario

    def _build_conversation_text(self, messages: List[ChatMessage]) -> str:
        """构建对话历史文本"""
        conversation_parts = []
        for idx, msg in enumerate(messages, 1):
            role = "护士" if msg.role == "user" else "患者"
            part = f"[轮次{idx}] {role}:\n{msg.content}\n"

            # 添加患者状态快照
            if msg.meta_data and msg.role == "assistant":
                patient_state = msg.meta_data.get("patient_state", {})
                if patient_state:
                    mood = patient_state.get('mood_score', 50)
                    rapport = patient_state.get('rapport_score', 50)
                    part += f"(患者状态: 心情{mood}, 信任{rapport})\n"

            conversation_parts.append(part)

        return "\n".join(conversation_parts)

    def _build_crisis_detection_summary(self, session: ChatSession) -> str:
        """
        构建危机检测摘要

        Args:
            session: 聊天会话对象

        Returns:
            危机检测摘要文本
        """
        if not session.has_suicide_risk:
            return "【危机检测】系统未检测到明显的自杀倾向。"

        if session.suicide_risk_alerted:
            return """【危机检测】系统检测到患者存在自杀倾向。
【用户应对】用户已点击报警按钮。"""
        else:
            return """【危机检测】系统检测到患者存在自杀倾向。
【用户应对】用户未采取任何行动。"""

    def _save_report(self, session_id: str, evaluation_data: dict) -> EvaluationReport:
        """保存评估报告到数据库"""
        radar_chart = evaluation_data.get("radar_chart", {})

        report_data = {
            "session_id": session_id,
            "total_score": evaluation_data.get("total_score", 0),
            "level_assessment": evaluation_data.get("level_assessment", ""),
            "radar_a_risk_identification": radar_chart.get("A_risk_identification", 0),
            "radar_b_communication": radar_chart.get("B_communication", 0),
            "radar_c_skill_application": radar_chart.get("C_skill_application", 0),
            "radar_d_safety_management": radar_chart.get("D_safety_management", 0),
            "radar_e_self_efficacy": radar_chart.get("E_self_efficacy", 0),
            "state_analysis": evaluation_data.get("state_analysis", ""),
            "detailed_feedback": evaluation_data.get("detailed_feedback", []),
            "technical_guidance": evaluation_data.get("technical_guidance", ""),
            "meta_data": evaluation_data.get("meta_data", {"ai_generated": True})
        }

        return self.evaluation_service.create_report(report_data)
