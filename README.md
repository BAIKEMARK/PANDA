# 基于THP的围产期抑郁管理智能培训系统 (PANDA)

## 📋 项目简介

针对护理人员在围产期抑郁（PND）管理中规范化能力不足的问题，基于健康思维计划（THP）结合AI技术，研发智能培训系统。通过标准化操作流程与智能化培训方案，提升护理人员对PND的识别、沟通支持及初步干预能力。

**核心功能**：
- **内容学习模块**：基于THP框架的在线多媒体课程
- **虚拟情景模拟**：AI驱动的PND案例互动演练
- **Agent智能体系统**：动态患者状态模拟，实时响应护士沟通方式
- **实训考核模块**：理论与实践结合的综合性评估
- **能力评估系统**：THP五维评分（风险识别、沟通支持、技能应用、安全管理、自我效能）

## 🛠️ 技术栈

### 后端
- **框架**：FastAPI 0.109.0 + SQLAlchemy 2.0.25
- **数据库**：MySQL 8.0+ + Redis 5.0+
- **AI框架**：LangChain 1.2.7 + LangChain Core 1.2.7 + LangChain OpenAI 1.1.7
- **数据验证**：Pydantic 2.7+
- **LLM提供商**：阿里百炼（通义千问）/ DeepSeek
- **认证**：JWT
- **架构**：分层模块化架构 + Agent智能体系统

### 前端
- **框架**：React 18 + TypeScript 5
- **构建工具**：Vite 5
- **UI库**：Ant Design 5.x
- **状态管理**：Zustand
- **图表**：Recharts

## 🔧 环境要求

- **Python**: 3.12+
- **Node.js**: v20+
- **MySQL**: 8.0+
- **Redis**: 5.0+ (用于实时状态管理)

## 📦 部署方案

### 1. 克隆项目

```bash
git clone <repository-url>
cd PANDA
```

### 2. 数据库初始化

```bash
# 登录MySQL
mysql -u root -p

# 执行初始化脚本
source docs/项目文档/resources/panda.sql
```

### 3. 启动 Redis

```bash
# Windows
redis-server

# Linux/Mac
sudo service redis-server start
# 或
redis-server
```

### 4. 后端部署

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（已有 .env 文件可跳过）
# cp .env.example .env

# 启动服务
python start.py
```

### 5. 前端部署

```bash
cd frontend

# 安装依赖
npm install

# 开发环境
npm run dev

# 生产构建
npm run build
```

### 6. 环境变量配置

**后端** (`backend/.env`):
```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=panda

# Redis配置
REDIS_URL=redis://localhost:6379/0
REDIS_TTL_STATE=86400  # 状态24小时过期
REDIS_MAX_HISTORY=50   # 对话历史保留50轮

# AI模型配置 - 阿里百炼平台
# 获取地址: https://bailian.console.aliyun.com/
AI_TEXT_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_TEXT_KEY=your_ai_api_key
AI_TEXT_MODEL=qwen-max

# LLM 高级配置
LLM_MAX_RETRIES=3
LLM_TIMEOUT=120
LLM_TEMPERATURE=0.7
LLM_STREAMING=false

