from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ScenarioResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    system_prompt: str
    patient_background: Optional[str]
    knowledge_tags: Optional[str]
    difficulty: int
    time_period: Optional[str]
    org_id: Optional[str]
    scope: str
    version: str
    version_notes: Optional[str]
    status: str
    published_at: Optional[datetime]
    published_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScenarioCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="场景标题")
    description: Optional[str] = Field(None, description="场景描述")
    system_prompt: str = Field(..., min_length=1, description="AI系统提示词")
    patient_background: Optional[str] = Field(None, description="患者背景信息")
    knowledge_tags: Optional[str] = Field(None, description="知识点标签")
    difficulty: int = Field(1, ge=1, le=5, description="难度等级")
    time_period: Optional[str] = Field(None, description="时间节点")
    org_id: Optional[str] = Field(None, description="机构ID")
    scope: str = Field("private", description="发布范围")
    version: str = Field("1.0.0", description="版本号")
    version_notes: Optional[str] = Field(None, description="版本说明")


class ScenarioUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    patient_background: Optional[str] = None
    knowledge_tags: Optional[str] = None
    difficulty: Optional[int] = None
    time_period: Optional[str] = None
    org_id: Optional[str] = None
    scope: Optional[str] = None
    version: Optional[str] = None
    version_notes: Optional[str] = None
    status: Optional[str] = None


class ScenarioListResponse(BaseModel):
    scenarios: List[ScenarioResponse]
    total: int
    skip: int
    limit: int
