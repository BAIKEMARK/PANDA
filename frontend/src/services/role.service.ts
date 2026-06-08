import api from './api';
import type { Role, Permission } from '../types/admin.types';

class RoleService {
  async list(scope?: string): Promise<Role[]> {
    const params: Record<string, string> = {};
    if (scope) params.scope = scope;
    const response = await api.get<Role[]>('/admin/roles', { params });
    return response.data;
  }

  async get(id: string): Promise<Role> {
    const response = await api.get<Role>(`/admin/roles/${id}`);
    return response.data;
  }

  async create(data: Partial<Role>): Promise<Role> {
    const response = await api.post<Role>('/admin/roles', data);
    return response.data;
  }

  async update(id: string, data: Partial<Role>): Promise<Role> {
    const response = await api.put<Role>(`/admin/roles/${id}`, data);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/roles/${id}`);
  }

  async assignPermissions(id: string, permissionIds: string[]): Promise<Role> {
    const response = await api.post<Role>(`/admin/roles/${id}/permissions`, {
      permission_ids: permissionIds,
    });
    return response.data;
  }

  async listAllPermissions(): Promise<Permission[]> {
    const response = await api.get<Permission[]>('/admin/roles/permissions/all');
    return response.data;
  }
}

export default new RoleService();
