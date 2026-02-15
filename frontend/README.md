# PANDA 前端项目

**围产期抑郁管理智能培训系统 - React 前端应用**

基于 React 19 + TypeScript + Vite 构建的现代化单页应用。

---

## 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| **框架** | React 19 + TypeScript | UI 框架 + 类型安全 |
| **构建** | Vite 7 | 快速构建工具 |
| **路由** | React Router v7 | 路由管理 |
| **UI库** | Ant Design 6 | 企业级组件库 |
| **样式** | Tailwind CSS 4 | 原子化 CSS |
| **状态** | Zustand | 轻量级状态管理 |
| **HTTP** | Axios | 请求库 |
| **图表** | Recharts | 数据可视化 |

---

## 项目结构

```
frontend/src/
├── components/              # 可复用组件
│   ├── chat/               # 对话组件
│   ├── course/             # 课程组件
│   ├── evaluation/         # 评估组件
│   └── layout/             # 布局组件
├── pages/                  # 页面组件
│   ├── LoginPage.tsx       # 登录页
│   ├── CourseListPage.tsx  # 课程列表
│   ├── ChatPage.tsx        # 对话页面
│   ├── EvaluationReportPage.tsx  # 评估报告
│   └── ProfilePage.tsx     # 个人中心
├── services/               # API 服务层
├── stores/                 # Zustand 状态管理
├── types/                  # TypeScript 类型
└── router/                 # 路由配置
```

---

## 核心功能

### 1. 认证模块
- 用户登录/注册
- JWT Token 管理
- 路由守卫

### 2. 课程模块
- 课程列表展示
- THP 层级筛选
- 学习进度跟踪

### 3. 场景模拟模块
- 训练场景列表
- 难度筛选
- 场景详情查看

### 4. 对话交互模块
- 创建对话会话
- 实时消息收发
- AI 对话交互
- 危机状态提醒

### 5. 评估报告模块
- THP 五维评分展示
- 雷达图可视化
- 详细反馈信息

### 6. 个人中心模块
- 用户信息管理
- 学习进度统计
- 账户设置

### 7. 动态菜单模块
- 基于角色的菜单加载
- 支持层级菜单结构
- 图标自动映射

---

## 路由配置

### 公开路由

| 路径 | 组件 |
|------|------|
| `/login` | LoginPage |
| `/register` | RegisterPage |

### 私有路由

| 路径 | 组件 |
|------|------|
| `/` | CourseListPage |
| `/courses/:id` | CourseDetailPage |
| `/scenarios` | ScenarioListPage |
| `/chat` | ChatPage |
| `/evaluation/:sessionId` | EvaluationReportPage |
| `/profile` | ProfilePage |

---

## 状态管理

### Zustand Stores

```typescript
// auth.store.ts - 认证状态
interface AuthStore {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

// chat.store.ts - 对话状态
interface ChatStore {
  currentSession: ChatSession | null
  messages: ChatMessage[]
  sendMessage: (content: string) => Promise<void>
}

// course.store.ts - 课程状态
interface CourseStore {
  courses: Course[]
  fetchCourses: (level?: string) => Promise<void>
}
```

---

## 环境配置

### 环境变量 (.env)

```bash
# API 地址
VITE_API_URL=http://localhost:8000/api

# 应用标题
VITE_APP_TITLE=PANDA 围产期抑郁管理智能培训系统
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
# 编辑 .env 文件
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 4. 构建生产版本

```bash
npm run build
```

---

## 开发规范

### 代码风格

```bash
# 运行 ESLint
npm run lint
```

### 组件规范

1. **函数式组件** + Hooks
2. **TypeScript** 定义 Props 类型
3. **命名规范**：
   - 组件：`PascalCase`
   - 函数：`camelCase`
   - 常量：`UPPER_SNAKE_CASE`

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
```

---

## 主要组件示例

### 对话组件

```tsx
import { ChatWindow } from '@/components/chat/ChatWindow'

<ChatWindow
  sessionId="session-123"
  onEndSession={(id) => console.log('会话结束:', id)}
/>
```

### 评估报告组件

```tsx
import { RadarChart } from '@/components/evaluation/RadarChart'

<RadarChart
  scores={{
    riskIdentification: 85,
    communicationSupport: 78,
    skillApplication: 82,
    safetyManagement: 90,
    selfEfficacy: 75
  }}
/>
```

---

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| 无法连接后端 | 检查 `VITE_API_URL` 配置 |
| 路由跳转异常 | 检查路由配置是否正确 |
| 组件样式丢失 | 确认 `tailwind.config.js` 配置正确 |
| 状态管理失效 | 检查 Zustand store 导入是否正确 |

---

## 相关文档

- [React 文档](https://react.dev/)
- [TypeScript 文档](https://www.typescriptlang.org/docs/)
- [Vite 文档](https://vite.dev/)
- [Ant Design 文档](https://ant.design/)
- [Zustand 文档](https://zustand-demo.pmnd.rs/)

---

## 许可证

Copyright © 2026 PANDA Team. All rights reserved.