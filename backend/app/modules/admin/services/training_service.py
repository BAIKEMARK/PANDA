from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from backend.app.models.training import TrainingClass, ClassStudent, ClassTask
from backend.app.core.common.exceptions import NotFoundException, ConflictException
from backend.app.modules.admin.services.permission_service import PermissionService


class TrainingService:
    def __init__(self, db: Session):
        self.db = db
        self.permission_service = PermissionService(db)

    def create_class(self, class_data: dict, current_user_id: str) -> TrainingClass:
        if not self.permission_service.is_super_admin(current_user_id):
            if not self.permission_service.user_belongs_to_org(current_user_id, class_data["org_id"]):
                raise ConflictException("无权在该机构创建班级")
        
        training_class = TrainingClass(
            id=str(uuid4()),
            **class_data
        )
        self.db.add(training_class)
        self.db.commit()
        self.db.refresh(training_class)
        return training_class

    def get_class(self, class_id: str, current_user_id: str) -> Optional[TrainingClass]:
        training_class = self.db.query(TrainingClass).filter(TrainingClass.id == class_id).first()
        if not training_class:
            return None
        
        if not self.permission_service.is_super_admin(current_user_id):
            if not self.permission_service.user_belongs_to_org(current_user_id, training_class.org_id):
                return None
        
        return training_class

    def list_classes(
        self,
        current_user_id: str,
        org_id: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[TrainingClass], int]:
        query = self.db.query(TrainingClass)
        
        if not self.permission_service.is_super_admin(current_user_id):
            user_orgs = self.permission_service.get_user_orgs(current_user_id)
            if org_id:
                if org_id not in user_orgs:
                    return [], 0
                query = query.filter(TrainingClass.org_id == org_id)
            else:
                query = query.filter(TrainingClass.org_id.in_(user_orgs))
        elif org_id:
            query = query.filter(TrainingClass.org_id == org_id)
        
        if status:
            query = query.filter(TrainingClass.status == status)
        
        total = query.count()
        classes = query.order_by(TrainingClass.created_at.desc()).offset(skip).limit(limit).all()
        return classes, total

    def update_class(self, class_id: str, class_data: dict, current_user_id: str) -> TrainingClass:
        training_class = self.get_class(class_id, current_user_id)
        if not training_class:
            raise NotFoundException(f"班级不存在: {class_id}")
        
        for key, value in class_data.items():
            if hasattr(training_class, key) and value is not None:
                setattr(training_class, key, value)
        
        self.db.commit()
        self.db.refresh(training_class)
        return training_class

    def delete_class(self, class_id: str, current_user_id: str) -> bool:
        training_class = self.get_class(class_id, current_user_id)
        if not training_class:
            raise NotFoundException(f"班级不存在: {class_id}")
        
        self.db.delete(training_class)
        self.db.commit()
        return True

    def add_students(self, class_id: str, user_ids: List[str], current_user_id: str) -> List[ClassStudent]:
        training_class = self.get_class(class_id, current_user_id)
        if not training_class:
            raise NotFoundException(f"班级不存在: {class_id}")
        
        students = []
        for user_id in user_ids:
            existing = self.db.query(ClassStudent).filter(
                ClassStudent.class_id == class_id,
                ClassStudent.user_id == user_id
            ).first()
            
            if not existing:
                student = ClassStudent(
                    class_id=class_id,
                    user_id=user_id,
                    status="active"
                )
                self.db.add(student)
                students.append(student)
        
        self.db.commit()
        return students

    def remove_student(self, class_id: str, user_id: str, current_user_id: str) -> bool:
        training_class = self.get_class(class_id, current_user_id)
        if not training_class:
            raise NotFoundException(f"班级不存在: {class_id}")
        
        student = self.db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id,
            ClassStudent.user_id == user_id
        ).first()
        
        if student:
            self.db.delete(student)
            self.db.commit()
            return True
        return False

    def list_students(self, class_id: str, current_user_id: str) -> List[ClassStudent]:
        training_class = self.get_class(class_id, current_user_id)
        if not training_class:
            raise NotFoundException(f"班级不存在: {class_id}")
        
        return self.db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()

    def add_task(self, class_id: str, task_data: dict, current_user_id: str) -> ClassTask:
        training_class = self.get_class(class_id, current_user_id)
        if not training_class:
            raise NotFoundException(f"班级不存在: {class_id}")
        
        task = ClassTask(
            id=str(uuid4()),
            class_id=class_id,
            **task_data
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def list_tasks(self, class_id: str, current_user_id: str) -> List[ClassTask]:
        training_class = self.get_class(class_id, current_user_id)
        if not training_class:
            raise NotFoundException(f"班级不存在: {class_id}")
        
        return self.db.query(ClassTask).filter(
            ClassTask.class_id == class_id
        ).order_by(ClassTask.sort_order).all()

    def delete_task(self, task_id: str, current_user_id: str) -> bool:
        task = self.db.query(ClassTask).filter(ClassTask.id == task_id).first()
        if not task:
            raise NotFoundException(f"任务不存在: {task_id}")
        
        training_class = self.get_class(task.class_id, current_user_id)
        if not training_class:
            raise NotFoundException(f"无权操作该任务")
        
        self.db.delete(task)
        self.db.commit()
        return True
