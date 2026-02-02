from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from backend.app.models.certificate import CertificateTemplate
from backend.app.common.exceptions import NotFoundException, ConflictException


class CertificateTemplateService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, org_id: str, name: str, **kwargs) -> CertificateTemplate:
        template = CertificateTemplate(
            id=str(uuid4()),
            org_id=org_id,
            name=name,
            **kwargs
        )
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def get(self, template_id: str) -> Optional[CertificateTemplate]:
        return self.db.query(CertificateTemplate).filter(
            CertificateTemplate.id == template_id
        ).first()

    def list(self, org_id: Optional[str] = None, status: Optional[str] = None,
             skip: int = 0, limit: int = 100) -> List[CertificateTemplate]:
        query = self.db.query(CertificateTemplate)
        if org_id:
            query = query.filter(CertificateTemplate.org_id == org_id)
        if status:
            query = query.filter(CertificateTemplate.status == status)
        return query.offset(skip).limit(limit).all()

    def update(self, template_id: str, **kwargs) -> CertificateTemplate:
        template = self.get(template_id)
        if not template:
            raise NotFoundException(f"模板不存在: {template_id}")
        
        for key, value in kwargs.items():
            if hasattr(template, key) and value is not None:
                setattr(template, key, value)
        
        self.db.commit()
        self.db.refresh(template)
        return template

    def delete(self, template_id: str) -> bool:
        template = self.get(template_id)
        if not template:
            raise NotFoundException(f"模板不存在: {template_id}")
        
        self.db.delete(template)
        self.db.commit()
        return True
