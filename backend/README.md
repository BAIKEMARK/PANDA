# PANDA 后端项目

**围产期抑郁管理智能培训系统 - FastAPI 后端服务**

基于 **LangChain 1.x** 框架构建的 AI 驱动智能培训系统，集成 **Agent** 智能体和 **Redis** 状态管理。

---

## 项目架构

本项目采用**分层模块化架构**，按业务领域垂直划分模块，通过事件总线实现模块间解耦通信。

### 核心技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| **FastAPI** | 0.109.0 | 现代异步 Web 框架 |
| **SQLAlchemy** | 2.0.25 | ORM 数据库操作 |
| **LangChain** | 1.2.7 | LLM 应用开发框架 |
| **LangChain Core** | 1.2.7 | 核心抽象层 |
| **LangChain OpenAI** | 1.1.7 | OpenAI 兼容接口 |
| **Pydantic** | 2.7+ | 数据验证和结构化输出 |
| **Redis** | 5.0.1 | 实时状态缓存 |
| **通义千问/DeepSeek** | - | LLM 提供商 |

### 架构设计原则

1. **按业务领域垂直切分**：每个业务域独立成一个完整模块
2. **保持分层架构**：每个模块内部保持 API → Service → Repository → Model
3. **依赖倒置**：模块间通过抽象接口通信，而非直接依赖具体实现
4. **共享基础设施**：config、db、common、infrastructure 作为独立的基础层
5. **单向依赖**：业务模块只能依赖共享层，不能横向依赖其他业务模块
6. **LangChain 集成**：AI 能力通过 LangChain 统一管理和调用
7. **Agent 智能体**：患者 Agent 通过规则引擎实现动态状态更新
8. **Redis 实时状态**：患者状态 Redis 缓存 + MySQL 持久化

---

## 项目结构

```
backend/
├── app/                              # 应用主目录
│   ├── main.py                       # 应用入口
│   │
│   ├── shared/                       # 共享基础设施层
│   │   ├── ai/                       # AI 基础设施
│   │   │   └── langchain_manager.py  # LLM 统一管理器（单例）
│   │   │
│   │   ├── db/                       # 数据库基础设施
│   │   │   ├── database.py           # Session管理、Base
│   │   │   └── init_db.py            # 初始化脚本
│   │   │
│   │   ├── common/                   # 通用模块
│   │   │   ├── constants.py          # 枚举常量
│   │   │   └── exceptions.py         # 自定义异常
│   │   │
│   │   ├── infrastructure/           # 基础设施服务
│   │   │   ├── ai_service.py         # AI 服务统一接口
│   │   │   ├── skill_config.py       # 技能配置管理（单例）
│   │   │   ├── event_bus.py          # 事件总线（模块间通信）
│   │   │   └── redis_state_manager.py # Redis 状态管理器
│   │   │
│   │   └── models/                   # ORM 模型引用
│   │
│   ├── config/                       # 配置层
│   │   ├── config.py                 # 全局配置类
│   │   ├── security.py               # 安全相关配置
│   │   └── skill_config.json         # 技能配置文件
│   │
│   ├── interfaces/                   # 模块间接口定义层
│   │   ├── __init__.py
│   │   └── scenario_interface.py     # 场景模块对外接口
│   │
│   ├── modules/                      # 业务模块层
│   │   ├── auth/                     # 模块1: 认证与用户管理
│   │   │   ├── api/                  # Controller 层
│   │   │   ├── services/             # Service 层
│   │   │   ├── repositories/         # Repository 层
│   │   │   └── schemas/              # DTO 层
│   │   │
│   │   ├── course/                   # 模块2: 课程管理
│   │   ├── scenario/                 # 模块3: 情景模拟
│   │   │
│   │   ├── chat/                     # 模块4: 对话交互
│   │   │   ├── api/                  # Controller 层
│   │   │   ├── services/             # Service 层
│   │   │   │   ├── chat_service.py
│   │   │   │   └── conversation_engine.py
│   │   │   ├── repositories/         # Repository 层
│   │   │   ├── schemas/              # DTO 层
│   │   │   ├── prompts/              # 对话提示词模块
│   │   │   │   └── conversation_prompt.py
│   │   │   └── chains/               # 对话链模块
│   │   │       └── conversation_chain.py
│   │   │
│   │   ├── agent/                    # 模块5: Agent 智能体系统
│   │   │   ├── core/                 # 核心组件
│   │   │   │   ├── agent_orchestrator.py    # Agent 编排器
│   │   │   │   ├── state_update_engine.py   # 状态更新引擎
│   │   │   │   └── crisis_detector.py       # 危机检测器
│   │   │   ├── chains/               # Agent 链
│   │   │   │   └── patient_agent_chain.py   # 患者 Agent 链
│   │   │   ├── prompts/              # Agent 提示词
│   │   │   │   └── patient_agent_prompt.py  # 患者 Agent 提示词
│   │   │   ├── services/             # Service 层
│   │   │   │   └── patient_state_service.py # 患者状态服务
│   │   │   ├── repositories/         # Repository 层
│   │   │   │   └── patient_state_repository.py # 患者状态仓储
│   │   │   └── models/               # 数据模型
│   │   │       ├── patient_state.py  # 患者状态模型
│   │   │       └── agent_response.py # Agent 响应模型
│   │   │
│   │   ├── evaluation/               # 模块6: 评估系统
│   │   │   ├── api/                  # Controller 层
│   │   │   ├── services/             # Service 层
│   │   │   ├── agents/               # Agent 层
│   │   │   │   └── mentor_agent.py
│   │   │   ├── schemas/              # DTO 层
│   │   │   ├── prompts/              # 评估提示词模块
│   │   │   │   └── evaluation_prompt.py
│   │   │   └── chains/               # 评估链模块
│   │   │       └── evaluation_chain.py
│   │   │
│   │   ├── progress/                 # 模块7: 学习进度
│   │   └── menu/                     # 模块8: 菜单权限
│   │
│   ├── models/                       # ORM 模型层（共享）
│   ├── schemas/                      # Pydantic 模型层（共享）
│   ├── common/                       # 通用模块
│   └── db/                           # 数据库
│
├── .env                              # 环境变量
├── .env.example                      # 环境变量示例
├── requirements.txt                  # Python 依赖
└── start.py                          # 启动脚本
```

