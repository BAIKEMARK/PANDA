# PANDA 后端项目

**围产期抑郁管理智能培训系统 - FastAPI 后端服务**

## 项目架构

本项目采用**分层模块化架构**，按业务领域垂直划分模块，通过事件总线实现模块间解耦通信。

### 架构设计原则

1. **按业务领域垂直切分**：每个业务域独立成一个完整模块
2. **保持分层架构**：每个模块内部保持 Controller → Service → Repository → Model
3. **依赖倒置**：模块间通过抽象接口通信，而非直接依赖具体实现
4. **共享基础设施**：core、db、common、infrastructure 作为独立的基础层
5. **单向依赖**：业务模块只能依赖共享层，不能横向依赖其他业务模块

## 项目结构

```
backend/
├── app/                              # 应用主目录
│   ├── main.py                       # 应用入口
│   │
│   ├── shared/                       # 共享基础设施层
│   │   ├── __init__.py
│   │   ├── core/                     # 核心配置
│   │   │   ├── config.py             # 配置管理
│   │   │   ├── security.py           # JWT、密码加密
│   │   │   ├── proxy.py              # 代理配置
│   │   │   └── skill_config.json     # 技能配置文件
│   │   ├── db/                       # 数据库基础设施
│   │   │   ├── database.py           # Session管理、Base
│   │   │   └── init_db.py            # 初始化脚本
│   │   ├── common/                   # 通用模块
│   │   │   ├── constants.py          # 枚举常量
│   │   │   └── exceptions.py         # 自定义异常
│   │   ├── infrastructure/           # 基础设施服务
│   │   │   ├── ai_service.py         # AI服务统一接口
│   │   │   ├── skill_config.py       # 技能配置管理（单例）
│   │   │   └── event_bus.py          # 事件总线（模块间通信）
│   │   └── models/                   # ORM模型引用
│   │
│   ├── interfaces/                   # 模块间接口定义层
│   │   ├── __init__.py
│   │   └── scenario_interface.py     # 场景模块对外接口
│   │
│   ├── modules/                      # 业务模块层
│   │   │
│   │   ├── auth/                     # 模块1: 认证与用户管理
│   │   │   ├── __init__.py
│   │   │   ├── api/                  # Controller层
│   │   │   │   └── routers.py        # /api/auth/*, /api/users/*
│   │   │   ├── services/             # Service层
│   │   │   │   ├── auth_service.py   # 登录、JWT生成
│   │   │   │   └── user_service.py   # 用户CRUD
│   │   │   ├── repositories/         # Repository层（数据访问）
│   │   │   │   └── user_repository.py
│   │   │   └── schemas/              # DTO层
│   │   │       └── user.py
│   │   │
│   │   ├── course/                   # 模块2: 课程管理
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   └── routers.py        # /api/courses/*
│   │   │   ├── services/
│   │   │   │   └── course_service.py
│   │   │   ├── repositories/
│   │   │   │   └── course_repository.py
│   │   │   └── schemas/
│   │   │       └── course.py
│   │   │
│   │   ├── scenario/                 # 模块3: 情景模拟
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   └── routers.py        # /api/scenarios/*
│   │   │   ├── services/
│   │   │   │   └── scenario_service.py
│   │   │   ├── repositories/
│   │   │   │   └── scenario_repository.py
│   │   │   └── schemas/
│   │   │       └── scenario.py
│   │   │
│   │   ├── chat/                     # 模块4: 对话交互
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   └── routers.py        # /api/chat/*
│   │   │   ├── services/
│   │   │   │   ├── chat_service.py            # 会话管理
│   │   │   │   └── conversation_engine.py     # 对话编排服务
│   │   │   ├── repositories/
│   │   │   │   └── chat_repository.py
│   │   │   └── schemas/
│   │   │       └── chat.py
│   │   │
│   │   ├── evaluation/               # 模块5: 评估系统
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   └── routers.py        # /api/evaluation/*
│   │   │   ├── services/
│   │   │   │   └── evaluation_service.py
│   │   │   ├── repositories/
│   │   │   │   └── evaluation_repository.py
│   │   │   ├── agents/               # 智能体
│   │   │   │   └── mentor_agent.py
│   │   │   └── schemas/
│   │   │       └── evaluation.py
│   │   │
│   │   └── progress/                 # 模块6: 学习进度
│   │       ├── __init__.py
│   │       ├── api/
│   │       │   └── routers.py        # /api/progress/*
│   │       ├── services/
│   │       │   └── progress_service.py
│   │       ├── repositories/
│   │       │   └── progress_repository.py
│   │       └── schemas/
│   │           └── progress.py
│   │
│   │   ├── menu/                      # 模块7: 菜单权限管理
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   └── routers.py        # /api/menus/*
│   │   │   ├── services/
│   │   │   │   └── menu_service.py
│   │   │   ├── repositories/
│   │   │   │   └── menu_repository.py
│   │   │   └── schemas/
│   │   │       └── menu.py
│   │
│   │   └── admin/                     # 模块8: 系统管理（预留）
│   │       ├── __init__.py            # 系统管理功能模块（用户、角色、菜单管理）
│   │       ├── api/                   # 仅管理员角色可访问
│   │       ├── services/
│   │       ├── repositories/
│   │       └── schemas/
│   │
│   ├── models/                       # ORM模型层（共享）
│   │   ├── user.py                   # 用户表
│   │   ├── course.py                 # 课程表
│   │   ├── scenario.py               # 场景表
│   │   ├── chat.py                   # 聊天会话、消息表
│   │   ├── evaluation.py             # 评估报告表
│   │   ├── progress.py               # 学习进度表
│   │   └── menu.py                   # 菜单、权限表
│   │
│   ├── schemas/                      # Pydantic模型层（共享）
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── scenario.py
│   │   ├── chat.py
│   │   ├── evaluation.py
│   │   └── progress.py
│   │
│   ├── common/                       # 通用模块
│   │   ├── constants.py              # 常量定义
│   │   └── exceptions.py             # 异常定义
│   │
│   ├── core/                         # 核心配置
│   │   ├── config.py                 # 应用配置
│   │   ├── security.py               # 安全相关
│   │   └── proxy.py                  # 代理配置
│   │
│   ├── db/                           # 数据库
│   │   ├── database.py               # 数据库连接
│   │   └── init_db.py                # 初始化
│   │
│   ├── utils/                        # 工具函数
│   │   └── google_search.py          # AI搜索工具
│   │
│   └── api/                          # 保留未迁移的路由
│       ├── __init__.py
│       └── health.py                 # 健康检查端点
│
├── .env                              # 环境变量
├── .env.example                      # 环境变量示例
└── requirements.txt                  # Python依赖
```

