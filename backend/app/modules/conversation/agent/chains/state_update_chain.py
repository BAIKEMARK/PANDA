"""
状态更新链
使用LLM分析护士输入并计算患者状态变化
"""
from typing import Dict, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from backend.app.core.ai.langchain_manager import langchain_manager
from backend.app.modules.conversation.agent.models.state_analysis import StateAnalysis


class StateUpdateChain:
    """
    状态更新链 - 使用LLM分析护士输入并计算状态变化

    替代原来的关键词匹配方法，提供更准确的状态变化计算
    """

    def __init__(self):
        """初始化状态更新链"""
        self.llm = langchain_manager.get_llm()
        self.output_parser = PydanticOutputParser(pydantic_object=StateAnalysis)

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的围产期抑郁沟通分析师。

【任务】
分析护士/学员的回复，计算患者状态的变化。

【当前患者状态】
心情: {mood_score}/100
满意度: {satisfaction_score}/100
抑郁程度: {depression_level}/100
信任度: {rapport_score}/100

【状态变化规则】
1. 共情（理解、感受、共情）:
   - mood: +10~15
   - rapport: +10~15

2. 说教（你应该、必须、不对）:
   - mood: -10~-20
   - rapport: -10~-20
   - satisfaction: -5~-10

3. 开放式提问（不能简单是/否回答）:
   - satisfaction: +8~12
   - rapport: +5~10

4. 支持性（陪你、一起、帮你）:
   - satisfaction: +10~15
   - mood: +5~10

5. 消极/冷漠（哦、嗯、随便）:
   - mood: -5~-10
   - satisfaction: -5~-10
   - rapport: -5~-10

6. 挖掘深层想法（鼓励表达）:
   - depression: -5~-10（减轻）

7. 触发创伤回忆:
   - depression: +5~15（加重）

【边界效应】
- 当前值 < 20 时，负面变化减缓50%
- 当前值 > 80 时，正面变化减缓50%
- 所有值必须保持在 0-100 范围内

【危机检测】
1. 自杀倾向检测 (suicide_risk):
   患者表达以下类似内容时标记为true:
   - "活着没意思"、"不想活了"、"想死"、"自杀"
   - "结束这一切"、"离开这个世界"
   - 表达绝望、无价值感（如"我是累赘"）
   - 提及死亡、自杀、自伤
   - 眼神空洞
   - 缓缓走向窗边
   或者患者表达的意思中有下面类似情况时标记为true:
   - （缓缓走向窗边，手指轻触玻璃，声音轻得像在自言自语）反正……我走了宝宝也不会记得妈妈。他哭的时候……我连抱他的力气都没有。
   

2. 患者离开检测 (patient_leaving):
   患者明确表示要离开时标记为true:
   - "我先走了"、"我要走了"、"回去了"
   - "不想说了"、"算了不聊了"
   注意: "想走"但未明确离开不算，必须是明确表达要离开

【输出要求】
只输出JSON格式的状态变化和危机检测结果。"""),
            ("human", """【护士回复】
{nurse_input}

【对话历史（最近3轮）】
{conversation_history}

请计算患者状态的变化，并检测是否存在危机情况。

{format_instructions}""")
        ])

        # 构建链
        self.chain = self.prompt_template | self.llm | self.output_parser

    async def ainvoke(
        self,
        nurse_input: str,
        current_state: Dict,
        conversation_history: Optional[list] = None
    ) -> StateAnalysis:
        """
        异步分析状态变化

        Args:
            nurse_input: 护士的输入
            current_state: 患者当前状态 {mood_score, satisfaction_score, depression_level, rapport_score}
            conversation_history: 对话历史（可选）

        Returns:
            StateAnalysis对象
        """
        if conversation_history is None:
            conversation_history = []

        # 格式化对话历史
        history_text = self._format_history(conversation_history)

        # 调用链
        result: StateAnalysis = await self.chain.ainvoke({
            "nurse_input": nurse_input,
            "mood_score": current_state.get("mood_score", 50),
            "satisfaction_score": current_state.get("satisfaction_score", 50),
            "depression_level": current_state.get("depression_level", 50),
            "rapport_score": current_state.get("rapport_score", 50),
            "conversation_history": history_text,
            "format_instructions": self.output_parser.get_format_instructions()
        })

        return result

    def invoke(
        self,
        nurse_input: str,
        current_state: Dict,
        conversation_history: Optional[list] = None
    ) -> StateAnalysis:
        """
        同步分析状态变化

        Args:
            nurse_input: 护士的输入
            current_state: 患者当前状态
            conversation_history: 对话历史（可选）

        Returns:
            StateAnalysis对象
        """
        if conversation_history is None:
            conversation_history = []

        history_text = self._format_history(conversation_history)

        result: StateAnalysis = self.chain.invoke({
            "nurse_input": nurse_input,
            "mood_score": current_state.get("mood_score", 50),
            "satisfaction_score": current_state.get("satisfaction_score", 50),
            "depression_level": current_state.get("depression_level", 50),
            "rapport_score": current_state.get("rapport_score", 50),
            "conversation_history": history_text,
            "format_instructions": self.output_parser.get_format_instructions()
        })

        return result

    def _format_history(self, history: list) -> str:
        """格式化对话历史"""
        if not history:
            return "（无历史对话）"

        formatted = []
        # 只取最近3轮
        recent = history[-3:] if len(history) > 3 else history

        for msg in recent:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                formatted.append(f"护士: {content}")
            elif role == "assistant":
                formatted.append(f"患者: {content}")

        return "\n".join(formatted) if formatted else "（无历史对话）"


# 创建全局实例
state_update_chain = StateUpdateChain()