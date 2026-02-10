# PANDA 前端项目

**围产期抑郁管理智能培训系统 - React 前端应用**

基于 **React 19** + **TypeScript** + **Vite** 构建的现代化单页应用（SPA），采用 **Ant Design** 组件库和 **Tailwind CSS** 进行 UI 开发。

---

## 技术栈

### 核心框架

| 技术 | 版本 | 用途 |
|------|------|------|
| **React** | 19.2.0 | UI 框架 |
| **TypeScript** | 5.9.3 | 类型安全 |
| **Vite** | 7.2.4 | 构建工具 |
| **React Router** | 7.12.0 | 路由管理 |

### UI 框架

| 技术 | 版本 | 用途 |
|------|------|------|
| **Ant Design** | 6.2.0 | 企业级 UI 组件库 |
| **@ant-design/icons** | 6.1.0 | 图标库 |
| **Tailwind CSS** | 4.1.18 | 原子化 CSS 框架 |
| **React Hot Toast** | 2.6.0 | 消息提示 |

### 状态管理

| 技术 | 版本 | 用途 |
|------|------|------|
| **Zustand** | 5.0.10 | 轻量级状态管理 |

### 数据可视化

| 技术 | 版本 | 用途 |
|------|------|------|
| **Recharts** | 3.6.0 | 图表库（雷达图等） |

### HTTP 与动画

| 技术 | 版本 | 用途 |
|------|------|------|
| **Axios** | 1.13.2 | HTTP 请求库 |
| **Framer Motion** | 11.15.0 | 动画库 |
| **GSAP** | 3.12.5 | 高性能动画 |

---

## 项目结构

