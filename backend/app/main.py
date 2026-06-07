"""
Main Application Entry Point
FastAPI 主应用程序入口 - 分层模块化架构
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from backend.app.core.config.settings import settings
from backend.app.db.database import init_database, get_db
from backend.app.core.config.logging import setup_logging, get_logger

# 导入中间件和异常处理器
from backend.app.core.middleware import (
    RequestIDMiddleware,
    global_exception_handler,
    not_found_exception_handler,
    unauthorized_exception_handler,
    forbidden_exception_handler,
    bad_request_exception_handler,
    validation_exception_handler,
    database_exception_handler
)
from backend.app.core.common.exceptions import (
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    BadRequestException
)

# 初始化统一日志配置
setup_logging()
logger = get_logger(__name__)

# 配置第三方库日志级别
logging.getLogger("langchain").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logging.getLogger("httpcore").setLevel(logging.INFO)

# 导入所有API路由（新的模块化架构）
from backend.app.api import health_router

# 认证与用户模块
from backend.app.modules.auth.api.routers import auth_router, users_router

# 课程模块
from backend.app.modules.course.api.routers import router as course_router

# 情景模拟模块
from backend.app.modules.scenario.api.routers import router as scenario_router

# 对话交互模块
from backend.app.modules.conversation.api.routers import router as chat_router

# 评估系统模块
from backend.app.modules.evaluation.api.routers import router as evaluation_router

# 学习进度模块
from backend.app.modules.progress.api.routers import router as progress_router

# 菜单管理模块
from backend.app.modules.menu.api.routers import router as menu_router

# 后台管理模块
from backend.app.modules.admin.api.organization import router as org_router
from backend.app.modules.admin.api.role import router as role_router
from backend.app.modules.admin.api.user import router as user_admin_router
from backend.app.modules.admin.api.training import router as training_router
from backend.app.modules.admin.api.course import router as course_admin_router
from backend.app.modules.admin.api.scenario import router as scenario_admin_router

# 证书管理模块
from backend.app.modules.certificate.api.certificate import router as certificate_router
from backend.app.modules.certificate.api.certificate_template import router as certificate_template_router

# 题库管理模块
from backend.app.modules.question.api.question import router as question_router


# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ================================================
# 配置中间件
# ================================================

# 1. 请求ID追踪中间件（最先执行）
app.add_middleware(RequestIDMiddleware)

# 2. CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================================
# 配置异常处理器
# ================================================

# 自定义业务异常
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)

# 请求验证异常
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 数据库异常
app.add_exception_handler(SQLAlchemyError, database_exception_handler)

# 全局异常处理器（兜底）
app.add_exception_handler(Exception, global_exception_handler)

# 注册所有路由（新的模块化架构）
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(course_router, prefix="/api")
app.include_router(scenario_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(evaluation_router, prefix="/api")
app.include_router(progress_router, prefix="/api")
app.include_router(menu_router, prefix="/api")
app.include_router(org_router, prefix="/api")
app.include_router(role_router, prefix="/api")
app.include_router(user_admin_router, prefix="/api")
app.include_router(training_router, prefix="/api")
app.include_router(course_admin_router, prefix="/api")
app.include_router(scenario_admin_router, prefix="/api")
app.include_router(certificate_router, prefix="/api")
app.include_router(certificate_template_router, prefix="/api")
app.include_router(question_router, prefix="/api")


# ================================================
# 根路径
# ================================================
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/api/docs",
        "redoc": "/api/redoc",
        "structure": "分层模块化架构 (modules/{auth,course,scenario,chat,evaluation,progress}/)"
    }


# ================================================
# 应用启动事件
# ================================================
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("\n" + "="*70)
    print(f"[START] {settings.APP_NAME} v{settings.APP_VERSION}")
    print("="*70)
    print(f"[API文档] http://localhost:8000/api/docs")
    print(f"[ReDoc文档] http://localhost:8000/api/redoc")
    print(f"[调试模式] {settings.DEBUG}")

    # 显示数据库配置
    print(f"\n[数据库配置]")
    print(f"   主机: {settings.DB_HOST}:{settings.DB_PORT}")
    print(f"   数据库: {settings.DB_NAME}")

    # 显示AI配置
    if settings.AI_TEXT_KEY:
        print(f"\n[AI配置]")
        print(f"   模型: {settings.AI_TEXT_MODEL}")
        print(f"   框架: LangChain")
        print(f"   状态: [OK] 已配置")
    else:
        print(f"\n[AI配置] [WARN] 未配置")

    print("="*70 + "\n")

    # 测试数据库连接
    init_database()

    # 初始化评估智能体以订阅事件
    from backend.app.modules.evaluation.agents.mentor_agent import MentorAgent
    db_gen = get_db()
    db = next(db_gen)
    try:
        mentor_agent = MentorAgent(db)
        print(f"[OK] MentorAgent 已初始化并订阅事件")
    except Exception as e:
        print(f"[WARN] MentorAgent 初始化失败: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("\n" + "="*70)
    print("[SHUTDOWN] 应用正在关闭...")
    print("="*70 + "\n")


# ================================================
# 主程序入口
# ================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
