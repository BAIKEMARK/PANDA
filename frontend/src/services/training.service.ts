import api from './api';
import type { TrainingClass, ClassStudent, ClassTask } from '../types/admin.types';

class TrainingService {
  async list(orgId?: string, status?: string, skip = 0, limit = 100): Promise<TrainingClass[]> {
    const params: Record<string, string | number> = { skip, limit };
    if (orgId) params.org_id = orgId;
    if (status) params.status = status;
    const response = await api.get<TrainingClass[]>('/admin/classes', { params });
    return response.data;
  }

  async get(id: string): Promise<TrainingClass> {
    const response = await api.get<TrainingClass>(`/admin/classes/${id}`);
    return response.data;
  }

  async create(data: Partial<TrainingClass>): Promise<TrainingClass> {
    const response = await api.post<TrainingClass>('/admin/classes', data);
    return response.data;
  }

  async update(id: string, data: Partial<TrainingClass>): Promise<TrainingClass> {
    const response = await api.put<TrainingClass>(`/admin/classes/${id}`, data);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/classes/${id}`);
  }

  async addStudents(classId: string, userIds: string[]): Promise<{ message: string }> {
    const response = await api.post(`/admin/classes/${classId}/students`, {
      user_ids: userIds,
    });
    return response.data;
  }

  async removeStudent(classId: string, userId: string): Promise<void> {
    await api.delete(`/admin/classes/${classId}/students/${userId}`);
  }

  async listStudents(classId: string): Promise<ClassStudent[]> {
    const response = await api.get<ClassStudent[]>(`/admin/classes/${classId}/students`);
    return response.data;
  }

  async addTask(classId: string, data: Partial<ClassTask>): Promise<ClassTask> {
    const response = await api.post<ClassTask>(`/admin/classes/${classId}/tasks`, data);
    return response.data;
  }

  async listTasks(classId: string): Promise<ClassTask[]> {
    const response = await api.get<ClassTask[]>(`/admin/classes/${classId}/tasks`);
    return response.data;
  }

  async deleteTask(taskId: string): Promise<void> {
    await api.delete(`/admin/classes/tasks/${taskId}`);
  }
}

export default new TrainingService();
