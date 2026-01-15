"""
Scenario CRUD Operations
场景CRUD操作
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from models.scenario import Scenario
from schemas.scenario import ScenarioCreate, ScenarioUpdate


def get_scenario(db: Session, scenario_id: str) -> Optional[Scenario]:
    """根据ID获取场景"""
    return db.query(Scenario).filter(Scenario.id == scenario_id).first()


def get_scenarios(db: Session, skip: int = 0, limit: int = 100) -> List[Scenario]:
    """获取场景列表"""
    return db.query(Scenario).order_by(Scenario.difficulty.asc()).offset(skip).limit(limit).all()


def get_scenarios_by_difficulty(db: Session, difficulty: int) -> List[Scenario]:
    """根据难度获取场景"""
    return db.query(Scenario).filter(Scenario.difficulty == difficulty).all()


def create_scenario(db: Session, scenario: ScenarioCreate) -> Scenario:
    """创建新场景"""
    db_scenario = Scenario(
        id=str(uuid.uuid4()),
        title=scenario.title,
        description=scenario.description,
        system_prompt=scenario.system_prompt,
        patient_background=scenario.patient_background,
        knowledge_tags=scenario.knowledge_tags,
        difficulty=scenario.difficulty,
        time_period=scenario.time_period
    )
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario


def update_scenario(db: Session, db_scenario: Scenario, scenario_in: ScenarioUpdate) -> Scenario:
    """更新场景"""
    update_data = scenario_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_scenario, field, value)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario


def delete_scenario(db: Session, scenario_id: str) -> Optional[Scenario]:
    """删除场景"""
    db_scenario = get_scenario(db, scenario_id)
    if db_scenario:
        db.delete(db_scenario)
        db.commit()
    return db_scenario
