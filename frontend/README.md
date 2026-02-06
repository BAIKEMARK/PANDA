# PANDA 前端项目

**围产期抑郁管理智能培训系统 - React 前端应用**

## 项目概述

本项目是基于 React 19 + TypeScript + Vite 构建的现代化单页应用（SPA），采用 Ant Design 组件库和 Tailwind CSS 进行UI开发。

## 技术栈

### 核心框架
- **React 19** - UI 框架
- **TypeScript** - 类型安全
- **Vite 7** - 构建工具
- **React Router v7** - 路由管理

### UI 框架
- **Ant Design 6** - 企业级 UI 组件库
- **Tailwind CSS 4** - 原子化 CSS 框架
- **React Hot Toast** - 消息提示

### 状态管理
- **Zustand** - 轻量级状态管理

### 数据可视化
- **Recharts** - 图表库（用于评估报告雷达图）

### HTTP 客户端
- **Axios** - HTTP 请求库

## 项目结构

```
frontend/
├── public/                          # 静态资源
│   └── vite.svg                    # Vite 图标
├── src/                             # 源代码目录
│   ├── App.tsx                      # 应用根组件
│   ├── main.tsx                     # 应用入口
│   ├── index.css                    # 全局样式
│   │
│   ├── components/                  # 可复用组件
│   │   ├── chat/                    # 对话相关组件
│   │   │   ├── ChatInput.tsx        # 聊天输入框
│   │   │   ├── ChatWindow.tsx       # 聊天窗口
│   │   │   └── MessageBubble.tsx    # 消息气泡
│   │   ├── course/                  # 课程相关组件
│   │   │   ├── CourseCard.tsx       # 课程卡片
│   │   │   └── LevelFilter.tsx      # 层级筛选器
│   │   ├── evaluation/              # 评估相关组件
│   │   │   ├── FeedbackSection.tsx  # 反馈区域
│   │   │   ├── RadarChart.tsx       # 雷达图
│   │   │   └── ScoreCard.tsx        # 评分卡片
│   │   ├── layout/                  # 布局组件
│   │   │   ├── AppLayout.tsx        # 应用布局
│   │   │   ├── Header.tsx           # 顶部导航
│   │   │   └── Sidebar.tsx          # 侧边栏（动态菜单）
│   │   └── scenario/                # 场景组件
│   │       └── ScenarioCard.tsx     # 场景卡片
│   │
│   ├── pages/                        # 页面组件
│   │   ├── LoginPage.tsx            # 登录页
│   │   ├── RegisterPage.tsx         # 注册页
│   │   ├── CourseListPage.tsx       # 课程列表
│   │   ├── CourseDetailPage.tsx     # 课程详情
│   │   ├── ScenarioListPage.tsx     # 场景列表
│   │   ├── ChatPage.tsx             # 对话页面
│   │   ├── EvaluationReportPage.tsx # 评估报告
│   │   ├── ProfilePage.tsx          # 个人中心
│   │   └── NotFoundPage.tsx         # 404页面
│   │
│   ├── router/                       # 路由配置
│   │   ├── index.ts                 # 路由导出
│   │   ├── index.tsx                # 路由定义
│   │   └── privateRoutes.tsx        # 路由守卫
│   │
│   ├── services/                     # API 服务层
│   │   ├── api.ts                   # Axios 实例配置
│   │   ├── auth.service.ts          # 认证服务
│   │   ├── chat.service.ts          # 对话服务
│   │   ├── course.service.ts        # 课程服务
│   │   ├── evaluation.service.ts    # 评估服务
│   │   ├── scenario.service.ts      # 场景服务
│   │   └── menu.service.ts          # 菜单服务（动态菜单）
│   │
│   ├── stores/                       # 状态管理
│   │   ├── auth.store.ts            # 认证状态
│   │   ├── chat.store.ts            # 对话状态
│   │   ├── course.store.ts          # 课程状态
│   │   ├── menu.store.ts            # 菜单状态（动态菜单）
│   │   └── ui.store.ts              # UI状态
│   │
│   └── types/                        # TypeScript 类型定义
│       ├── index.ts                 # 类型导出
│       ├── auth.types.ts            # 认证类型
│       ├── chat.types.ts            # 对话类型
│       ├── course.types.ts          # 课程类型
│       ├── evaluation.types.ts      # 评估类型
│       ├── menu.types.ts            # 菜单类型（动态菜单）
│       └── scenario.types.ts        # 场景类型
│
├── src/admin/                       # 管理端模块（预留）
│   ├── README.md                    # 管理端说明
│   ├── users/                       # 用户管理
│   ├── roles/                       # 角色管理
│   ├── menus/                       # 菜单管理
│   └── layout/                      # 管理端布局
│
├── .env.example                     # 环境变量示例
├── .gitignore                       # Git 忽略配置
├── eslint.config.js                 # ESLint 配置
├── index.html                       # HTML 入口
├── package.json                     # 项目依赖
├── pnpm-lock.yaml                   # pnpm 锁文件
├── postcss.config.js                # PostCSS 配置
├── tailwind.config.js               # Tailwind CSS 配置
├── tsconfig.app.json                # TS 配置（应用）
├── tsconfig.json                    # TS 配置（基础）
├── tsconfig.node.json               # TS 配置（Node）
└── vite.config.ts                   # Vite 配置
```

