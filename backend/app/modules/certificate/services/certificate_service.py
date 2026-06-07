from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from backend.app.models.certificate import Certificate
from backend.app.core.common.exceptions import NotFoundException, ConflictException


class CertificateService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: str, certificate_number: str, **kwargs) -> Certificate:
        existing = self.db.query(Certificate).filter(
            Certificate.certificate_number == certificate_number
        ).first()
        if existing:
            raise ConflictException(f"证书编号已存在: {certificate_number}")
        
        cert = Certificate(
            id=str(uuid4()),
            user_id=user_id,
            certificate_number=certificate_number,
            **kwargs
        )
        self.db.add(cert)
        self.db.commit()
        self.db.refresh(cert)
        return cert

    def get(self, cert_id: str) -> Optional[Certificate]:
        return self.db.query(Certificate).filter(Certificate.id == cert_id).first()

    def list(self, user_id: Optional[str] = None, org_id: Optional[str] = None, 
             skip: int = 0, limit: int = 100) -> List[Certificate]:
        query = self.db.query(Certificate)
        if user_id:
            query = query.filter(Certificate.user_id == user_id)
        if org_id:
            query = query.filter(Certificate.org_id == org_id)
        return query.offset(skip).limit(limit).all()

    def update(self, cert_id: str, **kwargs) -> Certificate:
        cert = self.get(cert_id)
        if not cert:
            raise NotFoundException(f"证书不存在: {cert_id}")
        
        for key, value in kwargs.items():
            if hasattr(cert, key) and value is not None:
                setattr(cert, key, value)
        
        self.db.commit()
        self.db.refresh(cert)
        return cert

    def delete(self, cert_id: str) -> bool:
        cert = self.get(cert_id)
        if not cert:
            raise NotFoundException(f"证书不存在: {cert_id}")
        
        self.db.delete(cert)
        self.db.commit()
        return True
