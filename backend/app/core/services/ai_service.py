"""
AI 服务统一接口
基于 LangChain 框架提供对话和评估功能
"""
from typing import List, Dict, Optional
from backend.app.core.config.settings import settings


class AIService:
    """AI 服务统一接口 - 基于 LangChain"""

    _instance: Optional['AIService'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化 LangChain AI 服务"""
        if not hasattr(self, '_initialized'):
            try:
                from backend.app.modules.conversation.chains.conversation_chain import conversation_chain
                from backend.app.modules.evaluation.chains.evaluation_chain import evaluation_chain

                self.conversation_chain = conversation_chain
                self.evaluation_chain = evaluation_chain
                self._initialized = True
            except Exception as e:
                print(f"[ERROR] AI服务初始化失败: {e}")
                raise

    def generate_conversation_response(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: List[Dict],
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """
        生成对话回复（使用 LangChain）

        Args:
            system_prompt: 系统提示词
            user_message: 用户最新消息
            conversation_history: 对话历史 [{role: "user/assistant", content: "..."}]
            max_tokens: 最大token数（LangChain 自动管理）
            temperature: 温度参数（在链初始化时配置）

        Returns:
            AI 生成的回复文本
        """
        try:
            # 直接传递完整的 system_prompt，不再解析
            # 因为 skill_prompt 内部包含 "【" 字符，用 split 会错误分割
            response = self.conversation_chain.invoke(
                system_prompt=system_prompt,
                user_message=user_message,
                conversation_history=conversation_history
            )

            return response

        except Exception as e:
            print(f"[ERROR] AI调用异常: {type(e).__name__} - {str(e)}")
            raise Exception(f"AI调用异常: {type(e).__name__} - {str(e)}")

    def _convert_ai_model_to_api(self, report_model) -> Dict:
        """
        将 AI 内部模型（0-25/15/10 分）转换为 API 响应模型（0-100 分）

        AI 内部分制:
        - A/B/C: 0-25 分
        - D: 0-15 分
        - E: 0-10 分

        API 响应分制: 全部转换为 0-100 分

        如果 AI 返回值超出定义范围，按比例缩放并限制在 0-100
        """
        radar = report_model.radar_chart

        def scale_to_100(value: int, max_defined: int) -> int:
            """将定义范围的分数缩放到 0-100，并处理超出范围的情况"""
            # 先按定义的满分进行缩放
            scaled = value * (100 / max_defined)
            # 限制在 0-100 范围内（处理 AI 返回异常值的情况）
            return min(max(scaled, 0), 100)

        return {
            "total_score": report_model.total_score,
            "level_assessment": report_model.level_assessment,
            "radar_chart": {
                # A/B/C: 定义满分 25 → 100 分制
                "A_risk_identification": scale_to_100(radar.A_risk_identification, 25),
                "B_communication": scale_to_100(radar.B_communication, 25),
                "C_skill_application": scale_to_100(radar.C_skill_application, 25),
                # D: 定义满分 15 → 100 分制
                "D_safety_management": scale_to_100(radar.D_safety_management, 15),
                # E: 定义满分 10 → 100 分制
                "E_self_efficacy": scale_to_100(radar.E_self_efficacy, 10)
            },
            "state_analysis": report_model.state_analysis,
            "detailed_feedback": [
                {
                    "dimension": item.dimension,
                    "status": item.status,
                    "dialogue_ref_id": item.dialogue_ref_id if item.dialogue_ref_id > 0 else None,
                    "user_input": item.user_input if item.user_input else None,
                    "patient_state_snapshot": item.patient_state_snapshot if item.patient_state_snapshot else None,
                    "critique": item.critique,
                    "expert_suggestion": item.expert_suggestion
                }
                for item in report_model.detailed_feedback
            ],
            "technical_guidance": report_model.technical_guidance,
            "meta_data": {"ai_generated": True, "langchain_version": "0.1.16"}
        }

    def generate_evaluation_report(
        self,
        conversation_text: str,
        evaluation_criteria: Dict,
        crisis_detection_summary: str = None,
        max_retries: int = 2
    ) -> Dict:
        """
        生成评估报告（统一入口，使用 LangChain）

        Args:
            conversation_text: 对话历史文本（包含场景信息）
            evaluation_criteria: 评估标准
            crisis_detection_summary: 危机检测摘要
            max_retries: 最大重试次数（LangChain 自动管理）

        Returns:
            评估报告字典（0-100 分制）
        """
        try:
            # 从 conversation_text 中提取场景信息
            scenario_title = "围产期抑郁场景"
            patient_background = "见对话历史"

            lines = conversation_text.split('\n')
            for line in lines:
                if '- 场景标题:' in line or '场景标题:' in line:
                    scenario_title = line.split(':', 1)[1].strip() if ':' in line else scenario_title
                elif '- 患者背景:' in line or '患者背景:' in line:
                    patient_background = line.split(':', 1)[1].strip() if ':' in line else patient_background

            # 调用 LangChain 评估链
            if isinstance(evaluation_criteria, dict):
                criteria_text = evaluation_criteria.get("text", str(evaluation_criteria))
            else:
                criteria_text = str(evaluation_criteria)

            report_model = self.evaluation_chain.invoke(
                conversation_text=conversation_text,
                scenario_title=scenario_title,
                patient_background=patient_background,
                evaluation_criteria=criteria_text,
                crisis_detection_summary=crisis_detection_summary
            )

            # 转换为 API 响应格式（0-100 分制）
            return self._convert_ai_model_to_api(report_model)

        except Exception as e:
            print(f"[ERROR] 评估生成失败: {type(e).__name__} - {str(e)}")
            raise Exception(f"评估生成失败: {type(e).__name__} - {str(e)}")


# 创建全局实例
ai_service = AIService()
