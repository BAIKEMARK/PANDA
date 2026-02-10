"""
API Package
API路由包 - 系统级端点
"""
from .health import router as health_router

__all__ = [
    "health_router",
]
