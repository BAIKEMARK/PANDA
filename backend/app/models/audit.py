from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(CHAR(36), primary_key=True, comment="日志ID")
    user_id = Column(CHAR(36), index=True, comment="操作用户")
    org_id = Column(CHAR(36), index=True, comment="机构ID")
    action = Column(String(100), nullable=False, comment="操作")
    resource_type = Column(String(50), index=True, comment="资源类型")
    resource_id = Column(CHAR(36), index=True, comment="资源ID")
    changes = Column(JSON, comment="变更内容")
    ip_address = Column(String(50), comment="IP地址")
    user_agent = Column(String(500), comment="用户代理")
    created_at = Column(DateTime, default=datetime.utcnow, index=True, comment="创建时间")