# CORS 配置
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=logs
LOG_FORMAT=text
LOG_TO_CONSOLE=True
LOG_MAX_BYTES_KB=1024
LOG_BACKUP_DAYS=30
```

**前端** (`frontend/.env`):
```bash
VITE_API_URL=http://localhost:8000/api
```

## 🚀 快速验证

启动后访问：
- **前端**：http://localhost:5173
- **API文档**：http://localhost:8000/api/docs
- **测试账号**：admin@panda.com / 123456

## 📂 项目结构

```
PANDA/
├── backend/                    # FastAPI后端
│   ├── app/
│   │   ├── main.py            # 应用入口
│   │   ├── core/              # 核心基础层
│   │   │   ├── config/        # 配置管理（settings, security, logging）
│   │   │   ├── ai/            # AI基础设施（langchain_manager）
│   │   │   ├── services/      # 基础服务（ai_service, event_bus, redis, skill_config）
│   │   │   └── common/        # 通用工具（constants, exceptions）
│   │   ├── interfaces/        # 模块间接口（依赖倒置）
│   │   ├── models/            # ORM模型
│   │   ├── schemas/           # Pydantic模型
│   │   ├── db/                # 数据库（Session, Base, 迁移脚本）
│   │   ├── api/               # 系统级端点（health check）
│   │   └── modules/           # 业务模块（分层模块化架构）
│   │       ├── auth/          # 认证与用户管理
│   │       ├── course/        # 课程管理
│   │       ├── scenario/      # 场景管理
│   │       ├── conversation/  # 对话模拟（统一业务域）
│   │       │   ├── api/       # API路由
│   │       │   ├── services/  # 业务服务
│   │       │   ├── repositories/ # 数据访问
│   │       │   ├── schemas/   # 数据模型
│   │       │   ├── chains/    # LangChain链
│   │       │   ├── prompts/   # 提示词模板
│   │       │   └── agent/     # Agent子系统
│   │       │       ├── config/    # 技能配置（skill_config.json）
│   │       │       ├── chains/    # Agent链
│   │       │       ├── core/      # Agent核心（orchestrator, state_engine, crisis_detector）
│   │       │       ├── models/    # 数据模型
│   │       │       ├── prompts/   # 提示词
│   │       │       ├── repositories/
│   │       │       └── services/
│   │       ├── evaluation/    # 评估系统
│   │       │   ├── agents/     # MentorAgent（事件驱动）
│   │       │   ├── chains/     # 评估链
│   │       │   └── prompts/    # 评估提示词
│   │       ├── progress/      # 学习进度
│   │       └── menu/          # 菜单管理
│   └── requirements.txt       # Python依赖
├── frontend/                   # React前端
│   ├── src/
│   │   ├── pages/            # 页面组件
│   │   ├── components/       # UI组件
│   │   │   ├── chat/        # 对话组件
│   │   │   ├── evaluation/  # 评估组件
│   │   │   ├── course/      # 课程组件
│   │   │   └── layout/      # 布局组件
│   │   ├── stores/          # Zustand状态管理
│   │   ├── services/        # API服务
│   │   └── router/          # 路由配置
│   └── package.json
├── docs/                      # 项目文档
│   ├── 项目介绍.md            # 项目背景和目标
│   ├── 开发规则.md            # 开发规范
│   ├── 管理端对接文档.md      # 管理端开发指南
│   ├── 后续开发任务清单.md    # 开发任务
│   └── 项目文档/              # 详细文档
│       └── resources/         # 资源文件
│           ├── 名词解释.md
│           ├── 后台管理需求.md
│           ├── 数据库设计.md
│           ├── 竞品分析.md
│           └── 系统功能设计.md
└── README.md                  # 项目说明
```

## 🏗️ 后端架构说明

### 核心基础层 (core/)

核心基础层包含整个项目共享的基础设施，是不可变的底层支撑：

```
core/
├── config/          # 配置管理
│   ├── settings.py      # 应用配置（从环境变量读取）
│   ├── security.py      # 安全配置（JWT、密码哈希）
│   └── logging.py       # 日志配置（按大小切割）
├── ai/              # AI基础设施
│   └── langchain_manager.py    # LLM统一管理器（单例）
├── services/        # 基础服务
│   ├── ai_service.py          # AI服务统一接口
│   ├── event_bus.py           # 事件总线（发布-订阅）
│   ├── redis_state_manager.py # Redis状态管理器
│   └── skill_config.py        # 技能配置加载器
└── common/          # 通用工具
    ├── constants.py           # 枚举常量
    └── exceptions.py          # 自定义异常
```

### 业务模块层 (modules/)

每个业务模块采用分层架构：

```
modules/{module_name}/
├── api/          # Controller层 - 处理HTTP请求
├── services/     # Service层 - 业务逻辑
├── repositories/ # Repository层 - 数据访问
└── schemas/      # DTO层 - Pydantic数据模型
```

### 对话模拟模块 (conversation/)

核心业务模块，整合了对话和Agent功能：

```
conversation/
├── api/                    # HTTP接口
│   └── routers.py          # /api/chat/* 端点
├── services/
│   ├── chat_service.py             # 对话服务
│   └── conversation_engine.py      # 对话编排引擎
├── agent/                  # Agent子系统
│   ├── config/
│   │   └── skill_config.json      # 患者行为规则
│   ├── core/
│   │   ├── agent_orchestrator.py  # Agent编排器
│   │   ├── state_update_engine.py # 状态更新引擎
│   │   └── crisis_detector.py     # 危机检测器
│   ├── chains/
│   │   ├── patient_agent_chain.py # 患者Agent链
│   │   └── state_update_chain.py  # 状态更新链
│   ├── prompts/
│   │   └── patient_agent_prompt.py
│   ├── services/
│   │   └── patient_state_service.py
│   └── repositories/
│       └── patient_state_repository.py
├── repositories/
│   └── chat_repository.py
└── schemas/
    └── chat.py
