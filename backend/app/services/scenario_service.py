"""
Scenario Service
场景服务 - 业务逻辑层
"""
from sqlalchemy.orm import Session
from typing import List, Optional

import crud.crud_scenario as crud_scenario
from schemas.scenario import ScenarioCreate, ScenarioUpdate
from models.scenario import Scenario
from common.exceptions import NotFoundException


class ScenarioService:
    """场景服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_scenario(self, scenario_data: ScenarioCreate) -> Scenario:
        """创建新场景"""
        return crud_scenario.create_scenario(self.db, scenario_data)

    def get_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """获取场景"""
        return crud_scenario.get_scenario(self.db, scenario_id)

    def get_scenarios(self, difficulty: Optional[int] = None) -> List[Scenario]:
        """获取场景列表"""
        if difficulty is not None:
            return crud_scenario.get_scenarios_by_difficulty(self.db, difficulty)
        return crud_scenario.get_scenarios(self.db)

    def update_scenario(self, scenario_id: str, scenario_data: ScenarioUpdate) -> Optional[Scenario]:
        """更新场景"""
        db_scenario = self.get_scenario(scenario_id)
        if not db_scenario:
            raise NotFoundException("场景不存在")
        return crud_scenario.update_scenario(self.db, db_scenario, scenario_data)

    def delete_scenario(self, scenario_id: str) -> bool:
        """删除场景"""
        db_scenario = crud_scenario.delete_scenario(self.db, scenario_id)
        return db_scenario is not None
