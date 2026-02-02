from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from backend.app.models.organization import Organization
from backend.app.common.exceptions import NotFoundException, ConflictException


class OrganizationService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, short_name: Optional[str] = None, **kwargs) -> Organization:
        existing = self.db.query(Organization).filter(Organization.name == name).first()
        if existing:
            raise ConflictException(f"机构名称已存在: {name}")
        
        org = Organization(
            id=str(uuid4()),
            name=name,
            short_name=short_name or name,
            **kwargs
        )
        self.db.add(org)
        self.db.commit()
        self.db.refresh(org)
        return org

    def get(self, org_id: str) -> Optional[Organization]:
        return self.db.query(Organization).filter(Organization.id == org_id).first()

    def get_by_name(self, name: str) -> Optional[Organization]:
        return self.db.query(Organization).filter(Organization.name == name).first()

    def list(self, status: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Organization]:
        query = self.db.query(Organization)
        if status:
            query = query.filter(Organization.status == status)
        return query.offset(skip).limit(limit).all()

    def update(self, org_id: str, **kwargs) -> Organization:
        org = self.get(org_id)
        if not org:
            raise NotFoundException(f"机构不存在: {org_id}")
        
        for key, value in kwargs.items():
            if hasattr(org, key) and value is not None:
                setattr(org, key, value)
        
        self.db.commit()
        self.db.refresh(org)
        return org

    def delete(self, org_id: str) -> bool:
        org = self.get(org_id)
        if not org:
            raise NotFoundException(f"机构不存在: {org_id}")
        
        self.db.delete(org)
        self.db.commit()
        return True
