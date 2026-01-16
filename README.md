# 基于THP的围产期抑郁管理智能培训系统 (PANDA)

## 🎯 项目简介

国家高度重视围产期心理健康，将心理风险识别与干预纳入妇幼健康服务体系。本项目针对护理人员在围产期抑郁（PND）管理中规范化能力不足的问题，基于健康思维计划（THP）结合AI技术，研发智能培训系统。

通过构建标准化操作流程与智能化培训方案，本系统旨在提升护理人员对PND的识别、沟通支持及初步干预能力，为护理人员参与围产期心理健康管理提供可推广的技术路径与实施模式。

---

## 📊 项目开发状态

**当前版本**: v0.1.0 (Alpha)
**最后更新**: 2025-01-16
**开发分支**: `zzy` (初始化提交)

### ✅ 已完成功能 (MVP核心功能)

#### 后端实现 (FastAPI + MySQL)
- ✅ **标准MVC架构** - Controller → Service → CRUD → Model 分层设计
- ✅ **用户认证系统**
  - 用户注册接口 (`POST /api/users/`)
  - 用户登录接口 (`POST /api/auth/login`)
  - JWT Token生成与验证机制
  - 密码哈希存储 (bcrypt)
- ✅ **课程管理模块**
  - 课程CRUD接口
  - 按THP层级筛选 (L1-L4)
  - 课程关联模型
- ✅ **情景模拟模块**
  - 场景CRUD接口
  - 难度等级筛选
  - 患者背景配置
- ✅ **AI对话模块**
  - 对话会话管理
  - 消息流式传输
  - 集成阿里百炼AI平台
  - 会话状态管理 (active/ended)
- ✅ **数据库设计**
  - 完整的ER模型设计
  - 用户、课程、场景、聊天表结构
  - 初始化测试数据

#### 前端实现 (React + Ant Design)
- ✅ **UI框架升级**
  - 从Tailwind CSS迁移到Ant Design 5.x
  - 统一的视觉风格和交互体验
  - 响应式布局设计
- ✅ **认证系统**
  - 登录页面 (Ant Design表单 + 渐变背景)
  - 注册页面 (表单验证 + 密码确认)
  - 注册成功提示与自动跳转
  - Zustand状态管理 + 持久化
- ✅ **布局系统**
  - 侧边栏导航 (固定256px宽度 + 深色主题)
  - 顶部Header (标题 + 用户信息 + 退出)
  - 主内容区 (自适应布局)
  - 路由守卫 (未登录自动跳转)
- ✅ **课程学习模块**
  - 课程列表页 (网格布局 + 层级筛选)
  - 课程卡片 (封面 + 进度条 + 标签)
  - 课程详情页 (Markdown渲染)
- ✅ **情景模拟模块**
  - 场景列表页 (难度星级展示)
  - 场景卡片 (患者背景 + 知识标签)
  - 一键开始练习
- ✅ **AI聊天界面**
  - 聊天窗口 (消息气泡 + 自动滚动)
  - 输入框 (多行文本 + Enter发送)
  - 打字指示器动画
  - 会话计时器
  - 结束对话确认
- ✅ **评估报告模块**
  - 能力雷达图 (Recharts)
  - 分数卡片 (知识/评估/沟通/干预)
  - AI反馈展示
  - 对话时间轴
- ✅ **个人中心**
  - 用户信息展示
  - 学习历史记录

### 🔨 待完成功能

#### 优先级 P0 (必须完成)
- ❌ **JWT Token验证中间件** - 保护需要认证的路由
- ❌ **EPDS量表组件** - 10题量表 + 实时计分
- ❌ **前端路由404处理** - 优雅的错误页面
- ❌ **全局错误处理** - 统一的错误提示机制

#### 优先级 P1 (重要功能)
- ❌ **课程进度保存** - 后端API + 前端自动保存
- ❌ **AI流式响应优化** - SSE或WebSocket
- ❌ **评估报告后端接口** - `GET /api/evaluation/sessions/{id}/report`
- ❌ **管理员后台** - 用户管理、内容管理、数据统计

