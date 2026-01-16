"""
API Package
API路由包 - Controller层
"""
from .health import router as health_router
from .auth import router as auth_router
from .users import router as user_router
from .courses import router as course_router
from .scenarios import router as scenario_router
from .chat import router as chat_router

__all__ = [
    "health_router",
    "auth_router",
    "user_router",
    "course_router",
    "scenario_router",
    "chat_router",
]
