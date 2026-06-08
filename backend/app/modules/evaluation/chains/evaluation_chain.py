"""
评估链 - 使用结构化输出
结合提示词模板、LLM 和 Pydantic 输出解析器
"""
import json
import re
from typing import Any, Dict, Optional
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.utils.json import parse_partial_json

from backend.app.core.ai.langchain_manager import langchain_manager
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

        # 构建链：解析前先拿到原始 LLM 输出，便于处理 Markdown 包裹和常见非法占位符。
        self.chain = self.prompt_template | self.llm_with_retry

    def _build_request_data(
        self,
        conversation_text: str,
        scenario_title: str,
        patient_background: str,
        evaluation_criteria: str,
        crisis_detection_summary: Optional[str] = None
    ) -> Dict[str, str]:
        return {
            "crisis_detection_summary": crisis_detection_summary or "【危机检测】系统未检测到明显的自杀倾向。",
            "evaluation_criteria": evaluation_criteria,
            "scenario_title": scenario_title,
            "patient_background": patient_background,
            "conversation_text": conversation_text,
            "format_instructions": self.output_parser.get_format_instructions()
        }

    @staticmethod
    def _coerce_content(raw_output: Any) -> str:
        content = getattr(raw_output, "content", raw_output)
        if isinstance(content, list):
            return "\n".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in content
            )
        return str(content)

    @staticmethod
    def _extract_json_object(text: str, allow_partial: bool = False) -> str:
        fenced = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
        candidate = fenced.group(1).strip() if fenced else text.strip()
        candidate = candidate.split("For troubleshooting,", 1)[0].strip()

        start = candidate.find("{")
        if start < 0:
            raise OutputParserException("评估模型输出中未找到 JSON 对象")

        in_string = False
        escape = False
        depth = 0
        for index, char in enumerate(candidate[start:], start=start):
            if in_string:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return candidate[start:index + 1]

        if allow_partial:
            return candidate[start:]

        raise OutputParserException("评估模型输出中的 JSON 对象不完整")

    @staticmethod
    def _replace_invalid_numeric_values(json_text: str) -> str:
        numeric_fields = (
            "total_score",
            "A_risk_identification",
            "B_communication",
            "C_skill_application",
            "D_safety_management",
            "E_self_efficacy",
            "dialogue_ref_id",
        )
        fields_pattern = "|".join(re.escape(field) for field in numeric_fields)

        def replace_invalid_value(match: re.Match) -> str:
            prefix = match.group("prefix")
            raw_value = match.group("value")
            delimiter = match.group("delimiter")
            value = raw_value.strip()

            try:
                json.loads(value)
            except json.JSONDecodeError:
                return f"{prefix}null{delimiter}"
            return match.group(0)

        return re.sub(
            rf'(?P<prefix>"(?:{fields_pattern})"\s*:\s*)'
            rf'(?P<value>[^,\}}\]\r\n]+)'
            rf'(?P<delimiter>\s*[,}}\]])',
            replace_invalid_value,
            json_text,
        )

    @staticmethod
    def _normalize_score(value: Any, default: int = 0, minimum: int = 0, maximum: int = 100) -> int:
        if value is None:
            number = default
        elif isinstance(value, bool):
            number = default
        elif isinstance(value, (int, float)):
            number = int(round(value))
        elif isinstance(value, str):
            try:
                number = int(round(float(value.strip())))
            except ValueError:
                number = default
        else:
            number = default
        return max(min(number, maximum), minimum)

    def _repair_report_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        radar = data.get("radar_chart")
        if not isinstance(radar, dict):
            radar = {}

        radar_limits = {
            "A_risk_identification": 25,
            "B_communication": 25,
            "C_skill_application": 25,
            "D_safety_management": 15,
            "E_self_efficacy": 10,
        }
        normalized_radar = {
            field: self._normalize_score(radar.get(field), maximum=limit)
            for field, limit in radar_limits.items()
        }
        data["radar_chart"] = normalized_radar

        total_score = self._normalize_score(sum(normalized_radar.values()), maximum=100)
        data["total_score"] = total_score

        if total_score >= 90:
            data["level_assessment"] = "优秀"
        elif total_score >= 80:
            data["level_assessment"] = "良好"
        elif total_score >= 60:
            data["level_assessment"] = "合格"
        else:
            data["level_assessment"] = "不合格"

        if not isinstance(data.get("state_analysis"), dict):
            data["state_analysis"] = {"summary": str(data.get("state_analysis") or "")}

        if not isinstance(data.get("detailed_feedback"), list):
            data["detailed_feedback"] = []
        for item in data["detailed_feedback"]:
            if isinstance(item, dict):
                item.setdefault("dimension", "综合评价")
                item.setdefault("status", "失败")
                item.setdefault("critique", "评估模型输出被截断，系统保留了可解析的反馈内容。")
                item.setdefault("expert_suggestion", "请重新生成评估报告以获取完整建议。")
                if item.get("dialogue_ref_id") is None:
                    item.pop("dialogue_ref_id", None)
                elif "dialogue_ref_id" in item:
                    item["dialogue_ref_id"] = self._normalize_score(
                        item.get("dialogue_ref_id"),
                        default=-1,
                        minimum=-1,
                        maximum=999999,
                    )

        if not isinstance(data.get("technical_guidance"), str):
            data["technical_guidance"] = str(data.get("technical_guidance") or "")

        return data

    def _parse_output(self, raw_output: Any) -> EvaluationReportModel:
        text = self._coerce_content(raw_output)
        try:
            return self.output_parser.parse(text)
        except OutputParserException as original_error:
            json_text = self._extract_json_object(text, allow_partial=True)
            json_text = self._replace_invalid_numeric_values(json_text)
            try:
                data = json.loads(json_text)
            except json.JSONDecodeError as json_error:
                try:
                    data = parse_partial_json(json_text)
                except json.JSONDecodeError:
                    raise OutputParserException(f"评估 JSON 修复后仍无法解析: {json_error}") from original_error
            if not isinstance(data, dict):
                raise OutputParserException("评估 JSON 解析结果不是对象") from original_error
            return EvaluationReportModel.model_validate(self._repair_report_data(data))

    def invoke(
        self,
        conversation_text: str,
        scenario_title: str,
        patient_background: str,
        evaluation_criteria: str,
        crisis_detection_summary: str = None
    ) -> EvaluationReportModel:
        """
        同步调用评估链

        Args:
            conversation_text: 对话历史文本
            scenario_title: 场景标题
            patient_background: 患者背景
            evaluation_criteria: 评估标准文本
            crisis_detection_summary: 危机检测摘要（自杀倾向等）

        Returns:
            EvaluationReportModel: 评估报告模型
        """
        request_data = self._build_request_data(
            conversation_text=conversation_text,
            scenario_title=scenario_title,
            patient_background=patient_background,
            evaluation_criteria=evaluation_criteria,
            crisis_detection_summary=crisis_detection_summary
        )
        return self._parse_output(self.chain.invoke(request_data))

    async def ainvoke(
        self,
        conversation_text: str,
        scenario_title: str,
        patient_background: str,
        evaluation_criteria: str,
        crisis_detection_summary: str = None
    ) -> EvaluationReportModel:
        """
        异步调用评估链

        Args:
            conversation_text: 对话历史文本
            scenario_title: 场景标题
            patient_background: 患者背景
            evaluation_criteria: 评估标准文本
            crisis_detection_summary: 危机检测摘要（自杀倾向等）

        Returns:
            EvaluationReportModel: 评估报告模型
        """
        request_data = self._build_request_data(
            conversation_text=conversation_text,
            scenario_title=scenario_title,
            patient_background=patient_background,
            evaluation_criteria=evaluation_criteria,
            crisis_detection_summary=crisis_detection_summary
        )
        return self._parse_output(await self.chain.ainvoke(request_data))

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
