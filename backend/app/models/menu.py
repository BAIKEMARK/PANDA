"""
Menu ORM Models
菜单数据库模型
"""
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from backend.app.db.database import Base


class Menu(Base):
    """菜单表"""
    __tablename__ = "menus"

    id = Column(CHAR(36), primary_key=True, comment="菜单ID")
    parent_id = Column(CHAR(36), ForeignKey("menus.id", ondelete="CASCADE"), nullable=True, comment="父菜单ID")
    title = Column(String(100), nullable=False, comment="菜单标题")
    icon = Column(String(50), comment="图标名称")
    path = Column(String(200), comment="路由路径")
    component = Column(String(200), comment="组件路径")
    sort_order = Column(Integer, default=0, comment="排序")
    is_visible = Column(Boolean, default=True, comment="是否可见")
    is_enabled = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关联子菜单（自引用）
    children = relationship(
        "Menu",
        backref=backref("parent", remote_side=[id]),
        cascade="all, delete-orphan"
    )
    # 关联权限
    permissions = relationship(
        "RoleMenuPermission",
        back_populates="menu",
        cascade="all, delete-orphan"
    )


class RoleMenuPermission(Base):
    """角色菜单权限表"""
    __tablename__ = "role_menu_permissions"

    id = Column(CHAR(36), primary_key=True, comment="权限ID")
    role = Column(
        SQLEnum("student", "instructor", "admin", name="role_enum"),
        nullable=False,
        comment="角色"
    )
    menu_id = Column(CHAR(36), ForeignKey("menus.id", ondelete="CASCADE"), nullable=False, comment="菜单ID")
    can_view = Column(Boolean, default=True, comment="可查看")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关联菜单
    menu = relationship("Menu", back_populates="permissions")