---

## LangChain AI 架构

### 设计理念

- **分散式管理**：各业务模块的 prompts/chains 归属各模块管理
- **统一入口**：所有 AI 调用通过 `AIService` 统一接口
- **共享基础**：LLM 实例通过 `LangChainManager` 单例共享
- **LCEL 链式调用**：使用 LangChain Expression Language 构建链

### AI 模块组织结构

```
shared/ai/
└── langchain_manager.py       # LLM 统一管理（单例模式）
    └── 职责：创建和管理 ChatOpenAI 实例

modules/chat/
├── prompts/
│   └── conversation_prompt.py  # 对话提示词
└── chains/
    └── conversation_chain.py   # 对话链（LCEL）

modules/agent/
├── chains/
│   └── patient_agent_chain.py  # 患者 Agent 链（LCEL）
└── prompts/
    └── patient_agent_prompt.py # 患者 Agent 提示词

modules/evaluation/
├── prompts/
│   └── evaluation_prompt.py    # 评估提示词（Pydantic 格式）
└── chains/
    └── evaluation_chain.py     # 评估链（结构化输出）

shared/infrastructure/
├── ai_service.py              # AI 服务统一接口
│   └── 职责：提供对话和评估的统一 API
│
├── event_bus.py               # 事件总线（发布-订阅）
│   └── 职责：模块间解耦通信
│
├── skill_config.py            # 技能配置管理
│   └── 职责：全局对话技能配置（config/skill_config.json）
│
└── redis_state_manager.py     # Redis 状态管理器
    └── 职责：患者状态的 Redis 缓存管理
```

### LCEL 链式调用

**对话链** (modules/chat/chains/conversation_chain.py):
```python
self.chain = (
    self.prompt_template      # ChatPromptTemplate
    | self.llm                # ChatOpenAI (通义千问/DeepSeek)
    | StrOutputParser()       # 字符串输出解析器
)
```

