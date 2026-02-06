from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.core.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.modules.admin.schemas.training import (
    TrainingClassCreate, TrainingClassUpdate, TrainingClassResponse,
    ClassStudentAdd, ClassTaskCreate
)
from backend.app.modules.admin.services.training_service import TrainingService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.core.common.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/admin/classes", tags=["班级管理"])


@router.post("/", response_model=TrainingClassResponse, status_code=status.HTTP_201_CREATED)
async def create_class(
    class_data: TrainingClassCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:create")
    
    service = TrainingService(db)
    audit_service = AuditService(db)
    
    try:
        training_class = service.create_class(class_data.model_dump(), current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="create_class",
            resource_type="training_class",
            resource_id=training_class.id,
            org_id=training_class.org_id,
            changes={"name": training_class.name}
        )
        return training_class
    except ConflictException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[TrainingClassResponse])
async def list_classes(
    org_id: Optional[str] = Query(None, description="机构ID"),
    status: Optional[str] = Query(None, description="状态"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:view")
    
    service = TrainingService(db)
    classes, total = service.list_classes(
        current_user.id,
        org_id=org_id,
        status=status,
        skip=skip,
        limit=limit
    )
    return classes


@router.get("/{class_id}", response_model=TrainingClassResponse)
async def get_class(
    class_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:view")
    
    service = TrainingService(db)
    training_class = service.get_class(class_id, current_user.id)
    if not training_class:
        raise HTTPException(status_code=404, detail="班级不存在")
    return training_class


@router.put("/{class_id}", response_model=TrainingClassResponse)
async def update_class(
    class_id: str,
    class_data: TrainingClassUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:edit")
    
    service = TrainingService(db)
    audit_service = AuditService(db)
    
    try:
        changes = class_data.model_dump(exclude_unset=True)
        training_class = service.update_class(class_id, changes, current_user.id)
        
        audit_service.log(
            user_id=current_user.id,
            action="update_class",
            resource_type="training_class",
            resource_id=class_id,
            org_id=training_class.org_id,
            changes=changes
        )
        return training_class
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    class_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:delete"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:delete")
    
    service = TrainingService(db)
    audit_service = AuditService(db)
    
    try:
        training_class = service.get_class(class_id, current_user.id)
        if not training_class:
            raise HTTPException(status_code=404, detail="班级不存在")
        
        service.delete_class(class_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="delete_class",
            resource_type="training_class",
            resource_id=class_id,
            org_id=training_class.org_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{class_id}/students", status_code=status.HTTP_201_CREATED)
async def add_students(
    class_id: str,
    student_data: ClassStudentAdd,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:edit")
    
    service = TrainingService(db)
    audit_service = AuditService(db)
    
    try:
        students = service.add_students(class_id, student_data.user_ids, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="add_students",
            resource_type="training_class",
            resource_id=class_id,
            changes={"user_ids": student_data.user_ids}
        )
        return {"message": f"成功添加 {len(students)} 名学员"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{class_id}/students/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_student(
    class_id: str,
    user_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:edit")
    
    service = TrainingService(db)
    audit_service = AuditService(db)
    
    try:
        service.remove_student(class_id, user_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="remove_student",
            resource_type="training_class",
            resource_id=class_id,
            changes={"user_id": user_id}
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{class_id}/students")
async def list_students(
    class_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:view")
    
    service = TrainingService(db)
    try:
        students = service.list_students(class_id, current_user.id)
        return students
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{class_id}/tasks", status_code=status.HTTP_201_CREATED)
async def add_task(
    class_id: str,
    task_data: ClassTaskCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:edit")
    
    service = TrainingService(db)
    audit_service = AuditService(db)
    
    try:
        task = service.add_task(class_id, task_data.model_dump(), current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="add_task",
            resource_type="training_class",
            resource_id=class_id,
            changes=task_data.model_dump()
        )
        return task
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{class_id}/tasks")
async def list_tasks(
    class_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:view")
    
    service = TrainingService(db)
    try:
        tasks = service.list_tasks(class_id, current_user.id)
        return tasks
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "class:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: class:edit")
    
    service = TrainingService(db)
    audit_service = AuditService(db)
    
    try:
        service.delete_task(task_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="delete_task",
            resource_type="class_task",
            resource_id=task_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
