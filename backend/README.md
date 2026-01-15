# 快速开始指南

## 项目已按照开发规则重构为标准MVC架构

### 新的项目结构

```
backend/
├── app/
│   ├── api/             # Controller层 - FastAPI路由
│   ├── core/            # 配置与安全
│   ├── crud/            # Model层 - 基础CRUD操作
│   ├── models/          # Model层 - SQLAlchemy ORM
│   ├── schemas/         # Model层 - Pydantic DTO
│   ├── services/        # Model层 - 业务逻辑
│   ├── db/              # 数据库会话
│   ├── common/          # 公共模块
│   └── main.py          # 应用入口
├── tests/               # Pytest测试
└── requirements.txt
```

### 启动方式

```bash
# 后端启动
cd backend/app
python main.py

# 或使用uvicorn
cd backend
uvicorn app.main:app --reload
```

### API文档

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### 6A 工作流

所有开发任务请遵循 `docs/开发规则.md` 中定义的6A工作流：
1. Align (对齐)
2. Architect (架构)
3. Atomize (原子化)
4. Approve (审批)
5. Automate (自动化执行)
6. Assess (评估)

### 下一步工作

1. 从旧app/目录迁移具体的业务代码
2. 创建models/中的ORM模型
3. 创建crud/中的CRUD操作
4. 创建api/中的路由
5. 迁移services/中的业务逻辑
