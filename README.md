# PANDA - 围产期抑郁管理智能培训系统

基于 **THP (Timely Care for Perinatal Depression)** 理论框架，结合 **AI Agent 智能体**技术的护理人员智能培训系统。

---

## 项目简介

针对护理人员在围产期抑郁（PND）管理中规范化能力不足的问题，通过标准化操作流程与智能化培训方案，提升护理人员对 PND 的识别、沟通支持及初步干预能力。

### 核心功能

| 功能 | 说明 |
|------|------|
| **内容学习** | 基于 THP 框架的在线多媒体课程（L1-L4 分层） |
| **虚拟情景模拟** | AI 驱动的 PND 案例互动演练 |
| **Agent 智能体系统** | 动态患者状态模拟，实时响应护士沟通方式 |
| **智能评估** | THP 五维能力评估（风险识别、沟通支持、技能应用、安全管理、自我效能） |
| **后台管理** | 用户、机构、班级、角色、题库、证书管理 |

### 技术亮点

- **LangChain 1.x** - LLM 应用开发框架
- **Agent 编排器** - 统一管理多个智能体
- **Redis + MySQL** - 实时状态缓存 + 持久化
- **事件驱动架构** - 模块间解耦通信
- **动态患者状态** - 四项指标实时更新
- **自杀风险检测** - 实时监测和报警机制

---

## 技术栈

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| **FastAPI** | 0.109.0 | 现代异步 Web 框架 |
| **SQLAlchemy** | 2.0.25 | ORM 数据库操作 |
| **Pydantic** | 2.7+ | 数据验证和结构化输出 |
| **LangChain** | 1.2.7 | LLM 应用开发框架 |
| **Redis** | 5.0.1 | 实时状态缓存 |
| **通义千问** | qwen-max | LLM 提供商（阿里百炼） |

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| **React** | 19.2.0 | UI 框架 |
| **TypeScript** | 5.9.3 | 类型安全 |
| **Vite** | 7.2.4 | 构建工具 |
| **Ant Design** | 6.2.0 | 企业级 UI 组件库 |
| **Tailwind CSS** | 4.1.18 | 原子化 CSS 框架 |
| **Zustand** | 5.0.10 | 轻量级状态管理 |
| **Recharts** | 3.6.0 | 数据可视化（雷达图） |

---

## 快速开始

### 环境要求

- **Python**: 3.12+
- **Node.js**: v20+
- **MySQL**: 8.0+
- **Redis**: 5.0+ (可选)

### 一、数据库初始化

```bash
mysql -u root -p
CREATE DATABASE panda CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE panda;
SOURCE backend/app/db/panda.sql;
```

### 二、后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入数据库和 AI 配置

# 启动服务
python start.py
```

访问：http://localhost:8000/api/docs

### 三、前端启动

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env

# 启动服务
npm run dev
```

访问：http://localhost:5173

### 四、测试账号

| 角色 | 邮箱 | 密码 |
|------|------|------|
| 管理员 | admin@panda.com | admin123 |
| 讲师 | teacher@panda.com | admin123 |
| 学员 | nurse1@hospital.com | admin123 |

---

## 项目结构

