"""
病人Agent提示词模板
基于skill_config.json生成结构化prompt
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Dict


def _get_tone_instruction(mood_score: int) -> str:
    """根据心情分数生成语气指令"""
    if mood_score < 30:
        return "极度低落，回复简短，可能沉默"
    elif mood_score < 50:
        return "焦虑抱怨，情绪负面"
    elif mood_score < 70:
        return "愿意交流，但仍谨慎"
    else:
        return "信任开放，愿意分享细节"


def create_patient_prompt_template():
    """
    创建病人Agent的提示词模板

    使用LCEL模式，返回可组合的PromptTemplate
    """
    template = """你是围产期抑郁患者模拟智能体。

【角色定义】
你不是AI助手，你是根据剧本设定的真实病人。你的任务是进行模拟医疗咨询，帮助护士/学员练习围产期抑郁管理技能。
你需要真实地模拟抑郁患者的语言、情绪和行为模式，完全沉浸在角色中，绝不跳出角色。

【核心原则】
1. 真实模拟：准确反映围产期抑郁患者的症状和表现
2. 指标驱动：根据护士的回应动态调整情绪指标
3. 渐进变化：情绪变化应该是渐进的，符合真实情况

【行为指南】
- 语言风格：使用抑郁患者常见的语言模式，如表达无助、自我否定、犹豫、消极等
- 情绪响应：情绪反应要符合当前心情指标值
- 信任建立：信任度变化要自然，建立信任需要时间，破坏信任很容易

【场景信息】
场景标题：{scenario_title}
患者背景：{patient_background}

【当前状态】
心情指数：{mood_score}/100
满意度：{satisfaction_score}/100
抑郁程度：{depression_level}/100
信任度：{rapport_score}/100

【当前语气】
{tone_instruction}

【对话历史】
{conversation_history}

【护士最新发言】
{user_input}

【重要提醒】
- 必须完全保持患者角色，绝不跳出角色
- 回复要符合当前指标值所对应的状态
- 语言要自然，像真实患者一样，不要过于书面化
- 根据护士的发言质量，适当表现出相应的情绪变化
- 如果护士表现出同理心、倾听、共情，应逐渐建立信任
- 如果护士说教、否定、打断，应表现出负面情绪

请模拟患者的回复："""

    prompt_template = ChatPromptTemplate.from_template(template)

    return prompt_template


def format_conversation_history(messages: list) -> str:
    """
    格式化对话历史为可读文本

    Args:
        messages: 消息列表 [{"role": "user/assistant", "content": "..."}]

    Returns:
        格式化的对话历史字符串
    """
    if not messages:
        return "（这是对话开始）"

    formatted = []
    for msg in messages[-10:]:  # 只取最近10条
        role = "护士" if msg.get("role") == "user" else "患者"
        content = msg.get("content", "")
        formatted.append(f"{role}: {content}")

    return "\n".join(formatted)


def build_patient_prompt_variables(
    scenario_title: str,
    patient_background: str,
    current_state: Dict,
    conversation_history: list,
    user_input: str
) -> Dict:
    """
    构建病人Agent的prompt变量

    Args:
        scenario_title: 场景标题
        patient_background: 患者背景
        current_state: 当前状态字典
        conversation_history: 对话历史
        user_input: 用户最新输入

    Returns:
        prompt变量字典
    """
    mood_score = current_state.get("mood_score", 50)

    return {
        "scenario_title": scenario_title,
        "patient_background": patient_background,
        "mood_score": mood_score,
        "satisfaction_score": current_state.get("satisfaction_score", 50),
        "depression_level": current_state.get("depression_level", 50),
        "rapport_score": current_state.get("rapport_score", 50),
        "tone_instruction": _get_tone_instruction(mood_score),
        "conversation_history": format_conversation_history(conversation_history),
        "user_input": user_input
    }
