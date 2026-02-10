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
| **通义千问** | qwen-max | LLM 提供商（阿里百炼） |

### 架构设计原则

1. **按业务领域垂直切分**：每个业务域独立成一个完整模块
2. **保持分层架构**：每个模块内部保持 API → Service → Repository → Model
3. **依赖倒置**：模块间通过抽象接口通信，而非直接依赖具体实现
4. **共享基础设施**：core、db、common 作为独立的基础层
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
│   ├── core/                         # 共享核心层
│   │   ├── ai/                       # AI 基础设施
│   │   │   └── langchain_manager.py  # LLM 统一管理器（单例）
│   │   ├── common/                   # 通用模块
│   │   │   ├── constants.py          # 枚举常量
│   │   │   └── exceptions.py         # 自定义异常
│   │   ├── services/                 # 基础设施服务
│   │   │   ├── ai_service.py         # AI 服务统一接口
│   │   │   ├── event_bus.py          # 事件总线（模块间通信）
│   │   │   └── redis_state_manager.py # Redis 状态管理器
│   │   ├── config/                   # 配置管理
│   │   │   ├── settings.py           # 全局配置类
│   │   │   ├── security.py           # 安全相关配置
│   │   │   └── logging.py            # 日志配置
│   │   └── middleware/               # 中间件
│   │
│   ├── interfaces/                   # 模块间接口定义层
│   │   └── scenario_interface.py     # 场景模块对外接口
│   │
│   ├── modules/                      # 业务模块层（10个模块）
│   │   ├── auth/                     # 认证与用户管理
│   │   │   ├── api/                  # Controller 层
│   │   │   ├── services/             # Service 层
│   │   │   ├── repositories/         # Repository 层
│   │   │   └── schemas/              # DTO 层
│   │   │
│   │   ├── course/                   # 课程管理
│   │   ├── scenario/                 # 情景模拟
│   │   │
│   │   ├── conversation/             # 对话交互（含 Agent）
│   │   │   ├── api/                  # Controller 层
│   │   │   ├── services/             # Service 层
│   │   │   ├── repositories/         # Repository 层
│   │   │   ├── schemas/              # DTO 层
│   │   │   │
│   │   │   ├── agent/                # Agent 智能体子模块
│   │   │   │   ├── core/             # 核心组件
│   │   │   │   │   └── agent_orchestrator.py    # Agent 编排器
│   │   │   │   ├── chains/           # Agent 链
│   │   │   │   │   └── patient_agent_chain.py   # 患者 Agent 链
│   │   │   │   ├── prompts/          # Agent 提示词
│   │   │   │   │   └── patient_agent_prompt.py  # 患者 Agent 提示词
│   │   │   │   ├── services/         # Agent 服务层
│   │   │   │   ├── repositories/     # Agent 仓储层
│   │   │   │   ├── models/           # Agent 数据模型
│   │   │   │   └── config/           # Agent 配置
│   │   │   │       └── skill_config.json     # 技能配置文件
│   │   │   │
│   │   ├── evaluation/               # 评估系统
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
│   │   ├── progress/                 # 学习进度
│   │   ├── menu/                     # 菜单权限
│   │   ├── admin/                    # 后台管理
│   │   │   ├── api/                  # 组织、角色、用户、培训、文件管理
│   │   │   ├── services/
│   │   │   └── repositories/
│   │   ├── certificate/              # 证书管理
│   │   └── question/                 # 题库管理
│   │
│   ├── models/                       # ORM 模型层（共享）
│   │   ├── user.py                   # 用户模型
│   │   ├── course.py                 # 课程模型
│   │   ├── scenario.py               # 场景模型
│   │   ├── chat.py                   # 对话模型（ChatSession, ChatMessage）
│   │   ├── evaluation.py             # 评估模型
│   │   ├── patient_state.py          # 患者状态模型
│   │   ├── progress.py               # 进度模型
│   │   ├── organization.py           # 组织/角色/权限模型
│   │   ├── training.py               # 培训班级模型
│   │   ├── menu.py                   # 菜单模型
│   │   ├── certificate.py            # 证书模型
│   │   ├── question.py               # 题库模型
│   │   └── audit.py                  # 审计日志模型
│   │
│   ├── schemas/                      # Pydantic 模型层（共享）
│   ├── common/                       # 通用模块
│   └── db/                           # 数据库会话
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
core/ai/
└── langchain_manager.py       # LLM 统一管理（单例模式）

