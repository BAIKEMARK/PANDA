"""
评估链 - 使用结构化输出
结合提示词模板、LLM 和 Pydantic 输出解析器
"""
from typing import Dict
from langchain_core.output_parsers import PydanticOutputParser

from backend.app.shared.ai.langchain_manager import langchain_manager
from backend.app.modules.evaluation.prompts.evaluation_prompt import (
    create_evaluation_prompt_template,
    create_evaluation_output_parser,
    EvaluationReportModel
)


class EvaluationChain:
    """评估链 - 结构化输出实现"""

    def __init__(self):
        """初始化评估链"""
        self.prompt_template = create_evaluation_prompt_template()
        self.output_parser = create_evaluation_output_parser()

        # 获取 LLM（带重试）
        llm = langchain_manager.get_llm()

        # 使用 with_types 绑定重试策略
        self.llm_with_retry = llm.with_retry(
            stop_after_attempt=3,
            wait_exponential_jitter=True
        )

        # 构建链
        self.chain = (
            self.prompt_template
            | self.llm_with_retry
            | self.output_parser
        )

    def invoke(
        self,
        conversation_text: str,
        scenario_title: str,
        patient_background: str,
        evaluation_criteria: str
    ) -> EvaluationReportModel:
        """
        同步调用评估链

        Args:
            conversation_text: 对话历史文本
            scenario_title: 场景标题
            patient_background: 患者背景
            evaluation_criteria: 评估标准文本

        Returns:
            EvaluationReportModel: 评估报告模型
        """
        # 构建请求数据
        request_data = {
            "evaluation_criteria": evaluation_criteria,
            "scenario_title": scenario_title,
            "patient_background": patient_background,
            "conversation_text": conversation_text,
            "format_instructions": self.output_parser.get_format_instructions()
        }

        result = self.chain.invoke(request_data)

        return result

    async def ainvoke(
        self,
        conversation_text: str,
        scenario_title: str,
        patient_background: str,
        evaluation_criteria: str
    ) -> EvaluationReportModel:
        """
        异步调用评估链

        Args:
            conversation_text: 对话历史文本
            scenario_title: 场景标题
            patient_background: 患者背景
            evaluation_criteria: 评估标准文本

        Returns:
            EvaluationReportModel: 评估报告模型
        """
        result = await self.chain.ainvoke({
            "evaluation_criteria": evaluation_criteria,
            "scenario_title": scenario_title,
            "patient_background": patient_background,
            "conversation_text": conversation_text,
            "format_instructions": self.output_parser.get_format_instructions()
        })

        return result

    def to_dict(self, report_model: EvaluationReportModel) -> Dict:
        """
        将 EvaluationReportModel 转换为字典

        Args:
            report_model: 评估报告模型

        Returns:
            字典格式的评估报告
        """
        return {
            "total_score": report_model.total_score,
            "level_assessment": report_model.level_assessment,
            "radar_chart": {
                "A_risk_identification": report_model.radar_chart.A_risk_identification,
                "B_communication": report_model.radar_chart.B_communication,
                "C_skill_application": report_model.radar_chart.C_skill_application,
                "D_safety_management": report_model.radar_chart.D_safety_management,
                "E_self_efficacy": report_model.radar_chart.E_self_efficacy,
            },
            "state_analysis": report_model.state_analysis,
            "detailed_feedback": [
                {
                    "dimension": fb.dimension,
                    "status": fb.status,
                    "dialogue_ref_id": fb.dialogue_ref_id if fb.dialogue_ref_id > 0 else None,
                    "user_input": fb.user_input if fb.user_input else None,
                    "patient_state_snapshot": fb.patient_state_snapshot if fb.patient_state_snapshot else None,
                    "critique": fb.critique,
                    "expert_suggestion": fb.expert_suggestion
                }
                for fb in report_model.detailed_feedback
            ],
            "technical_guidance": report_model.technical_guidance,
            "meta_data": {"ai_generated": True, "langchain_version": "0.1.16"}
        }


# 创建全局实例
evaluation_chain = EvaluationChain()
