# MVP开发

这份 **MVP 开发任务流程** 是专门为 **3人团队 + Vibe Coding (AI辅助编程)** 模式定制的。

## 👥 人员角色分配 (3人团队)
为了最高效协作，建议采用**全栈思维**，但侧重分明：
| 角色                          | 代号    | 核心职责                                                     | 技能侧重                          | AI 工具重点                               |
| :---------------------------- | :------ | :----------------------------------------------------------- | :-------------------------------- | :---------------------------------------- |
| **产品 & 后端 AI 核心负责人** | **P-A** | 1. 数据库 Schema 设计<br>2. **Python FastAPI 开发**<br>3. **Agent Prompt 编排** (核心！)<br>4. 对接大模型 API | Python, Prompt Engineering, MySQL | AI 生成 API 接口、SQL 语句、Prompt 优化   |
| **前端全栈负责人**            | **P-B** | 1. React + Vite 项目搭建与配置<br>2. **前端页面开发** (聊天窗、报告页)<br>3. API 对接与状态管理<br>4. 部署上线 | React, Vite, Tailwind CSS, TypeScript | AI 生成 React 组件、页面布局、API Client  |
| **内容 & 测试集成负责人**     | **P-C** | 1. **撰写 PRD 与 Prompt 模板** (THP知识)<br>2. 准备课程数据与 Case 脚本<br>3. **黑盒测试与 Prompt 调优**<br>4. 项目管理与进度追踪 | 医疗背景/逻辑梳理, 测试           | AI 生成测试用例、润色文档、生成 Mock 数据 |
---
## 🗓️ 4周 MVP 开发任务流程图
### Phase 1: 架构搭建与数据底座 (Day 1-5)
**目标**：跑通 React + Vite + Python + MySQL 的环境，定义好数据结构。
| 任务               | 负责人    | AI 辅助操作                                                  | 交付物                               |
| :----------------- | :-------- | :----------------------------------------------------------- | :----------------------------------- |
| **1.1 环境初始化** | P-B       | 指令：`Create a React + Vite project with TypeScript and Tailwind CSS.` <br> 指令：`Set up a Python FastAPI project structure.` | 可运行的前后端空项目                 |
| **1.2 数据库设计** | P-A       | 指令：`Generate Prisma Schema for a medical training system... (粘贴上文表结构)` | `schema.prisma` 文件                 |
| **1.3 建库与联调** | P-A & P-B | 指令：`Generate SQL to create tables...` <br> 指令：`Create a React service to test DB connection.` | 前端能成功从 MySQL 读/写一条测试数据 |
| **1.4 基础组件库** | P-B       | 指令：`Generate a responsive layout with Sidebar and Header using Shadcn UI.` | 通用 Layout 组件                     |
| **1.5 内容准备**   | P-C       | 独立工作：整理 THP 核心理论 Markdown 文档；编写 3 个场景的初步 Prompt。 | 3份 MD 文档，3个 Prompt 草稿         |
---
### Phase 2: 课程学习与 Agent 原型 (Day 6-12)
**目标**：完成理论学习模块，并跑通第一个“傻瓜版”AI对话。
| 任务                      | 负责人    | AI 辅助操作                                                  | 交付物                     |
| :------------------------ | :-------- | :----------------------------------------------------------- | :------------------------- |
| **2.1 课程展示页**        | P-B       | 指令：`Create a markdown viewer component using react-markdown.` | 课程阅读页面               |
| **2.2 进度管理逻辑**      | P-A       | 指令：`Write a Prisma query to update course progress.`      | 学习进度解锁功能           |
| **2.3 Python Agent 基础** | P-A       | 指令：`Create a FastAPI endpoint `/chat` that accepts message and history, calls OpenAI API, and returns response.` | 能回复的 Python 接口       |
| **2.4 聊天前端UI**        | P-B       | 指令：`Create a chat interface UI with input box and message bubbles.` | 聊天界面（未接后端）       |
| **2.5 前后端联调 (M1)**   | P-B & P-A | 手动联调：确保前端发消息，Python 能调通 LLM 并返回。         | **里程碑1：能聊天的 Demo** |
---
### Phase 3: 深度开发与业务逻辑 (Day 13-19)
**目标**：引入医疗场景逻辑（EPDS量表、角色扮演、Prompt 调优）。
| 任务                      | 负责人    | AI 辅助操作                                                  | 交付物                   |
| :------------------------ | :-------- | :----------------------------------------------------------- | :----------------------- |
| **3.1 Prompt 编排与入库** | P-C & P-A | 指令：`Refine this system prompt for a postpartum depression patient...` <br> 动作：将 Prompt 存入 MySQL `scenarios` 表。 | 带有真实人设的数据库记录 |
| **3.2 Agent 逻辑升级**    | P-A       | 指令：`Update `/chat` endpoint to fetch system prompt from DB based on session_id.` | 动态切换不同病人的 Agent |
| **3.3 EPDS 量表交互**     | P-B       | 指令：`Create a form component with 10 radio buttons for EPDS scale.` | 量表答题组件             |
| **3.4 评估逻辑开发**      | P-A       | 指令：`Write a prompt to analyze conversation history and output JSON score for empathy and skills.` | Python `/evaluate` 接口  |
| **3.5 报告页开发**        | P-B       | 指令：`Create a radar chart component using Recharts based on JSON data.` | 评分展示页面             |
---
### Phase 4: 优化、测试与部署 (Day 20-28)
**目标**：打磨细节，修复 Bug，准备 Demo 演示。
| 任务                   | 负责人    | AI 辅助操作                                                  | 交付物                    |
| :--------------------- | :-------- | :----------------------------------------------------------- | :------------------------ |
| **4.1 流式传输优化**   | P-A & P-B | 指令：`Implement Server-Sent Events (SSE) in FastAPI for streaming response.` | 打字机效果的对话体验      |
| **4.2 安全与边界测试** | P-C       | 动作：模拟攻击性对话（如劝药、辱骂），检查 Agent 是否有正确兜底回复。 | 修复后的 Prompt 版本 v2.0 |
| **4.3 UI/UX 美化**     | P-B       | 指令：`Improve the styling of the chat interface to look more professional.` | 精修后的界面              |
| **4.4 部署上线**       | P-A       | 指令：`Generate a Dockerfile for this FastAPI app.` <br> 动作：部署服务器 (Vercel + Railway/阿里云)。 | 公网可访问的 URL          |
| **4.5 最终验收**       | 全员      | 模拟真实用户走完：注册 -> 学习 -> 模拟 -> 查报告 全流程。    | **MVP 1.0 版本发布**      |
---
## 💡 Vibe Coding 协作规范 (团队公约)
为了确保三个人用 AI 写代码不冲突，请遵守以下公约：
### 1. Prompt 驱动开发
*   **不要手写 Boilerplate**：任何数据库 Model、API 基础代码、React 基础组件，优先让 AI 生成。
*   **Prompt 要具体**：
    *   ❌ *Bad:* "帮我写个聊天框。"
    *   ✅ *Good:* "Create a chat interface component using Tailwind CSS. It should have a fixed header, a scrollable message area (user right, bot left), and a fixed bottom input area."
### 2. Git 分支策略

- 一人一个分支,每天晚上10点前提交分支

*   `main`: 稳定版本，随时可部署。
*   `feature/backend-ai`: P-A 专用，搞 Python 和 Agent。
*   `feature/frontend-ui`: P-B 专用，搞 React 和页面。
*   `feature/content-db`: P-C 专用，更新 SQL 脚本和配置。
### 3. 接口先行
*   **原则**：P-B 写前端时，如果 P-A 的接口还没写好，**先用 Mock 数据 (假数据)** 把页面跑通。
*   AI 辅助指令：`Generate mock data for this user profile object.`
### 4. 代码审查
*   AI 生成的代码**不要直接 Ctrl+C/V 进主分支**。
*   每个人合并代码前，必须让另一个人看一眼（尤其是 AI 生成的复杂 SQL 和 Prompt 逻辑）。
### 5. 每日站会 (10分钟)
*   **P-A**: "Agent 的 Prompt 昨天调优了，现在情绪识别准了。"
*   **P-B**: "课程页做好了，今天准备搞聊天窗的流式传输。"
*   **P-C**: "我发现 Case 2 的剧本有点问题，AI 容易跑题，我改好了 Prompt，A 你更新一下 DB。"