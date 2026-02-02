from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from backend.app.models.user import User
from backend.app.models.organization import UserOrganization
from backend.app.config.security import get_password_hash
from backend.app.common.exceptions import NotFoundException, ConflictException
from backend.app.modules.admin.services.permission_service import PermissionService


class UserAdminService:
    def __init__(self, db: Session):
        self.db = db
        self.permission_service = PermissionService(db)

    def create_user(self, user_data: dict, current_user_id: str) -> User:
        existing = self.db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            raise ConflictException(f"邮箱已存在: {user_data['email']}")
        
        user = User(
            id=str(uuid4()),
            email=user_data["email"],
            name=user_data["name"],
            password_hash=get_password_hash(user_data["password"]),
            role=user_data.get("role", "student"),
            org_id=user_data.get("org_id"),
            phone=user_data.get("phone"),
            department=user_data.get("department"),
            title=user_data.get("title"),
            employee_id=user_data.get("employee_id")
        )
        self.db.add(user)
        
        if user_data.get("org_id") and user_data.get("role_id"):
            user_org = UserOrganization(
                user_id=user.id,
                org_id=user_data["org_id"],
                role_id=user_data["role_id"],
                status="active"
            )
            self.db.add(user_org)
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: str, current_user_id: str) -> Optional[User]:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        if not self.permission_service.is_super_admin(current_user_id):
            user_orgs = self.permission_service.get_user_orgs(current_user_id)
            if user.org_id and user.org_id not in user_orgs:
                return None
        
        return user

    def list_users(
        self,
        current_user_id: str,
        org_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[User], int]:
        query = self.db.query(User)
        
        if not self.permission_service.is_super_admin(current_user_id):
            user_orgs = self.permission_service.get_user_orgs(current_user_id)
            if org_id:
                if org_id not in user_orgs:
                    return [], 0
                query = query.filter(User.org_id == org_id)
            else:
                query = query.filter(User.org_id.in_(user_orgs))
        elif org_id:
            query = query.filter(User.org_id == org_id)
        
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        return users, total

    def update_user(self, user_id: str, user_data: dict, current_user_id: str) -> User:
        user = self.get_user(user_id, current_user_id)
        if not user:
            raise NotFoundException(f"用户不存在: {user_id}")
        
        for key, value in user_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: str, current_user_id: str) -> bool:
        user = self.get_user(user_id, current_user_id)
        if not user:
            raise NotFoundException(f"用户不存在: {user_id}")
        
        self.db.delete(user)
        self.db.commit()
        return True

    def assign_org(self, user_id: str, org_id: str, role_id: str, current_user_id: str) -> UserOrganization:
        user = self.get_user(user_id, current_user_id)
        if not user:
            raise NotFoundException(f"用户不存在: {user_id}")
        
        existing = self.db.query(UserOrganization).filter(
            UserOrganization.user_id == user_id,
            UserOrganization.org_id == org_id
        ).first()
        
        if existing:
            existing.role_id = role_id
            existing.status = "active"
        else:
            existing = UserOrganization(
                user_id=user_id,
                org_id=org_id,
                role_id=role_id,
                status="active"
            )
            self.db.add(existing)
        
        self.db.commit()
        self.db.refresh(existing)
        return existing

    def remove_org(self, user_id: str, org_id: str, current_user_id: str) -> bool:
        user = self.get_user(user_id, current_user_id)
        if not user:
            raise NotFoundException(f"用户不存在: {user_id}")
        
        user_org = self.db.query(UserOrganization).filter(
            UserOrganization.user_id == user_id,
            UserOrganization.org_id == org_id
        ).first()
        
        if user_org:
            self.db.delete(user_org)
            self.db.commit()
            return True
        return False
