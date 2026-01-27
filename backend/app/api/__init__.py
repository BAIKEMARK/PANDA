"""
API Package
API路由包 - Controller层（仅保留未迁移的路由）
"""
from .health import router as health_router

__all__ = [
    "health_router",
]
