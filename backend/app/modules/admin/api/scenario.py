from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.core.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.modules.admin.schemas.scenario import ScenarioCreate, ScenarioUpdate, ScenarioResponse, ScenarioListResponse
from backend.app.modules.admin.services.scenario_admin_service import ScenarioAdminService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.core.common.exceptions import NotFoundException

router = APIRouter(prefix="/admin/scenarios", tags=["场景管理"])


@router.post("/", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    scenario_data: ScenarioCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "scenario:create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: scenario:create")
    
    service = ScenarioAdminService(db)
    audit_service = AuditService(db)
    
    try:
        scenario = service.create_scenario(scenario_data.model_dump(), current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="create_scenario",
            resource_type="scenario",
            resource_id=scenario.id,
            org_id=scenario.org_id,
            changes={"title": scenario.title}
        )
        return scenario
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=ScenarioListResponse)
async def list_scenarios(
    org_id: Optional[str] = Query(None, description="机构ID"),
    scope: Optional[str] = Query(None, description="发布范围"),
    status: Optional[str] = Query(None, description="状态"),
    difficulty: Optional[int] = Query(None, description="难度等级"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "scenario:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: scenario:view")
    
    service = ScenarioAdminService(db)
    scenarios, total = service.list_scenarios(
        current_user.id,
        org_id=org_id,
        scope=scope,
        status=status,
        difficulty=difficulty,
        skip=skip,
        limit=limit
    )
    return ScenarioListResponse(scenarios=scenarios, total=total, skip=skip, limit=limit)


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "scenario:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: scenario:view")
    
    service = ScenarioAdminService(db)
    scenario = service.get_scenario(scenario_id, current_user.id)
    if not scenario:
        raise HTTPException(status_code=404, detail="场景不存在")
    return scenario


@router.put("/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    scenario_id: str,
    scenario_data: ScenarioUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "scenario:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: scenario:edit")
    
    service = ScenarioAdminService(db)
    audit_service = AuditService(db)
    
    try:
        changes = scenario_data.model_dump(exclude_unset=True)
        scenario = service.update_scenario(scenario_id, changes, current_user.id)
        
        audit_service.log(
            user_id=current_user.id,
            action="update_scenario",
            resource_type="scenario",
            resource_id=scenario_id,
            org_id=scenario.org_id,
            changes=changes
        )
        return scenario
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scenario(
    scenario_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "scenario:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: scenario:edit")
    
    service = ScenarioAdminService(db)
    audit_service = AuditService(db)
    
    try:
        scenario = service.get_scenario(scenario_id, current_user.id)
        if not scenario:
            raise HTTPException(status_code=404, detail="场景不存在")
        
        service.delete_scenario(scenario_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="delete_scenario",
            resource_type="scenario",
            resource_id=scenario_id,
            org_id=scenario.org_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{scenario_id}/publish", response_model=ScenarioResponse)
async def publish_scenario(
    scenario_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "scenario:publish"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: scenario:publish")
    
    service = ScenarioAdminService(db)
    audit_service = AuditService(db)
    
    try:
        scenario = service.publish_scenario(scenario_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="publish_scenario",
            resource_type="scenario",
            resource_id=scenario_id,
            org_id=scenario.org_id
        )
        return scenario
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{scenario_id}/archive", response_model=ScenarioResponse)
async def archive_scenario(
    scenario_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "scenario:archive"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: scenario:archive")
    
    service = ScenarioAdminService(db)
    audit_service = AuditService(db)
    
    try:
        scenario = service.archive_scenario(scenario_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="archive_scenario",
            resource_type="scenario",
            resource_id=scenario_id,
            org_id=scenario.org_id
        )
        return scenario
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