modules/conversation/agent/
├── prompts/
│   └── patient_agent_prompt.py # 患者 Agent 提示词
└── chains/
    └── patient_agent_chain.py  # 患者 Agent 链（LCEL）

modules/evaluation/
├── prompts/
│   └── evaluation_prompt.py    # 评估提示词（Pydantic 格式）
└── chains/
    └── evaluation_chain.py     # 评估链（结构化输出）

core/services/
├── ai_service.py              # AI 服务统一接口
├── event_bus.py               # 事件总线（发布-订阅）
└── redis_state_manager.py     # Redis 状态管理器

modules/conversation/agent/config/
└── skill_config.json          # 技能配置文件
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

#### 1. Agent Orchestrator

**职责**：协调所有 Agent 组件，处理每轮对话

**流程**：
1. 接收用户输入（护士消息）
2. 获取当前患者状态（从 Redis）
3. 调用 Patient Agent 生成回复
4. 调用 State Update Engine 计算状态变化
5. 检测是否触发危机
6. 更新 Redis 状态
7. 持久化到 MySQL

#### 2. Patient Agent Chain

**职责**：生成符合患者角色设定的回复

**特点**：
- 使用 LCEL 构建：prompt | llm | StrOutputParser
- Prompt 包含动态状态（心情、满意度、抑郁程度、信任度）
- 根据场景配置（system_prompt）和患者背景生成回复

#### 3. State Update Engine

**职责**：基于 skill_config.json 规则计算状态变化

**四项指标**：
- `mood_score` (心情指数): 0-100
- `satisfaction_score` (满意度): 0-100
- `depression_level` (抑郁程度): 0-100
- `rapport_score` (信任度): 0-100

#### 4. Crisis Detector

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

### Redis + MySQL 混合存储

| 操作 | Redis | MySQL |
|------|-------|-------|
| 读取状态 | ✅ 实时读取 (< 10ms) | - |
| 更新状态 | ✅ 立即更新 | ✅ 异步持久化 |
| 状态历史 | - | ✅ 每次变更记录 |
| 会话快照 | ✅ 快速恢复 | ✅ 长期存储 |

---

## 环境配置

### 环境变量 (.env)

```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=panda
DB_CHARSET=utf8mb4

# JWT认证配置
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI模型配置
AI_TEXT_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_TEXT_KEY=your_ai_api_key_here
AI_TEXT_MODEL=qwen-max
AI_TIMEOUT=30

# CORS配置
CORS_ORIGINS_STR=http://localhost:3000,http://localhost:5173

# Redis 配置
REDIS_URL=redis://localhost:6379/0
REDIS_TTL_STATE=86400
REDIS_MAX_HISTORY=50

# 日志配置
LOG_LEVEL=DEBUG
LOG_DIR=logs
LOG_FORMAT=text
LOG_TO_CONSOLE=True
LOG_MAX_BYTES_KB=1024
LOG_BACKUP_DAYS=30
```

---

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动 Redis (可选)

```bash
# Windows
redis-server

# Linux/Mac
sudo service redis-server start
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入数据库、Redis 和 AI 配置
```

### 4. 初始化数据库

```bash
mysql -u root -p panda < app/db/panda.sql
```

### 5. 启动应用

