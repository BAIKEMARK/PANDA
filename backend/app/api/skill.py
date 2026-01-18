"""
Skill API Router
技能API路由 - 管理全局对话技能配置
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
from pathlib import Path

from backend.app.core.skill import skill_manager

router = APIRouter(prefix="/skill", tags=["技能管理"])


# ==================== 响应模型 ====================

class SkillInfoResponse(BaseModel):
    """技能信息响应"""
    name: str
    description: str
    version: str
    enabled: bool
    role_definition: str
    core_principles: List[str]
    behavior_guidelines: Dict
    indicator_rules: Dict
    cris_thresholds: Dict
    crisis_responses: Dict


class SkillPromptResponse(BaseModel):
    """技能提示词响应"""
    enabled: bool
    prompt: str


class SkillUpdateRequest(BaseModel):
    """技能更新请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    role_definition: Optional[str] = None
    core_principles: Optional[List[str]] = None
    behavior_guidelines: Optional[Dict] = None
    indicator_rules: Optional[Dict] = None
    cris_thresholds: Optional[Dict] = None
    crisis_responses: Optional[Dict] = None


# ==================== API端点 ====================

@router.get("/info", response_model=SkillInfoResponse)
async def get_skill_info():
    """
    获取全局技能配置信息

    返回当前全局技能的详细配置，包括：
    - 名称和描述
    - 版本号
    - 启用状态
    - 指导原则列表
    - 评估标准
    """
    try:
        return skill_manager.get_skill_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取技能信息失败: {str(e)}")


@router.get("/prompt", response_model=SkillPromptResponse)
async def get_skill_prompt():
    """
    获取技能提示词

    返回用于AI对话的技能提示词，该提示词会在所有对话场景中应用。
    """
    try:
        return {
            "enabled": skill_manager.is_enabled(),
            "prompt": skill_manager.get_skill_prompt()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取技能提示词失败: {str(e)}")


@router.post("/reload")
async def reload_skill_config():
    """
    重新加载技能配置

    从配置文件重新加载技能配置，用于配置文件更新后生效。
    """
    try:
        skill_manager.reload_config()
        return {
            "message": "技能配置已重新加载",
            "info": skill_manager.get_skill_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重新加载配置失败: {str(e)}")


@router.post("/update")
async def update_skill_config(request: SkillUpdateRequest):
    """
    更新技能配置

    更新技能配置的部分字段，所有字段都是可选的。
    更新后需要重新加载配置才能生效。

    - **name**: 技能名称
    - **description**: 技能描述
    - **enabled**: 是否启用
    - **instructions**: 指导原则列表
    - **evaluation_criteria**: 评估标准
    """
    try:
        # 获取配置文件路径
        config_path = Path(__file__).parent.parent / "core" / "skill_config.json"

        if not config_path.exists():
            raise HTTPException(status_code=404, detail="配置文件不存在")

        # 读取当前配置
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 更新字段
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key in config["global_skill"]:
                config["global_skill"][key] = value

        # 写回配置文件
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        # 重新加载配置
        skill_manager.reload_config()

        return {
            "message": "技能配置已更新",
            "info": skill_manager.get_skill_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新配置失败: {str(e)}")