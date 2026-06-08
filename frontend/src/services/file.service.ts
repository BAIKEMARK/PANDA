import api from './api';
import type { FileInfo, FileListResponse, FileUploadResponse } from '../types/file.types';

class FileService {
  async upload(
    file: File,
    category = 'courseware',
    orgId?: string,
    resourceType?: string,
    resourceId?: string,
    description?: string
  ): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    const params: Record<string, string> = { category };
    if (orgId) params.org_id = orgId;
    if (resourceType) params.resource_type = resourceType;
    if (resourceId) params.resource_id = resourceId;
    if (description) params.description = description;

    const response = await api.post<FileUploadResponse>('/admin/files/upload', formData, {
      params,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async list(
    orgId?: string,
    category?: string,
    resourceType?: string,
    resourceId?: string,
    skip = 0,
    limit = 100
  ): Promise<FileListResponse> {
    const params: Record<string, string | number> = { skip, limit };
    if (orgId) params.org_id = orgId;
    if (category) params.category = category;
    if (resourceType) params.resource_type = resourceType;
    if (resourceId) params.resource_id = resourceId;

    const response = await api.get<FileListResponse>('/admin/files', { params });
    return response.data;
  }

  async get(id: string): Promise<FileInfo> {
    const response = await api.get<FileInfo>(`/admin/files/${id}`);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/files/${id}`);
  }

  getDownloadUrl(id: string): string {
    return `${api.defaults.baseURL}/admin/files/${id}/download`;
  }

  getViewUrl(id: string): string {
    return `${api.defaults.baseURL}/admin/files/${id}/view`;
  }
}

export default new FileService();