**患者 Agent 链** (modules/agent/chains/patient_agent_chain.py):
```python
self.chain = (
    self.prompt_template      # ChatPromptTemplate (包含动态状态)
    | self.llm                # ChatOpenAI
    | StrOutputParser()       # 字符串输出解析器
)
```

**评估链** (modules/evaluation/chains/evaluation_chain.py):
```python
self.chain = (
    self.prompt_template
    | llm.with_retry(stop_after_attempt=3)
    | PydanticOutputParser()  # 结构化输出
)
```

---

## Agent 智能体系统

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent Orchestrator                       │
│                   (Agent 编排器 - 核心协调)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Patient Agent │   │ State Engine  │   │ Crisis Detector│
│   (患者回复)   │   │  (状态更新)    │   │  (危机检测)    │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        │                   ▼                   │
        │         ┌─────────────────┐           │
        │         │ Redis State     │           │
        │         │ Manager         │           │
        │         │ (实时状态缓存)   │           │
        │         └────────┬────────┘           │
        │                  │                    │
        ▼                  ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                   Patient State Service                   │
│                   (状态持久化服务)                         │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
                  ┌─────────────────┐
                  │  patient_states │
                  │   (MySQL表)     │
                  └─────────────────┘
```

### 核心组件

#### 1. Agent Orchestrator (agent_orchestrator.py)

**职责**：协调所有 Agent 组件，处理每轮对话

**流程**：
1. 接收用户输入（护士消息）
2. 获取当前患者状态（从 Redis）
3. 调用 Patient Agent 生成回复
4. 调用 State Update Engine 计算状态变化
5. 检测是否触发危机
6. 更新 Redis 状态
7. 持久化到 MySQL

#### 2. Patient Agent Chain (patient_agent_chain.py)

**职责**：生成符合患者角色设定的回复

**特点**：
- 使用 LCEL 构建：prompt | llm | StrOutputParser
- Prompt 包含动态状态（心情、满意度、抑郁程度、信任度）
- 根据场景配置（system_prompt）和患者背景生成回复

#### 3. State Update Engine (state_update_engine.py)

**职责**：基于 skill_config.json 规则计算状态变化

**四项指标**：
- `mood_score` (心情指数): 0-100
- `satisfaction_score` (满意度): 0-100
- `depression_level` (抑郁程度): 0-100
- `rapport_score` (信任度): 0-100

**规则匹配示例**：
```json
{
  "indicator_rules": {
    "mood_score": {
      "change_rules": [
        "护士表现出同理心 (+5~10)",
        "共情回应 (+3~8)",
        "说教打断 (-5~-10)"
      ]
    }
  },
  "cris_thresholds": {
    "mood_too_low": 15,
    "depression_too_high": 85,
    "rapport_broken": 10
  }
}
```

#### 4. Crisis Detector (crisis_detector.py)

**职责**：检测患者状态是否触发危机阈值

**危机类型**：
- `mood_crisis` - 心情过低 (< 15)
- `depression_crisis` - 抑郁程度过高 (> 85)
- `rapport_crisis` - 信任破裂 (< 10)
- `satisfaction_crisis` - 满意度过低 (< 10)

---

## Redis 状态管理

### 数据结构

#### 实时状态 (patient:state:{session_id})

```
Key: patient:state:{session_id}
Type: Hash
TTL: 24小时

Fields:
  - mood_score: 45          # 心情指数 (0-100)
  - satisfaction_score: 42  # 满意度 (0-100)
  - depression_level: 65    # 抑郁程度 (0-100)
  - rapport_score: 40       # 信任度 (0-100)
  - message_count: 3        # 对话轮次
  - is_crisis: false        # 是否危机状态
  - crisis_type: null       # 危机类型
```

#### 对话历史 (patient:history:{session_id})

```
Key: patient:history:{session_id}
Type: List
Max Length: 50轮

