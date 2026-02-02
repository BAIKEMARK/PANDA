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

# 配置环境变量
cp .env.example .env
# 编辑 .env，配置数据库密码、Redis和AI密钥

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
├── backend/              # FastAPI后端
│   ├── app/
│   │   ├── modules/      # 业务模块（分层模块化架构）
│   │   │   ├── auth/     # 认证与用户
│   │   │   ├── course/   # 课程管理
│   │   │   ├── scenario/ # 情景模拟
│   │   │   ├── chat/     # 对话交互
│   │   │   ├── agent/    # Agent智能体系统
│   │   │   │   ├── core/ # 核心组件
│   │   │   │   │   ├── agent_orchestrator.py    # Agent编排器
│   │   │   │   │   ├── state_update_engine.py   # 状态更新引擎
│   │   │   │   │   └── crisis_detector.py       # 危机检测器
│   │   │   │   ├── chains/     # Agent链
│   │   │   │   ├── prompts/    # Agent提示词
│   │   │   │   ├── services/   # 状态服务
│   │   │   │   └── repositories/# 状态仓储
│   │   │   ├── evaluation/# 评估系统
│   │   │   ├── progress/ # 学习进度
│   │   │   └── menu/     # 菜单管理
│   │   ├── shared/       # 共享基础设施
│   │   │   ├── ai/       # LangChain核心
│   │   │   ├── db/       # 数据库
│   │   │   ├── common/   # 通用工具
│   │   │   └── infrastructure/ # 基础服务
│   │   │       └── redis_state_manager.py # Redis状态管理
│   │   ├── config/       # 配置层
│   │   │   └── skill_config.json # 技能配置
│   │   ├── interfaces/   # 模块间接口
│   │   ├── models/       # ORM模型
│   │   ├── schemas/      # Pydantic模型
│   │   └── main.py       # 应用入口
│   └── requirements.txt  # Python依赖
├── frontend/             # React前端
│   └── src/
│       ├── pages/        # 页面组件
│       ├── components/   # UI组件
│       └── services/     # API调用
├── docs/                 # 项目文档
│   ├── THP.md           # THP框架说明
│   ├── 项目介绍.md       # 项目详细介绍
│   ├── 开发规则.md       # 开发规范
│   └── 项目文档/         # 详细文档
│       └── resources/    # 资源文件
│           ├── 数据库设计.md  # 数据库设计
│           └── panda.sql     # SQL脚本
└── README.md             # 项目说明
```

## 🏗️ 后端架构说明

### 分层模块化架构

项目采用**分层模块化架构**，每个业务模块包含完整的层次结构：

```
modules/{module_name}/
├── api/          # API路由层
├── schemas/      # 数据模型层
├── services/     # 业务逻辑层
└── repositories/ # 数据访问层
```

## 📚 文档

- [项目介绍](docs/项目介绍.md) - 项目背景和目标
- [开发规则](docs/开发规则.md) - 开发规范和最佳实践
- [数据库设计](docs/项目文档/resources/数据库设计.md) - 数据库设计和ER图
- [后端文档](backend/README.md) - 后端架构详细说明
- [AI模块架构](docs/ai_module_architecture.md) - LangChain集成详细文档
- [后续开发任务清单](docs/后续开发任务清单.md) - 后续开发任务

## 🔄 更新日志

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