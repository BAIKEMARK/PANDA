"""
Schemas Module Init
Pydantic 数据模型初始化
"""
from .user import UserBase, UserCreate, UserLogin, UserUpdate, UserResponse, Token
from .course import CourseBase, CourseCreate, CourseUpdate, CourseResponse
from .scenario import ScenarioBase, ScenarioCreate, ScenarioUpdate, ScenarioResponse
from .chat import ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse

__all__ = [
    # 用户相关
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    "Token",
    # 课程相关
    "CourseBase",
    "CourseCreate",
    "CourseUpdate",
    "CourseResponse",
    # 场景相关
    "ScenarioBase",
    "ScenarioCreate",
    "ScenarioUpdate",
    "ScenarioResponse",
    # 对话相关
    "ChatSessionCreate",
    "ChatSessionResponse",
    "ChatMessageCreate",
    "ChatMessageResponse",
]