## 模块说明

### 1. 共享基础设施层 (shared/)

提供所有业务模块共享的基础能力。

#### shared/infrastructure/ai_service.py
- **功能**：AI服务统一接口
- **职责**：封装所有AI调用（阿里百炼/通义千问）
- **方法**：
  - `generate_conversation_response()` - 生成对话回复
  - `generate_evaluation_report()` - 生成评估报告

#### shared/infrastructure/skill_config.py
- **功能**：技能配置管理
- **职责**：读取和管理全局对话技能配置（skill_config.json）
- **模式**：单例模式

#### shared/infrastructure/event_bus.py
- **功能**：事件总线
- **职责**：实现发布-订阅模式，模块间异步通信
- **事件定义**：
  - `chat.session_ended` - 会话结束事件
  - `evaluation.generated` - 评估生成事件

### 2. 认证与用户模块 (modules/auth/)

**职责**：用户身份管理、认证授权

**API端点**：
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户
- `POST /api/users/` - 用户注册
- `GET /api/users/` - 用户列表
- `GET /api/users/{id}` - 用户详情
- `PUT /api/users/{id}` - 更新用户
- `DELETE /api/users/{id}` - 删除用户

### 3. 课程管理模块 (modules/course/)

**职责**：课程内容管理、THP层级分类

**API端点**：
- `POST /api/courses/` - 创建课程
- `GET /api/courses/` - 课程列表（可按层级筛选）
- `GET /api/courses/{id}` - 课程详情
- `PUT /api/courses/{id}` - 更新课程
- `DELETE /api/courses/{id}` - 删除课程

