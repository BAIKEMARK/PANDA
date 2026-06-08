import api from './api';
import type { Question } from '../types/admin.types';

class QuestionService {
  async list(orgId?: string, questionType?: string, status?: string, skip = 0, limit = 100): Promise<Question[]> {
    const params: Record<string, string | number> = { skip, limit };
    if (orgId) params.org_id = orgId;
    if (questionType) params.question_type = questionType;
    if (status) params.status = status;
    const response = await api.get<Question[]>('/admin/questions', { params });
    return response.data;
  }

  async get(id: string): Promise<Question> {
    const response = await api.get<Question>(`/admin/questions/${id}`);
    return response.data;
  }

  async create(data: Partial<Question>): Promise<Question> {
    const response = await api.post<Question>('/admin/questions', data);
    return response.data;
  }

  async update(id: string, data: Partial<Question>): Promise<Question> {
    const response = await api.put<Question>(`/admin/questions/${id}`, data);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/questions/${id}`);
  }
}

export default new QuestionService();
