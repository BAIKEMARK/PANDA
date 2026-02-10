"""
Health Check API Router
健康检查API路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone

from backend.app.db.database import get_db
from backend.app.core.config.settings import settings
from backend.app.core.services.redis_state_manager import redis_state_manager
from backend.app.core.ai.langchain_manager import langchain_manager

router = APIRouter(tags=["系统"])


@router.get("/health")
async def health_check():
    """基础健康检查"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """详细健康检查 - 检查所有依赖服务"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "app": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "debug": settings.DEBUG
        },
        "services": {}
    }

    # 检查数据库
    try:
        db.execute(text("SELECT 1"))
        health_status["services"]["database"] = {
            "status": "healthy",
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "database": settings.DB_NAME
        }
    except Exception as e:
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"

    # 检查Redis
    try:
        if redis_state_manager.check_health():
            health_status["services"]["redis"] = {
                "status": "healthy",
                "host": settings.REDIS_HOST,
                "port": settings.REDIS_PORT
            }
        else:
            health_status["services"]["redis"] = {
                "status": "unhealthy",
                "error": "Redis ping failed"
            }
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["services"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"

    # 检查AI服务配置
    try:
        if settings.AI_TEXT_KEY:
            llm = langchain_manager.get_llm()
            health_status["services"]["ai"] = {
                "status": "configured",
                "model": settings.AI_TEXT_MODEL,
                "provider": "通义千问"
            }
        else:
            health_status["services"]["ai"] = {
                "status": "not_configured",
                "message": "AI服务未配置"
            }
    except Exception as e:
        health_status["services"]["ai"] = {
            "status": "error",
            "error": str(e)
        }

    return health_status
