from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Numeric, JSON
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(CHAR(36), primary_key=True, comment="证书ID")
    user_id = Column(CHAR(36), nullable=False, index=True, comment="用户ID")
    certificate_number = Column(String(100), unique=True, nullable=False, index=True, comment="证书编号")
    issue_date = Column(DateTime, default=datetime.utcnow, comment="颁发日期")
    credit_hours = Column(Numeric(4, 1), default=0.0, comment="学分")
    org_id = Column(CHAR(36), index=True, comment="机构ID")
    class_id = Column(CHAR(36), index=True, comment="班级ID")
    template_id = Column(CHAR(36), comment="模板ID")
    status = Column(SQLEnum("valid", "revoked", name="cert_status"), default="valid", comment="状态")
    revoked_at = Column(DateTime, comment="撤销时间")
    revoked_by = Column(CHAR(36), comment="撤销人")


class CertificateTemplate(Base):
    __tablename__ = "certificate_templates"

    id = Column(CHAR(36), primary_key=True, comment="模板ID")
    org_id = Column(CHAR(36), nullable=False, index=True, comment="机构ID")
    name = Column(String(255), nullable=False, comment="模板名称")
    template_config = Column(JSON, comment="模板配置(JSON)")
    status = Column(SQLEnum("active", "inactive", name="template_status"), default="active", comment="状态")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
