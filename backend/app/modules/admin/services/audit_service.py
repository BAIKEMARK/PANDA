from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from backend.app.models.audit import AuditLog
from fastapi import Request


class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log(
        self,
        user_id: Optional[str],
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        org_id: Optional[str] = None,
        changes: Optional[dict] = None,
        request: Optional[Request] = None
    ) -> AuditLog:
        log = AuditLog(
            id=str(uuid4()),
            user_id=user_id,
            org_id=org_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes,
            ip_address=self._get_client_ip(request) if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_logs(
        self,
        user_id: Optional[str] = None,
        org_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        query = self.db.query(AuditLog)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if org_id:
            query = query.filter(AuditLog.org_id == org_id)
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        if start_date:
            query = query.filter(AuditLog.created_at >= start_date)
        if end_date:
            query = query.filter(AuditLog.created_at <= end_date)
        
        return query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

    def _get_client_ip(self, request: Request) -> Optional[str]:
        if request:
            forwarded = request.headers.get("X-Forwarded-For")
            if forwarded:
                return forwarded.split(",")[0].strip()
            return request.client.host if request.client else None
        return None
