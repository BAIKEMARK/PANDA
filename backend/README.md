# PANDA 后端项目

**围产期抑郁管理智能培训系统 - FastAPI 后端服务**

基于 **LangChain** 框架构建的 AI 驱动智能培训系统。

---

## 项目架构

本项目采用**分层模块化架构**，按业务领域垂直划分模块，通过事件总线实现模块间解耦通信。

### 核心技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| **FastAPI** | 0.100+ | 现代异步 Web 框架 |
| **SQLAlchemy** | 2.0+ | ORM 数据库操作 |
| **LangChain** | 0.1.16 | LLM 应用开发框架 |
| **LangChain Core** | 0.1.40 | 核心抽象层 |
| **Pydantic** | 2.x | 数据验证和结构化输出 |
| **通义千问/DeepSeek** | - | LLM 提供商 |

### 架构设计原则

1. **按业务领域垂直切分**：每个业务域独立成一个完整模块
2. **保持分层架构**：每个模块内部保持 API → Service → Repository → Model
3. **依赖倒置**：模块间通过抽象接口通信，而非直接依赖具体实现
4. **共享基础设施**：config、db、common、infrastructure 作为独立的基础层
5. **单向依赖**：业务模块只能依赖共享层，不能横向依赖其他业务模块
6. **LangChain 集成**：AI 能力通过 LangChain 统一管理和调用
7. **分散式 AI 模块**：各模块的 prompts/chains 归属各模块管理

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
│   │   │   └── event_bus.py          # 事件总线（模块间通信）
│   │   │
│   │   └── models/                   # ORM 模型引用
│   │
│   ├── config/                       # 配置层（原 core/）
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
│   │   ├── evaluation/               # 模块5: 评估系统
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
│   │   ├── progress/                 # 模块6: 学习进度
│   │   └── menu/                     # 模块7: 菜单权限
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
└── skill_config.py            # 技能配置管理
    └── 职责：全局对话技能配置（config/skill_config.json）
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

**评估链** (modules/evaluation/chains/evaluation_chain.py):
```python
self.chain = (
    self.prompt_template
    | llm.with_retry(stop_after_attempt=3)
    | PydanticOutputParser()  # 结构化输出
)
```

### 调用流程

```
┌─────────────────────────────────────────────────────────────┐
│                     模块层 (modules)                         │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  | ConversationEngine|         |   MentorAgent    |         │
│  └────────┬─────────┘         └────────┬─────────┘         │
└───────────┼────────────────────────────┼────────────────────┘
            │                            │
            ▼                            ▼
┌─────────────────────────────────────────────────────────────┐
│              服务层 (infrastructure)                         │
│              ┌────────────────────────┐                    │
│              │      AIService         │                    │
│              │  - generate_conversation_response()        │
│              │  - generate_evaluation_report()            │
│              └───────────┬────────────┬──────────────────┘ │
└──────────────────────────┼────────────┼──────────────────┘
                          │            │
            ┌─────────────┘            └─────────────┐
            ▼                                          ▼
┌─────────────────────────┐          ┌─────────────────────────┐
│  modules/chat/chains/   │          │ modules/evaluation/     │
│  ConversationChain      │          │ chains/                 │
│  (属于 chat 模块)       │          │ EvaluationChain         │
└─────────────────────────┘          │ (属于 evaluation 模块)  │
                                   └─────────────────────────┘
                          │
                          ▼
                  ┌─────────────────────┐
                  │ shared/ai/          │
                  │ langchain_manager   │
                  │ (共享 LLM 实例)     │
                  └─────────────────────┘
```

### 事件驱动流程

```
Chat API 结束会话
    ↓
EventBus.publish(chat.session_ended)
    ↓
MentorAgent 订阅并处理
    ↓
AIService.generate_evaluation_report()
    ↓
EvaluationChain.invoke()
    ↓
评估报告保存到数据库
```

---

## 模块说明

### 1. 共享基础设施层 (shared/)

#### shared/ai/langchain_manager.py
- **功能**：LLM 统一管理器
- **职责**：创建和管理 ChatOpenAI 实例（单例模式）
- **配置**：禁用代理、自动重试、超时控制、详细日志

