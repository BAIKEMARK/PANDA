from sqlalchemy.orm import Session
from typing import List, Optional, Any
from uuid import uuid4
from datetime import datetime, date

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
        request: Optional[Request] = None,
    ) -> AuditLog:
        """记录审计日志。

        注意：将 changes 中的 datetime/date 等不可 JSON 序列化类型转换为字符串，
        避免 JSON 字段写入时抛出 `Object of type datetime is not JSON serializable`。
        """
        sanitized_changes = self._sanitize_changes(changes) if changes is not None else None

        log = AuditLog(
            id=str(uuid4()),
            user_id=user_id,
            org_id=org_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=sanitized_changes,
            ip_address=self._get_client_ip(request) if request else None,
            user_agent=request.headers.get("user-agent") if request else None,
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

    def _sanitize_changes(self, value: Any) -> Any:
        """递归转换 changes 中不可 JSON 序列化的对象（如 datetime）为字符串。"""
        if isinstance(value, (datetime, date)):
            # 统一使用 ISO 格式，便于前端解析或展示
            return value.isoformat()
        if isinstance(value, dict):
            return {k: self._sanitize_changes(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._sanitize_changes(v) for v in value]
        return value
