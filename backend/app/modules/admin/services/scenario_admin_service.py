from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from uuid import uuid4
from datetime import datetime

from backend.app.models.scenario import Scenario
from backend.app.core.common.exceptions import NotFoundException
from backend.app.modules.admin.services.permission_service import PermissionService


class ScenarioAdminService:
    def __init__(self, db: Session):
        self.db = db
        self.permission_service = PermissionService(db)

    def create_scenario(self, scenario_data: dict, current_user_id: str) -> Scenario:
        # 检查shared scope只能由系统级权限设置
        scope = scenario_data.get("scope", "private")
        if scope == "shared" and not self.permission_service.is_super_admin(current_user_id):
            from backend.app.core.common.exceptions import ForbiddenException
            raise ForbiddenException("只有系统级权限可以设置共享范围")
        
        scenario = Scenario(
            id=str(uuid4()),
            title=scenario_data["title"],
            description=scenario_data.get("description"),
            system_prompt=scenario_data["system_prompt"],
            patient_background=scenario_data.get("patient_background"),
            knowledge_tags=scenario_data.get("knowledge_tags"),
            difficulty=scenario_data.get("difficulty", 1),
            time_period=scenario_data.get("time_period"),
            org_id=scenario_data.get("org_id"),
            scope=scope,
            version=scenario_data.get("version", "1.0.0"),
            version_notes=scenario_data.get("version_notes"),
            status=scenario_data.get("status", "draft"),
            created_by=current_user_id
        )
        self.db.add(scenario)
        self.db.commit()
        self.db.refresh(scenario)
        return scenario

    def get_scenario(self, scenario_id: str, current_user_id: str) -> Optional[Scenario]:
        scenario = self.db.query(Scenario).filter(Scenario.id == scenario_id).first()
        if not scenario:
            return None
        
        is_super_admin = self.permission_service.is_super_admin(current_user_id)
        
        if not is_super_admin:
            # 检查权限：private只有创建者可见，platform需要属于该机构，shared全平台可见
            if scenario.scope == "private":
                if scenario.created_by != current_user_id:
                    return None
            elif scenario.scope == "platform":
                user_orgs = self.permission_service.get_user_orgs(current_user_id)
                if scenario.org_id and scenario.org_id not in user_orgs:
                    return None
            # shared: 全平台可见，无需额外检查
        
        return scenario

    def list_scenarios(
        self,
        current_user_id: str,
        org_id: Optional[str] = None,
        scope: Optional[str] = None,
        status: Optional[str] = None,
        difficulty: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Scenario], int]:
        from sqlalchemy import or_
        
        query = self.db.query(Scenario)
        is_super_admin = self.permission_service.is_super_admin(current_user_id)
        
        if not is_super_admin:
            user_orgs = self.permission_service.get_user_orgs(current_user_id)
            
            # 构建权限过滤条件
            conditions = []
            
            # 1. shared: 全平台可见
            conditions.append(Scenario.scope == "shared")
            
            # 2. platform: 该平台内用户可见
            if user_orgs:
                conditions.append(
                    (Scenario.scope == "platform") & (Scenario.org_id.in_(user_orgs))
                )
            
            # 3. private: 只有创建者及更高权限用户可见
            # 对于非超级管理员，只能看到自己创建的private场景
            conditions.append(
                (Scenario.scope == "private") & (Scenario.created_by == current_user_id)
            )
            
            # 如果指定了org_id，需要额外检查
            if org_id:
                if org_id not in user_orgs:
                    return [], 0
                # 在权限条件基础上，再过滤org_id
                query = query.filter(
                    or_(*conditions) & (Scenario.org_id == org_id)
                )
            else:
                query = query.filter(or_(*conditions))
        else:
            # 超级管理员可以看到所有
            if org_id:
                query = query.filter(Scenario.org_id == org_id)
        
        if scope:
            query = query.filter(Scenario.scope == scope)
        if status:
            query = query.filter(Scenario.status == status)
        if difficulty is not None:
            query = query.filter(Scenario.difficulty == difficulty)
        
        total = query.count()
        scenarios = query.order_by(Scenario.difficulty, Scenario.created_at.desc()).offset(skip).limit(limit).all()
        return scenarios, total

    def update_scenario(self, scenario_id: str, scenario_data: dict, current_user_id: str) -> Scenario:
        scenario = self.get_scenario(scenario_id, current_user_id)
        if not scenario:
            raise NotFoundException(f"场景不存在: {scenario_id}")
        
        # 检查shared scope只能由系统级权限设置
        if "scope" in scenario_data and scenario_data["scope"] == "shared":
            if not self.permission_service.is_super_admin(current_user_id):
                from backend.app.core.common.exceptions import ForbiddenException
                raise ForbiddenException("只有系统级权限可以设置共享范围")
        
        for key, value in scenario_data.items():
            if hasattr(scenario, key) and value is not None:
                setattr(scenario, key, value)
        
        self.db.commit()
        self.db.refresh(scenario)
        return scenario

    def delete_scenario(self, scenario_id: str, current_user_id: str) -> bool:
        scenario = self.get_scenario(scenario_id, current_user_id)
        if not scenario:
            raise NotFoundException(f"场景不存在: {scenario_id}")
        
        self.db.delete(scenario)
        self.db.commit()
        return True

    def publish_scenario(self, scenario_id: str, current_user_id: str) -> Scenario:
        scenario = self.get_scenario(scenario_id, current_user_id)
        if not scenario:
            raise NotFoundException(f"场景不存在: {scenario_id}")
        
        scenario.status = "published"
        scenario.published_at = datetime.utcnow()
        scenario.published_by = current_user_id
        
        self.db.commit()
        self.db.refresh(scenario)
        return scenario

    def archive_scenario(self, scenario_id: str, current_user_id: str) -> Scenario:
        scenario = self.get_scenario(scenario_id, current_user_id)
        if not scenario:
            raise NotFoundException(f"场景不存在: {scenario_id}")
        
        scenario.status = "archived"
        
        self.db.commit()
        self.db.refresh(scenario)
        return scenario
