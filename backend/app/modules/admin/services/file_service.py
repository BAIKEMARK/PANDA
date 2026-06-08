from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import uuid4
from pathlib import Path

from backend.app.models.file import File
from backend.app.core.config.settings import settings
from backend.app.core.common.exceptions import NotFoundException, ConflictException
from backend.app.modules.admin.services.permission_service import PermissionService


class FileService:
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.permission_service = PermissionService(db)

    def save_file(
        self,
        file_content: bytes,
        filename: str,
        org_id: Optional[str],
        uploaded_by: str,
        category: str = "courseware",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        description: Optional[str] = None
    ) -> File:
        file_ext = Path(filename).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise ConflictException(f"不支持的文件类型: {file_ext}")

        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            raise ConflictException(f"文件大小超过限制: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB")

        stored_filename = f"{uuid4().hex}{file_ext}"
        category_dir = self.upload_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        file_path = category_dir / stored_filename
        with open(file_path, 'wb') as f:
            f.write(file_content)

        import mimetypes
        mime_type, _ = mimetypes.guess_type(filename)
        
        relative_path = file_path.relative_to(Path.cwd())

        file_record = File(
            id=str(uuid4()),
            org_id=org_id,
            filename=filename,
            stored_filename=stored_filename,
            file_path=str(relative_path),
            file_type=file_ext,
            file_size=len(file_content),
            mime_type=mime_type,
            category=category,
            resource_type=resource_type,
            resource_id=resource_id,
            uploaded_by=uploaded_by,
            description=description,
            status="active"
        )
        self.db.add(file_record)
        self.db.commit()
        self.db.refresh(file_record)
        return file_record

    def get_file(self, file_id: str, current_user_id: str) -> Optional[File]:
        file_record = self.db.query(File).filter(
            File.id == file_id,
            File.status == "active"
        ).first()
        
        if not file_record:
            return None
        
        if not self.permission_service.is_super_admin(current_user_id):
            if file_record.org_id:
                if not self.permission_service.user_belongs_to_org(current_user_id, file_record.org_id):
                    return None
        
        return file_record

    def list_files(
        self,
        current_user_id: str,
        org_id: Optional[str] = None,
        category: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[File], int]:
        query = self.db.query(File).filter(File.status == "active")
        
        if not self.permission_service.is_super_admin(current_user_id):
            user_orgs = self.permission_service.get_user_orgs(current_user_id)
            if org_id:
                if org_id not in user_orgs:
                    return [], 0
                query = query.filter(File.org_id == org_id)
            else:
                query = query.filter((File.org_id.in_(user_orgs)) | (File.org_id.is_(None)))
        elif org_id:
            query = query.filter(File.org_id == org_id)
        
        if category:
            query = query.filter(File.category == category)
        if resource_type:
            query = query.filter(File.resource_type == resource_type)
        if resource_id:
            query = query.filter(File.resource_id == resource_id)
        
        total = query.count()
        files = query.order_by(File.created_at.desc()).offset(skip).limit(limit).all()
        return files, total

    def delete_file(self, file_id: str, current_user_id: str) -> bool:
        file_record = self.get_file(file_id, current_user_id)
        if not file_record:
            raise NotFoundException(f"文件不存在: {file_id}")
        
        file_path = Path(file_record.file_path)
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path
        if file_path.exists():
            file_path.unlink()
        
        file_record.status = "deleted"
        self.db.commit()
        return True

    def get_file_content(self, file_id: str, current_user_id: str) -> tuple[bytes, str, str]:
        file_record = self.get_file(file_id, current_user_id)
        if not file_record:
            raise NotFoundException(f"文件不存在: {file_id}")
        
        file_path = Path(file_record.file_path)
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path
        
        if not file_path.exists():
            raise NotFoundException(f"文件不存在: {file_path}")
        
        with open(file_path, 'rb') as f:
            content = f.read()
        
        return content, file_record.mime_type or "application/octet-stream", file_record.filename
