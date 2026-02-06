"""
Health Check API Router
健康检查API路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.db.database import get_db
from backend.app.core.config.settings import settings

router = APIRouter(tags=["系统"])


@router.get("/health")
async def health_check():
    """基础健康检查"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """详细健康检查"""
    health_info = {
        "status": "healthy",
        "app": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "debug": settings.DEBUG
        },
        "database": {"status": "unknown"},
        "ai_configured": bool(settings.AI_TEXT_KEY)
    }

    # 测试数据库连接
    try:
        db.execute(text("SELECT 1"))
        health_info["database"] = {"status": "connected"}
    except Exception as e:
        health_info["database"] = {"status": "error", "message": str(e)}

    return health_info
