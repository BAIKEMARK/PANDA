# PANDA 后端项目

**围产期抑郁管理智能培训系统 - FastAPI 后端服务**

基于 **FastAPI** + **LangChain** 构建的 AI 驱动智能培训系统，集成 **Agent 智能体**和 **Redis** 实时状态管理。

---

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| **FastAPI** | 0.109.0 | 现代异步 Web 框架 |
| **SQLAlchemy** | 2.0.25 | ORM 数据库操作 |
| **LangChain** | 1.2.7 | LLM 应用开发框架 |
| **Pydantic** | 2.7+ | 数据验证和结构化输出 |
| **Redis** | 5.0+ | 实时状态缓存 |
| **通义千问** | - | LLM 提供商 |

---

## 项目架构

### 架构原则

1. **分层模块化**：API → Service → Repository → Model
2. **依赖倒置**：模块间通过抽象接口通信
3. **事件驱动**：通过事件总线实现模块解耦
4. **LangChain 集成**：AI 能力统一管理和调用

### 目录结构

```
backend/app/
├── main.py                     # 应用入口
├── core/                       # 核心基础设施
│   ├── ai/                    # AI 统一管理器
│   ├── services/              # 基础服务（AI/事件/Redis）
│   ├── common/                # 通用模块
│   └── config/                # 配置管理
├── modules/                   # 业务模块
│   ├── auth/                  # 认证与用户管理
│   ├── course/                # 课程管理
│   ├── scenario/              # 情景模拟
│   ├── conversation/          # 对话交互 + Agent
│   ├── evaluation/            # 评估系统
│   ├── progress/              # 学习进度
│   ├── menu/                  # 菜单权限
│   └── admin/                 # 后台管理
├── models/                    # ORM 模型
├── schemas/                   # Pydantic 模型
└── db/                        # 数据库配置
```

---

## 核心模块

### 1. Agent 智能体系统

**路径**: `modules/conversation/agent/`

#### 组件架构

```
AgentOrchestrator (编排器)
    ├── PatientAgentChain    # 患者 Agent 链
    ├── StateUpdateEngine    # 状态更新引擎
    └── CrisisDetector       # 危机检测器
```

#### 患者状态模型

- `mood_score` - 心情指数 (0-100)
- `satisfaction_score` - 满意度 (0-100)
- `depression_level` - 抑郁程度 (0-100)
- `rapport_score` - 信任度 (0-100)

#### 技能配置

**文件**: `modules/conversation/agent/config/skill_config.json`

定义了全局对话行为准则和状态更新规则。

### 2. 评估系统

**路径**: `modules/evaluation/`

#### THP 五维评估

- A. 风险识别能力
- B. 沟通支持能力
- C. 技能应用能力
- D. 安全管理能力
- E. 自我效能感

#### 评估流程

1. 会话结束触发评估
2. 收集对话历史和状态数据
3. 通过 LangChain 评估链生成报告
4. 保存评估结果到数据库

### 3. Redis 状态管理

**管理器**: `core/services/redis_state_manager.py`

#### 数据结构

```
patient:state:{session_id}    # 实时状态 (Hash, TTL: 24h)
patient:history:{session_id}  # 对话历史 (List, Max: 50轮)
```

---

## API 端点

### 认证模块
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 对话模块
- `POST /api/chat/sessions` - 创建会话
- `POST /api/chat/messages` - 发送消息
- `PUT /api/chat/sessions/{id}/end` - 结束会话

### 评估模块
- `GET /api/evaluation/sessions/{id}/report` - 获取评估报告

详细 API 文档：http://localhost:8000/api/docs

---

## 环境配置

### 环境变量 (.env)

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
AI_TEXT_KEY=your_api_key
AI_TEXT_MODEL=qwen-max

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=http://localhost:5173
```

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
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件
```

### 4. 初始化数据库

```bash
mysql -u root -p panda < docs/项目文档/resources/panda.sql
```

### 5. 启动应用

```bash
python start.py
```

---

## 开发指南

### 代码规范

1. **模块结构**: `api/services/repositories/schemas`
2. **导入顺序**: 标准库 → 第三方库 → 本地模块
3. **命名规范**:
   - 类名：`PascalCase`
   - 函数/变量：`snake_case`
   - 常量：`UPPER_SNAKE_CASE`

### 添加新模块

```bash
modules/
└── your_module/
    ├── api/routers.py       # 路由定义
    ├── services/            # 业务逻辑
    ├── repositories/        # 数据访问
    └── schemas/             # 数据模型
```

### Git 提交规范

```
feat(scope): 新功能
fix(scope): 修复 bug
refactor(scope): 重构
docs: 文档更新
chore: 构建/工具相关
```

---

## 故障排查

### 常见问题

| 问题 | 解决方案 |
|------|---------|
| 数据库连接失败 | 检查 `.env` 中的数据库配置 |
| Redis 连接失败 | 运行 `redis-cli ping` 检查服务 |
| AI 调用失败 | 检查 `AI_TEXT_KEY` 是否正确 |
| 模块导入错误 | 使用 `python start.py` 启动 |

---

## 更新日志

### v0.4.0 (2026-02-05)
- ✅ 核心架构重构 (`core/` 目录优化)
- ✅ 对话模块统一 (`conversation/` 合并 chat + agent)
- ✅ 统一日志系统

### v0.3.0 (2026-01-31)
- ✅ Agent 智能体系统实现
- ✅ Redis 实时状态管理
- ✅ 动态患者状态更新

---

## 许可证

Copyright © 2026 PANDA Team. All rights reserved.