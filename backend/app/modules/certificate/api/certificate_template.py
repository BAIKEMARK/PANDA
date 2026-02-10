from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.core.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.modules.certificate.schemas.certificate_template import (
    CertificateTemplateCreate, CertificateTemplateUpdate, CertificateTemplateResponse
)
from backend.app.modules.certificate.services.certificate_template_service import CertificateTemplateService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.core.common.exceptions import NotFoundException

router = APIRouter(prefix="/admin/certificate-templates", tags=["证书模板管理"])


@router.post("/", response_model=CertificateTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: CertificateTemplateCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    
    service = CertificateTemplateService(db)
    audit_service = AuditService(db)
    
    template = service.create(**template_data.model_dump())
    audit_service.log(
        user_id=current_user.id,
        action="create_certificate_template",
        resource_type="certificate_template",
        resource_id=template.id,
        org_id=template.org_id,
        changes={"name": template.name}
    )
    return template


@router.get("/", response_model=List[CertificateTemplateResponse])
async def list_templates(
    org_id: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    # 证书模板仅限具有 org:view 权限或更高角色的用户访问
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:view"):
        # 降级为空列表而不是抛错，避免非管理员登录直接看到权限错误
        return []

    service = CertificateTemplateService(db)
    return service.list(org_id=org_id, status=status, skip=skip, limit=limit)


@router.get("/{template_id}", response_model=CertificateTemplateResponse)
async def get_template(
    template_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    
    service = CertificateTemplateService(db)
    template = service.get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    return template


@router.put("/{template_id}", response_model=CertificateTemplateResponse)
async def update_template(
    template_id: str,
    template_data: CertificateTemplateUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    
    service = CertificateTemplateService(db)
    audit_service = AuditService(db)
    
    try:
        changes = template_data.model_dump(exclude_unset=True)
        template = service.update(template_id, **changes)
        
        audit_service.log(
            user_id=current_user.id,
            action="update_certificate_template",
            resource_type="certificate_template",
            resource_id=template_id,
            org_id=template.org_id,
            changes=changes
        )
        return template
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:delete"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
    
    service = CertificateTemplateService(db)
    audit_service = AuditService(db)
    
    try:
        template = service.get(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="模板不存在")
        
        service.delete(template_id)
        audit_service.log(
            user_id=current_user.id,
            action="delete_certificate_template",
            resource_type="certificate_template",
            resource_id=template_id,
            org_id=template.org_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
