from sqlalchemy import Column, String, DateTime, Integer, Enum as SQLEnum, Text
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(CHAR(36), primary_key=True, comment="文件ID")
    org_id = Column(CHAR(36), index=True, comment="机构ID")
    filename = Column(String(255), nullable=False, comment="原始文件名")
    stored_filename = Column(String(255), nullable=False, comment="存储文件名")
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_type = Column(String(50), comment="文件类型")
    file_size = Column(Integer, comment="文件大小(字节)")
    mime_type = Column(String(100), comment="MIME类型")
    category = Column(String(50), default="courseware", comment="文件分类: courseware/document/image/video")
    resource_type = Column(String(50), comment="关联资源类型: course/scenario/exam")
    resource_id = Column(CHAR(36), index=True, comment="关联资源ID")
    uploaded_by = Column(CHAR(36), nullable=False, comment="上传人")
    description = Column(Text, comment="文件描述")
    status = Column(SQLEnum("active", "deleted", name="file_status"), default="active", comment="状态")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
