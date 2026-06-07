from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TrainingClassCreate(BaseModel):
    org_id: str = Field(..., description="机构ID")
    name: str = Field(..., description="班级名称")
    description: Optional[str] = Field(None, description="描述")
    start_date: datetime = Field(..., description="开始时间")
    end_date: datetime = Field(..., description="结束时间")
    trainer_id: Optional[str] = Field(None, description="负责人ID")
    credit_rule: Optional[Dict[str, Any]] = Field(None, description="学分规则")
    completion_rule: Optional[Dict[str, Any]] = Field(None, description="结业标准")


class TrainingClassUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    trainer_id: Optional[str] = None
    credit_rule: Optional[Dict[str, Any]] = None
    completion_rule: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class TrainingClassResponse(BaseModel):
    id: str
    org_id: str
    name: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    trainer_id: Optional[str]
    credit_rule: Optional[Dict[str, Any]]
    completion_rule: Optional[Dict[str, Any]]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ClassStudentAdd(BaseModel):
    user_ids: List[str] = Field(..., description="学员ID列表")


class ClassTaskCreate(BaseModel):
    resource_type: str = Field(..., description="资源类型: course/scenario/exam")
    resource_id: str = Field(..., description="资源ID")
    resource_version: Optional[str] = Field(None, description="资源版本")
    deadline: Optional[datetime] = Field(None, description="截止日期")
    sort_order: int = Field(0, description="排序")
