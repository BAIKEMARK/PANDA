"""
课程 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.modules.course.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from backend.app.modules.course.services.course_service import CourseService
from backend.app.core.common.exceptions import NotFoundException
from backend.app.core.dependencies import get_current_user, require_role
from backend.app.models.user import User

router = APIRouter(prefix="/courses", tags=["课程"])


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(require_role("admin", "instructor")),
    db: Session = Depends(get_db)
):
    """
    创建新课程

    - **title**: 课程标题
    - **content_url**: 内容URL
    - **level**: THP层级 (L1/L2/L3/L4)
    - **sort_order**: 排序
    - **description**: 课程描述
    """
    service = CourseService(db)
    return service.create_course(course_data)


@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    level: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取课程列表，可按层级筛选
    
    学生角色只显示已发布的课程，其他角色显示所有状态的课程
    根据scope进行权限过滤：
    - private: 只有创建者可见
    - platform: 该平台内用户可见
    - shared: 全平台可见
    """
    service = CourseService(db)
    user_role = current_user.role if current_user else None
    user_id = current_user.id if current_user else None
    return service.get_courses(level, user_role=user_role, user_id=user_id)


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: str,
    db: Session = Depends(get_db)
):
    """获取单个课程详情"""
    service = CourseService(db)
    course = service.get_course(course_id)
    if not course:
        raise NotFoundException("课程不存在")
    return course


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course_data: CourseUpdate,
    current_user: User = Depends(require_role("admin", "instructor")),
    db: Session = Depends(get_db)
):
    """更新课程信息"""
    service = CourseService(db)
    course = service.update_course(course_id, course_data)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: str,
    current_user: User = Depends(require_role("admin", "instructor")),
    db: Session = Depends(get_db)
):
    """删除课程"""
    service = CourseService(db)
    success = service.delete_course(course_id)
    if not success:
        raise NotFoundException("课程不存在")
    return None
