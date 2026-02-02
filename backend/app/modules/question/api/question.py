from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.modules.question.schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse
from backend.app.modules.question.services.question_service import QuestionService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.common.exceptions import NotFoundException

router = APIRouter(prefix="/admin/questions", tags=["题库管理"])


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "question:create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: question:create")
    
    service = QuestionService(db)
    audit_service = AuditService(db)
    
    question = service.create(**question_data.model_dump())
    audit_service.log(
        user_id=current_user.id,
        action="create_question",
        resource_type="question",
        resource_id=question.id,
        org_id=question.org_id,
        changes={"question_text": question.question_text}
    )
    return question


@router.get("/", response_model=List[QuestionResponse])
async def list_questions(
    org_id: Optional[str] = None,
    question_type: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "question:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: question:view")
    
    service = QuestionService(db)
    return service.list(org_id=org_id, question_type=question_type, status=status, skip=skip, limit=limit)


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "question:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: question:view")
    
    service = QuestionService(db)
    question = service.get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: str,
    question_data: QuestionUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "question:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: question:edit")
    
    service = QuestionService(db)
    audit_service = AuditService(db)
    
    try:
        changes = question_data.model_dump(exclude_unset=True)
        question = service.update(question_id, **changes)
        
        audit_service.log(
            user_id=current_user.id,
            action="update_question",
            resource_type="question",
            resource_id=question_id,
            org_id=question.org_id,
            changes=changes
        )
        return question
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "question:delete"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: question:delete")
    
    service = QuestionService(db)
    audit_service = AuditService(db)
    
    try:
        question = service.get(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="题目不存在")
        
        service.delete(question_id)
        audit_service.log(
            user_id=current_user.id,
            action="delete_question",
            resource_type="question",
            resource_id=question_id,
            org_id=question.org_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
