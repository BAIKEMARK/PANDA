from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.modules.admin.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse, UserOrgAssign
from backend.app.modules.admin.services.user_admin_service import UserAdminService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.common.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/admin/users", tags=["用户管理"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    org_role: Optional[UserOrgAssign] = None,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "user:create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: user:create")
    
    service = UserAdminService(db)
    audit_service = AuditService(db)
    
    user_dict = user_data.model_dump()
    if org_role:
        user_dict["org_id"] = org_role.org_id
        user_dict["role_id"] = org_role.role_id
    
    try:
        user = service.create_user(user_dict, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="create_user",
            resource_type="user",
            resource_id=user.id,
            org_id=user.org_id,
            changes={"email": user.email, "name": user.name}
        )
        return user
    except ConflictException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=UserListResponse)
async def list_users(
    org_id: Optional[str] = Query(None, description="机构ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "user:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: user:view")
    
    service = UserAdminService(db)
    users, total = service.list_users(current_user.id, org_id=org_id, skip=skip, limit=limit)
    return UserListResponse(users=users, total=total, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "user:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: user:view")
    
    service = UserAdminService(db)
    user = service.get_user(user_id, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "user:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: user:edit")
    
    service = UserAdminService(db)
    audit_service = AuditService(db)
    
    try:
        changes = user_data.model_dump(exclude_unset=True)
        user = service.update_user(user_id, changes, current_user.id)
        
        audit_service.log(
            user_id=current_user.id,
            action="update_user",
            resource_type="user",
            resource_id=user_id,
            org_id=user.org_id,
            changes=changes
        )
        return user
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "user:delete"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: user:delete")
    
    service = UserAdminService(db)
    audit_service = AuditService(db)
    
    try:
        user = service.get_user(user_id, current_user.id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        service.delete_user(user_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="delete_user",
            resource_type="user",
            resource_id=user_id,
            org_id=user.org_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{user_id}/organizations", response_model=UserResponse)
async def assign_user_org(
    user_id: str,
    org_data: UserOrgAssign,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "user:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: user:edit")
    
    service = UserAdminService(db)
    audit_service = AuditService(db)
    
    try:
        service.assign_org(user_id, org_data.org_id, org_data.role_id, current_user.id)
        user = service.get_user(user_id, current_user.id)
        
        audit_service.log(
            user_id=current_user.id,
            action="assign_user_org",
            resource_type="user",
            resource_id=user_id,
            org_id=org_data.org_id,
            changes={"org_id": org_data.org_id, "role_id": org_data.role_id}
        )
        return user
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}/organizations/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user_org(
    user_id: str,
    org_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "user:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: user:edit")
    
    service = UserAdminService(db)
    audit_service = AuditService(db)
    
    try:
        service.remove_org(user_id, org_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="remove_user_org",
            resource_type="user",
            resource_id=user_id,
            org_id=org_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
