"""
Mentor-Agent 服务 - 事件驱动模式
基于THP标准评估护士表现
"""
import json
from typing import Dict
from sqlalchemy.orm import Session

from backend.app.models.chat import ChatSession, ChatMessage
from backend.app.models.evaluation import EvaluationReport
from backend.app.models.scenario import Scenario
from backend.app.modules.evaluation.services.evaluation_service import EvaluationService
from backend.app.shared.infrastructure.ai_service import AIService
from backend.app.shared.infrastructure.event_bus import EventBus, Events


class MentorAgent:
    """导师智能体 - 评估报告生成（事件驱动）"""

    def __init__(self, db: Session):
        self.db = db
        self.evaluation_service = EvaluationService(db)
        self.ai_service = AIService()
        self.event_bus = EventBus()

        # 订阅会话结束事件
        self.event_bus.subscribe(
            Events.CHAT_SESSION_ENDED,
            self._handle_session_ended
        )

    def _handle_session_ended(self, event_data: Dict):
        """处理会话结束事件（自动触发评估）"""
        session_id = event_data.get("session_id")
        if session_id:
            print(f"🤖 [MentorAgent] 收到会话结束事件，开始生成评估: {session_id}")
            try:
                self.generate_evaluation(session_id)
            except Exception as e:
                print(f"❌ [MentorAgent] 评估生成失败: {e}")
                # 发布失败事件
                self.event_bus.publish(
                    Events.EVALUATION_FAILED,
                    {"session_id": session_id, "error": str(e)}
                )

    def generate_evaluation(self, session_id: str) -> EvaluationReport:
        """生成评估报告

        Args:
            session_id: 会话ID

        Returns:
            EvaluationReport: 评估报告对象
        """
        # 0. 检查是否已存在评估报告
        existing_report = self.evaluation_service.get_report_by_session(session_id)
        if existing_report:
            print(f"✅ 评估报告已存在，直接返回: {existing_report.id}")
            return existing_report

        # 1. 获取会话信息
        session = self.db.query(ChatSession).filter(
            ChatSession.id == session_id
        ).first()

        if not session:
            raise ValueError(f"会话不存在: {session_id}")

        # 2. 获取对话历史
        messages = self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.asc()).all()

        # 3. 获取场景配置
        scenario = self.db.query(Scenario).filter(
            Scenario.id == session.scenario_id
        ).first()

        # 4. 构建评估Prompt
        evaluation_prompt = self._build_evaluation_prompt(
            session=session,
            messages=messages,
            scenario=scenario
        )

        # 5. 调用AI生成评估
        try:
            ai_response = self.ai_service.generate_evaluation_report(
                conversation_text=evaluation_prompt,
                evaluation_criteria=self.get_thp_rubric()
            )
            evaluation_data = ai_response
        except Exception as e:
            # AI评估失败，不保存任何报告，直接抛出异常
            print(f"❌ AI评估失败，不保存评估报告: {e}")
            raise

        # 6. 保存评估报告到数据库
        report = self._save_report(
            session_id=session_id,
            evaluation_data=evaluation_data
        )

        # 发布评估生成成功事件
        self.event_bus.publish(
            Events.EVALUATION_GENERATED,
            {"session_id": session_id, "report_id": report.id}
        )

        return report

    def _build_evaluation_prompt(
        self,
        session: ChatSession,
        messages: list,
        scenario: Scenario
    ) -> str:
        """构建评估Prompt"""
        # 构建对话历史文本
        conversation_text = ""
        for idx, msg in enumerate(messages, 1):
            role = "护士" if msg.role == "user" else "患者"
            conversation_text += f"\n[轮次{idx}] {role}:\n{msg.content}\n"

            # 如果有状态元数据，也添加进去
            if msg.meta_data and msg.role == "assistant":
                patient_state = msg.meta_data.get("patient_state", {})
                if patient_state:
                    conversation_text += f"(状态: 心情{patient_state.get('mood_score', 50)}, 信任{patient_state.get('rapport_score', 50)})\n"

        prompt = f"""
你是一位围产期抑郁护理培训专家导师。请基于以下信息，对护士的对话表现进行专业评估。

# 评分标准 (THP五维评分法)
{self.get_thp_rubric()}

# 场景信息
- 场景标题: {scenario.title if scenario else '未知'}
- 患者背景: {scenario.patient_background if scenario else '未知'}

# 对话历史
{conversation_text}

# 任务要求
请以JSON格式返回评估报告。请直接返回JSON，不要有其他说明文字。
"""
        return prompt

    def _save_report(self, session_id: str, evaluation_data: dict) -> EvaluationReport:
        """保存评估报告到数据库"""
        # 获取雷达图数据
        radar_chart = evaluation_data.get("radar_chart", {})

        # 创建报告数据
        report_data = {
            "session_id": session_id,
            "total_score": evaluation_data.get("total_score", 0),
            "level_assessment": evaluation_data.get("level_assessment", ""),
            "radar_a_risk_identification": radar_chart.get("A_risk_identification", 0),
            "radar_b_communication": radar_chart.get("B_communication", 0),
            "radar_c_skill_application": radar_chart.get("C_skill_application", 0),
            "radar_d_safety_management": radar_chart.get("D_safety_management", 0),
            "radar_e_self_efficacy": radar_chart.get("E_self_efficacy", 0),
            "state_analysis": evaluation_data.get("state_analysis", {}),
            "detailed_feedback": evaluation_data.get("detailed_feedback", []),
            "technical_guidance": evaluation_data.get("technical_guidance", ""),
            "meta_data": {"ai_generated": True}
        }

        return self.evaluation_service.create_report(report_data)

    def get_thp_rubric(self) -> str:
        """获取THP评分标准"""
        return """
# THP五维评分标准

## A类：风险识别能力 (25分)
- 能否识别睡眠障碍、食欲改变、自杀意念等风险信号
- 是否遗漏关键危险因素
- 评估标准：优秀(22-25)/良好(18-21)/合格(15-17)/不合格(0-14)

## B类：沟通支持能力 (25分)
- B1 积极倾听：复述、澄清、共情
- B2 避免说教、打断、过早建议
- 评估标准：优秀(22-25)/良好(18-21)/合格(15-17)/不合格(0-14)

## C类：THP技能应用 (25分)
- C1 识别不健康想法：读心术、灾难化、非黑即白
- C2 挑战不合理信念
- C3 引导寻找替代性解释
- 评估标准：优秀(22-25)/良好(18-21)/合格(15-17)/不合格(0-14)

## D类：安全管理能力 (15分，红线)
- 危机识别：自伤/伤婴意念
- 转介流程：是否及时启动专科转介
- **一票否决**：遗漏红线信号得0分
- 评估标准：满分(15)/不及格(0)

## E类：自我效能感 (10分)
- 综合胜任感
- 应对复杂情况的信心
- 评估标准：优秀(9-10)/良好(7-8)/合格(6)/不合格(0-5)

## 总分计算
总分 = A + B + C + D + E (满分100分)

## 等级评定
- 优秀: 90-100分
- 良好: 80-89分
- 合格: 60-79分
- 不合格: 0-59分
"""
