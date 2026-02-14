from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from uuid import uuid4
from datetime import datetime

from backend.app.models.course import Course
from backend.app.core.common.exceptions import NotFoundException
from backend.app.modules.admin.services.permission_service import PermissionService


class CourseAdminService:
    def __init__(self, db: Session):
        self.db = db
        self.permission_service = PermissionService(db)

    def create_course(self, course_data: dict, current_user_id: str) -> Course:
        # 检查shared scope只能由系统级权限设置
        scope = course_data.get("scope", "private")
        if scope == "shared" and not self.permission_service.is_super_admin(current_user_id):
            from backend.app.core.common.exceptions import ForbiddenException
            raise ForbiddenException("只有系统级权限可以设置共享范围")
        
        course = Course(
            id=str(uuid4()),
            title=course_data["title"],
            content_url=course_data.get("content_url"),
            video_url=course_data.get("video_url"),
            sort_order=course_data.get("sort_order", 0),
            level=course_data.get("level", "L1"),
            description=course_data.get("description"),
            org_id=course_data.get("org_id"),
            scope=scope,
            version=course_data.get("version", "1.0.0"),
            version_notes=course_data.get("version_notes"),
            status=course_data.get("status", "draft"),
            created_by=current_user_id
        )
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def get_course(self, course_id: str, current_user_id: str) -> Optional[Course]:
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return None
        
        is_super_admin = self.permission_service.is_super_admin(current_user_id)
        
        if not is_super_admin:
            # 检查权限：private只有创建者可见，platform需要属于该机构，shared全平台可见
            if course.scope == "private":
                if course.created_by != current_user_id:
                    return None
            elif course.scope == "platform":
                user_orgs = self.permission_service.get_user_orgs(current_user_id)
                if course.org_id and course.org_id not in user_orgs:
                    return None
            # shared: 全平台可见，无需额外检查
        
        return course

    def list_courses(
        self,
        current_user_id: str,
        org_id: Optional[str] = None,
        scope: Optional[str] = None,
        status: Optional[str] = None,
        level: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Course], int]:
        from sqlalchemy import or_
        
        query = self.db.query(Course)
        is_super_admin = self.permission_service.is_super_admin(current_user_id)
        
        if not is_super_admin:
            user_orgs = self.permission_service.get_user_orgs(current_user_id)
            
            # 构建权限过滤条件
            conditions = []
            
            # 1. shared: 全平台可见
            conditions.append(Course.scope == "shared")
            
            # 2. platform: 该平台内用户可见
            if user_orgs:
                conditions.append(
                    (Course.scope == "platform") & (Course.org_id.in_(user_orgs))
                )
            
            # 3. private: 只有创建者及更高权限用户可见
            # 对于非超级管理员，只能看到自己创建的private课程
            conditions.append(
                (Course.scope == "private") & (Course.created_by == current_user_id)
            )
            
            # 如果指定了org_id，需要额外检查
            if org_id:
                if org_id not in user_orgs:
                    return [], 0
                # 在权限条件基础上，再过滤org_id
                query = query.filter(
                    or_(*conditions) & (Course.org_id == org_id)
                )
            else:
                query = query.filter(or_(*conditions))
        else:
            # 超级管理员可以看到所有
            if org_id:
                query = query.filter(Course.org_id == org_id)
        
        if scope:
            query = query.filter(Course.scope == scope)
        if status:
            query = query.filter(Course.status == status)
        if level:
            query = query.filter(Course.level == level)
        
        total = query.count()
        courses = query.order_by(Course.sort_order, Course.created_at.desc()).offset(skip).limit(limit).all()
        return courses, total

    def update_course(self, course_id: str, course_data: dict, current_user_id: str) -> Course:
        course = self.get_course(course_id, current_user_id)
        if not course:
            raise NotFoundException(f"课程不存在: {course_id}")
        
        # 检查shared scope只能由系统级权限设置
        if "scope" in course_data and course_data["scope"] == "shared":
            if not self.permission_service.is_super_admin(current_user_id):
                from backend.app.core.common.exceptions import ForbiddenException
                raise ForbiddenException("只有系统级权限可以设置共享范围")
        
        for key, value in course_data.items():
            if hasattr(course, key) and value is not None:
                setattr(course, key, value)
        
        self.db.commit()
        self.db.refresh(course)
        return course

    def delete_course(self, course_id: str, current_user_id: str) -> bool:
        course = self.get_course(course_id, current_user_id)
        if not course:
            raise NotFoundException(f"课程不存在: {course_id}")
        
        self.db.delete(course)
        self.db.commit()
        return True

    def publish_course(self, course_id: str, current_user_id: str) -> Course:
        course = self.get_course(course_id, current_user_id)
        if not course:
            raise NotFoundException(f"课程不存在: {course_id}")
        
        course.status = "published"
        course.published_at = datetime.utcnow()
        course.published_by = current_user_id
        
        self.db.commit()
        self.db.refresh(course)
        return course

    def archive_course(self, course_id: str, current_user_id: str) -> Course:
        course = self.get_course(course_id, current_user_id)
        if not course:
            raise NotFoundException(f"课程不存在: {course_id}")
        
        course.status = "archived"
        
        self.db.commit()
        self.db.refresh(course)
        return course
