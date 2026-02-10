from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class OrganizationCreate(BaseModel):
    name: str = Field(..., description="机构名称")
    short_name: Optional[str] = Field(None, description="简称")
    logo_url: Optional[str] = Field(None, description="LOGO")
    contact_name: Optional[str] = Field(None, description="联系人")
    contact_phone: Optional[str] = Field(None, description="联系电话")
    contact_email: Optional[str] = Field(None, description="联系邮箱")
    valid_until: Optional[datetime] = Field(None, description="有效期")
    config: Optional[Dict[str, Any]] = Field(None, description="机构配置")


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    logo_url: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    valid_until: Optional[datetime] = None
    status: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class OrganizationResponse(BaseModel):
    id: str
    name: str
    short_name: Optional[str]
    logo_url: Optional[str]
    contact_name: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    valid_until: Optional[datetime]
    status: str
    config: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