## 核心功能模块

### 1. 认证模块

**组件**：`pages/LoginPage.tsx`, `pages/RegisterPage.tsx`

**状态管理**：`stores/auth.store.ts`

**服务**：`services/auth.service.ts`

**功能**：
- 用户登录/注册
- JWT Token 管理
- 自动登录

### 2. 课程模块

**组件**：`pages/CourseListPage.tsx`, `pages/CourseDetailPage.tsx`

**可复用组件**：`components/course/CourseCard.tsx`, `components/course/LevelFilter.tsx`

**状态管理**：`stores/course.store.ts`

**服务**：`services/course.service.ts`

**功能**：
- 课程列表展示（支持按THP层级筛选）
- 课程详情查看
- 课程学习进度跟踪

### 3. 场景模拟模块

**组件**：`pages/ScenarioListPage.tsx`

**可复用组件**：`components/scenario/ScenarioCard.tsx`

**服务**：`services/scenario.service.ts`

**功能**：
- 训练场景列表展示
- 按难度筛选场景
- 查看场景详情

### 4. 对话交互模块

**组件**：`pages/ChatPage.tsx`

**可复用组件**：`components/chat/ChatWindow.tsx`, `components/chat/ChatInput.tsx`, `components/chat/MessageBubble.tsx`

**状态管理**：`stores/chat.store.ts`

**服务**：`services/chat.service.ts`

**功能**：
- 创建对话会话
- 实时消息收发
- AI 对话交互
- 会话历史记录
- 结束会话并生成评估

### 5. 评估报告模块

**组件**：`pages/EvaluationReportPage.tsx`

**可复用组件**：`components/evaluation/RadarChart.tsx`, `components/evaluation/ScoreCard.tsx`, `components/evaluation/FeedbackSection.tsx`

**服务**：`services/evaluation.service.ts`

**功能**：
- THP 五维评分展示
- 雷达图可视化
- 详细反馈信息
- 评分建议

### 6. 个人中心模块

**组件**：`pages/ProfilePage.tsx`

**功能**：
- 用户信息展示
- 学习进度统计
- 个人设置

### 7. 菜单权限模块

**组件**：`components/layout/Sidebar.tsx`（动态菜单加载）

**状态管理**：`stores/menu.store.ts`

**服务**：`services/menu.service.ts`

**类型定义**：`types/menu.types.ts`

**功能**：
- 基于用户角色动态加载菜单
- 支持层级菜单结构
- 图标映射（数据库图标名 → React 组件）
- 为未来多租户功能预留扩展

**角色类型**：`student`（学生）, `instructor`（讲师）, `admin`（管理员）

### 8. 管理端模块 (admin/) - 预留

