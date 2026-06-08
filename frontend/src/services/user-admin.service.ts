import api from './api';
import type { User, UserListResponse, UserOrgAssign } from '../types/admin.types';

class UserAdminService {
  async list(orgId?: string, skip = 0, limit = 100): Promise<UserListResponse> {
    const params: Record<string, string | number> = { skip, limit };
    if (orgId) params.org_id = orgId;
    const response = await api.get<UserListResponse>('/admin/users', { params });
    return response.data;
  }

  async get(id: string): Promise<User> {
    const response = await api.get<User>(`/admin/users/${id}`);
    return response.data;
  }

  async create(data: Partial<User> & { password: string; org_role?: UserOrgAssign }): Promise<User> {
    const { org_role, ...userData } = data;
    const response = await api.post<User>('/admin/users', userData, {
      params: org_role,
    });
    return response.data;
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    const response = await api.put<User>(`/admin/users/${id}`, data);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/users/${id}`);
  }

  async assignOrg(userId: string, orgId: string, roleId: string): Promise<User> {
    const response = await api.post<User>(`/admin/users/${userId}/organizations`, {
      org_id: orgId,
      role_id: roleId,
    });
    return response.data;
  }

  async removeOrg(userId: string, orgId: string): Promise<void> {
    await api.delete(`/admin/users/${userId}/organizations/${orgId}`);
  }
}

export default new UserAdminService();
