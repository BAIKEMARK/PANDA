# PANDA 前端

基于 React 19 + TypeScript + Vite 的现代化单页应用。

## 技术栈

| 技术 | 说明 |
|------|------|
| React 19 | UI 框架 |
| TypeScript | 类型安全 |
| Vite 7 | 快速构建 |
| Ant Design 6 | 组件库 |
| Zustand | 状态管理 |
| React Router 7 | 路由管理 |

## 项目结构

```
frontend/src/
├── pages/              # 页面组件
├── components/         # 可复用组件
│   ├── chat/          # 对话组件
│   ├── course/        # 课程组件
│   └── evaluation/    # 评估组件
├── services/          # API 服务层
├── stores/            # 状态管理
├── types/             # TypeScript 类型
└── router/            # 路由配置
```

## 核心功能

- 认证与权限管理
- 课程学习与进度跟踪
- AI 对话情景模拟
- 评估报告可视化
- 动态菜单权限

## 快速开始

```bash
# 安装依赖
npm install

# 配置环境
cp .env.example .env

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173

## 环境变量

```bash
# API 地址
VITE_API_URL=http://localhost:8000/api

# 应用标题
VITE_APP_TITLE=PANDA 围产期抑郁管理智能培训系统
```

## 路由

| 路径 | 组件 | 说明 |
|------|------|------|
| `/login` | LoginPage | 登录页 |
| `/` | CourseListPage | 课程列表 |
| `/chat` | ChatPage | 对话页面 |
| `/evaluation/:id` | EvaluationReportPage | 评估报告 |

## 开发指南

详见 [开发规则](../docs/开发规则.md)

## 相关文档

- [架构设计](../docs/架构设计.md) - 系统架构详解