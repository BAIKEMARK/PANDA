# PANDA AI 模块架构文档

> 版本: 2.0.0
> 更新时间: 2026-01-29
> 状态: 生产就绪

---

## 目录

1. [概览](#1-概览)
2. [架构设计](#2-架构设计)
3. [核心组件](#3-核心组件)
4. [LangChain 集成](#4-langchain-集成)
5. [链式调用 (LCEL)](#5-链式调用-lcel)
6. [提示词管理](#6-提示词管理)
7. [事件驱动架构](#7-事件驱动架构)
8. [技能配置系统](#8-技能配置系统)
9. [数据流](#9-数据流)
10. [使用示例](#10-使用示例)
11. [扩展指南](#11-扩展指南)
12. [最佳实践](#12-最佳实践)

---

## 1. 概览

### 1.1 设计目标

AI 模块基于 **LangChain 框架** 构建，提供以下核心能力：

- **对话生成**: 多轮对话管理，支持上下文记忆
- **评估报告**: 基于 THP 五维评分的结构化评估
- **可扩展性**: 分散式模块化设计，易于添加新的 AI 能力
- **可维护性**: 统一的服务接口，简化业务层调用
- **技能配置**: 灵活的对话行为配置系统

### 1.2 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| LangChain | 0.1.16 | LLM 应用开发框架 |
| LangChain Core | 0.1.40 | 核心抽象层 |
| LangChain OpenAI | 0.0.6 | OpenAI 兼容 API |
| Pydantic | 2.x | 数据验证和结构化输出 |
| 通义千问/DeepSeek | - | LLM 提供商 |

### 1.3 设计理念

- **分散式管理**: 各业务模块的 prompts/chains 归属各模块管理
- **统一入口**: 所有 AI 调用通过 `AIService` 统一接口
- **共享基础**: LLM 实例通过 `LangChainManager` 单例共享
- **LCEL 链式调用**: 使用 LangChain Expression Language 构建链

### 1.4 目录结构

```
backend/app/
├── shared/
│   ├── ai/                           # AI 基础设施（共享）
│   │   └── langchain_manager.py       # LLM 统一管理器（单例）
│   │
│   └── infrastructure/               # 基础服务
│       ├── ai_service.py             # AI 服务统一接口
│       ├── event_bus.py              # 事件总线
│       └── skill_config.py           # 技能配置管理
│
├── config/                           # 配置层
│   ├── config.py                     # 全局配置类
│   └── skill_config.json             # 技能配置文件
│
└── modules/
    ├── chat/                         # 对话模块
    │   ├── chains/
    │   │   └── conversation_chain.py  # 对话链
    │   └── prompts/
    │       └── conversation_prompt.py # 对话提示词
    │
    └── evaluation/                   # 评估模块
        ├── chains/
        │   └── evaluation_chain.py    # 评估链
        └── prompts/
            └── evaluation_prompt.py   # 评估提示词
```

---

## 2. 架构设计

### 2.1 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                     业务层 (modules/)                        │
│  - evaluation/agents/MentorAgent                             │
│  - chat/services/ConversationEngine                          │
│  - chat/chains/ConversationChain                             │
│  - evaluation/chains/EvaluationChain                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   AI 服务层 (infrastructure/)                 │
│  - AIService (统一接口)                                      │
│  - SkillConfig (技能配置)                                    │
│  - EventBus (事件总线)                                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   LLM 管理层 (shared/ai/)                     │
│  - LangChainManager (LLM 单例实例)                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     LLM 提供商                                │
│  通义千问: https://dashscope.aliyuncs.com/compatible-mode/v1│
│  DeepSeek: https://api.deepseek.com                          │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 设计模式

| 模式 | 应用场景 | 文件 |
|------|----------|------|
| **单例模式** | LLM 实例管理、AI 服务、事件总线、技能配置 | `langchain_manager.py`, `ai_service.py`, `event_bus.py`, `skill_config.py` |
| **适配器模式** | 统一不同 AI 服务的接口 | `ai_service.py` |
| **策略模式** | 提示词模板选择 | `modules/*/prompts/` |
| **观察者模式** | 事件驱动的评估触发 | `event_bus.py` + `MentorAgent` |
| **LCEL (LangChain Expression Language)** | 声明式链组合 | `modules/*/chains/` |

### 2.3 架构演进 (v2.0)

**v1.0 → v2.0 主要变更**：

| 变更项 | v1.0 | v2.0 |
|--------|------|------|
| prompts/chains 位置 | `shared/core/` (集中式) | `modules/*/` (分散式) |
| core 目录 | `app/core/` | `app/config/` |
| shared/core | `app/shared/core/` | `app/shared/ai/` |
| AIService 调用 | 解析 system_prompt | 直接传递完整 prompt |
| 技能配置路径 | `core/skill_config.json` | `config/skill_config.json` |

---

## 3. 核心组件

### 3.1 LangChainManager (LLM 管理器)

**文件**: `backend/app/shared/ai/langchain_manager.py`

**职责**:
- 创建和管理 LLM 实例（单例）
- 配置 httpx 客户端（禁用代理）
- 提供模型信息查询

**关键代码**:
```python
class LangChainManager:
    _instance: Optional['LangChainManager'] = None
    _llm: Optional[BaseChatModel] = None

    def _initialize_llm(self):
        self._llm = ChatOpenAI(
            base_url=settings.AI_TEXT_URL,
            api_key=settings.AI_TEXT_KEY,
            model=settings.AI_TEXT_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            timeout=settings.LLM_TIMEOUT,
            max_retries=settings.LLM_MAX_RETRIES,
            http_client=_create_httpx_client(),  # 禁用代理
            verbose=True,  # 启用详细日志
        )
```

**设计要点**:
- 使用 `ChatOpenAI` 兼容通义千问/DeepSeek API
- 显式设置 `proxies=None` 禁用代理（AI API 直连）
- 自动重试机制（`max_retries=3`）
- 启用 `verbose=True` 用于调试

---

### 3.2 AIService (AI 服务统一接口)

**文件**: `backend/app/shared/infrastructure/ai_service.py`

**职责**:
- 提供统一的 AI 服务接口
- 对话生成 (`generate_conversation_response`)
- 评估报告生成 (`generate_evaluation_report`)
- 模型转换（AI 内部分数 → API 分数）

**接口定义**:
```python
class AIService:
    def generate_conversation_response(
        self,
        system_prompt: str,          # 完整的系统提示词
        user_message: str,
        conversation_history: List[Dict],
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """生成对话回复"""
        # 直接传递完整 system_prompt，不再解析
        response = self.conversation_chain.invoke(
            system_prompt=system_prompt,
            user_message=user_message,
            conversation_history=conversation_history
        )
        return response

    def generate_evaluation_report(
        self,
        conversation_text: str,
        evaluation_criteria: Dict,
        max_retries: int = 2
    ) -> Dict:
        """生成评估报告（0-100分制）"""
        report_model = self.evaluation_chain.invoke(...)
        return self._convert_ai_model_to_api(report_model)
```

**v2.0 简化**:
- ❌ 移除：system_prompt 解析逻辑
- ✅ 新增：直接传递完整 system_prompt
- ✅ 新增：`_convert_ai_model_to_api()` 模型转换方法

---

### 3.3 ConversationChain (对话链)

**文件**: `backend/app/modules/chat/chains/conversation_chain.py`

**职责**:
- 使用 LCEL 构建对话处理链
- 支持同步和异步调用
- 管理对话历史

**LCEL 链定义**:
```python
self.chain = (
    self.prompt_template      # 1. ChatPromptTemplate
    | self.llm                # 2. ChatOpenAI
    | StrOutputParser()       # 3. 字符串输出解析器
)
```

**v2.0 简化接口**:
```python
def invoke(
    self,
    system_prompt: str,          # 完整系统提示词
    user_message: str,
    conversation_history: List[Dict]
) -> str:
    """同步调用"""
    history = convert_history_to_messages(conversation_history)
    response = self.chain.invoke({
        "system_prompt": system_prompt,
        "history": history,
        "user_message": user_message
    })
    return response
```

---

### 3.4 EvaluationChain (评估链)

**文件**: `backend/app/modules/evaluation/chains/evaluation_chain.py`

**职责**:
- 生成结构化评估报告
- 使用 Pydantic 进行数据验证
- THP 五维评分（AI 内部 0-25/15/10 分）

**LCEL 链定义**:
```python
self.chain = (
    self.prompt_template
    | self.llm_with_retry          # 带重试的 LLM
    | self.output_parser           # Pydantic 输出解析器
)
```

**AI 内部评分体系**:
```python
class RadarChart(BaseModel):
    A_risk_identification: int = Field(ge=0, le=25)      # 0-25 分
    B_communication: int = Field(ge=0, le=25)            # 0-25 分
    C_skill_application: int = Field(ge=0, le=25)        # 0-25 分
    D_safety_management: int = Field(ge=0, le=15)        # 0-15 分
    E_self_efficacy: int = Field(ge=0, le=10)            # 0-10 分
    # 总计: 25+25+25+15+10 = 100 分
```

**模型转换** (AIService):
```python
def scale_to_100(value: int, max_defined: int) -> int:
    """将 AI 内部分数转换为 API 0-100 分"""
    scaled = value * (100 / max_defined)
    return min(max(scaled, 0), 100)  # 限制在 0-100 范围

def _convert_ai_model_to_api(self, report_model) -> Dict:
    return {
        "radar_chart": {
            "A_risk_identification": scale_to_100(radar.A, 25),
            "B_communication": scale_to_100(radar.B, 25),
            "C_skill_application": scale_to_100(radar.C, 25),
            "D_safety_management": scale_to_100(radar.D, 15),
            "E_self_efficacy": scale_to_100(radar.E, 10),
        },
        # ... 其他字段
    }
```

---

### 3.5 EventBus (事件总线)

**文件**: `backend/app/shared/infrastructure/event_bus.py`

**职责**:
- 模块间解耦通信
- 发布-订阅模式

**事件类型**:
```python
class Events:
    CHAT_SESSION_ENDED = "chat.session_ended"        # 会话结束
    EVALUATION_GENERATED = "evaluation.generated"    # 评估生成完成
    EVALUATION_FAILED = "evaluation.failed"          # 评估失败
```

---

## 4. LangChain 集成

### 4.1 核心抽象

LangChain 提供的核心抽象：

| 抽象 | 说明 | 实现 |
|------|------|------|
| **LLM** | 大语言模型接口 | `ChatOpenAI` |
| **Prompt Template** | 提示词模板 | `ChatPromptTemplate` |
| **Output Parser** | 输出解析器 | `StrOutputParser`, `PydanticOutputParser` |
| **Chain** | 链式调用 | LCEL (`\|` 操作符) |

### 4.2 兼容性配置

使用 OpenAI 兼容模式调用通义千问/DeepSeek：

```python
llm = ChatOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 通义
    # 或
    base_url="https://api.deepseek.com",  # DeepSeek
    api_key=settings.AI_TEXT_KEY,
    model="qwen-max"  # 或 "deepseek-chat"
)
```

### 4.3 消息类型

```python
from langchain_core.messages import HumanMessage, AIMessage

messages = [
    HumanMessage(content="用户消息"),
    AIMessage(content="AI 回复")
]
```

---

## 5. 链式调用 (LCEL)

### 5.1 LCEL 介绍

**LCEL (LangChain Expression Language)** 是 LangChain 的声明式链组合语法：

```python
chain = (
    component_1
    | component_2
    | component_3
)
```

### 5.2 对话链实现

**文件**: `modules/chat/chains/conversation_chain.py`

```python
from langchain_core.output_parsers import StrOutputParser

class ConversationChain:
    def __init__(self):
        self.prompt_template = create_conversation_prompt_template()
        self.llm = langchain_manager.get_llm()
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def invoke(self, system_prompt: str, user_message: str, conversation_history: List[Dict]) -> str:
        history = convert_history_to_messages(conversation_history)
        response = self.chain.invoke({
            "system_prompt": system_prompt,
            "history": history,
            "user_message": user_message
        })
        return response
```

### 5.3 评估链实现

**文件**: `modules/evaluation/chains/evaluation_chain.py`

```python
from langchain_core.output_parsers import PydanticOutputParser

class EvaluationChain:
    def __init__(self):
        self.prompt_template = create_evaluation_prompt_template()
        self.output_parser = create_evaluation_output_parser()
        llm = langchain_manager.get_llm()
        self.llm_with_retry = llm.with_retry(stop_after_attempt=3)
        self.chain = self.prompt_template | self.llm_with_retry | self.output_parser

    def invoke(self, conversation_text: str, scenario_title: str, ...) -> EvaluationReportModel:
        result = self.chain.invoke({
            "evaluation_criteria": evaluation_criteria,
            "scenario_title": scenario_title,
            "conversation_text": conversation_text,
            "format_instructions": self.output_parser.get_format_instructions()
        })
        return result
```

---

## 6. 提示词管理

### 6.1 分散式组织结构

```
modules/
├── chat/
│   └── prompts/
│       └── conversation_prompt.py
└── evaluation/
    └── prompts/
        └── evaluation_prompt.py
```

**设计原则**:
- 每个 AI 功能归属对应业务模块
- 避免共享目录臃肿
- 模块内聚，职责明确

### 6.2 对话提示词

**文件**: `modules/chat/prompts/conversation_prompt.py`

```python
def create_conversation_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_message}")
    ])

def convert_history_to_messages(history: List[Dict]) -> list:
    """将历史对话转换为 LangChain 消息格式"""
    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages
```

### 6.3 评估提示词

**文件**: `modules/evaluation/prompts/evaluation_prompt.py`

```python
def create_evaluation_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", "你是围产期抑郁护理培训专家导师。"),
        ("human", "{evaluation_criteria}\n\n{conversation_text}\n\n{format_instructions}")
    ])

def create_evaluation_output_parser() -> PydanticOutputParser:
    return PydanticOutputParser(pydantic_object=EvaluationReportModel)

# Pydantic 输出模型
class EvaluationReportModel(BaseModel):
    total_score: int = Field(description="总分 (0-100)")
    level_assessment: str = Field(description="等级评定")
    radar_chart: RadarChart
    detailed_feedback: List[DetailedFeedbackItem]
    technical_guidance: str
```

---

## 7. 事件驱动架构

### 7.1 事件流程

```
┌─────────────────┐
│ Chat API        │
│ 结束会话         │
└────────┬────────┘
         │
         ↓ publish(session_ended)
┌─────────────────┐
│  EventBus       │
│  事件分发        │
└────────┬────────┘
         │
         ↓ notify
┌─────────────────┐
│  MentorAgent    │
│  订阅者          │
│  generate...()  │
└────────┬────────┘
         │
         ↓ ai_service.generate_evaluation_report()
┌─────────────────┐
│  EvaluationChain│
│  生成评估        │
└─────────────────┘
```

### 7.2 事件订阅

**MentorAgent** 初始化时订阅：
```python
class MentorAgent:
    def __init__(self, db: Session):
        self.event_bus = event_bus
        self.event_bus.subscribe(
            Events.CHAT_SESSION_ENDED,
            self._handle_session_ended
        )
```

### 7.3 事件发布

**Chat API** 结束会话时：
```python
event_bus.publish(
    Events.CHAT_SESSION_ENDED,
    {"session_id": session_id}
)
```

---

## 8. 技能配置系统

### 8.1 配置文件

**文件**: `backend/app/config/skill_config.json`

```json
{
  "global_skill": {
    "enabled": true,
    "name": "围产期抑郁患者模拟行为准则",
    "role_definition": "你不是AI助手，你是根据以下剧本设定的真实病人。",
    "core_principles": [
      "真实模拟：准确反映围产期抑郁患者的症状和表现",
      "指标驱动：根据护士的回应动态调整情绪指标",
      "渐进变化：情绪变化应该是渐进的，符合真实情况",
      "危机响应：在指标达到阈值时触发危机行为"
    ],
    "behavior_guidelines": {
      "language_style": "使用抑郁患者常见的语言模式",
      "emotional_response": "情绪反应要符合当前心情指标值",
      "rapport_building": "信任度变化要自然"
    },
    "indicator_rules": {
      "mood_score": {
        "tone_mapping": {
          "<30": "极度低落，回复简短",
          "30-50": "焦虑抱怨，情绪负面",
          "50-70": "愿意交流，但仍谨慎",
          ">70": "信任开放，愿意分享"
        }
      }
    },
    "system_prompt_template": "你是围产期抑郁患者模拟智能体。\n\n【核心原则】\n{core_principles}\n\n【行为指南】\n- 语言风格：{language_style}\n- 情绪响应：{emotional_response}\n- 信任建立：{rapport_building}\n\n【当前状态】\n心情：{mood_score}/100\n满意度：{satisfaction_score}/100\n抑郁程度：{depression_level}/100\n信任度：{rapport_score}/100\n\n【语气映射】\n{tone_mapping}\n\n请基于以上指导原则和当前状态，模拟真实患者的回复。"
  }
}
```

### 8.2 配置管理器

**文件**: `backend/app/shared/infrastructure/skill_config.py`

```python
class SkillConfigManager:
    """技能配置管理器 - 单例模式"""

    _instance: Optional['SkillConfigManager'] = None

    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self.get_global_skill().get("enabled", False)

    def get_skill_prompt(self, current_state: dict = None) -> str:
        """获取技能提示词（自动替换占位符）"""
        if not self.is_enabled():
            return ""

        skill = self.get_global_skill()
        template = skill.get("system_prompt_template", "")

        # 获取各部分内容
        behavior = skill.get("behavior_guidelines", {})
        core_principles = skill.get("core_principles", [])
        indicator_rules = skill.get("indicator_rules", {})

        # 替换占位符
        prompt = template
        prompt = prompt.replace("{core_principles}", "\n".join([f"• {p}" for p in core_principles]))
        prompt = prompt.replace("{language_style}", behavior.get("language_style", ""))
        prompt = prompt.replace("{emotional_response}", behavior.get("emotional_response", ""))
        # ... 其他替换

        return prompt

# 全局实例
skill_config_manager = SkillConfigManager()
```

### 8.3 集成到对话

**ConversationEngine** 使用技能配置：

```python
class ConversationEngine:
    def __init__(self, ...):
        self.skill_config = skill_config_manager

    def generate_ai_response(self, session_id: str, user_message: str):
        # 获取技能提示词
        skill_prompt = ""
        if self.skill_config.is_enabled():
            skill_prompt = self.skill_config.get_skill_prompt()

        # 构建完整系统提示词
        system_prompt = f"【系统提示】\n{scenario_prompt}\n\n"
        if skill_prompt:
            system_prompt += f"【全局技能指导】\n{skill_prompt}\n\n"
        system_prompt += f"【患者背景】\n{patient_background}\n"

        # 调用 AI 服务
        response = self.ai_service.generate_conversation_response(
            system_prompt=system_prompt,
            user_message=user_message,
            conversation_history=history
        )
        return response
```

---

## 9. 数据流

### 9.1 对话生成流程

```
用户输入
  ↓
ConversationEngine.generate_ai_response()
  ↓ 获取技能配置
  skill_config_manager.get_skill_prompt()
  ↓ 构建 system_prompt
  │ - 【系统提示】场景配置
  │ - 【全局技能指导】技能配置（如果启用）
  │ - 【患者背景】患者信息
  ↓
AIService.generate_conversation_response()
  ↓ 直接传递完整 system_prompt
ConversationChain.invoke()
  ↓
┌─────────────────────────────────────┐
│ ChatPromptTemplate                   │
│ - system_prompt (完整)              │
│ - history (历史对话)                 │
│ - user_message                       │
└─────────────────┬───────────────────┘
                  ↓
            ┌─────────────┐
            │ ChatOpenAI  │
            │ (LLM)       │
            └─────────────┘
                  ↓
            ┌─────────────┐
            │ StrOutput   │
            │ Parser      │
            └─────────────┘
                  ↓
            AI 回复文本
```

### 9.2 评估生成流程

```
会话结束事件
  ↓
MentorAgent._handle_session_ended()
  ↓
获取会话数据
  - ChatSession
  - ChatMessage[]
  - Scenario
  ↓
AIService.generate_evaluation_report()
  ↓
EvaluationChain.invoke()
  ↓
┌─────────────────────────────────────┐
│ ChatPromptTemplate                   │
│ - evaluation_criteria (THP标准)     │
│ - conversation_text                 │
│ - format_instructions (Pydantic)    │
└─────────────────┬───────────────────┘
                  ↓
            ┌─────────────┐
            │ ChatOpenAI  │
            │ with_retry  │
            └─────────────┘
                  ↓
            ┌─────────────┐
            │ Pydantic     │
            │ Output       │
            │ Parser      │
            └─────────────┘
                  ↓
      EvaluationReportModel
        (AI 内部 0-25/15/10 分)
                  ↓
      _convert_ai_model_to_api()
                  ↓
        API 响应 (0-100 分)
                  ↓
            保存到数据库
```

---

## 10. 使用示例

### 10.1 对话生成

```python
from backend.app.shared.infrastructure.ai_service import ai_service

# 生成对话回复
response = ai_service.generate_conversation_response(
    system_prompt="""【系统提示】
你是一位产后6周的妈妈，名叫小丽，32岁。

【全局技能指导】
你是围产期抑郁患者模拟智能体。

【核心原则】
• 真实模拟：准确反映围产期抑郁患者的症状和表现
• 指标驱动：根据护士的回应动态调整情绪指标

【患者背景】
小丽，32岁，已婚，研究生学历，教师（产假中）。
""",
    user_message="你好",
    conversation_history=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好...谢谢你愿意听我说话。"}
    ]
)

print(response)
# （低头摆弄着手指，声音很轻）你好...又见到你了。
```

### 10.2 评估报告生成

```python
from backend.app.shared.infrastructure.ai_service import ai_service

# 生成评估报告
report = ai_service.generate_evaluation_report(
    conversation_text="""
    对话历史：
    护士: 你好，我是你的责任护士
    患者: 你好，我最近心情不太好
    护士: 能跟我说说吗？
    患者: （叹气）我也不知道从哪里说起...就是觉得特别累
    ...
    """,
    evaluation_criteria="""
    THP五维评分标准：
    - A类：风险识别能力 (25分)
    - B类：沟通支持能力 (25分)
    - C类：THP技能应用 (25分)
    - D类：安全管理能力 (15分)
    - E类：自我效能感 (10分)
    """
)

print(report)
# {
#     "total_score": 85,
#     "level_assessment": "良好",
#     "radar_chart": {
#         "A_risk_identification": 88,  # AI 内部 22 → API 88
#         "B_communication": 84,        # AI 内部 21 → API 84
#         "C_skill_application": 80,    # AI 内部 20 → API 80
#         "D_safety_management": 80,    # AI 内部 12 → API 80
#         "E_self_efficacy": 70        # AI 内部 7  → API 70
#     },
#     "detailed_feedback": [...],
#     ...
# }
```

### 10.3 事件发布

```python
from backend.app.shared.infrastructure.event_bus import event_bus, Events

# 发布会话结束事件
event_bus.publish(
    Events.CHAT_SESSION_ENDED,
    {"session_id": "session_123"}
)
```

---

## 11. 扩展指南

### 11.1 添加新的 AI 能力

#### 步骤 1: 在对应模块创建链

**文件**: `modules/new_feature/chains/my_chain.py`

```python
from typing import Dict
from langchain_core.output_parsers import StrOutputParser
from backend.app.shared.ai.langchain_manager import langchain_manager
from backend.app.modules.new_feature.prompts.my_prompt import create_my_prompt_template

class MyChain:
    def __init__(self):
        self.prompt = create_my_prompt_template()
        self.llm = langchain_manager.get_llm()
        self.chain = self.prompt | self.llm | StrOutputParser()

    def invoke(self, input_data: Dict) -> str:
        return self.chain.invoke(input_data)

# 创建全局实例
my_chain = MyChain()
```

#### 步骤 2: 添加提示词模板

**文件**: `modules/new_feature/prompts/my_prompt.py`

```python
from langchain_core.prompts import ChatPromptTemplate

def create_my_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}。"),
        ("human", "{input}")
    ])
```

#### 步骤 3: 扩展 AIService

**文件**: `shared/infrastructure/ai_service.py`

```python
class AIService:
    def __init__(self):
        # ... 现有初始化 ...
        from backend.app.modules.new_feature.chains.my_chain import my_chain
        self.my_chain = my_chain

    def generate_my_capability(self, input_data: Dict) -> str:
        """新的 AI 能力"""
        return self.my_chain.invoke(input_data)
```

### 11.2 修改技能配置

编辑 `config/skill_config.json`:

```json
{
  "global_skill": {
    "enabled": true,
    "core_principles": [
      "新的原则1",
      "新的原则2"
    ],
    "system_prompt_template": "更新后的模板..."
  }
}
```

无需重启，配置会在下次调用时自动加载。

---

## 12. 最佳实践

### 12.1 提示词工程

✅ **推荐做法**:
```python
# 使用模板化提示词
template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}。你的任务是{task}。"),
    ("human", "{input}")
])

# 明确的格式要求
format_instructions = """
请以 JSON 格式返回，包含以下字段：
- score: 分数
- reason: 原因
"""
```

❌ **避免做法**:
```python
# 硬编码提示词
prompt = "你是医生，用户说：" + user_input

# 模糊的要求
prompt = "给我一个评估"
```

### 12.2 错误处理

✅ **推荐做法**:
```python
try:
    response = self.chain.invoke(data)
except Exception as e:
    print(f"❌ AI调用失败: {e}")
    raise  # 重新抛出，让上层处理
```

❌ **避免做法**:
```python
# 吞掉异常
try:
    response = self.chain.invoke(data)
except:
    pass

# 只打印不处理
except Exception as e:
    print(e)  # 错误信息丢失
```

### 12.3 单例模式

✅ **推荐做法**:
```python
# 使用全局实例
from backend.app.shared.infrastructure.ai_service import ai_service

response = ai_service.generate_conversation_response(...)
```

❌ **避免做法**:
```python
# 每次都创建新实例
def some_function():
    ai_service = AIService()  # 创建多个 LLM 实例
    return ai_service.generate(...)
```

### 12.4 类型注解

✅ **推荐做法**:
```python
from typing import List, Dict, Optional

def generate_report(
    conversation_text: str,
    evaluation_criteria: Dict,
    max_retries: int = 2
) -> Dict:
    ...
```

---

## 附录

### A. 相关文件索引

| 文件路径 | 说明 |
|---------|------|
| `backend/app/shared/ai/langchain_manager.py` | LLM 管理器 |
| `backend/app/modules/chat/chains/conversation_chain.py` | 对话链 |
| `backend/app/modules/evaluation/chains/evaluation_chain.py` | 评估链 |
| `backend/app/modules/chat/prompts/conversation_prompt.py` | 对话提示词 |
| `backend/app/modules/evaluation/prompts/evaluation_prompt.py` | 评估提示词 |
| `backend/app/shared/infrastructure/ai_service.py` | AI 服务接口 |
| `backend/app/shared/infrastructure/event_bus.py` | 事件总线 |
| `backend/app/shared/infrastructure/skill_config.py` | 技能配置管理器 |
| `backend/app/config/skill_config.json` | 技能配置文件 |
| `backend/app/config/config.py` | 全局配置类 |

### B. 参考资料

- [LangChain 官方文档](https://python.langchain.com/)
- [通义千问集成指南](https://python.langchain.ac.cn/docs/integrations/chat/tongyi/)
- [LCEL 教程](https://python.langchain.com/docs/expression_language/)
- [Pydantic 文档](https://docs.pydantic.dev/)

### C. 版本历史

| 版本 | 日期         | 变更 |
|------|------------|------|
| 2.0.0 | 2026-01-29 | 架构重构：分散式 prompts/chains，简化 AIService，技能配置系统 |
| 1.0.0 | 2026-01-15 | 初始版本，LangChain 架构 |

---

**文档维护**: AI 模块团队
**最后更新**: 2026-01-29