```bash
# 方式1：使用启动脚本（推荐）
python start.py

# 方式2：直接使用 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. 访问 API 文档

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## API 路由结构

### 系统路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/` | GET | 系统信息 |
| `/api/health` | GET | 健康检查 |

### 认证与用户

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/register` | POST | 用户注册 |
| `/api/login` | POST | 用户登录 |
| `/api/users/me` | GET | 获取当前用户 |
| `/api/users/me` | PUT | 更新当前用户 |

### 课程管理

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/courses` | GET | 课程列表 |
| `/api/courses` | POST | 创建课程 |
| `/api/courses/{id}` | GET | 课程详情 |
| `/api/courses/{id}` | PUT | 更新课程 |
| `/api/courses/{id}` | DELETE | 删除课程 |

### 场景管理

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/scenarios` | GET | 场景列表 |
| `/api/scenarios` | POST | 创建场景 |
| `/api/scenarios/{id}` | GET | 场景详情 |
| `/api/scenarios/{id}` | PUT | 更新场景 |
| `/api/scenarios/{id}` | DELETE | 删除场景 |

### 对话交互

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/chat/sessions` | POST | 创建会话 |
| `/api/chat/sessions/{id}` | GET | 获取会话 |
| `/api/chat/sessions/{id}/messages` | GET | 获取消息列表 |
| `/api/chat/messages` | POST | 发送消息 |
| `/api/chat/sessions/{id}/end` | PUT | 结束会话 |
| `/api/chat/sessions/{id}/alert` | POST | 自杀风险报警 |

### 评估系统

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/evaluation/sessions/{id}/evaluate` | POST | 生成评估报告 |
| `/api/evaluation/sessions/{id}/status` | GET | 获取评估状态 |
| `/api/evaluation/sessions/{id}/report` | GET | 获取评估报告 |
| `/api/evaluation/reports` | GET | 报告列表 |

### 学习进度

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/progress/dashboard` | GET | 学习仪表板 |
| `/api/progress` | GET | 学习进度列表 |
| `/api/progress` | POST | 记录学习进度 |

### 菜单权限

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/menus` | GET | 菜单列表 |
| `/api/menus/user` | GET | 用户菜单（动态） |
| `/api/menus` | POST | 创建菜单 |
| `/api/menus/{id}` | PUT | 更新菜单 |
| `/api/menus/{id}` | DELETE | 删除菜单 |

### 后台管理

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/admin/organizations` | GET/POST | 机构管理 |
| `/api/admin/roles` | GET/POST | 角色管理 |
| `/api/admin/users` | GET/POST | 用户管理 |
| `/api/admin/classes` | GET/POST | 班级管理 |
| `/api/admin/certificates` | GET/POST | 证书管理 |
| `/api/admin/questions` | GET/POST | 题库管理 |

---

## 开发指南

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
   - 确认模型名称（`qwen-max`）
   - 检查网络连接

4. **模块导入错误**
   - 使用 `python start.py` 启动（自动设置 PYTHONPATH）

---

## 更新日志

### v0.4.0 (2026-02-05)
- ✅ 架构重构：优化项目结构
  - 重构 `shared/` 目录为 `core/`
  - 合并 `chat/` 和 `agent/` 模块为 `conversation/`
  - 将 `skill_config.json` 移至模块内部

### v0.3.0 (2026-01-31)
- ✅ 升级 LangChain 到 1.2.7
- ✅ 升级 Pydantic 到 2.7+
- ✅ 实现 Agent 智能体系统
- ✅ 集成 Redis 实时状态管理

### v0.2.0 (2024-01-29)
- ✅ 重构 AI 模块架构
- ✅ 修复技能配置加载路径
- ✅ 简化 AIService 调用接口

### v0.1.0 (2024-01-15)
- ✅ 迁移到 LangChain 框架
- ✅ 实现分层模块化架构
- ✅ 集成事件总线

---

## 许可证

Copyright © 2026 PANDA Team. All rights reserved.