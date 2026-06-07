"""
场景数据访问层（Repository）
场景CRUD操作
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from backend.app.models.scenario import Scenario
from backend.app.modules.scenario.schemas.scenario import ScenarioCreate, ScenarioUpdate


class ScenarioRepository:
    """场景数据访问仓库"""

    def __init__(self, db: Session):
        self.db = db

    def get_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """根据ID获取场景"""
        return self.db.query(Scenario).filter(Scenario.id == scenario_id).first()

    def get_scenarios(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        user_id: Optional[str] = None,
        user_orgs: Optional[List[str]] = None,
        is_super_admin: bool = False
    ) -> List[Scenario]:
        """获取场景列表，根据用户权限过滤"""
        from sqlalchemy import or_

        query = self.db.query(Scenario)

        # 状态过滤
        if status:
            query = query.filter(Scenario.status == status)

        # 权限过滤：非超级管理员需要按scope过滤
        if not is_super_admin and user_id:
            conditions = []

            # 1. shared: 全平台可见
            conditions.append(Scenario.scope == "shared")

            # 2. platform: 该平台内用户可见
            if user_orgs:
                conditions.append(
                    (Scenario.scope == "platform") & (Scenario.org_id.in_(user_orgs))
                )

            # 3. private: 只有创建者可见
            conditions.append(
                (Scenario.scope == "private") & (Scenario.created_by == user_id)
            )

            query = query.filter(or_(*conditions))

        return query.order_by(Scenario.difficulty.asc()).offset(skip).limit(limit).all()

    def get_scenarios_by_difficulty(
        self,
        difficulty: int,
        status: Optional[str] = None,
        user_id: Optional[str] = None,
        user_orgs: Optional[List[str]] = None,
        is_super_admin: bool = False
    ) -> List[Scenario]:
        """根据难度获取场景，根据用户权限过滤"""
        from sqlalchemy import or_

        query = self.db.query(Scenario).filter(Scenario.difficulty == difficulty)

        # 状态过滤
        if status:
            query = query.filter(Scenario.status == status)

        # 权限过滤：非超级管理员需要按scope过滤
        if not is_super_admin and user_id:
            conditions = []

            # 1. shared: 全平台可见
            conditions.append(Scenario.scope == "shared")

            # 2. platform: 该平台内用户可见
            if user_orgs:
                conditions.append(
                    (Scenario.scope == "platform") & (Scenario.org_id.in_(user_orgs))
                )

            # 3. private: 只有创建者可见
            conditions.append(
                (Scenario.scope == "private") & (Scenario.created_by == user_id)
            )

            query = query.filter(or_(*conditions))

        return query.all()

    def create_scenario(self, scenario_data: ScenarioCreate) -> Scenario:
        """创建新场景"""
        db_scenario = Scenario(
            id=str(uuid.uuid4()),
            title=scenario_data.title,
            description=scenario_data.description,
            system_prompt=scenario_data.system_prompt,
            patient_background=scenario_data.patient_background,
            knowledge_tags=scenario_data.knowledge_tags,
            difficulty=scenario_data.difficulty,
            time_period=scenario_data.time_period
        )
        self.db.add(db_scenario)
        self.db.commit()
        self.db.refresh(db_scenario)
        return db_scenario

    def update_scenario(self, db_scenario: Scenario, scenario_data: ScenarioUpdate) -> Scenario:
        """更新场景"""
        update_data = scenario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_scenario, field, value)
        self.db.commit()
        self.db.refresh(db_scenario)
        return db_scenario

    def delete_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """删除场景"""
        db_scenario = self.get_scenario(scenario_id)
        if db_scenario:
            self.db.delete(db_scenario)
            self.db.commit()
        return db_scenario
