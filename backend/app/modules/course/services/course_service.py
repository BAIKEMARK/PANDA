"""
课程服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.models.course import Course
from backend.app.modules.course.schemas.course import CourseCreate, CourseUpdate
from backend.app.modules.course.repositories.course_repository import CourseRepository
from backend.app.core.common.exceptions import NotFoundException
from backend.app.modules.admin.services.permission_service import PermissionService


class CourseService:
    """课程服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = CourseRepository(db)
        self.permission_service = PermissionService(db)

    def create_course(self, course_data: CourseCreate) -> Course:
        """创建新课程"""
        return self.repository.create_course(course_data)

    def get_course(self, course_id: str) -> Optional[Course]:
        """获取课程"""
        return self.repository.get_course(course_id)

    def get_courses(
        self, 
        level: Optional[str] = None, 
        user_role: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> List[Course]:
        """获取课程列表
        
        Args:
            level: 课程层级筛选
            user_role: 用户角色，如果为'student'则只返回已发布的课程
            user_id: 用户ID，用于权限过滤
        """
        status = None
        if user_role == "student":
            status = "published"
        
        # 获取用户权限信息
        is_super_admin = False
        user_orgs = []
        if user_id:
            is_super_admin = self.permission_service.is_super_admin(user_id)
            user_orgs = self.permission_service.get_user_orgs(user_id)
        
        if level:
            return self.repository.get_courses_by_level(
                level, 
                status=status,
                user_id=user_id,
                user_orgs=user_orgs,
                is_super_admin=is_super_admin
            )
        return self.repository.get_courses(
            status=status,
            user_id=user_id,
            user_orgs=user_orgs,
            is_super_admin=is_super_admin
        )

    def update_course(self, course_id: str, course_data: CourseUpdate) -> Optional[Course]:
        """更新课程"""
        db_course = self.get_course(course_id)
        if not db_course:
            raise NotFoundException("课程不存在")
        return self.repository.update_course(db_course, course_data)

    def delete_course(self, course_id: str) -> bool:
        """删除课程"""
        db_course = self.repository.delete_course(course_id)
        return db_course is not None
