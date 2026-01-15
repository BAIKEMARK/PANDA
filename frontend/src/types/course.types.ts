/**
 * 课程相关类型定义
 * 对应后端 backend/app/schemas/course.py 和 backend/app/models/course.py
 */

// 课程层级枚举
export enum CourseLevel {
  L1 = 'L1',
  L2 = 'L2',
  L3 = 'L3',
  L4 = 'L4',
}

// 课程类型
export interface Course {
  id: string;
  title: string;
  content_url: string | null;
  sort_order: number;
  level: CourseLevel;
  description: string | null;
  created_at: string;
}

// 课程创建DTO
export interface CourseCreate {
  title: string;
  content_url?: string;
  sort_order?: number;
  level: CourseLevel;
  description?: string;
}

// 课程更新DTO
export interface CourseUpdate {
  title?: string;
  content_url?: string;
  sort_order?: number;
  level?: CourseLevel;
  description?: string;
}

// 学习进度类型
export interface UserProgress {
  id: string;
  user_id: string;
  course_id: string;
  is_completed: boolean;
  completed_at: string | null;
}

// 本地存储的阅读进度
export interface ReadingProgress {
  courseId: string;
  timestamp: number;
  scrollPosition: number;
  completedSections: string[];
}