### 4. 情景模拟模块 (modules/scenario/)

**职责**：训练场景管理、场景配置

**API端点**：
- `POST /api/scenarios/` - 创建场景
- `GET /api/scenarios/` - 场景列表（可按难度筛选）
- `GET /api/scenarios/{id}` - 场景详情
- `PUT /api/scenarios/{id}` - 更新场景
- `DELETE /api/scenarios/{id}` - 删除场景

**对外接口**：`interfaces/scenario_interface.py`
- `get_scenario_config()` - 获取场景配置
- `get_patient_background()` - 获取患者背景
- `get_system_prompt()` - 获取系统提示词

### 5. 对话交互模块 (modules/chat/)

**职责**：对话会话管理、消息记录、AI对话编排

**API端点**：
- `POST /api/chat/sessions` - 创建会话
- `GET /api/chat/sessions/{id}` - 会话详情
- `GET /api/chat/sessions/{id}/messages` - 会话消息列表
- `POST /api/chat/messages` - 发送消息并获取AI回复
- `PUT /api/chat/sessions/{id}/end` - 结束会话并生成评估

**核心组件**：
- `conversation_engine.py` - 对话编排引擎
  - 通过 **ScenarioInterface** 获取场景配置
  - 通过 **AIService** 调用AI
  - 通过 **EventBus** 发布会话结束事件

### 6. 评估系统模块 (modules/evaluation/)

**职责**：THP五维评分、评估报告生成

**API端点**：
- `POST /api/evaluation/sessions/{id}/evaluate` - 生成评估报告
- `GET /api/evaluation/sessions/{id}/report` - 获取会话评估报告
- `GET /api/evaluation/reports/{id}` - 根据ID获取报告
- `GET /api/evaluation/reports` - 评估报告列表
- `DELETE /api/evaluation/reports/{id}` - 删除报告

**核心组件**：
- `agents/mentor_agent.py` - AI智能体
  - 订阅 `chat.session_ended` 事件
  - 事件触发时自动生成评估报告

### 7. 学习进度模块 (modules/progress/)

**职责**：用户学习进度跟踪

**API端点**：
- `POST /api/progress/courses/{id}/start` - 开始学习课程
- `GET /api/progress/courses/{id}` - 课程学习进度
- `GET /api/progress/` - 所有课程学习进度
- `PUT /api/progress/courses/{id}` - 更新学习进度

### 8. 菜单权限模块 (modules/menu/)

**职责**：菜单管理、基于角色的访问控制（RBAC）

**API端点**：
- `GET /api/menus/user?role=xxx` - 获取用户可访问的菜单列表
- `GET /api/menus/` - 获取所有菜单（管理员）
- `GET /api/menus/{id}` - 获取菜单详情
- `POST /api/menus/` - 创建菜单
- `PUT /api/menus/{id}` - 更新菜单
- `DELETE /api/menus/{id}` - 删除菜单
- `GET /api/menus/permissions` - 获取所有角色菜单权限
- `POST /api/menus/permissions` - 更新角色菜单权限

**数据库表**：
- `menus` - 菜单表（支持层级结构）
- `role_menu_permissions` - 角色菜单权限关联表

**角色类型**：`student`（学生）, `instructor`（讲师）, `admin`（管理员）

### 9. 系统管理模块 (modules/admin/) - 预留

**职责**：系统管理功能（仅管理员可访问）

**规划功能**：
- 用户管理（增删改查）
- 角色管理（角色权限配置）
- 菜单管理（动态菜单配置）

**开发状态**：目录结构已预留，待开发

## 模块依赖关系

```
                    shared/
                 (共享基础设施层)
                       ↕
                  interfaces/
                 (抽象接口层)
                       ↕
    ┌─────────────────────────────────────────┐
    │              modules/                    │
    │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
    │  │ auth │ │course│ │scenario│  │progress│  │
    │  └──────┘ └──────┘ └──┬───┘ └──────┘   │
    │                      │                  │
    │                  ┌───┴────┐             │
    │                  │  chat  │             │
    │                  └───┬────┘             │
    │                      │                  │
    │                  ┌───┴────────┐         │
    │                  │ evaluation │         │
    │                  └────────────┘         │
    └─────────────────────────────────────────┘
```