**职责**：系统管理功能（仅管理员可访问）

**规划功能**：
- 用户管理（增删改查）
- 角色管理（角色权限配置）
- 菜单管理（动态菜单配置）

**开发状态**：目录结构已预留，待开发

## 路由配置

### 公开路由

| 路径 | 组件 | 说明 |
|------|------|------|
| `/login` | LoginPage | 登录页 |
| `/register` | RegisterPage | 注册页 |

### 私有路由（需要认证）

| 路径 | 组件 | 说明 |
|------|------|------|
| `/` | CourseListPage | 课程列表（首页） |
| `/courses/:id` | CourseDetailPage | 课程详情 |
| `/scenarios` | ScenarioListPage | 场景列表 |
| `/chat` | ChatPage | 对话页面 |
| `/evaluation/:sessionId` | EvaluationReportPage | 评估报告 |
| `/profile` | ProfilePage | 个人中心 |
| `*` | NotFoundPage | 404页面 |

## 状态管理

### Zustand Store 结构

```typescript
// auth.store.ts - 认证状态
interface AuthStore {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => void
}

// chat.store.ts - 对话状态
interface ChatStore {
  currentSession: ChatSession | null
  messages: ChatMessage[]
  isTyping: boolean
  createSession: (scenarioId: string) => Promise<void>
  sendMessage: (content: string) => Promise<void>
  endSession: () => Promise<void>
}

// course.store.ts - 课程状态
interface CourseStore {
  courses: Course[]
  currentCourse: Course | null
  selectedLevel: string
  fetchCourses: (level?: string) => Promise<void>
}

// ui.store.ts - UI状态
interface UIStore {
  sidebarCollapsed: boolean
  loading: boolean
  toggleSidebar: () => void
  setLoading: (loading: boolean) => void
}
```

## API 服务层

### Axios 配置

```typescript
// services/api.ts
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器：自动添加 Token
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：统一错误处理
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

### 服务模块

| 服务文件 | 功能 |
|---------|------|
| `auth.service.ts` | 登录、注册、获取当前用户 |
| `course.service.ts` | 获取课程列表、课程详情 |
| `scenario.service.ts` | 获取场景列表、场景详情 |
| `chat.service.ts` | 创建会话、发送消息、结束会话 |
| `evaluation.service.ts` | 获取评估报告 |

## 环境配置

### 环境变量 (.env)

```bash
# API 地址
VITE_API_URL=http://localhost:8000/api

# 应用标题
VITE_APP_TITLE=PANDA 围产期抑郁管理智能培训系统
```

## 快速开始

### 1. 安装依赖

```bash
# 使用 pnpm（推荐）
pnpm install

# 或使用 npm
npm install

# 或使用 yarn
yarn install
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置 API 地址
```

### 3. 启动开发服务器

```bash
# 开发模式
pnpm dev

# 访问 http://localhost:5173
```

### 4. 构建生产版本

```bash
# 构建
pnpm build

# 预览构建结果
pnpm preview
```

## 开发规范

### 代码风格

项目使用 ESLint 进行代码检查：

```bash
# 运行 ESLint
pnpm lint
```

### 组件开发规范

1. **函数式组件**：优先使用函数式组件 + Hooks
2. **TypeScript**：所有组件必须定义 Props 类型
3. **命名规范**：
   - 组件：PascalCase（如 `ChatWindow.tsx`）
   - 工具函数：camelCase（如 `formatDate.ts`）
   - 常量：UPPER_SNAKE_CASE（如 `API_BASE_URL`）
4. **文件组织**：
   - 一个文件一个组件
   - 组件文件与组件名称保持一致
   - 相关组件放在同一目录

### 状态管理规范

1. **全局状态**：使用 Zustand stores
2. **局部状态**：使用 React Hooks（useState, useReducer）
3. **服务器状态**：优先考虑使用 React Query 或 SWR（可选）

### API 调用规范

```typescript
// ✅ 推荐：使用服务层
import { chatService } from '@/services/chat.service'

