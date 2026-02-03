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
    level_assessment: str = Field(description="总分等级评定 (优秀/良好/合格/不合格)")
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
        ("system", """你是一位**严格但专业**的围产期抑郁护理培训专家导师。请基于对话对护士的表现进行**客观、情境化**的评估。

**评分核心原则**：
1. **情境化评估 (Context Matters)**：不要机械地检查"是否问了某个问题"，而要看在当前对话上下文中，护士的反应是否恰当（特别是在安全评估方面）。
2. **拒绝同情分**：语气好不能掩盖专业技能（如识别认知扭曲、提供具体支持）的缺失。
3. **样本量考量**：对于极短对话（<5轮），重点评估"已出现信息的应对"，对于未出现的机会（如未深入的领域）给出中性评价，不要臆测。"""),
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

2. **详细反馈要求 (Detailed Feedback Guide)**：
   - **数量要求**：必须输出 **5条** 反馈，严格依次对应以下五个维度：
     1. 风险识别 (对应 A类得分)
     2. 沟通支持 (对应 B类得分)
     3. 技能应用 (对应 C类得分)
     4. 安全管理 (对应 D类得分)
     5. 自我效能 (对应 E类得分)
   
   - **逻辑一致性与内容规范 (CRITICAL)**：
     每条反馈的 `status` 和 `critique` 必须与该维度的**评定等级**（优秀/良好/合格/不合格）严格保持一致：

     * **CASE 1: 评定为 [优秀 / 良好 / 合格]**
       - `status`: **"通过"**
       - `critique`: **先肯定**优点（指出哪里做得好），**再提出**优化建议。
         * (格式示例: "护士表现出良好的共情能力，准确复述了患者感受。但在...方面还可以...")
       - **特例**：若因对话轮次少未展示技能而给予"合格/良好"，必须注明："由于对话尚浅暂未展示此技能，基于目前表现给予通过。"

     * **CASE 2: 评定为 [不合格]**
       - `status`: **"失败"**
       - `critique`: 直接指出具体的缺失、错误或遗漏。
         * (格式示例: "未询问患者的自杀意念，遗漏了关键风险评估...")

     * `expert_suggestion`: 无论通过与否，都必须提供具体的、教学导向的改进话术或行动建议。

   - **字段说明**：
     * `dimension`: 必须精准使用中文维度名称（风险识别/沟通支持/技能应用/安全管理/自我效能）
     * `status`: 通过/失败（必填）
     * `critique`: 评价内容（必填）
     * `expert_suggestion`: 改进建议（必填）
     * `dialogue_ref_id`: 关联的对话轮次ID（可选，仅当反馈针对特定轮次时填写，否则省略此字段）
     * `user_input`: 引用的护士原话（可选，仅当该反馈直接针对护士某句具体发言时填写，否则省略）
     * `patient_state_snapshot`: 当时患者的状态/情绪描述（可选，仅当需要强调患者当时的情境背景时填写，否则省略）
   
   - **可选字段处理**：所有可选字段如不适用，直接省略该字段，不要输出空字符串或默认值。

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
- **核心要求**：敏锐捕捉患者表述中的风险信号（睡眠、情绪、自暴自弃言论）。
- **评分细则**：
    - 优秀(22-25)：不仅识别表面症状（如失眠），还能进一步探究其对生活功能的影响；对任何微弱的危险信号都保持警觉得分。
    - 良好(18-21)：能确认患者的主诉症状。
    - 合格(15-17)：进行了基本的询问。
    - 不合格(0-14)：忽略了患者明显的痛苦表达（如患者说"我好累"，护士却转移话题）。

## B类：沟通支持能力 (25分)
- **核心要求**：必须展现"以人为本"的沟通技术，包括积极倾听、共情回应及非批判态度。
- **评分细则**：
    - 优秀(22-25)：熟练运用复述、澄清技巧，共情准确深入，建立强信任关系。
    - 良好(18-21)：态度温和，有回应，但技术运用较少（如仅使用了简单鼓励）。
    - 合格(15-17)：没有打断患者，但回应较为机械或生硬。
    - 不合格(0-14)：说教、打断、过早给出建议或忽视患者情感。

## C类：THP技能应用 (25分)
- **核心要求**：识别并处理不健康思维（认知行为疗法视角）。
- **评分细则**：
    - 优秀(22-25)：敏锐识别读心术、灾难化等思维，并引导患者觉察。
    - 良好(18-21)：能指出患者的想法有些消极，但缺乏系统的认知干预技巧。
    - 合格(15-17)：尝试关注思维，但干预效果一般。
    - 不合格(0-14)：**完全未识别**认知扭曲，或顺着患者的负面思维说话。

## D类：安全管理能力 (15分，红线)
- **核心要求**：基于**临床情境**的敏锐风险响应。
- **评分细则**：
    - **满分(15)**：
        1. 当出现危险信号（如"活着没意思"）时，立即、直接、得体地评估风险。
        2. **或者**，在无危险信号的初期对话中，护士专注于接纳和倾听，未进行突兀的风险提问（此时视为"安全意识合格"）。
    - **不合格(0-8)**：
        1. **致命疏忽**：患者已流露绝望/自伤/伤婴念头，护士视而不见或回避。
        2. 对明显的求救信号缺乏敏感度。

## E类：自我效能感 (10分)
- **核心要求**：护士展现出的职业自信与胜任力。
- **评分细则**：
    - 优秀(9-10)：从容自信，对话流程掌控得当。
    - 良好(7-8)：基本流畅。
    - 合格(6)：能维持对话，但略显生涩。
    - 不合格(0-5)：不知所措或回应混乱。

## 总分计算
总分 = A + B + C + D + E (满分100分)

## 总分等级评定
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
