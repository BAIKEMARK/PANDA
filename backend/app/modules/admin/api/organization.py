from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.core.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from backend.app.modules.admin.services.organization_service import OrganizationService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.core.common.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/admin/organizations", tags=["机构管理"])


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:create")
    
    service = OrganizationService(db)
    audit_service = AuditService(db)
    
    try:
        org = service.create(**org_data.model_dump())
        audit_service.log(
            user_id=current_user.id,
            action="create_organization",
            resource_type="organization",
            resource_id=org.id,
            org_id=org.id,
            changes={"name": org.name}
        )
        return org
    except ConflictException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[OrganizationResponse])
async def list_organizations(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:view")
    
    service = OrganizationService(db)
    orgs = service.list(status=status, skip=skip, limit=limit)
    return orgs


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:view")
    
    service = OrganizationService(db)
    org = service.get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="机构不存在")
    return org


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: str,
    org_data: OrganizationUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:edit")
    
    service = OrganizationService(db)
    audit_service = AuditService(db)
    
    try:
        old_org = service.get(org_id)
        if not old_org:
            raise HTTPException(status_code=404, detail="机构不存在")
        
        changes = org_data.model_dump(exclude_unset=True)
        org = service.update(org_id, **changes)
        
        audit_service.log(
            user_id=current_user.id,
            action="update_organization",
            resource_type="organization",
            resource_id=org_id,
            org_id=org_id,
            changes=changes
        )
        return org
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:delete"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:delete")
    
    service = OrganizationService(db)
    audit_service = AuditService(db)
    
    try:
        service.delete(org_id)
        audit_service.log(
            user_id=current_user.id,
            action="delete_organization",
            resource_type="organization",
            resource_id=org_id,
            org_id=org_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
