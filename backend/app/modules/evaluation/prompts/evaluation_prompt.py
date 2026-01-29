"""
评估提示词模板
使用 LangChain 的结构化输出解析器
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict


# ==================== 定义评估报告的数据模型 ====================
class THPRadarChart(BaseModel):
    """THP 雷达图数据"""
    A_risk_identification: int = Field(description="风险识别能力得分 (0-25)")
    B_communication: int = Field(description="沟通支持能力得分 (0-25)")
    C_skill_application: int = Field(description="THP技能应用得分 (0-25)")
    D_safety_management: int = Field(description="安全管理能力得分 (0-15)")
    E_self_efficacy: int = Field(description="自我效能感得分 (0-10)")


class DetailedFeedbackItem(BaseModel):
    """详细反馈项 - 与 API Schema 中的 FeedbackItem 保持一致"""
    dimension: str = Field(description="评估维度 (如: 风险识别、沟通技巧、技能应用、安全管理)")
    status: str = Field(description="通过/失败")
    dialogue_ref_id: int = Field(default=-1, description="对话轮次引用 (可选)")
    user_input: str = Field(default="", description="用户输入 (可选)")
    patient_state_snapshot: str = Field(default="", description="患者状态快照 (可选)")
    critique: str = Field(description="批评意见 - 指出不足之处")
    expert_suggestion: str = Field(description="专家建议 - 具体改进建议")


class EvaluationReportModel(BaseModel):
    """评估报告完整模型"""
    total_score: int = Field(description="总分 (0-100)")
    level_assessment: str = Field(description="等级评定 (优秀/良好/合格/不合格)")
    radar_chart: THPRadarChart = Field(description="五维雷达图数据")
    state_analysis: Dict = Field(description="状态分析")
    detailed_feedback: List[DetailedFeedbackItem] = Field(description="详细反馈列表")
    technical_guidance: str = Field(description="技术指导")


# ==================== 提示词模板 ====================
def create_evaluation_prompt_template() -> ChatPromptTemplate:
    """
    创建评估提示词模板

    Returns:
        ChatPromptTemplate: 评估提示词模板
    """
    template = ChatPromptTemplate.from_messages([
        ("system", "你是一位围产期抑郁护理培训专家导师。请基于对话对话对护士的表现进行全面评估，重点关注其优点、不足和具体改进建议。"),
        ("human", """请基于以下信息，对护士的对话表现进行专业评估。

# 评分标准
{evaluation_criteria}

# 场景信息
- 场景标题: {scenario_title}
- 患者背景: {patient_background}

# 对话历史
{conversation_text}

# 任务要求
1. 请严格按照以下JSON格式返回评估报告：
{format_instructions}

2. **详细反馈要求** (detailed_feedback)：
   - 必须包含至少 5 条详细反馈
   - 每条反馈必须包含以下字段：
     * dimension: 评估维度（风险识别/沟通技巧/技能应用/安全管理/自我效能）
     * status: 通过/失败（根据该维度表现判断）
     * critique: 批评意见（指出具体的不足之处）
     * expert_suggestion: 专家建议（具体可操作的改进建议）
   - 可选字段：dialogue_ref_id（对话轮次引用）、user_input（用户输入内容）、patient_state_snapshot（患者状态快照）

请直接返回JSON，不要有其他说明文字。""")
    ])

    return template


def get_thp_rubric_text() -> str:
    """
    获取 THP 评分标准文本

    Returns:
        评分标准文本
    """
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


def create_evaluation_output_parser():
    """
    创建评估输出解析器

    Returns:
        PydanticOutputParser: 结构化输出解析器
    """
    return PydanticOutputParser(pydantic_object=EvaluationReportModel)
