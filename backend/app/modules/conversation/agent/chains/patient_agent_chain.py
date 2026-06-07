"""
病人Agent链
使用LangChain LCEL模式实现病人角色模拟
"""
from typing import Dict, Optional
from langchain_core.output_parsers import StrOutputParser

from backend.app.core.ai.langchain_manager import langchain_manager
from backend.app.modules.conversation.agent.prompts.patient_agent_prompt import (
    create_patient_prompt_template,
    build_patient_prompt_variables
)


class PatientAgentChain:
    """
    病人Agent链 - 结构化输出实现

    使用LCEL模式: prompt | llm | parser
    """

    def __init__(self):
        """初始化病人Agent链"""
        self.prompt_template = create_patient_prompt_template()

        # 获取LLM（已在 langchain_manager 中配置了 max_retries）
        llm = langchain_manager.get_llm()

        # 构建链
        self.chain = (
            self.prompt_template
            | llm
            | StrOutputParser()
        )

    def invoke(
        self,
        scenario_title: str,
        patient_background: str,
        current_state: Dict,
        conversation_history: list,
        user_input: str
    ) -> str:
        """
        同步调用病人Agent链

        Args:
            scenario_title: 场景标题
            patient_background: 患者背景
            current_state: 当前状态字典
            conversation_history: 对话历史
            user_input: 用户最新输入

        Returns:
            患者回复文本
        """
        # 构建prompt变量
        prompt_vars = build_patient_prompt_variables(
            scenario_title=scenario_title,
            patient_background=patient_background,
            current_state=current_state,
            conversation_history=conversation_history,
            user_input=user_input
        )

        # 调用链
        result = self.chain.invoke(prompt_vars)

        return result

    async def ainvoke(
        self,
        scenario_title: str,
        patient_background: str,
        current_state: Dict,
        conversation_history: list,
        user_input: str
    ) -> str:
        """
        异步调用病人Agent链

        Args:
            scenario_title: 场景标题
            patient_background: 患者背景
            current_state: 当前状态字典
            conversation_history: 对话历史
            user_input: 用户最新输入

        Returns:
            患者回复文本
        """
        # 构建prompt变量
        prompt_vars = build_patient_prompt_variables(
            scenario_title=scenario_title,
            patient_background=patient_background,
            current_state=current_state,
            conversation_history=conversation_history,
            user_input=user_input
        )

        # 异步调用链
        result = await self.chain.ainvoke(prompt_vars)

        return result


# 创建全局实例
patient_agent_chain = PatientAgentChain()
