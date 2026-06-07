from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CertificateCreate(BaseModel):
    user_id: str = Field(..., description="用户ID")
    certificate_number: str = Field(..., description="证书编号")
    credit_hours: float = Field(0.0, description="学分")
    org_id: Optional[str] = Field(None, description="机构ID")
    class_id: Optional[str] = Field(None, description="班级ID")
    template_id: Optional[str] = Field(None, description="模板ID")


class CertificateUpdate(BaseModel):
    status: Optional[str] = None
    revoked_at: Optional[datetime] = None
    revoked_by: Optional[str] = None


class CertificateResponse(BaseModel):
    id: str
    user_id: str
    certificate_number: str
    issue_date: datetime
    credit_hours: float
    org_id: Optional[str]
    class_id: Optional[str]
    template_id: Optional[str]
    status: str
    revoked_at: Optional[datetime]
    revoked_by: Optional[str]

    class Config:
        from_attributes = True
