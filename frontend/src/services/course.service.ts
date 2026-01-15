/**
 * 课程服务
 * 处理课程相关的API调用
 */
import api from './api';
import type { Course, CourseLevel } from '../types/course.types';

class CourseService {
  /**
   * 获取课程列表 (可选按层级筛选)
   */
  async getCourses(level?: CourseLevel): Promise<Course[]> {
    const params = level ? { level } : {};
    const response = await api.get<Course[]>('/courses/', { params });
    return response.data;
  }

  /**
   * 获取单个课程详情
   */
  async getCourse(courseId: string): Promise<Course> {
    const response = await api.get<Course>(`/courses/${courseId}`);
    return response.data;
  }

  /**
   * 创建课程 (管理员功能)
   */
  async createCourse(data: Partial<Course>): Promise<Course> {
    const response = await api.post<Course>('/courses/', data);
    return response.data;
  }

  /**
   * 更新课程 (管理员功能)
   */
  async updateCourse(courseId: string, data: Partial<Course>): Promise<Course> {
    const response = await api.put<Course>(`/courses/${courseId}`, data);
    return response.data;
  }

  /**
   * 删除课程 (管理员功能)
   */
  async deleteCourse(courseId: string): Promise<void> {
    await api.delete(`/courses/${courseId}`);
  }
}

export default new CourseService();
