from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.core.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.modules.admin.schemas.course import CourseCreate, CourseUpdate, CourseResponse, CourseListResponse
from backend.app.modules.admin.services.course_admin_service import CourseAdminService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.core.common.exceptions import NotFoundException

router = APIRouter(prefix="/admin/courses", tags=["课程管理"])


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:create")
    
    service = CourseAdminService(db)
    audit_service = AuditService(db)
    
    try:
        course = service.create_course(course_data.model_dump(), current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="create_course",
            resource_type="course",
            resource_id=course.id,
            org_id=course.org_id,
            changes={"title": course.title}
        )
        return course
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=CourseListResponse)
async def list_courses(
    org_id: Optional[str] = Query(None, description="机构ID"),
    scope: Optional[str] = Query(None, description="发布范围"),
    status: Optional[str] = Query(None, description="状态"),
    level: Optional[str] = Query(None, description="THP层级"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:view")
    
    service = CourseAdminService(db)
    courses, total = service.list_courses(
        current_user.id,
        org_id=org_id,
        scope=scope,
        status=status,
        level=level,
        skip=skip,
        limit=limit
    )
    return CourseListResponse(courses=courses, total=total, skip=skip, limit=limit)


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:view")
    
    service = CourseAdminService(db)
    course = service.get_course(course_id, current_user.id)
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course_data: CourseUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:edit")
    
    service = CourseAdminService(db)
    audit_service = AuditService(db)
    
    try:
        changes = course_data.model_dump(exclude_unset=True)
        course = service.update_course(course_id, changes, current_user.id)
        
        audit_service.log(
            user_id=current_user.id,
            action="update_course",
            resource_type="course",
            resource_id=course_id,
            org_id=course.org_id,
            changes=changes
        )
        return course
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:edit")
    
    service = CourseAdminService(db)
    audit_service = AuditService(db)
    
    try:
        course = service.get_course(course_id, current_user.id)
        if not course:
            raise HTTPException(status_code=404, detail="课程不存在")
        
        service.delete_course(course_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="delete_course",
            resource_type="course",
            resource_id=course_id,
            org_id=course.org_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{course_id}/publish", response_model=CourseResponse)
async def publish_course(
    course_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:publish"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:publish")
    
    service = CourseAdminService(db)
    audit_service = AuditService(db)
    
    try:
        course = service.publish_course(course_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="publish_course",
            resource_type="course",
            resource_id=course_id,
            org_id=course.org_id
        )
        return course
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{course_id}/archive", response_model=CourseResponse)
async def archive_course(
    course_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:archive"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:archive")
    
    service = CourseAdminService(db)
    audit_service = AuditService(db)
    
    try:
        course = service.archive_course(course_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="archive_course",
            resource_type="course",
            resource_id=course_id,
            org_id=course.org_id
        )
        return course
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
