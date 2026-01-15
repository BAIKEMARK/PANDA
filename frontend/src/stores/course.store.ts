/**
 * 课程状态管理
 */
import { create } from 'zustand';
import type { Course, CourseLevel } from '../types/course.types';
import courseService from '../services/course.service';

interface CourseStore {
  courses: Course[];
  currentCourse: Course | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  loadCourses: (level?: CourseLevel) => Promise<void>;
  loadCourse: (courseId: number | string) => Promise<void>;
  setCurrentCourse: (course: Course | null) => void;
}

export const useCourseStore = create<CourseStore>((set) => ({
  courses: [],
  currentCourse: null,
  isLoading: false,
  error: null,

  loadCourses: async (level?: CourseLevel) => {
    set({ isLoading: true, error: null });
    try {
      const courses = await courseService.getCourses(level);
      set({ courses, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '加载课程失败';
      set({
        error: errorMessage,
        isLoading: false,
      });
      throw error;
    }
  },

  loadCourse: async (courseId: number | string) => {
    set({ isLoading: true, error: null });
    try {
      const course = await courseService.getCourse(String(courseId));
      set({ currentCourse: course, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '加载课程详情失败';
      set({
        error: errorMessage,
        isLoading: false,
      });
      throw error;
    }
  },

  setCurrentCourse: (course: Course | null) => {
    set({ currentCourse: course });
  },
}));
