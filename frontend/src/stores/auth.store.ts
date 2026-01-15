/**
 * 认证状态管理
 * 使用Zustand + persist中间件实现状态持久化
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, AuthState } from '../types/auth.types';
import authService from '../services/auth.service';

interface AuthStore extends AuthState {
  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, name: string, password: string) => Promise<void>;
  logout: () => void;
  loadUser: () => Promise<void>;
  updateUser: (user: User) => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      // Initial state
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      // Login action
      login: async (email: string, password: string) => {
        set({ isLoading: true });
        try {
          const response = await authService.login({ email, password });
          authService.saveToken(response.access_token);
          authService.saveUser(response.user);
          set({
            user: response.user,
            token: response.access_token,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      // Register action
      register: async (email: string, name: string, password: string) => {
        set({ isLoading: true });
        try {
          // 注册用户
          await authService.register({
            email,
            name,
            password,
          });
          set({ isLoading: false });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      // Logout action
      logout: () => {
        authService.clearAuth();
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },

      // Load user from local storage
      loadUser: async () => {
        const token = authService.getToken();
        const user = authService.getUser();

        if (token && user) {
          set({
            user,
            token,
            isAuthenticated: true,
          });
        }
      },

      // Update user info
      updateUser: (user: User) => {
        authService.saveUser(user);
        set({ user });
      },
    }),
    {
      name: 'auth-storage', // localStorage key
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
