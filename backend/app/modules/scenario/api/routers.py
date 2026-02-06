"""
场景 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.database import get_db
from backend.app.modules.scenario.schemas.scenario import ScenarioCreate, ScenarioResponse, ScenarioUpdate
from backend.app.modules.scenario.services.scenario_service import ScenarioService
from backend.app.core.common.exceptions import NotFoundException

router = APIRouter(prefix="/scenarios", tags=["场景"])


@router.post("/", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    scenario_data: ScenarioCreate,
    db: Session = Depends(get_db)
):
    """
    创建新训练场景

    - **title**: 场景标题
    - **description**: 场景描述
    - **system_prompt**: AI系统提示词
    - **patient_background**: 患者背景
    - **difficulty**: 难度等级 (1-5)
    - **time_period**: 时间节点
    """
    service = ScenarioService(db)
    return service.create_scenario(scenario_data)


@router.get("/", response_model=List[ScenarioResponse])
async def get_scenarios(
    difficulty: int = None,
    db: Session = Depends(get_db)
):
    """获取场景列表，可按难度筛选"""
    service = ScenarioService(db)
    return service.get_scenarios(difficulty)


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """获取单个场景详情"""
    service = ScenarioService(db)
    scenario = service.get_scenario(scenario_id)
    if not scenario:
        raise NotFoundException("场景不存在")
    return scenario


@router.put("/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    scenario_id: str,
    scenario_data: ScenarioUpdate,
    db: Session = Depends(get_db)
):
    """更新场景信息"""
    service = ScenarioService(db)
    scenario = service.update_scenario(scenario_id, scenario_data)
    return scenario


@router.delete("/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """删除场景"""
    service = ScenarioService(db)
    success = service.delete_scenario(scenario_id)
    if not success:
        raise NotFoundException("场景不存在")
    return None