**依赖规则**：
1. 业务模块只能依赖 `shared/` 和 `interfaces/`
2. 业务模块之间通过接口或事件总线通信
3. `shared/` 不依赖任何业务模块

## 关键设计模式

### 1. 事件驱动（Event-Driven）

```python
# 发布事件
event_bus.publish("chat.session_ended", {"session_id": "xxx"})

# 订阅事件
event_bus.subscribe("chat.session_ended", self.handle_session_ended)
```

**优势**：
- 模块间解耦
- 异步处理
- 易于扩展

### 2. 依赖注入（Dependency Injection）

```python
class ConversationEngine:
    def __init__(
        self,
        db: Session,
        ai_service: AIService,
        scenario_interface: ScenarioInterface
    ):
        self.db = db
        self.ai_service = ai_service
        self.scenario_interface = scenario_interface
```

**优势**：
- 降低耦合
- 便于测试
- 灵活配置

### 3. 接口隔离（Interface Segregation）

```python
class ScenarioInterface(ABC):
    @abstractmethod
    def get_scenario_config(self, scenario_id: str) -> Optional[Dict]:
        pass
```

**优势**：
- 模块间通过抽象接口通信
- 隐藏实现细节
- 便于替换实现

## 环境配置

### 环境变量 (.env)

```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=panda
DB_USER=root
DB_PASSWORD=your_password

# AI配置
AI_TEXT_KEY=your_ai_key
AI_TEXT_MODEL=deepseek-v3.2

# 代理配置（可选）
HTTP_PROXY=http://127.0.0.1:7897
HTTPS_PROXY=http://127.0.0.1:7897
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入数据库和AI配置
```

### 3. 启动应用

```bash
# 方式1：使用Python
cd app
python main.py

# 方式2：使用Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问API文档

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 开发规范

### 6A 工作流

所有开发任务请遵循 `docs/开发规则.md` 中定义的6A工作流：
1. **Align** (对齐) - 明确需求和目标
2. **Architect** (架构) - 设计技术方案
3. **Atomize** (原子化) - 拆分为小任务
4. **Approve** (审批) - 代码审查
5. **Automate** (自动化执行) - 自动化测试和部署
6. **Assess** (评估) - 效果评估和复盘

### 代码规范

1. **模块结构**：每个业务模块统一使用 `api/services/repositories/schemas` 结构
2. **导入顺序**：标准库 → 第三方库 → 本地模块
3. **命名规范**：
   - 类名：PascalCase
   - 函数/变量：snake_case
   - 常量：UPPER_SNAKE_CASE
4. **注释规范**：所有公开的类和函数必须添加文档字符串

### Git 提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

**type 类型**：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**：
```
feat(chat): 实现对话会话结束事件发布

- 通过EventBus发布chat.session_ended事件
- evaluation模块订阅该事件自动生成评估报告
- 移除chat模块对evaluation模块的直接依赖

Closes #123
```

## 测试

```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/modules/test_chat.py

# 查看测试覆盖率
pytest --cov=app --cov-report=html
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t panda-backend .

# 运行容器
docker run -p 8000:8000 --env-file .env panda-backend
```

### 生产环境配置

- 使用 `gunicorn` 或 `uvicorn` 作为ASGI服务器
- 配置 `nginx` 作为反向代理
- 启用HTTPS
- 配置日志收集和监控

## 故障排查

### 常见问题

1. **数据库连接失败**
   - 检查 `.env` 中的数据库配置
   - 确认数据库服务已启动
   - 检查防火墙设置

2. **AI调用失败**
   - 检查 `AI_TEXT_KEY` 是否正确配置
   - 确认网络代理设置（如果需要）
   - 查看AI服务状态

3. **模块导入错误**
   - 确认 `PYTHONPATH` 已正确设置
   - 检查模块间的依赖关系
   - 运行 `python -m pytest` 检查

## 项目文档

- [开发规则](../docs/开发规则.md)
- [项目介绍](../docs/项目介绍.md)
- [THP评估体系](../docs/THP.md)
- [后续开发任务](../docs/后续开发任务清单.md)

## 许可证

Copyright © 2024 PANDA Team. All rights reserved.