#### 优先级 P2 (增强功能)
- ❌ **实训考核模块** - OSCE考试、题库系统
- ❌ **证书生成** - 带唯一编码的结业证书
- ❌ **数据导出** - Excel/PDF导出功能
- ❌ **多租户支持** - 医院隔离部署

### 🐛 已知问题

1. **CORS配置** - 已支持localhost:5173-5175，生产环境需更新
2. **SECRET_KEY** - 使用硬编码密钥，生产环境需从环境变量读取
3. **API权限控制** - 所有接口目前未做Token验证
4. **数据库schema路径** - 文档中路径与实际不符 (`app/database/` → `backend/database/`)

---

## 🛠️ 技术栈

### 后端技术栈
- **框架**: FastAPI 0.104+
- **数据库**: MySQL 8.0.43
- **ORM**: SQLAlchemy 2.0+
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt
- **AI平台**: 阿里百炼 (通义千问)
- **架构模式**: MVC (Controller → Service → CRUD → Model)

### 前端技术栈
- **框架**: React 18 + TypeScript 5
- **构建工具**: Vite 5
- **UI库**: Ant Design 5.x
- **状态管理**: Zustand 4 + persist中间件
- **路由**: React Router 6
- **HTTP客户端**: Axios
- **图表**: Recharts 2
- **Markdown渲染**: react-markdown

## 核心功能模块

### 1. 内容学习模块
基于THP框架的在线多媒体课程系统，强调实用性与本土化。
- **多媒体课件**：集成专家视频、交互式图表（如抑郁评估流程图）及政策指南全文。
- **学习管理**：支持课程目录解锁、书签断点续学。
- **即时测验**：课件中穿插知识点测验（选择、判断等），即时反馈解析。
- **知识库与FAQ**：提供PND管理循证知识库，支持快速查询（如EPDS评分标准、哺乳期用药安全等）。

### 2. 虚拟情景模拟模块 (核心)
采用AI虚拟仿真技术，提供高沉浸感的PND案例互动演练。
- **多场景案例库**：涵盖孕早期焦虑、早产儿母亲心理、产后抑郁等10+典型情境。
- **AI智能交互**：支持文本/语音与虚拟患者对话，具备情绪表情渲染与多分支剧情逻辑。
- **集成评估工具**：对话中可无缝调用EPDS、PHQ-9、GAD-7量表，AI模拟患者作答并生成评分。
- **智能引导系统**：根据学员表现提供差异化提示（如“检测到患者可能存在抑郁情绪”），逐步培养独立判断。
- **复盘分析**：对话结束后生成回放与分析报告，评估关键行为覆盖率、同理心使用情况及决策合理性。

### 3. 实训考核模块
提供理论与实践结合的综合性评估体系，符合继续教育考核规范。
- **章节测验**：随学随测，巩固理论知识。
- **综合技能考核**：模拟OSCE考试，随机抽取案例进行全流程评估（无提示），静默记录行为数据。
- **题库与笔试**：内置约200道客观题，支持自动组卷与判分。
- **防作弊监控**：支持摄像头监考、人脸识别及防切屏限制。
- **证书管理**：自动生成带唯一编码的培训结业证书，支持学分认定。

### 4. 能力档案与数据分析模块
可视化的学员成长档案与教学管理辅助工具。
- **个人能力雷达图**：从知识理解、评估技能、沟通技能、干预决策四个维度量化能力。
- **学习轨迹**：时间轴形式展示学习历程与能力提升曲线。
- **班级/全员监控**：管理员可查看全员进度、成绩分布及薄弱环节统计。
- **质量控制**：通过数据对比不同批次培训效果，关联临床指标（如筛查率、转介率），评估培训实效。
- **数据对接**：支持导出Excel/PDF，提供API对接医院HR系统或上级教育平台。

### 5. 系统管理与维护模块
灵活的后台管理，支持多机构部署。
- **内容管理**：可视化编辑课程、题库及模拟场景剧本（支持分支逻辑预设）。
- **多租户支持**：支持不同医院/学校作为独立租户，数据隔离，统一标准。
- **用户与权限**：批量导入学员，分配学员、导师、管理员角色。
- **学分配置**：自定义继续教育学分规则与学时换算。
- **运维监控**：服务器状态监控、日志查询及数据备份。

