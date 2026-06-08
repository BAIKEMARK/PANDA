/**
 * 菜单状态管理
 * 使用 Zustand 管理菜单状态
 */
import { create } from 'zustand';
import type { MenuItem } from '@/types';
import menuService from '@/services/menu.service';
import { getApiErrorMessage } from '@/utils/error';

interface MenuState {
  // 状态
  menus: MenuItem[];
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchUserMenus: () => Promise<void>;
  clearMenus: () => void;
  setError: (error: string | null) => void;
}

export const useMenuStore = create<MenuState>((set) => ({
  // 初始状态
  menus: [],
  isLoading: false,
  error: null,

  // 获取用户菜单
  fetchUserMenus: async () => {
    set({ isLoading: true, error: null });
    try {
      const menus = await menuService.getUserMenus();
      set({ menus, isLoading: false });
    } catch (error: unknown) {
      set({
        error: getApiErrorMessage(error, '获取菜单失败'),
        isLoading: false,
        menus: [],
      });
      throw error;
    }
  },

  // 清空菜单
  clearMenus: () => {
    set({ menus: [], error: null });
  },

  // 设置错误
  setError: (error: string | null) => {
    set({ error });
  },
}));
