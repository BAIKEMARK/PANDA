"""
Course Service
课程服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import List, Optional

import crud.crud_course as crud_course
from schemas.course import CourseCreate, CourseUpdate
from models.course import Course
from common.exceptions import NotFoundException


class CourseService:
    """课程服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_course(self, course_data: CourseCreate) -> Course:
        """创建新课程"""
        return crud_course.create_course(self.db, course_data)

    def get_course(self, course_id: str) -> Optional[Course]:
        """获取课程"""
        return crud_course.get_course(self.db, course_id)

    def get_courses(self, level: Optional[str] = None) -> List[Course]:
        """获取课程列表"""
        if level:
            return crud_course.get_courses_by_level(self.db, level)
        return crud_course.get_courses(self.db)

    def update_course(self, course_id: str, course_data: CourseUpdate) -> Optional[Course]:
        """更新课程"""
        db_course = self.get_course(course_id)
        if not db_course:
            raise NotFoundException("课程不存在")
        return crud_course.update_course(self.db, db_course, course_data)

    def delete_course(self, course_id: str) -> bool:
        """删除课程"""
        db_course = crud_course.delete_course(self.db, course_id)
        return db_course is not None
