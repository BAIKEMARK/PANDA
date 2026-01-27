"""
课程数据访问层（Repository）
课程CRUD操作
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from backend.app.models.course import Course
from backend.app.modules.course.schemas.course import CourseCreate, CourseUpdate


class CourseRepository:
    """课程数据访问仓库"""

    def __init__(self, db: Session):
        self.db = db

    def get_course(self, course_id: str) -> Optional[Course]:
        """根据ID获取课程"""
        return self.db.query(Course).filter(Course.id == course_id).first()

    def get_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        """获取课程列表"""
        return self.db.query(Course).order_by(Course.sort_order.asc()).offset(skip).limit(limit).all()

    def get_courses_by_level(self, level: str) -> List[Course]:
        """根据层级获取课程"""
        return self.db.query(Course).filter(Course.level == level).order_by(Course.sort_order.asc()).all()

    def create_course(self, course_data: CourseCreate) -> Course:
        """创建新课程"""
        db_course = Course(
            id=str(uuid.uuid4()),
            title=course_data.title,
            content_url=course_data.content_url,
            sort_order=course_data.sort_order,
            level=course_data.level,
            description=course_data.description
        )
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def update_course(self, db_course: Course, course_data: CourseUpdate) -> Course:
        """更新课程"""
        update_data = course_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_course, field, value)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def delete_course(self, course_id: str) -> Optional[Course]:
        """删除课程"""
        db_course = self.get_course(course_id)
        if db_course:
            self.db.delete(db_course)
            self.db.commit()
        return db_course