[
  {
    "role": "user",
    "content": "护士的消息",
    "state_snapshot": { "mood_score": 45, ... }
  },
  {
    "role": "assistant",
    "content": "患者的回复",
    "state_snapshot": { "mood_score": 50, ... }
  }
]
```

### Redis + MySQL 混合存储

| 操作 | Redis | MySQL |
|------|-------|-------|
| 读取状态 | ✅ 实时读取 (< 10ms) | - |
| 更新状态 | ✅ 立即更新 | ✅ 异步持久化 |
| 状态历史 | - | ✅ 每次变更记录 |
| 会话快照 | ✅ 快速恢复 | ✅ 长期存储 |

---

## 模块说明

### 1. 共享基础设施层 (shared/)

#### shared/infrastructure/redis_state_manager.py
- **功能**：Redis 状态管理器（单例）
- **方法**：
  - `get_patient_state(session_id)` - 获取患者状态
  - `update_patient_state(session_id, updates)` - 更新患者状态
  - `save_state_snapshot(session_id)` - 保存状态快照
  - `restore_state_snapshot(session_id, snapshot_id)` - 恢复状态快照

#### shared/infrastructure/ai_service.py
- **功能**：AI 服务统一接口
- **方法**：
  - `generate_conversation_response(system_prompt, user_message, conversation_history)` - 生成对话回复
  - `generate_evaluation_report(conversation_text, evaluation_criteria)` - 生成评估报告

#### shared/infrastructure/event_bus.py
- **功能**：事件总线（发布-订阅模式）
- **事件类型**：
  - `CHAT_SESSION_ENDED` - 会话结束
  - `EVALUATION_GENERATED` - 评估生成完成

#### shared/infrastructure/skill_config.py
- **功能**：技能配置管理器（单例）
- **配置文件**：`config/skill_config.json`
- **职责**：读取和管理全局对话技能配置

### 2. Agent 智能体模块 (modules/agent/)

**核心组件**：
- `core/agent_orchestrator.py` - Agent 编排器
  - 协调 Patient Agent、State Engine、Crisis Detector
  - 处理每轮对话的完整流程
  - 管理 Redis 状态更新和 MySQL 持久化

- `core/state_update_engine.py` - 状态更新引擎
  - 基于 skill_config.json 规则计算状态变化
  - 智能语义匹配护士输入
  - 边界衰减（接近极值时变化减缓）

- `core/crisis_detector.py` - 危机检测器
  - 检测四项指标是否触发危机阈值
  - 返回危机类型和响应模板

- `chains/patient_agent_chain.py` - 患者 Agent 链
  - 使用 LCEL 构建：prompt | llm | StrOutputParser
  - Prompt 包含动态状态和场景配置

- `services/patient_state_service.py` - 患者状态服务
  - Redis 状态管理
  - MySQL 状态历史记录
  - 状态快照和恢复

- `repositories/patient_state_repository.py` - 患者状态仓储
  - 状态变更记录的 CRUD 操作
  - 状态历史查询

### 3. 对话交互模块 (modules/chat/)

**API端点**：
- `POST /api/chat/sessions` - 创建会话
- `POST /api/chat/messages` - 发送消息并获取 AI 回复
- `PUT /api/chat/sessions/{id}/end` - 结束会话（触发评估）

**核心组件**：
- `services/conversation_engine.py` - 对话编排引擎
  - 通过 `AgentOrchestrator` 调用患者 Agent
  - 通过 `EventBus` 发布会话结束事件
  - 集成技能配置到系统提示词

- `chains/conversation_chain.py` - 对话链
  - 使用 LCEL 构建：prompt | llm | StrOutputParser
  - 处理多轮对话历史

- `prompts/conversation_prompt.py` - 提示词模板
  - ChatPromptTemplate 模板
  - 支持系统提示、历史对话、用户消息

### 4. 评估系统模块 (modules/evaluation/)

**API端点**：
- `GET /api/evaluation/reports/{id}` - 获取评估报告

**核心组件**：
- `agents/mentor_agent.py` - AI 评估智能体
  - 订阅 `CHAT_SESSION_ENDED` 事件
  - 使用 LangChain 评估链生成报告
  - 基于 THP 五维评分体系

- `chains/evaluation_chain.py` - 评估链
  - 使用 LCEL 构建：prompt | llm.with_retry | PydanticOutputParser
  - 结构化输出评估报告

### 5. 其他模块

- **auth/** - 认证与用户管理
- **course/** - 课程管理
- **scenario/** - 情景模拟
- **progress/** - 学习进度
- **menu/** - 菜单权限

---

## 技能配置系统

### 配置文件：config/skill_config.json

技能配置定义了全局对话行为准则，包括：

```json
{
  "global_skill": {
    "enabled": true,
    "role_definition": "角色定义",
    "core_principles": ["核心原则1", "核心原则2"],
    "behavior_guidelines": {
      "language_style": "语言风格",
      "emotional_response": "情绪响应",
      "rapport_building": "信任建立"
    },
    "indicator_rules": {
      "mood_score": {
        "change_rules": [
          "护士表现出同理心 (+5~10)",
          "共情回应 (+3~8)"
        ],
        "tone_mapping": {
          "<30": "极度低落",
          "30-50": "焦虑",
          "50-70": "谨慎",
          ">70": "开放"
        }
      }
    },
    "cris_thresholds": {
      "mood_too_low": 15,
      "depression_too_high": 85
    },
    "crisis_responses": {
      "extreme_low_mood": "（沉默不语）"
    },
    "system_prompt_template": "包含占位符的模板"
  }
}
```

### 状态更新规则

**规则格式**：`"描述 (+X~Y)"` 或 `"描述 (-X~-Y)"`

**匹配策略**：
1. **积极行为**：同理心、共情、关心、倾听、支持、鼓励、认同
2. **消极行为**：说教、否定、打断、评判、冷漠、敷衍
3. **提问行为**：疑问词、问号
4. **默认匹配**：长文本（>15字符）且无明显负面词

**边界衰减**：
- 接近 0 时，负面变化减缓 (×0.5)
- 接近 100 时，正面变化减缓 (×0.5)

---

## 环境配置

### 环境变量 (.env)

```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=panda

