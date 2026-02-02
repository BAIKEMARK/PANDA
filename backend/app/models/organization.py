from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.db.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(CHAR(36), primary_key=True, comment="机构ID")
    name = Column(String(255), nullable=False, comment="机构名称")
    short_name = Column(String(100), comment="简称")
    logo_url = Column(String(500), comment="LOGO")
    contact_name = Column(String(100), comment="联系人")
    contact_phone = Column(String(50), comment="联系电话")
    contact_email = Column(String(255), comment="联系邮箱")
    valid_until = Column(DateTime, comment="有效期")
    status = Column(SQLEnum("active", "inactive", name="org_status"), default="active", comment="状态")
    config = Column(JSON, comment="机构配置")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class Role(Base):
    __tablename__ = "roles"

    id = Column(CHAR(36), primary_key=True, comment="角色ID")
    code = Column(String(50), unique=True, nullable=False, index=True, comment="角色代码")
    name = Column(String(100), nullable=False, comment="角色名称")
    description = Column(String(500), comment="角色说明")
    scope = Column(SQLEnum("system", "org", name="role_scope"), default="org", comment="作用域")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(CHAR(36), primary_key=True, comment="权限ID")
    code = Column(String(100), unique=True, nullable=False, index=True, comment="权限代码")
    name = Column(String(100), nullable=False, comment="权限名称")
    module = Column(String(50), nullable=False, index=True, comment="模块")
    action = Column(String(50), nullable=False, comment="操作")
    description = Column(String(500), comment="权限说明")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(CHAR(36), primary_key=True, comment="角色ID")
    permission_id = Column(CHAR(36), primary_key=True, comment="权限ID")


class UserOrganization(Base):
    __tablename__ = "user_organizations"

    user_id = Column(CHAR(36), primary_key=True, comment="用户ID")
    org_id = Column(CHAR(36), primary_key=True, comment="机构ID")
    role_id = Column(CHAR(36), nullable=False, comment="角色ID")
    status = Column(SQLEnum("active", "inactive", name="user_org_status"), default="active", comment="状态")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
