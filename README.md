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
- **AI平台**：阿里百炼（通义千问）
- **认证**：JWT

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
cp app/.env.example app/.env
# 编辑 app/.env，配置数据库密码和AI密钥

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

**后端** (`backend/app/.env`):
```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=panda_pnd
AI_TEXT_KEY=your_ai_api_key
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
├── backend/           # FastAPI后端
│   ├── app/          # 应用代码
│   │   ├── api/      # API路由
│   │   ├── models/   # ORM模型
│   │   ├── schemas/  # 数据模型
│   │   ├── services/ # 业务逻辑
│   │   └── crud/     # 数据访问
│   └── database/     # 数据库脚本
├── frontend/         # React前端
│   └── src/
│       ├── pages/    # 页面组件
│       ├── components/ # UI组件
│       └── services/ # API调用
└── docs/            # 项目文档
```
