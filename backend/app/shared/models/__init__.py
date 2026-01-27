"""
共享数据模型模块
引用原有 models 模块
"""
from backend.app.models.user import User
from backend.app.models.course import Course
from backend.app.models.scenario import Scenario
from backend.app.models.chat import ChatSession, ChatMessage
from backend.app.models.evaluation import EvaluationReport
from backend.app.models.progress import UserProgress

__all__ = [
    "User",
    "Course",
    "Scenario",
    "ChatSession",
    "ChatMessage",
    "EvaluationReport",
    "UserProgress"
]