#### shared/infrastructure/ai_service.py
- **功能**：AI 服务统一接口
- **方法**：
  - `generate_conversation_response(system_prompt, user_message, conversation_history)` - 生成对话回复
  - `generate_evaluation_report(conversation_text, evaluation_criteria)` - 生成评估报告
- **特点**：统一所有 AI 调用入口，方便监控和扩展

#### shared/infrastructure/event_bus.py
- **功能**：事件总线（发布-订阅模式）
- **事件类型**：
  - `CHAT_SESSION_ENDED` - 会话结束
  - `EVALUATION_GENERATED` - 评估生成完成

#### shared/infrastructure/skill_config.py
- **功能**：技能配置管理器（单例）
- **配置文件**：`config/skill_config.json`
- **职责**：读取和管理全局对话技能配置

### 2. 对话交互模块 (modules/chat/)

**API端点**：
- `POST /api/chat/sessions` - 创建会话
- `POST /api/chat/messages` - 发送消息并获取 AI 回复
- `PUT /api/chat/sessions/{id}/end` - 结束会话（触发评估）

**核心组件**：
- `services/conversation_engine.py` - 对话编排引擎
  - 通过 `AIService` 调用 LangChain 对话链
  - 通过 `EventBus` 发布会话结束事件
  - 集成技能配置到系统提示词

- `chains/conversation_chain.py` - 对话链
  - 使用 LCEL 构建：prompt | llm | StrOutputParser
  - 处理多轮对话历史

- `prompts/conversation_prompt.py` - 提示词模板
  - ChatPromptTemplate 模板
  - 支持系统提示、历史对话、用户消息

### 3. 评估系统模块 (modules/evaluation/)

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

- `prompts/evaluation_prompt.py` - 评估提示词
  - 包含 THP 评分标准
  - Pydantic 输出格式定义

### 4. 其他模块

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
        "tone_mapping": {
          "<30": "极度低落",
          "30-50": "焦虑",
          "50-70": "谨慎",
          ">70": "开放"
        }
      }
    },
    "system_prompt_template": "包含占位符的模板"
  }
}
```

### 占位符替换

`get_skill_prompt(current_state)` 方法会自动替换模板中的占位符：
- `{core_principles}` - 核心原则列表
- `{language_style}` - 语言风格
- `{emotional_response}` - 情绪响应
- `{rapport_building}` - 信任建立
- `{tone_mapping}` - 语气映射
- `{mood_score}`, `{satisfaction_score}`, `{depression_level}`, `{rapport_score}` - 当前状态值

### 触发条件

- **启用条件**：`enabled: true`
- **应用范围**：每次对话请求都会包含技能提示词
- **集成方式**：通过 `ConversationEngine` 添加到系统提示词

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

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入数据库和 AI 配置
```

### 3. 启动应用

```bash
# 方式1：使用启动脚本（推荐）
python start.py

# 方式2：直接使用 uvicorn
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问 API 文档

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
refactor(ai): 优化 AI 模块架构

- prompts 和 chains 移至各模块内部
- 简化 AIService 调用接口
- 修复技能配置加载路径
- 删除调试打印输出
```

---

## 测试

```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/modules/test_chat.py

# 查看测试覆盖率
pytest --cov=app --cov-report=html
```

---

## 故障排查

### 常见问题

1. **数据库连接失败**
   - 检查 `.env` 中的数据库配置
   - 确认数据库服务已启动

2. **AI 调用失败**
   - 检查 `AI_TEXT_KEY` 是否正确配置
   - 确认模型名称（`qwen-max` 或 `deepseek-v3.2`）
   - 检查网络连接

3. **模块导入错误**
   - 使用 `python start.py` 启动（自动设置 PYTHONPATH）
   - 或从项目根目录运行：`PYTHONPATH=E:/project/PANDA python backend/start.py`

4. **技能配置未加载**
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
| [THP 评估体系](../docs/THP.md) | 五维评分标准 |

---

## 更新日志

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