# Redis 配置
REDIS_URL=redis://localhost:6379/0
REDIS_TTL_STATE=86400  # 状态24小时过期
REDIS_MAX_HISTORY=50   # 对话历史保留50轮

# AI 模型配置 - 阿里百炼平台
AI_TEXT_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_TEXT_KEY=sk-*******************
AI_TEXT_MODEL=qwen-max

# LLM 高级配置
LLM_MAX_RETRIES=3
LLM_TIMEOUT=120
LLM_TEMPERATURE=0.7
LLM_STREAMING=false

# CORS 配置
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# JWT 认证
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `REDIS_URL` | Redis 连接地址 | redis://localhost:6379/0 |
| `REDIS_TTL_STATE` | 状态过期时间（秒） | 86400 (24小时) |
| `REDIS_MAX_HISTORY` | 对话历史保留轮数 | 50 |
| `AI_TEXT_URL` | 通义千问 API 地址 | https://dashscope.aliyuncs.com/compatible-mode/v1 |
| `AI_TEXT_MODEL` | 模型名称 | qwen-max / deepseek-v3.2 |
| `LLM_MAX_RETRIES` | 最大重试次数 | 3 |
| `LLM_TIMEOUT` | 超时时间（秒） | 120 |
| `LLM_TEMPERATURE` | 温度参数 | 0.7 |

---

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动 Redis

```bash
# Windows
redis-server

# Linux/Mac
sudo service redis-server start
# 或
redis-server
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入数据库、Redis 和 AI 配置
```

### 4. 初始化数据库

```bash
# 使用 SQL 文件初始化
mysql -u root -p panda < docs/项目文档/resources/panda.sql
```

### 5. 启动应用

```bash
# 方式1：使用启动脚本（推荐）
python start.py

# 方式2：直接使用 uvicorn
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. 访问 API 文档

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## 开发指南

### AI 模块开发

#### 添加新的 AI 能力

1. **在对应模块创建 chains/**：例如 `modules/new_feature/chains/`
2. **创建 prompts/**：例如 `modules/new_feature/prompts/`
3. **扩展 AIService**：在 `shared/infrastructure/ai_service.py` 添加新方法

#### 示例：添加新的对话链

```python
# modules/new_feature/chains/my_chain.py
from langchain_core.output_parsers import StrOutputParser
from backend.app.shared.ai.langchain_manager import langchain_manager

