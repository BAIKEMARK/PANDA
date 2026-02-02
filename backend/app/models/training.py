from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, JSON, Integer
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from backend.app.db.database import Base


class TrainingClass(Base):
    __tablename__ = "training_classes"

    id = Column(CHAR(36), primary_key=True, comment="班级ID")
    org_id = Column(CHAR(36), nullable=False, index=True, comment="机构ID")
    name = Column(String(255), nullable=False, comment="班级名称")
    description = Column(String(1000), comment="描述")
    start_date = Column(DateTime, nullable=False, comment="开始时间")
    end_date = Column(DateTime, nullable=False, comment="结束时间")
    trainer_id = Column(CHAR(36), comment="负责人ID")
    credit_rule = Column(JSON, comment="学分规则")
    completion_rule = Column(JSON, comment="结业标准")
    status = Column(SQLEnum("draft", "active", "completed", "archived", name="class_status"), default="draft", comment="状态")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class ClassStudent(Base):
    __tablename__ = "class_students"

    class_id = Column(CHAR(36), primary_key=True, comment="班级ID")
    user_id = Column(CHAR(36), primary_key=True, comment="学员ID")
    joined_at = Column(DateTime, default=datetime.utcnow, comment="加入时间")
    status = Column(SQLEnum("active", "completed", "dropped", name="student_status"), default="active", comment="状态")


class ClassTask(Base):
    __tablename__ = "class_tasks"

    id = Column(CHAR(36), primary_key=True, comment="任务ID")
    class_id = Column(CHAR(36), nullable=False, index=True, comment="班级ID")
    resource_type = Column(SQLEnum("course", "scenario", "exam", name="resource_type"), nullable=False, comment="资源类型")
    resource_id = Column(CHAR(36), nullable=False, comment="资源ID")
    resource_version = Column(String(50), comment="资源版本(锁定)")
    deadline = Column(DateTime, comment="截止日期")
    sort_order = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
