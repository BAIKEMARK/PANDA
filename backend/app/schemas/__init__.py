"""
Schemas Module Init
Pydantic 数据模型初始化
"""
from .user import UserBase, UserCreate, UserLogin, UserUpdate, UserResponse, Token
from .course import CourseBase, CourseCreate, CourseUpdate, CourseResponse
from .scenario import ScenarioBase, ScenarioCreate, ScenarioUpdate, ScenarioResponse
from .chat import ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse
from .progress import UserProgressBase, UserProgressCreate, UserProgressUpdate, UserProgressResponse
from .evaluation import RadarChart, StateAnalysis, FeedbackItem, EvaluationReportResponse

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
    # 学习进度相关
    "UserProgressBase",
    "UserProgressCreate",
    "UserProgressUpdate",
    "UserProgressResponse",
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
    # 评估报告相关
    "RadarChart",
    "StateAnalysis",
    "FeedbackItem",
    "EvaluationReportResponse",
]