class MyChain:
    def __init__(self):
        self.llm = langchain_manager.get_llm()
        self.chain = self.prompt_template | self.llm | StrOutputParser()
```

### 代码规范

1. **模块结构**：每个业务模块使用 `api/services/repositories/schemas` 结构
2. **AI 组件组织**：prompts 和 chains 归属各模块管理
3. **导入顺序**：标准库 → 第三方库 → 本地模块（使用 `from backend.app.`）
4. **命名规范**：
   - 类名：`PascalCase`
   - 函数/变量：`snake_case`
   - 常量：`UPPER_SNAKE_CASE`
5. **类型注解**：所有公开函数必须添加类型注解

### Git 提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

**type 类型**：
- `feat`: 新功能
- `fix`: 修复 bug
- `refactor`: 重构
- `docs`: 文档更新
- `chore`: 构建/工具相关

**示例**：
```
feat(agent): 实现患者 Agent 智能体系统

- 添加 AgentOrchestrator 编排器
- 实现 StateUpdateEngine 状态更新引擎
- 添加 CrisisDetector 危机检测器
- 集成 Redis 实时状态管理
```

---

## 测试

```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/modules/test_agent.py

# 查看测试覆盖率
pytest --cov=app --cov-report=html
```

---

## 故障排查

### 常见问题

1. **数据库连接失败**
   - 检查 `.env` 中的数据库配置
   - 确认数据库服务已启动

2. **Redis 连接失败**
   - 检查 Redis 是否启动：`redis-cli ping`
   - 确认 `REDIS_URL` 配置正确

3. **AI 调用失败**
   - 检查 `AI_TEXT_KEY` 是否正确配置
   - 确认模型名称（`qwen-max` 或 `deepseek-v3.2`）
   - 检查网络连接

4. **模块导入错误**
   - 使用 `python start.py` 启动（自动设置 PYTHONPATH）
   - 或从项目根目录运行：`PYTHONPATH=E:/project/PANDA python backend/start.py`

5. **技能配置未加载**
   - 检查 `config/skill_config.json` 是否存在
   - 确认 `enabled` 字段为 `true`
   - 查看控制台是否有配置加载日志

---

## 项目文档

| 文档 | 说明 |
|------|------|
| [AI 模块架构](../docs/ai_module_architecture.md) | LangChain 集成详细文档 |
| [开发规则](../docs/开发规则.md) | 6A 工作流和开发规范 |
| [项目介绍](../docs/项目介绍.md) | 项目背景和目标 |
| [数据库设计](../docs/项目文档/resources/数据库设计.md) | 数据库结构和 ER 图 |
| [SQL 脚本](../docs/项目文档/resources/panda.sql) | 完整建表脚本 |

---

## 更新日志

### v0.3.0 (2026-01-31)
- ✅ 升级 LangChain 到 1.2.7
- ✅ 升级 Pydantic 到 2.7+
- ✅ 实现 Agent 智能体系统
  - AgentOrchestrator 编排器
  - PatientAgentChain 患者链
  - StateUpdateEngine 状态更新引擎
  - CrisisDetector 危机检测器
- ✅ 集成 Redis 实时状态管理
  - RedisStateManager 状态管理器
  - Redis + MySQL 混合存储
- ✅ 实现动态患者状态更新
  - 四项指标（心情/满意度/抑郁程度/信任度）
  - 基于 skill_config.json 规则匹配
- ✅ 添加 patient_states 表和状态历史记录

### v0.2.0 (2024-01-29)
- ✅ 重构 AI 模块架构
  - prompts 和 chains 移至各模块内部
  - 重命名 `core/` → `config/`
  - 重命名 `shared/core/` → `shared/ai/`
- ✅ 修复技能配置加载路径
- ✅ 简化 AIService 调用接口
- ✅ 删除重复代码和旧实现
- ✅ 统一导入路径为 `backend.app.*`

### v0.1.0 (2024-01-15)
- ✅ 迁移到 LangChain 框架
- ✅ 实现分层模块化架构
- ✅ 集成事件总线
- ✅ 实现 THP 五维评估体系

---

## 许可证

Copyright © 2024 PANDA Team. All rights reserved.