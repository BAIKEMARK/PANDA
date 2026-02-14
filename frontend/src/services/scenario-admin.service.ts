import api from './api';

export interface Scenario {
  id: string;
  title: string;
  description?: string;
  system_prompt: string;
  patient_background?: string;
  knowledge_tags?: string;
  difficulty: number;
  time_period?: string;
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

export interface ScenarioListResponse {
  scenarios: Scenario[];
  total: number;
  skip: number;
  limit: number;
}

class ScenarioAdminService {
  async list(params?: {
    org_id?: string;
    scope?: string;
    status?: string;
    difficulty?: number;
    skip?: number;
    limit?: number;
  }): Promise<ScenarioListResponse> {
    const response = await api.get<ScenarioListResponse>('/admin/scenarios', { params });
    return response.data;
  }

  async get(id: string): Promise<Scenario> {
    const response = await api.get<Scenario>(`/admin/scenarios/${id}`);
    return response.data;
  }

  async create(data: Partial<Scenario>): Promise<Scenario> {
    const response = await api.post<Scenario>('/admin/scenarios', data);
    return response.data;
  }

  async update(id: string, data: Partial<Scenario>): Promise<Scenario> {
    const response = await api.put<Scenario>(`/admin/scenarios/${id}`, data);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/scenarios/${id}`);
  }

  async publish(id: string): Promise<Scenario> {
    const response = await api.post<Scenario>(`/admin/scenarios/${id}/publish`);
    return response.data;
  }

  async archive(id: string): Promise<Scenario> {
    const response = await api.post<Scenario>(`/admin/scenarios/${id}/archive`);
    return response.data;
  }
}

export default new ScenarioAdminService();
