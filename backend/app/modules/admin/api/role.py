from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.modules.admin.schemas.role import RoleCreate, RoleUpdate, RoleResponse, RolePermissionAssign, PermissionResponse
from backend.app.modules.admin.services.role_service import RoleService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.common.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/admin/roles", tags=["角色管理"])


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:create")
    
    service = RoleService(db)
    audit_service = AuditService(db)
    
    try:
        role = service.create(**role_data.model_dump())
        audit_service.log(
            user_id=current_user.id,
            action="create_role",
            resource_type="role",
            resource_id=role.id,
            changes={"code": role.code, "name": role.name}
        )
        return role
    except ConflictException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[RoleResponse])
async def list_roles(
    scope: Optional[str] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:view")
    
    service = RoleService(db)
    roles = service.list(scope=scope)
    for role in roles:
        role.permissions = service.get_permissions(role.id)
    return roles


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:view")
    
    service = RoleService(db)
    role = service.get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    role.permissions = service.get_permissions(role_id)
    return role


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: str,
    role_data: RoleUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:edit")
    
    service = RoleService(db)
    audit_service = AuditService(db)
    
    try:
        changes = role_data.model_dump(exclude_unset=True)
        role = service.update(role_id, **changes)
        
        audit_service.log(
            user_id=current_user.id,
            action="update_role",
            resource_type="role",
            resource_id=role_id,
            changes=changes
        )
        role.permissions = service.get_permissions(role_id)
        return role
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{role_id}/permissions", response_model=RoleResponse)
async def assign_permissions(
    role_id: str,
    permission_data: RolePermissionAssign,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:edit")
    
    service = RoleService(db)
    audit_service = AuditService(db)
    
    try:
        role = service.assign_permissions(role_id, permission_data.permission_ids)
        audit_service.log(
            user_id=current_user.id,
            action="assign_permissions",
            resource_type="role",
            resource_id=role_id,
            changes={"permission_ids": permission_data.permission_ids}
        )
        role.permissions = service.get_permissions(role_id)
        return role
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/permissions/all", response_model=List[PermissionResponse])
async def list_all_permissions(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "org:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: org:view")
    
    from backend.app.models.organization import Permission
    perms = db.query(Permission).all()
    return perms
