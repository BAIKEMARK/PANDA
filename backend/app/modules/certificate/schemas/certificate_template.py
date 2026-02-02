from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class CertificateTemplateCreate(BaseModel):
    org_id: str = Field(..., description="机构ID")
    name: str = Field(..., description="模板名称")
    template_config: Optional[Dict[str, Any]] = Field(None, description="模板配置")
    status: Optional[str] = Field("active", description="状态")


class CertificateTemplateUpdate(BaseModel):
    name: Optional[str] = None
    template_config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class CertificateTemplateResponse(BaseModel):
    id: str
    org_id: str
    name: str
    template_config: Optional[Dict[str, Any]]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
