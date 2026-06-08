from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile, Query
from fastapi.responses import StreamingResponse, FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session
from typing import Optional
import io

from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.core.common.middleware.permission import get_current_user_dependency
from backend.app.modules.admin.services.permission_service import PermissionService
from backend.app.modules.admin.services.file_service import FileService
from backend.app.modules.admin.services.audit_service import AuditService
from backend.app.modules.admin.schemas.file import (
    FileResponse as FileRecordResponse,
    FileListResponse,
    FileUploadResponse,
)
from backend.app.core.common.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/admin/files", tags=["文件管理"])


@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    org_id: Optional[str] = Query(None),
    category: str = Query("courseware", description="文件分类"),
    resource_type: Optional[str] = Query(None, description="关联资源类型"),
    resource_id: Optional[str] = Query(None, description="关联资源ID"),
    description: Optional[str] = Query(None, description="文件描述"),
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:edit")
    
    file_service = FileService(db)
    audit_service = AuditService(db)
    
    try:
        content = await file.read()
        file_record = file_service.save_file(
            file_content=content,
            filename=file.filename or "unknown",
            org_id=org_id or current_user.org_id,
            uploaded_by=current_user.id,
            category=category,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description
        )
        
        audit_service.log(
            user_id=current_user.id,
            action="upload_file",
            resource_type="file",
            resource_id=file_record.id,
            org_id=file_record.org_id,
            changes={"filename": file_record.filename, "category": category}
        )
        
        file_url = f"/api/admin/files/{file_record.id}/download"
        return FileUploadResponse(file=file_record, url=file_url)
    except ConflictException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=FileListResponse)
async def list_files(
    org_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    resource_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:view")
    
    file_service = FileService(db)
    files, total = file_service.list_files(
        current_user.id,
        org_id=org_id,
        category=category,
        resource_type=resource_type,
        resource_id=resource_id,
        skip=skip,
        limit=limit
    )
    return FileListResponse(files=files, total=total, skip=skip, limit=limit)


@router.get("/{file_id}", response_model=FileRecordResponse)
async def get_file(
    file_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:view"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:view")
    
    file_service = FileService(db)
    file_record = file_service.get_file(file_id, current_user.id)
    if not file_record:
        raise HTTPException(status_code=404, detail="文件不存在")
    return file_record


@router.get("/{file_id}/download")
async def download_file(
    file_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    file_service = FileService(db)
    
    try:
        content, mime_type, filename = file_service.get_file_content(file_id, current_user.id)
        return StreamingResponse(
            io.BytesIO(content),
            media_type=mime_type,
            headers={"Content-Disposition": f'inline; filename="{filename}"'}
        )
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{file_id}/view")
async def view_file(
    file_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    file_service = FileService(db)
    
    try:
        file_record = file_service.get_file(file_id, current_user.id)
        if not file_record:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        from pathlib import Path
        file_path = Path(file_record.file_path)
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        return FastAPIFileResponse(
            path=str(file_path),
            media_type=file_record.mime_type or "application/octet-stream",
            filename=file_record.filename
        )
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    permission_service = PermissionService(db)
    if not permission_service.has_permission(current_user.id, "course:edit"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足: course:edit")
    
    file_service = FileService(db)
    audit_service = AuditService(db)
    
    try:
        file_record = file_service.get_file(file_id, current_user.id)
        if not file_record:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        file_service.delete_file(file_id, current_user.id)
        audit_service.log(
            user_id=current_user.id,
            action="delete_file",
            resource_type="file",
            resource_id=file_id,
            org_id=file_record.org_id
        )
        return None
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
