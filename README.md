# PANDA - 围产期抑郁管理智能培训系统

基于 THP (Timely Care for Perinatal Depression) 理论框架，结合 AI 技术的护理人员智能培训系统。

## 项目简介

针对护理人员在围产期抑郁（PND）管理中规范化能力不足的问题，通过标准化操作流程与智能化培训方案，提升护理人员对 PND 的识别、沟通支持及初步干预能力。

**核心功能**：
- **内容学习**：基于 THP 框架的在线多媒体课程
- **虚拟情景模拟**：AI 驱动的 PND 案例互动演练
- **Agent 智能体系统**：动态患者状态模拟，实时响应护士沟通方式
- **智能评估**：THP 五维能力评估（风险识别、沟通支持、技能应用、安全管理、自我效能）

## 技术栈

### 后端
- **框架**：FastAPI 0.109.0 + SQLAlchemy 2.0.25
- **数据库**：MySQL 8.0+ + Redis 5.0+
- **AI 框架**：LangChain 1.2.7
- **LLM 提供商**：阿里百炼
- **认证**：JWT

### 前端
- **框架**：React 19 + TypeScript 5
- **构建工具**：Vite 5
- **UI 库**：Ant Design 5.x
- **状态管理**：Zustand

## 环境要求

- **Python**: 3.12+
- **Node.js**: v20+
- **MySQL**: 8.0+
- **Redis**: 5.0+

## 部署方案

### 1. 克隆项目

```bash
git clone https://github.com/BAIKEMARK/PANDA.git
cd PANDA
```

### 2. 数据库初始化

```bash
mysql -u root -p
CREATE DATABASE panda CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE panda;
SOURCE backend/app/db/panda.sql;
```

### 3. 启动 Redis

```bash
# Windows
redis-server

# Linux/Mac
sudo service redis-server start
```

### 4. 后端部署

```bash
cd backend
pip install -r requirements.txt
python start.py
```

### 5. 前端部署

```bash
cd frontend
npm install
npm run dev
```

### 6. 环境变量配置

**后端** (`backend/.env`):
```bash
# 数据库
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/panda

# Redis
REDIS_URL=redis://localhost:6379/0

# AI 模型 - 阿里百炼平台
AI_TEXT_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_TEXT_KEY=your_api_key
AI_TEXT_MODEL=qwen-max

# JWT
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:5173
```

**前端** (`frontend/.env`):
```bash
VITE_API_URL=http://localhost:8000/api
```

## 快速验证

启动后访问：
- **前端**：http://localhost:5173
- **API 文档**：http://localhost:8000/api/docs
- **测试账号**：admin@panda.com / 123456

## 文档

- [项目介绍](docs/项目介绍.md) - 项目背景和目标
- [开发规则](docs/开发规则.md) - 开发规范和最佳实践
- [后端文档](backend/README.md) - 后端架构详细说明
- [前端文档](frontend/README.md) - 前端架构详细说明
- [管理端对接文档](docs/管理端对接文档.md) - 管理端开发交付指南
- [后续开发任务清单](docs/后续开发任务清单.md) - 开发任务规划

## 更新日志

### v0.4.0 (2026-02-05)
- ✅ 核心基础层重构 (`core/config/`, `core/ai/`, `core/services/`, `core/common/`)
- ✅ 对话模块统一 (`conversation/` 合并 chat + agent)
- ✅ 统一日志系统（按大小切割，1MB/文件）
- ✅ 自杀风险检测集成评估系统

### v0.3.0 (2026-01-31)
- ✅ Agent 智能体系统实现
- ✅ Redis 实时状态管理
- ✅ 动态患者状态更新（四项指标）

### v0.2.0 (2024-01-29)
- ✅ AI 模块架构重构
- ✅ 技能配置系统
- ✅ 事件总线集成

### v0.1.0 (2024-01-15)
- ✅ 基础框架搭建
- ✅ THP 五维评估体系

---

**许可证**：本项目仅供学习和研究使用。