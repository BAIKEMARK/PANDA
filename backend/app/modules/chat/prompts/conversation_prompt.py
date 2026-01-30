"""
对话提示词模板
使用 LangChain 的 ChatPromptTemplate 构建对话提示词
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict


def create_conversation_prompt_template() -> ChatPromptTemplate:
    """
    创建对话提示词模板

    Returns:
        ChatPromptTemplate: LangChain 提示词模板
    """
    template = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        MessagesPlaceholder(variable_name="history"),  # 历史对话占位符
        ("human", "{user_message}")
    ])

    return template


def build_system_prompt(
    scenario_system_prompt: str,
    patient_background: str,
    skill_prompt: str = ""
) -> str:
    """
    构建完整的系统提示词

    Args:
        scenario_system_prompt: 场景系统提示词
        patient_background: 患者背景
        skill_prompt: 技能提示词（可选）

    Returns:
        完整的系统提示词
    """
    system_parts = []

    # 基础系统提示
    system_parts.append(f"【系统提示】\n{scenario_system_prompt}\n")

    # 全局技能指导（如果启用）
    if skill_prompt:
        system_parts.append(f"【全局技能指导】\n{skill_prompt}\n")

    # 患者背景
    system_parts.append(f"【患者背景】\n{patient_background}\n")

    return "\n".join(system_parts)


def convert_history_to_messages(history: List[Dict]) -> list:
    """
    将历史对话转换为 LangChain 消息格式

    Args:
        history: 历史对话 [{"role": "user", "content": "..."}]

    Returns:
        LangChain 消息列表 [HumanMessage, AIMessage, ...]
    """
    messages = []
    for msg in history:
        role = msg.get("role")
        content = msg.get("content", "")

        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
        # 忽略 system 消息（已在 system_prompt 中）

    return messages