const sendMessage = async (content: string) => {
  try {
    const response = await chatService.sendMessage(sessionId, content)
    // 处理响应
  } catch (error) {
    // 错误处理
  }
}

// ❌ 不推荐：直接在组件中调用 axios
import axios from 'axios'

const sendMessage = async (content: string) => {
  await axios.post('/api/chat/messages', { content })
}
```

## 组件使用示例

### 对话组件

```tsx
import { ChatWindow } from '@/components/chat/ChatWindow'

function ChatPage() {
  return (
    <ChatWindow
      sessionId="session-123"
      onEndSession={(sessionId) => {
        console.log('会话结束:', sessionId)
      }}
    />
  )
}
```

### 评估报告组件

```tsx
import { RadarChart } from '@/components/evaluation/RadarChart'

function EvaluationReport() {
  const scores = {
    riskIdentification: 85,
    communicationSupport: 78,
    skillApplication: 82,
    safetyManagement: 90,
    selfEfficacy: 75
  }

  return <RadarChart scores={scores} />
}
```

## 路由守卫

使用 `PrivateRoute` 组件保护需要认证的路由：

```tsx
import { PrivateRoute } from '@/router/privateRoutes'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/courses"
        element={
          <PrivateRoute>
            <CourseListPage />
          </PrivateRoute>
        }
      />
    </Routes>
  )
}
```

## 样式开发

### Tailwind CSS

项目使用 Tailwind CSS 进行样式开发：

```tsx
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow">
  <h2 className="text-xl font-semibold text-gray-900">标题</h2>
  <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
    按钮
  </button>
</div>
```

### Ant Design 组件

```tsx
import { Button, Table, Modal } from 'antd'
import { UserOutlined } from '@ant-design/icons'

function MyComponent() {
  return (
    <Button type="primary" icon={<UserOutlined />}>
      点击
    </Button>
  )
}
```

## 构建和部署

### 构建优化

```bash
# 构建
pnpm build

# 输出目录：dist/
```

### Docker 部署

```dockerfile
FROM node:20-alpine as builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 环境变量

生产环境需要配置以下环境变量：

```bash
VITE_API_URL=https://api.panda-system.com/api
```

## 故障排查

### 常见问题

1. **无法连接后端 API**
   - 检查 `.env` 中的 `VITE_API_URL` 配置
   - 确认后端服务已启动
   - 检查浏览器控制台的网络请求

2. **路由跳转异常**
   - 确认使用了 `react-router-dom` 的 `Link` 组件
   - 检查路由配置是否正确
   - 查看浏览器控制台是否有错误

3. **组件样式丢失**
   - 确认 `tailwind.config.js` 配置正确
   - 检查是否正确引入 `index.css`
   - 清除缓存重新构建

4. **状态管理失效**
   - 检查 Zustand store 是否正确导入
   - 确认组件是否使用了正确的 selector
   - 查看浏览器 DevTools 中的状态

### 开发工具

- **React Developer Tools** - React 组件调试
- **Redux DevTools** - Zustand 状态调试（支持）
- **网络面板** - API 请求调试

## 性能优化

### 代码分割

```tsx
import { lazy, Suspense } from 'react'

const EvaluationReportPage = lazy(() => import('./pages/EvaluationReportPage'))

function App() {
  return (
    <Suspense fallback={<div>加载中...</div>}>
      <EvaluationReportPage />
    </Suspense>
  )
}
```

### 图片优化

使用 Vite 的 `?url` 导入图片：

```tsx
import logoUrl from '@/assets/logo.png?url'

<img src={logoUrl} alt="Logo" />
```

## 相关文档

- [React 文档](https://react.dev/)
- [TypeScript 文档](https://www.typescriptlang.org/docs/)
- [Vite 文档](https://vite.dev/)
- [Ant Design 文档](https://ant.design/)
- [Tailwind CSS 文档](https://tailwindcss.com/)
- [Zustand 文档](https://zustand-demo.pmnd.rs/)

## 许可证

Copyright © 2026 PANDA Team. All rights reserved.