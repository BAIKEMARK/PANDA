# 基于THP的围产期抑郁管理智能培训系统 (PANDA)

## 📋 项目简介

针对护理人员在围产期抑郁（PND）管理中规范化能力不足的问题，基于健康思维计划（THP）结合AI技术，研发智能培训系统。通过标准化操作流程与智能化培训方案，提升护理人员对PND的识别、沟通支持及初步干预能力。

**核心功能**：
- **内容学习模块**：基于THP框架的在线多媒体课程
- **虚拟情景模拟**：AI驱动的PND案例互动演练
- **实训考核模块**：理论与实践结合的综合性评估
- **能力评估系统**：THP五维评分（风险识别、沟通支持、技能应用、安全管理、自我效能）

## 🛠️ 技术栈

### 后端
- **框架**：FastAPI + SQLAlchemy 2.0
- **数据库**：MySQL 8.0+
- **AI框架**：LangChain + LangChain Core
- **LLM提供商**：阿里百炼（通义千问）
- **认证**：JWT
- **架构**：分层模块化架构

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
source backend/database/schema.sql
```

### 3. 后端部署

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，配置数据库密码和AI密钥

# 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. 前端部署

```bash
cd frontend

# 安装依赖
npm install

# 开发环境
npm run dev

# 生产构建
npm run build
```

### 5. 环境变量配置

**后端** (`backend/.env`):
```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=panda

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
│   │   │   ├── evaluation/# 评估系统
│   │   │   ├── progress/ # 学习进度
│   │   │   └── menu/     # 菜单管理
│   │   ├── shared/       # 共享基础设施
│   │   │   ├── core/     # LangChain核心
│   │   │   ├── db/       # 数据库
│   │   │   ├── common/   # 通用工具
│   │   │   └── infrastructure/ # 基础服务
│   │   ├── models/       # ORM模型
│   │   ├── schemas/      # Pydantic模型
│   │   ├── api/          # API路由
│   │   ├── core/         # 核心配置
│   │   ├── db/           # 数据库配置
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
│   └── 开发规则.md       # 开发规范
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

### 共享基础设施 (shared/)

- **core/**: LangChain核心组件
  - `langchain_manager.py`: LLM统一管理（单例模式）
  - `chains/`: 对话链和评估链（LCEL）
  - `prompts/`: 提示词模板

- **infrastructure/**: 基础服务
  - `ai_service.py`: AI服务统一接口
  - `event_bus.py`: 事件总线（发布/订阅）
  - `skill_config.py`: 技能配置管理

### AI模块技术栈

- **LangChain**: LLM应用开发框架
- **LCEL (LangChain Expression Language)**: 声明式链组合
- **Pydantic Output Parser**: 结构化输出
- **事件驱动架构**: 模块间解耦通信

## 🤖 AI配置说明

### LangChain配置

系统使用LangChain框架统一管理AI调用，支持：

- **对话生成**: 使用 `ConversationChain` 处理多轮对话
- **评估报告**: 使用 `EvaluationChain` 生成结构化评估
- **自动重试**: 内置指数退避重试机制
- **错误处理**: 统一的异常处理和降级策略

### 模型配置

- **主模型**: `qwen-max`（通义千问最强模型）
- **超时时间**: 120秒
- **重试次数**: 3次
- **温度参数**: 0.7（平衡创造性和准确性）

## 📚 文档

- [THP框架说明](docs/THP.md) - THP五维评分体系详解
- [项目介绍](docs/项目介绍.md) - 项目背景和目标
- [开发规则](docs/开发规则.md) - 开发规范和最佳实践

## 📄 许可证

本项目仅供学习和研究使用。
