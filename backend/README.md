# PANDA 后端

基于 **FastAPI** + **LangChain** 的 AI 智能培训系统后端服务。

## 技术栈

| 技术 | 说明 |
|------|------|
| FastAPI | 异步 Web 框架 |
| LangChain | LLM 应用开发 |
| SQLAlchemy | ORM 数据库操作 |
| Redis | 实时状态缓存 |
| 通义千问 | LLM 服务 |

## 项目结构

```
backend/app/
├── main.py              # 应用入口
├── core/                # 核心基础设施
│   ├── ai/             # AI 管理器
│   ├── services/       # 基础服务
│   └── config/         # 配置管理
└── modules/            # 业务模块
    ├── auth/           # 认证管理
    ├── course/         # 课程管理
    ├── conversation/   # 对话 + Agent
    └── evaluation/     # 评估系统
```

## 核心模块

### AI 智能体系统
- **Patient Agent** - 患者模拟，动态对话生成
- **Mentor Agent** - 导师评估，THP 五维能力分析
- **State Engine** - 实时状态更新（Redis）
- **Crisis Detector** - 危机风险检测

### 评估系统
- THP 五维能力评估
- LangChain 评估链
- 自动生成评估报告

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env

# 启动服务
python start.py
```

访问 http://localhost:8000/api/docs

## 环境变量

```bash
# 数据库
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=panda

# JWT
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI 模型
AI_TEXT_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AI_TEXT_KEY=sk-your-api-key
AI_TEXT_MODEL=qwen-max

# Redis
REDIS_URL=redis://localhost:6379/0
```

## API 端点

| 模块 | 端点 |
|------|------|
| 认证 | `POST /api/auth/login` |
| 对话 | `POST /api/chat/messages` |
| 评估 | `GET /api/evaluation/sessions/{id}/report` |

完整文档：http://localhost:8000/api/docs

## 开发指南

详见 [开发规则](../docs/开发规则.md)

## 相关文档

- [架构设计](../docs/架构设计.md) - 系统架构详解
- [数据库设计](../docs/项目文档/resources/数据库设计.md) - 数据表结构