```
PANDA/
├── backend/                          # 后端服务
│   ├── app/
│   │   ├── main.py                   # 应用入口
│   │   ├── core/                     # 核心基础层
│   │   │   ├── ai/                   # AI 基础设施
│   │   │   ├── services/             # 基础服务（AI、事件总线、Redis）
│   │   │   ├── config/               # 配置管理
│   │   │   ├── common/               # 通用工具
│   │   │   └── middleware/           # 中间件
│   │   ├── modules/                  # 业务模块层
│   │   │   ├── auth/                 # 认证与用户管理
│   │   │   ├── course/               # 课程管理
│   │   │   ├── scenario/             # 场景管理
│   │   │   ├── conversation/         # 对话交互 + Agent
│   │   │   ├── evaluation/           # 评估系统
│   │   │   ├── progress/             # 学习进度
│   │   │   ├── menu/                 # 菜单权限
│   │   │   ├── admin/                # 后台管理
│   │   │   ├── certificate/          # 证书管理
│   │   │   └── question/             # 题库管理
│   │   ├── models/                   # SQLAlchemy ORM 模型
│   │   ├── schemas/                  # Pydantic 数据模型
│   │   └── db/                       # 数据库会话
│   ├── requirements.txt              # Python 依赖
│   └── start.py                      # 启动脚本
│
├── frontend/                         # 前端应用
│   ├── src/
│   │   ├── pages/                    # 页面组件
│   │   ├── components/               # UI 组件
│   │   ├── services/                 # API 服务层
│   │   ├── stores/                   # Zustand 状态管理
│   │   ├── types/                    # TypeScript 类型
│   │   ├── router/                   # 路由配置
│   │   └── main.tsx                  # 应用入口
│   └── package.json                  # Node 依赖
│
├── docs/                             # 项目文档
│   ├── 项目介绍.md
│   ├── 开发规则.md
│   └── 项目文档/
│
├── quick_start.bat                   # Windows 快速启动
├── quick_start.sh                    # Linux/Mac 快速启动
└── README.md                         # 本文件
```

---

## 核心业务模块

### 1. Agent 智能体系统

```
┌─────────────────────────────────────────┐
│         Agent Orchestrator (编排器)      │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Patient  │ │  State   │ │  Crisis      │
│  Agent   │ │  Engine  │ │  Detector    │
│ (患者回复)│ │(状态更新) │ │  (危机检测)  │
└──────────┘ └──────────┘ └──────────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
              ┌──────────────┐
              │   Redis      │
              │  状态缓存    │
              └──────────────┘
```

**四项动态指标**：
- `mood_score` - 心情指数 (0-100)
- `satisfaction_score` - 满意度 (0-100)
- `depression_level` - 抑郁程度 (0-100)
- `rapport_score` - 信任度 (0-100)

### 2. THP 五维评估系统

- **A 类** - 风险识别能力
- **B 类** - 沟通支持能力
- **C 类** - THP 技能应用
- **D 类** - 安全管理能力
- **E 类** - 自我效能感

### 3. 业务模块清单

| 模块 | 功能 |
|------|------|
| `auth` | 用户注册/登录、JWT 认证 |
| `course` | THP 分层课程管理 (L1-L4) |
| `scenario` | 情景模拟训练场景 |
| `conversation` | AI 对话交互、Agent 智能体 |
| `evaluation` | THP 五维评估、AI 报告生成 |
| `progress` | 学习进度跟踪 |
| `menu` | 动态菜单权限管理 |
| `admin` | 后台管理（用户/机构/班级/角色） |
| `certificate` | 证书管理 |
| `question` | 题库管理 |

---

## 环境配置

### 后端环境变量 (`backend/.env`)

```bash
# 数据库
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=panda
DB_CHARSET=utf8mb4

# JWT 认证
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI 模型 - 阿里百炼平台
AI_TEXT_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_TEXT_KEY=sk-your-api-key
AI_TEXT_MODEL=qwen-max

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# CORS
CORS_ORIGINS_STR=http://localhost:5173
```

### 前端环境变量 (`frontend/.env`)

```bash
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=PANDA
VITE_ENABLE_STREAMING=true
```

---

## 文档

| 文档 | 说明 |
|------|------|
| [项目介绍](docs/项目介绍.md) | 项目背景和目标 |
| [开发规则](docs/开发规则.md) | 6A 工作流和开发规范 |
| [后端文档](backend/README.md) | 后端架构、AI 模块、开发指南 |
| [前端文档](frontend/README.md) | 前端架构、组件库、开发规范 |

---

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

## 许可证

本项目仅供学习和研究使用。

Copyright © 2026 PANDA Team. All rights reserved.