from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FileResponse(BaseModel):
    id: str
    org_id: Optional[str]
    filename: str
    stored_filename: str
    file_path: str
    file_type: Optional[str]
    file_size: Optional[int]
    mime_type: Optional[str]
    category: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    uploaded_by: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FileListResponse(BaseModel):
    files: list[FileResponse]
    total: int
    skip: int
    limit: int


class FileUploadResponse(BaseModel):
    file: FileResponse
    url: str
