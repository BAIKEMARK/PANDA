"""
Main Application Entry Point
FastAPI 主应用程序入口 - 标准MVC架构
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.proxy import setup_proxy
from backend.app.db.database import init_database

# 导入所有API路由（Controller层）
from backend.app.api import (
    health_router,
    user_router,
    course_router,
    scenario_router,
    chat_router
)
from backend.app.api.auth import router as auth_router


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

# 注册所有路由
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(course_router, prefix="/api")
app.include_router(scenario_router, prefix="/api")
app.include_router(chat_router, prefix="/api")


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
        "structure": "标准MVC架构 (backend/app/api/ -> backend/app/services/ -> backend/app/crud/ -> backend/app/models/)"
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

    # 显示代理配置
    if settings.HTTP_PROXY or settings.HTTPS_PROXY:
        print(f"\n🌐 代理配置:")
        if settings.HTTP_PROXY:
            print(f"   HTTP:  {settings.HTTP_PROXY}")
        if settings.HTTPS_PROXY:
            print(f"   HTTPS: {settings.HTTPS_PROXY}")
    else:
        print(f"\n🌐 代理: 未配置 (直连)")

    # 显示AI配置
    if settings.AI_TEXT_KEY:
        print(f"\n🤖 AI配置:")
        print(f"   模型: {settings.AI_TEXT_MODEL}")
        print(f"   状态: ✅ 已配置")
    else:
        print(f"\n🤖 AI配置: ⚠️  未配置")

    # 显示MVC架构信息
    print(f"\n🏗️  MVC架构:")
    print(f"   Controller (api/): {len([user_router, course_router, scenario_router, chat_router])} 个路由模块")
    print(f"   Service (services/): 4 个服务模块")
    print(f"   CRUD (crud/): 4 个CRUD模块")
    print(f"   Model (models/): 5 个ORM模型")
    print(f"   Schema (schemas/): 4 个DTO模型")

    print("="*70 + "\n")

    # 设置代理
    setup_proxy()

    # 测试数据库连接
    init_database()


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