```
frontend/
├── src/                              # 源代码目录
│   ├── main.tsx                      # 应用入口
│   ├── App.tsx                       # 应用根组件
│   ├── index.css                     # 全局样式
│   │
│   ├── pages/                        # 页面组件
│   │   ├── LoginPage.tsx             # 登录页
│   │   ├── RegisterPage.tsx          # 注册页
│   │   ├── CourseListPage.tsx        # 课程列表
│   │   ├── CourseDetailPage.tsx      # 课程详情
│   │   ├── ScenarioListPage.tsx      # 场景列表
│   │   ├── ChatPage.tsx              # 对话页面
│   │   ├── EvaluationReportPage.tsx  # 评估报告
│   │   ├── LearningDashboardPage.tsx # 学习仪表板
│   │   ├── ProfilePage.tsx           # 个人中心
│   │   └── NotFoundPage.tsx          # 404页面
│   │
│   ├── admin/                        # 管理端模块
│   │   ├── pages/                    # 管理端页面
│   │   │   ├── UserManagePage.tsx    # 用户管理
│   │   │   ├── OrganizationPage.tsx  # 机构管理
│   │   │   ├── TrainingClassPage.tsx # 班级管理
│   │   │   ├── RoleManagePage.tsx    # 角色管理
│   │   │   ├── MenuManagePage.tsx    # 菜单管理
│   │   │   ├── QuestionBankPage.tsx  # 题库管理
│   │   │   ├── CertificatePage.tsx   # 证书管理
│   │   │   └── CourseManagePage.tsx  # 课程管理
│   │   └── components/               # 管理端组件
│   │
│   ├── components/                   # 可复用组件
│   │   ├── layout/                   # 布局组件
│   │   │   ├── AppLayout.tsx         # 应用布局
│   │   │   ├── Header.tsx            # 顶部导航
│   │   │   └── Sidebar.tsx           # 侧边栏（动态菜单）
│   │   ├── chat/                     # 对话组件
│   │   │   ├── ChatInput.tsx         # 聊天输入框
│   │   │   ├── ChatWindow.tsx        # 聊天窗口
│   │   │   └── MessageBubble.tsx     # 消息气泡
│   │   ├── course/                   # 课程组件
│   │   │   ├── CourseCard.tsx        # 课程卡片
│   │   │   └── LevelFilter.tsx       # 层级筛选器
│   │   ├── scenario/                 # 场景组件
│   │   │   └── ScenarioCard.tsx      # 场景卡片
│   │   └── evaluation/               # 评估组件
│   │       ├── RadarChart.tsx        # 雷达图
│   │       ├── ScoreCard.tsx         # 评分卡片
│   │       └── FeedbackSection.tsx   # 反馈区域
│   │
│   ├── router/                       # 路由配置
│   │   ├── index.ts                 # 路由导出
│   │   └── index.tsx                # 路由定义
│   │
│   ├── services/                     # API 服务层
│   │   ├── api.ts                   # Axios 实例配置
│   │   ├── auth.service.ts          # 认证服务
│   │   ├── chat.service.ts          # 对话服务
│   │   ├── course.service.ts        # 课程服务
│   │   ├── scenario.service.ts      # 场景服务
│   │   ├── evaluation.service.ts    # 评估服务
│   │   ├── progress.service.ts      # 进度服务
│   │   └── menu.service.ts          # 菜单服务（动态菜单）
│   │
│   ├── stores/                       # Zustand 状态管理
│   │   ├── auth.store.ts            # 认证状态
│   │   ├── chat.store.ts            # 对话状态
│   │   ├── course.store.ts          # 课程状态
│   │   ├── menu.store.ts            # 菜单状态（动态菜单）
│   │   └── ui.store.ts              # UI 状态
│   │
│   ├── types/                        # TypeScript 类型定义
│   │   ├── index.ts                 # 类型导出
│   │   ├── auth.types.ts            # 认证类型
│   │   ├── chat.types.ts            # 对话类型
│   │   ├── course.types.ts          # 课程类型
│   │   ├── scenario.types.ts        # 场景类型
│   │   ├── evaluation.types.ts      # 评估类型
│   │   └── menu.types.ts            # 菜单类型
│   │
│   ├── hooks/                        # 自定义 Hooks
│   │   ├── useAuth.ts               # 认证 Hook
│   │   ├── useChat.ts               # 对话 Hook
│   │   └── useRouter.ts             # 路由 Hook
│   │
│   └── utils/                        # 工具函数
│       ├── format.ts                # 格式化工具
│       └── validation.ts            # 验证工具
│
├── public/                           # 静态资源
│   └── vite.svg                     # Vite 图标
│
├── .env.example                      # 环境变量示例
├── package.json                      # 项目依赖
├── vite.config.ts                    # Vite 配置
├── tailwind.config.js                # Tailwind CSS 配置
└── tsconfig.json                     # TypeScript 配置
```

---

## 核心功能模块

### 1. 认证模块

**组件**：`pages/LoginPage.tsx`, `pages/RegisterPage.tsx`

**状态管理**：`stores/auth.store.ts`

**服务**：`services/auth.service.ts`

**功能**：
- 用户登录/注册
- JWT Token 管理
- 自动登录
- 路由守卫

### 2. 课程模块

**组件**：`pages/CourseListPage.tsx`, `pages/CourseDetailPage.tsx`

**可复用组件**：`components/course/CourseCard.tsx`, `components/course/LevelFilter.tsx`

**状态管理**：`stores/course.store.ts`

**服务**：`services/course.service.ts`

**功能**：
- 课程列表展示（支持按 THP 层级筛选）
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
- 启动对话会话

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
- 自杀风险报警

### 5. 评估报告模块

**组件**：`pages/EvaluationReportPage.tsx`

**可复用组件**：`components/evaluation/RadarChart.tsx`, `components/evaluation/ScoreCard.tsx`, `components/evaluation/FeedbackSection.tsx`

**服务**：`services/evaluation.service.ts`

**功能**：
- THP 五维评分展示
- 雷达图可视化
- 详细反馈信息
- 评分建议

### 6. 学习仪表板

**组件**：`pages/LearningDashboardPage.tsx`

**服务**：`services/progress.service.ts`

**功能**：
- 学习进度统计
- 课程完成情况
- 场景训练记录
- 评估历史查看

