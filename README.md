# PANDA

> 围产期抑郁管理智能培训系统

基于 **THP 理论**的 AI 智能培训系统，通过虚拟情景模拟和智能评估，提升护理人员对围产期抑郁的识别、沟通和干预能力。

## 核心功能

- 📚 **在线课程** - 基于 THP 框架的多媒体课程
- 🎭 **AI 情景模拟** - 动态患者 Agent，真实对话演练
- 📊 **智能评估** - THP 五维能力评估与反馈
- 🎯 **危机检测** - 实时监测自杀风险倾向

## 技术栈

| 类别 | 技术 |
|------|------|
| 后端 | FastAPI + LangChain + MySQL + Redis |
| 前端 | React 19 + TypeScript + Ant Design + Vite |
| AI | 通义千问 |

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/BAIKEMARK/PANDA.git
cd PANDA

# 2. 初始化数据库
mysql -u root -p < docs/项目文档/resources/panda.sql

# 3. 启动后端
cd backend && pip install -r requirements.txt && python start.py

# 4. 启动前端
cd frontend && npm install && npm run dev
```

**访问地址**
- 前端: http://localhost:5173
- API 文档: http://localhost:8000/api/docs
- 测试账号: admin@panda.com / 123456

## 文档

| 文档 | 说明 |
|------|------|
| [快速开始](docs/快速开始.md) | 详细安装指南 |
| [项目介绍](docs/项目介绍.md) | 项目背景与目标 |
| [架构设计](docs/架构设计.md) | 系统架构详解 |
| [后端文档](backend/README.md) | 后端开发指南 |
| [前端文档](frontend/README.md) | 前端开发指南 |
| [开发规范](docs/开发规则.md) | 编码规范与最佳实践 |

## 项目结构

```
PANDA/
├── backend/     # FastAPI 后端
├── frontend/    # React 前端
└── docs/        # 详细文档
```

## 版本历史

- **v0.4.0** (2026-02-05) - 核心架构重构
- **v0.3.0** (2026-01-31) - Agent 智能体系统

---

## 许可证

本项目仅供学习和研究使用。