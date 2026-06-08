import api from './api';
import type { Organization } from '../types/admin.types';

class OrganizationService {
  async list(status?: string, skip = 0, limit = 100): Promise<Organization[]> {
    const params: Record<string, string | number> = { skip, limit };
    if (status) params.status = status;
    const response = await api.get<Organization[]>('/admin/organizations', { params });
    return response.data;
  }

  async get(id: string): Promise<Organization> {
    const response = await api.get<Organization>(`/admin/organizations/${id}`);
    return response.data;
  }

  async create(data: Partial<Organization>): Promise<Organization> {
    const response = await api.post<Organization>('/admin/organizations', data);
    return response.data;
  }

  async update(id: string, data: Partial<Organization>): Promise<Organization> {
    const response = await api.put<Organization>(`/admin/organizations/${id}`, data);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/organizations/${id}`);
  }
}

export default new OrganizationService();