### 7. 菜单权限模块

**组件**：`components/layout/Sidebar.tsx`（动态菜单加载）

**状态管理**：`stores/menu.store.ts`

**服务**：`services/menu.service.ts`

**类型定义**：`types/menu.types.ts`

**功能**：
- 基于用户角色动态加载菜单
- 支持层级菜单结构
- 图标映射（数据库图标名 → React 组件）

**角色类型**：`student`（学生）, `instructor`（讲师）, `admin`（管理员）

### 8. 管理端模块 (admin/)

**职责**：系统管理功能（仅管理员可访问）

**页面**：
- `UserManagePage.tsx` - 用户管理
- `OrganizationPage.tsx` - 机构管理
- `TrainingClassPage.tsx` - 班级管理
- `RoleManagePage.tsx` - 角色管理
- `MenuManagePage.tsx` - 菜单管理
- `QuestionBankPage.tsx` - 题库管理
- `CertificatePage.tsx` - 证书管理
- `CourseManagePage.tsx` - 课程管理

---

## 路由配置

### 公开路由

| 路径 | 组件 | 说明 |
|------|------|------|
| `/login` | LoginPage | 登录页 |
| `/register` | RegisterPage | 注册页 |

### 私有路由（需要认证）

| 路径 | 组件 | 说明 |
|------|------|------|
| `/` | LearningDashboardPage | 学习仪表板（首页） |
| `/courses` | CourseListPage | 课程列表 |
| `/courses/:id` | CourseDetailPage | 课程详情 |
| `/scenarios` | ScenarioListPage | 场景列表 |
| `/chat/:sessionId` | ChatPage | 对话页面 |
| `/evaluation/:sessionId` | EvaluationReportPage | 评估报告 |
| `/profile` | ProfilePage | 个人中心 |

### 管理端路由（需要管理员权限）

| 路径 | 组件 | 说明 |
|------|------|------|
| `/admin/users` | UserManagePage | 用户管理 |
| `/admin/organizations` | OrganizationPage | 机构管理 |
| `/admin/classes` | TrainingClassPage | 班级管理 |
| `/admin/roles` | RoleManagePage | 角色管理 |
| `/admin/menus` | MenuManagePage | 菜单管理 |
| `/admin/questions` | QuestionBankPage | 题库管理 |
| `/admin/certificates` | CertificatePage | 证书管理 |
| `/admin/courses` | CourseManagePage | 课程管理 |

---

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

// menu.store.ts - 菜单状态（动态菜单）
interface MenuStore {
  menus: MenuItem[]
  userMenus: MenuItem[]
  fetchMenus: () => Promise<void>
  fetchUserMenus: () => Promise<void>
}

// ui.store.ts - UI状态
interface UIStore {
  sidebarCollapsed: boolean
  loading: boolean
  toggleSidebar: () => void
  setLoading: (loading: boolean) => void
}
```

---

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
| `progress.service.ts` | 获取学习进度、仪表板数据 |
| `menu.service.ts` | 获取菜单列表、用户菜单 |

---

## 环境配置

### 环境变量 (.env)

```bash
# API 地址
VITE_API_URL=http://localhost:8000/api

# 应用名称
VITE_APP_NAME=PANDA

# 启用流式响应
VITE_ENABLE_STREAMING=true
```

---

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置 API 地址
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问：http://localhost:5173

### 4. 构建生产版本

```bash
npm run build
```

---

## 开发规范

### 代码风格

项目使用 ESLint 进行代码检查：

```bash
npm run lint
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

---

## 样式开发

### Tailwind CSS

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

---

## 相关文档

- [React 文档](https://react.dev/)
- [TypeScript 文档](https://www.typescriptlang.org/docs/)
- [Vite 文档](https://vite.dev/)
- [Ant Design 文档](https://ant.design/)
- [Tailwind CSS 文档](https://tailwindcss.com/)
- [Zustand 文档](https://zustand-demo.pmnd.rs/)

---

## 许可证

Copyright © 2026 PANDA Team. All rights reserved.