```

### 事件驱动架构

系统使用事件总线实现模块间解耦：

```
ChatService.end_session()
    ↓
EventBus.publish(CHAT_SESSION_ENDED)
    ↓
MentorAgent (订阅者)
    ↓
自动生成评估报告
```

## 🤖 Agent智能体系统

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                  Agent Orchestrator                      │
│                   (Agent 编排器)                          │
└───────────────────────────┬─────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Patient Agent │   │ State Update  │   │ Crisis Detector│
│    Chain      │   │    Chain      │   │   (规则检测)   │
└───────────────┘   └───────────────┘   └───────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                            ▼
                ┌─────────────────────────┐
                │   Patient State Service │
                │      (状态持久化)        │
                └───────────┬─────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
        ┌───────────────┐           ┌───────────────┐
        │     Redis     │           │    MySQL      │
        │  (实时缓存)    │           │ (持久化存储)   │
        └───────────────┘           └───────────────┘
```

### 患者状态模型

系统通过四维指标模拟患者状态：

| 指标 | 范围 | 说明 |
|------|------|------|
| `mood_score` | 0-100 | 心情指数，越高越积极 |
| `satisfaction_score` | 0-100 | 满意度，反映患者对沟通的满意程度 |
| `depression_level` | 0-100 | 抑郁程度，越高症状越严重 |
| `rapport_score` | 0-100 | 信任度，反映护患关系亲疏 |

### 技能配置系统

`skill_config.json` 定义患者行为规则：

- **角色定义**：患者角色设定
- **核心原则**：模拟行为准则
- **指标规则**：状态变化规则（护士共情 +10~15，说教 -10~-20）
- **危机阈值**：触发危机的临界值
- **危机响应**：危机发生时的患者反应

## 📚 文档

- [项目介绍](docs/项目介绍.md) - 项目背景和目标
- [开发规则](docs/开发规则.md) - 开发规范和最佳实践
- [数据库设计](docs/项目文档/resources/数据库设计.md) - 数据库设计和ER图
- [后端文档](backend/README.md) - 后端架构详细说明
- [管理端对接文档](docs/管理端对接文档.md) - 管理端开发交付指南
- [后续开发任务清单](docs/后续开发任务清单.md) - 后续开发任务

## 🗄️ 数据库迁移

项目使用增量迁移脚本管理数据库变更，位于 `backend/app/db/migrations/` 目录。

### 首次部署

```bash
# 1. 登录 MySQL 并创建数据库
mysql -u root -p
CREATE DATABASE panda CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE panda;

# 2. 执行主初始化脚本
SOURCE backend/app/db/panda.sql;

# 3. 执行增量迁移（如有）
SOURCE backend/app/db/migrations/add_video_url.sql;
```

### 迁移文件清单

| 文件名 | 说明 | 新增字段 |
|--------|------|----------|
| `add_suicide_risk_fields.sql` | 自杀风险检测 | `chat_sessions.has_suicide_risk`, `suicide_risk_alerted` |
| `add_video_url.sql` | 课程视频支持 | `courses.video_url` |

## 🔄 更新日志

### v0.4.0 (2025-02-05) - 架构重构版
- ✅ **目录结构重构**
  - `config/` → `core/config/`
  - `shared/` → 拆分到 `core/ai/`, `core/services/`, `core/common/`
  - `chat/` + `agent/` → 合并为 `conversation/`
  - `skill_config.json` → `conversation/agent/config/`
- ✅ **统一日志系统**
  - 按大小切割日志（1MB）
  - 文件命名：`app.YYYY-MM-DD_N.log`
  - 可配置保留天数
- ✅ **自杀风险集成评估**
  - 危机检测摘要注入评估提示词
  - A类风险识别评分受自杀倾向影响
- ✅ **代码清理**
  - 移除调试端点 `api/agent.py`
  - 更新所有导入路径

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
- ✅ 技能配置系统
- ✅ 事件总线集成

### v0.1.0 (2024-01-15)
- ✅ 基础框架搭建
- ✅ THP 五维评估体系
- ✅ 分层模块化架构

## 📄 许可证

本项目仅供学习和研究使用。