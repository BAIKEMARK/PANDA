"""
场景服务 - 业务逻辑层
实现 ScenarioInterface 接口
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.models.scenario import Scenario
from backend.app.modules.scenario.schemas.scenario import ScenarioCreate, ScenarioUpdate
from backend.app.modules.scenario.repositories.scenario_repository import ScenarioRepository
from backend.app.core.common.exceptions import NotFoundException
from backend.app.interfaces.scenario_interface import ScenarioInterface, ScenarioConfig


class ScenarioService(ScenarioInterface):
    """场景服务类 - 实现场景接口"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ScenarioRepository(db)

    # ==================== CRUD 操作 ====================

    def create_scenario(self, scenario_data: ScenarioCreate) -> Scenario:
        """创建新场景"""
        return self.repository.create_scenario(scenario_data)

    def get_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """获取场景"""
        return self.repository.get_scenario(scenario_id)

    def get_scenarios(self, difficulty: Optional[int] = None) -> List[Scenario]:
        """获取场景列表"""
        if difficulty is not None:
            return self.repository.get_scenarios_by_difficulty(difficulty)
        return self.repository.get_scenarios()

    def update_scenario(self, scenario_id: str, scenario_data: ScenarioUpdate) -> Optional[Scenario]:
        """更新场景"""
        db_scenario = self.get_scenario(scenario_id)
        if not db_scenario:
            raise NotFoundException("场景不存在")
        return self.repository.update_scenario(db_scenario, scenario_data)

    def delete_scenario(self, scenario_id: str) -> bool:
        """删除场景"""
        db_scenario = self.repository.delete_scenario(scenario_id)
        return db_scenario is not None

    # ==================== ScenarioInterface 接口实现 ====================

    def get_scenario_config(self, scenario_id: str) -> Optional[ScenarioConfig]:
        """
        获取场景配置（供 chat 模块使用）

        Args:
            scenario_id: 场景ID

        Returns:
            ScenarioConfig 对象，不存在返回 None
        """
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return None

        return ScenarioConfig(
            id=scenario.id,
            title=scenario.title,
            description=scenario.description or "",
            system_prompt=scenario.system_prompt,
            patient_background=scenario.patient_background or "",
            difficulty=scenario.difficulty,
            time_period=scenario.time_period or ""
        )

    def get_patient_background(self, scenario_id: str) -> str:
        """
        获取患者背景

        Args:
            scenario_id: 场景ID

        Returns:
            患者背景文本
        """
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return ""
        return scenario.patient_background or ""

    def get_system_prompt(self, scenario_id: str) -> str:
        """
        获取系统提示词

        Args:
            scenario_id: 场景ID

        Returns:
            系统提示词
        """
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return ""
        return scenario.system_prompt
