"""
Common Constants Module
常量定义模块
"""
from enum import Enum


class UserRole(str, Enum):
    """用户角色枚举"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class CourseLevel(str, Enum):
    """课程层级枚举"""
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"


class SessionStatus(str, Enum):
    """会话状态枚举"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class MessageRole(str, Enum):
    """消息角色枚举"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
