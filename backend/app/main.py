"""
Main Application Entry Point
FastAPI 主应用程序入口 - 分层模块化架构
"""
import logging
import re

# 自定义日志格式化器：将 Unicode 转义序列解码为中文
class UnicodeFormatter(logging.Formatter):
    """自定义格式化器，将日志中的 Unicode 转义序列解码为可读中文"""
    def format(self, record):
        message = super().format(record)
        # 将 \uXXXX 转义序列解码为实际字符
        try:
            message = message.encode('utf-8').decode('unicode_escape')
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass  # 如果解码失败，保持原样
        return message

# 配置详细日志（包括 LangChain 和 HTTP 请求）
handler = logging.StreamHandler()
handler.setFormatter(UnicodeFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[handler]
)

# LangChain 日志
langchain_logger = logging.getLogger("langchain")
langchain_logger.setLevel(logging.DEBUG)

# HTTP 客户端日志（显示完整 API 请求）
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.INFO)

# HTTP core 日志
httpcore_logger = logging.getLogger("httpcore")
httpcore_logger.setLevel(logging.INFO)

# OpenAI 客户端日志（应用 Unicode 解码）
openai_logger = logging.getLogger("openai")
openai_logger.handlers = [handler]

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config.config import settings
from backend.app.db.database import init_database, get_db

# 导入所有API路由（新的模块化架构）
from backend.app.api import health_router

# 认证与用户模块
from backend.app.modules.auth.api.routers import auth_router, users_router

# 课程模块
from backend.app.modules.course.api.routers import router as course_router

# 情景模拟模块
from backend.app.modules.scenario.api.routers import router as scenario_router

# 对话交互模块
from backend.app.modules.chat.api.routers import router as chat_router

# 评估系统模块
from backend.app.modules.evaluation.api.routers import router as evaluation_router

# 学习进度模块
from backend.app.modules.progress.api.routers import router as progress_router

# 菜单管理模块
from backend.app.modules.menu.api.routers import router as menu_router


# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("="*70)
    print(f"📖 API文档: http://localhost:8000/api/docs")
    print(f"🔧 ReDoc文档: http://localhost:8000/api/redoc")
    print(f"🔧 调试模式: {settings.DEBUG}")

    # 显示数据库配置
    print(f"\n📊 数据库配置:")
    print(f"   主机: {settings.DB_HOST}:{settings.DB_PORT}")
    print(f"   数据库: {settings.DB_NAME}")

    # 显示AI配置
    if settings.AI_TEXT_KEY:
        print(f"\n🤖 AI配置:")
        print(f"   模型: {settings.AI_TEXT_MODEL}")
        print(f"   框架: LangChain")
        print(f"   状态: ✅ 已配置")
    else:
        print(f"\n🤖 AI配置: ⚠️  未配置")

    print("="*70 + "\n")

    # 测试数据库连接
    init_database()

    # 初始化评估智能体以订阅事件
    from backend.app.modules.evaluation.agents.mentor_agent import MentorAgent
    db_gen = get_db()
    db = next(db_gen)
    try:
        mentor_agent = MentorAgent(db)
        print(f"✅ MentorAgent 已初始化并订阅事件")
    except Exception as e:
        print(f"⚠️  MentorAgent 初始化失败: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("\n" + "="*70)
    print("👋 应用正在关闭...")
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
