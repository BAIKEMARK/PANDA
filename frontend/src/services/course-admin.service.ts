import api from './api';

export interface Course {
  id: string;
  title: string;
  content_url?: string;
  video_url?: string;
  sort_order: number;
  level: 'L1' | 'L2' | 'L3' | 'L4';
  description?: string;
  org_id?: string;
  scope: 'private' | 'platform' | 'shared';
  version: string;
  version_notes?: string;
  status: 'draft' | 'pending' | 'published' | 'archived';
  published_at?: string;
  published_by?: string;
  created_at: string;
  updated_at: string;
}

export interface CourseListResponse {
  courses: Course[];
  total: number;
  skip: number;
  limit: number;
}

class CourseAdminService {
  async list(params?: {
    org_id?: string;
    scope?: string;
    status?: string;
    level?: string;
    skip?: number;
    limit?: number;
  }): Promise<CourseListResponse> {
    const response = await api.get<CourseListResponse>('/admin/courses', { params });
    return response.data;
  }

  async get(id: string): Promise<Course> {
    const response = await api.get<Course>(`/admin/courses/${id}`);
    return response.data;
  }

  async create(data: Partial<Course>): Promise<Course> {
    const response = await api.post<Course>('/admin/courses', data);
    return response.data;
  }

  async update(id: string, data: Partial<Course>): Promise<Course> {
    const response = await api.put<Course>(`/admin/courses/${id}`, data);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/courses/${id}`);
  }

  async publish(id: string): Promise<Course> {
    const response = await api.post<Course>(`/admin/courses/${id}/publish`);
    return response.data;
  }

  async archive(id: string): Promise<Course> {
    const response = await api.post<Course>(`/admin/courses/${id}/archive`);
    return response.data;
  }
}

export default new CourseAdminService();
