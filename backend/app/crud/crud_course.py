"""
Course CRUD Operations
课程CRUD操作
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from backend.app.models.course import Course
from backend.app.schemas.course import CourseCreate, CourseUpdate


def get_course(db: Session, course_id: str) -> Optional[Course]:
    """根据ID获取课程"""
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
    """获取课程列表"""
    return db.query(Course).order_by(Course.sort_order.asc()).offset(skip).limit(limit).all()


def get_courses_by_level(db: Session, level: str) -> List[Course]:
    """根据层级获取课程"""
    return db.query(Course).filter(Course.level == level).order_by(Course.sort_order.asc()).all()


def create_course(db: Session, course: CourseCreate) -> Course:
    """创建新课程"""
    db_course = Course(
        id=str(uuid.uuid4()),
        title=course.title,
        content_url=course.content_url,
        sort_order=course.sort_order,
        level=course.level.value,
        description=course.description
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, db_course: Course, course_in: CourseUpdate) -> Course:
    """更新课程"""
    update_data = course_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_course, field, value)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: str) -> Optional[Course]:
    """删除课程"""
    db_course = get_course(db, course_id)
    if db_course:
        db.delete(db_course)
        db.commit()
    return db_course
