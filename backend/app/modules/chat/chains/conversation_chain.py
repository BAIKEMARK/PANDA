"""
对话链 - 使用 LCEL 构建
结合提示词模板、LLM 和输出解析器
"""
from typing import Dict, List
from langchain_core.output_parsers import StrOutputParser

from backend.app.shared.ai.langchain_manager import langchain_manager
from backend.app.modules.chat.prompts.conversation_prompt import (
    create_conversation_prompt_template,
    convert_history_to_messages
)


class ConversationChain:
    """对话链 - LCEL 实现"""

    def __init__(self):
        """初始化对话链"""
        self.prompt_template = create_conversation_prompt_template()
        self.llm = langchain_manager.get_llm()
        # 使用 LCEL 构建链: prompt | llm | StrOutputParser
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def invoke(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: List[Dict]
    ) -> str:
        """
        同步调用对话链

        Args:
            system_prompt: 完整的系统提示词（包含场景、技能、背景等）
            user_message: 用户消息
            conversation_history: 对话历史

        Returns:
            AI 回复文本
        """
        # 转换历史消息
        history = convert_history_to_messages(conversation_history)

        # 构建请求数据
        request_data = {
            "system_prompt": system_prompt,
            "history": history,
            "user_message": user_message
        }

        # 调用链
        response = self.chain.invoke(request_data)

        return response

    async def ainvoke(
        self,
        scenario_system_prompt: str,
        patient_background: str,
        user_message: str,
        conversation_history: List[Dict],
        skill_prompt: str = ""
    ) -> str:
        """
        异步调用对话链

        Args:
            scenario_system_prompt: 场景系统提示词
            patient_background: 患者背景
            user_message: 用户消息
            conversation_history: 对话历史
            skill_prompt: 技能提示词（可选）

        Returns:
            AI 回复文本
        """
        # 构建系统提示词
        system_prompt = build_system_prompt(
            scenario_system_prompt,
            patient_background,
            skill_prompt
        )

        # 转换历史消息
        history = convert_history_to_messages(conversation_history)

        # 异步调用链
        response = await self.chain.ainvoke({
            "system_prompt": system_prompt,
            "history": history,
            "user_message": user_message
        })

        return response


# 创建全局实例
conversation_chain = ConversationChain()