## 智能体构建流程

1.  **知识结构化**：将THP干预内容转化为结构化知识单元，构建智能体知识库。
2.  **情景脚本设计**：基于真实案例设计不同PND风险等级的训练脚本。
3.  **对话与决策逻辑设计**：嵌入THP干预原则，构建智能对话决策流程。
4.  **测试与优化**：通过护理人员试用反馈，持续迭代优化交互逻辑。

## 技术栈

-   **前端框架**: [React](https://react.dev/) + [Vite](https://vitejs.dev/)
-   **后端/算法**: Python 3.12.12
-   **数据库**: MySQL 8.0.43

## 开发环境要求

在开始项目之前，请确保您的开发环境满足以下版本要求：

-   **Python**: 3.12.12
-   **Node.js**: v20.15.1
-   **MySQL**: 8.0.43

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd PANDA
```

### 2. 数据库配置

确保 MySQL 8.0.43+ 已安装并运行。

```bash
# 登录 MySQL
mysql -u root -p

# 执行初始化脚本
source backend/database/schema.sql
```

或使用命令行：
```bash
mysql -u root -p < backend/database/schema.sql
```

### 3. 后端配置

```bash
# 进入后端目录
cd backend

# 安装 Python 依赖
pip install -r requirements.txt

# 复制环境变量配置文件
cp app/.env.example app/.env

# 编辑 app/.env 文件，配置数据库连接和AI密钥
# 必须配置：
# - DB_PASSWORD: 你的MySQL密码
# - AI_TEXT_KEY: 阿里百炼平台API密钥

# 启动后端服务
python -m uvicorn app.main:app --reload --port 8000
```

后端服务将在 `http://localhost:8000` 启动
- API文档: `http://localhost:8000/api/docs`
- ReDoc文档: `http://localhost:8000/api/redoc`

### 4. 前端配置

打开新的终端窗口：

```bash
# 进入前端目录
cd frontend

# 安装 Node.js 依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

### 5. 验证安装

访问以下地址验证安装是否成功：

- **前端页面**: http://localhost:5173
- **API健康检查**: http://localhost:8000/api/health
- **API文档**: http://localhost:8000/api/docs

### 6. 测试账号

系统已初始化管理员账号：
- **邮箱**: admin@panda.com
- **密码**: 123456
- **角色**: 系统管理员

## 环境变量说明

### 后端环境变量 (`backend/app/.env`)

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DB_HOST` | 数据库主机地址 | localhost |
| `DB_PORT` | 数据库端口 | 3306 |
| `DB_USER` | 数据库用户名 | root |
| `DB_PASSWORD` | 数据库密码 | your_password |
| `DB_NAME` | 数据库名称 | panda_pnd |
| `AI_TEXT_KEY` | 阿里百炼API密钥 | sk-xxx |
| `GOOGLE_API_KEY` | Google搜索API密钥 | AIzaxxx |

### 前端环境变量 (`frontend/.env`)

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `VITE_API_URL` | 后端API地址 | http://localhost:8000/api |

## 项目结构

```
PANDA/
├── backend/               # Python后端 (FastAPI)
│   ├── app/              # 应用主目录
│   │   ├── main.py       # FastAPI主应用入口
│   │   ├── core/         # 核心模块 (配置、安全、代理)
│   │   ├── api/          # API路由层 (Controller)
│   │   │   ├── auth.py   # 认证接口 (登录/登出)
│   │   │   ├── users.py  # 用户管理
│   │   │   ├── courses.py # 课程管理
│   │   │   ├── scenarios.py # 场景管理
│   │   │   ├── chat.py   # AI对话接口
│   │   │   └── health.py # 健康检查
│   │   ├── services/     # 业务逻辑层 (Service)
│   │   ├── crud/         # 数据访问层 (CRUD)
│   │   ├── models/       # SQLAlchemy ORM模型
│   │   ├── schemas/      # Pydantic DTO模型
│   │   ├── db/           # 数据库连接
│   │   ├── common/       # 公共工具 (常量、异常)
│   │   ├── utils/        # 工具函数 (Google搜索)
│   │   └── .env          # 环境变量配置
│   ├── database/         # 数据库脚本
│   │   └── schema.sql    # 初始化SQL脚本
│   └── requirements.txt  # Python依赖
├── frontend/             # React前端 (Vite)
│   ├── src/
│   │   ├── pages/        # 页面组件
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── CourseListPage.tsx
│   │   │   ├── ScenarioListPage.tsx
│   │   │   ├── ChatPage.tsx
│   │   │   └── EvaluationReportPage.tsx
│   │   ├── components/   # React组件
│   │   │   ├── layout/   # 布局组件 (Sidebar/Header)
│   │   │   ├── chat/     # 聊天组件
│   │   │   ├── course/   # 课程组件
│   │   │   ├── scenario/ # 场景组件
│   │   │   └── evaluation/ # 评估组件
│   │   ├── services/     # API服务层
│   │   ├── stores/       # Zustand状态管理
│   │   ├── types/        # TypeScript类型定义
│   │   ├── router/       # React Router配置
│   │   └── main.tsx      # 应用入口
│   ├── package.json      # Node.js依赖
│   ├── vite.config.ts    # Vite配置
│   └── tailwind.config.js # Tailwind配置
├── docs/                 # 项目文档
│   ├── MVP开发.md
│   ├── 数据库设计.md
│   ├── 系统功能设计.md
│   └── ...
├── init.bat              # Windows初始化脚本
├── init.sh               # Linux/Mac初始化脚本
└── README.md             # 本文件
```

## 开发指南

### API 接口

所有API接口都以 `/api` 为前缀，主要接口包括：

**认证接口**:
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出

**用户管理**:
- `POST /api/users/` - 用户注册
- `GET /api/users/` - 获取用户列表
- `GET /api/users/{user_id}` - 获取用户详情

**课程管理**:
- `GET /api/courses/` - 获取课程列表
- `GET /api/courses/{course_id}` - 获取课程详情

**情景模拟**:
- `GET /api/scenarios/` - 获取场景列表
- `GET /api/scenarios/{scenario_id}` - 获取场景详情

**AI对话**:
- `POST /api/chat/sessions` - 创建对话会话
- `GET /api/chat/sessions/{session_id}/messages` - 获取消息历史
- `POST /api/chat/messages` - 发送消息
- `PUT /api/chat/sessions/{session_id}/end` - 结束会话

**系统**:
- `GET /api/health` - 健康检查

详细API文档请访问：`http://localhost:8000/api/docs`

### 代码规范

- **Python**: 遵循 PEP 8 规范
- **TypeScript/React**: 遵循 ESLint 配置
- **Git**: 使用 feature 分支开发模式

## 常见问题

### Q: 数据库连接失败？
A: 请检查 `backend/app/.env` 中的数据库配置是否正确，确保MySQL服务正在运行。

### Q: AI接口调用失败？
A: 请确认已在 `backend/app/.env` 中配置有效的 `AI_TEXT_KEY`。

### Q: 前端无法连接后端？
A: 确保后端服务在 8000 端口运行，检查 `frontend/.env` 中的 `VITE_API_URL` 配置。

### Q: 注册成功但无法登录？
A: 确认已重启后端服务（新增auth.py路由需要重启）。

---

## 📝 变更日志

### v0.1.0 (2025-01-16) - 初始化提交

**新增功能**:
- ✨ 后端FastAPI MVC架构搭建
- ✨ 前端React + Ant Design UI框架
- ✨ 用户注册/登录功能
- ✨ 课程学习模块（列表/详情）
- ✨ 情景模拟模块（场景列表）
- ✨ AI聊天对话模块
- ✨ 评估报告模块（雷达图/评分）
- ✨ JWT认证机制

**技术债务**:
- ⚠️ JWT Token验证中间件未实现
- ⚠️ API接口权限控制未完善
- ⚠️ EPDS量表组件待开发
- ⚠️ 评估报告后端接口待补充

**技术栈**:
- 后端: FastAPI + MySQL + SQLAlchemy
- 前端: React 18 + TypeScript + Ant Design 5
- AI: 阿里百炼通义千问

---

## 📄 许可证

[TODO: 添加许可证信息]

## 📞 联系方式

[TODO: 添加联系信息]
