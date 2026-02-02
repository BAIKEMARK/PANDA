from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.modules.certificate.schemas.certificate import CertificateCreate, CertificateUpdate, CertificateResponse
from backend.app.modules.certificate.services.certificate_service import CertificateService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.common.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/admin/certificates", tags=["证书管理"])


@router.post("/", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
async def create_certificate(
    cert_data: CertificateCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "certificate:issue"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: certificate:issue")
    
    service = CertificateService(db)
    audit_service = AuditService(db)
    
    try:
        cert = service.create(**cert_data.model_dump())
        audit_service.log(
            user_id=current_user.id,
            action="issue_certificate",
            resource_type="certificate",
            resource_id=cert.id,
            org_id=cert.org_id,
            changes={"certificate_number": cert.certificate_number}
        )
        return cert
    except ConflictException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[CertificateResponse])
async def list_certificates(
    user_id: Optional[str] = None,
    org_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "certificate:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: certificate:view")
    
    service = CertificateService(db)
    return service.list(user_id=user_id, org_id=org_id, skip=skip, limit=limit)


@router.get("/{cert_id}", response_model=CertificateResponse)
async def get_certificate(
    cert_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "certificate:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: certificate:view")
    
    service = CertificateService(db)
    cert = service.get(cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="证书不存在")
    return cert


@router.put("/{cert_id}", response_model=CertificateResponse)
async def update_certificate(
    cert_id: str,
    cert_data: CertificateUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "certificate:revoke"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: certificate:revoke")
    
    service = CertificateService(db)
    audit_service = AuditService(db)
    
    try:
        changes = cert_data.model_dump(exclude_unset=True)
        cert = service.update(cert_id, **changes)
        
        audit_service.log(
            user_id=current_user.id,
            action="update_certificate",
            resource_type="certificate",
            resource_id=cert_id,
            org_id=cert.org_id,
            changes=changes
        )
        return cert
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
