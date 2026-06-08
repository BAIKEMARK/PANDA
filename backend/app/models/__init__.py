"""
ORM Models Package
数据库模型包
"""
from .user import User
from .course import Course
from .scenario import Scenario
from .chat import ChatSession, ChatMessage
from .progress import UserProgress
from .evaluation import EvaluationReport
from .menu import Menu, RoleMenuPermission
from .organization import Organization, Role, Permission, RolePermission, UserOrganization
from .training import TrainingClass, ClassStudent, ClassTask
from .question import QuestionBank
from .audit import AuditLog
from .certificate import Certificate, CertificateTemplate
from .quiz import Quiz, QuizResult

__all__ = [
    "User",
    "Course",
    "UserProgress",
    "Scenario",
    "ChatSession",
    "ChatMessage",
    "EvaluationReport",
    "Menu",
    "RoleMenuPermission",
    "Organization",
    "Role",
    "Permission",
    "RolePermission",
    "UserOrganization",
    "TrainingClass",
    "ClassStudent",
    "ClassTask",
    "QuestionBank",
    "AuditLog",
    "Certificate",
    "CertificateTemplate",
    "Quiz",
    "QuizResult",
]
