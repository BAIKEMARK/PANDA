# PANDA - 围产期抑郁管理智能培训系统

> 基于 THP (Timely Care for Perinatal Depression) 理论的 AI 智能培训系统

## 简介

PANDA 是一套针对护理人员围产期抑郁管理能力的智能化培训系统，通过 AI 驱动的虚拟情景模拟和智能评估，提升护理人员的识别、沟通和干预能力。

### 核心功能

- 📚 **在线课程学习** - 基于 THP 框架的多媒体课程
- 🎭 **AI 情景模拟** - 动态患者 Agent，真实对话演练
- 📊 **智能评估报告** - THP 五维能力评估与反馈
- 🎯 **危机检测系统** - 实时监测自杀风险倾向

## 技术栈

| 类别 | 技术 |
|------|------|
| 后端 | FastAPI + LangChain + MySQL + Redis |
| 前端 | React 19 + TypeScript + Ant Design + Vite |
| AI | 通义千问 (阿里百炼) |

## 快速开始

### 环境要求

- Python 3.12+
- Node.js 20+
- MySQL 8.0+
- Redis 5.0+

### 安装运行

```bash
# 1. 克隆项目
git clone https://github.com/BAIKEMARK/PANDA.git
cd PANDA

# 2. 初始化数据库
mysql -u root -p
CREATE DATABASE panda CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE panda;
SOURCE backend/app/db/panda.sql;

# 3. 启动后端
cd backend
pip install -r requirements.txt
python start.py

# 4. 启动前端
cd frontend
npm install
npm run dev
```

### 访问地址

- 🌐 前端: http://localhost:5173
- 📖 API文档: http://localhost:8000/api/docs
- 👤 测试账号: admin@panda.com / 123456

## 项目结构

```
PANDA/
├── backend/           # FastAPI 后端
│   └── app/
│       ├── core/      # 核心基础设施
│       └── modules/   # 业务模块
├── frontend/          # React 前端
│   └── src/
│       ├── components/  # 可复用组件
│       ├── pages/       # 页面组件
│       └── stores/      # 状态管理
└── docs/              # 项目文档
```

## 文档

- [项目介绍](docs/项目介绍.md) - 项目背景和目标
- [后端文档](backend/README.md) - 后端架构详细说明
- [前端文档](frontend/README.md) - 前端架构详细说明
- [开发规则](docs/开发规则.md) - 开发规范

## 版本历史

- **v0.4.0** (2026-02-05) - 核心架构重构，对话模块统一
- **v0.3.0** (2026-01-31) - Agent 智能体系统实现
- **v0.2.0** (2024-01-29) - AI 模块架构重构
- **v0.1.0** (2024-01-15) - 基础框架搭建

## 许可证

本项目仅供学习和研究使用。