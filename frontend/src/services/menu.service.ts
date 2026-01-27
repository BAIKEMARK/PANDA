/**
 * 菜单服务
 * 处理菜单相关的 API 调用
 */
import apiClient from './api';
import type { MenuItem, MenuTreeNode } from '../types/menu.types';

/**
 * 菜单服务类
 */
class MenuService {
  /**
   * 根据用户角色获取可访问的菜单树
   * @param role 用户角色 (student/instructor/admin)
   */
  async getUserMenus(role: string): Promise<MenuItem[]> {
    const { data } = await apiClient.get<MenuItem[]>('/menus/user', {
      params: { role }
    });
    return data;
  }

  /**
   * 获取完整菜单树（管理员使用）
   */
  async getMenuTree(): Promise<MenuTreeNode[]> {
    const { data } = await apiClient.get<MenuTreeNode[]>('/menus/tree');
    return data;
  }

  /**
   * 获取所有菜单列表
   */
  async getAllMenus(): Promise<MenuItem[]> {
    const { data } = await apiClient.get<MenuItem[]>('/menus/');
    return data;
  }

  /**
   * 获取菜单详情
   */
  async getMenuById(id: string): Promise<MenuItem> {
    const { data } = await apiClient.get<MenuItem>(`/menus/${id}`);
    return data;
  }
}

// 导出单例
export default new MenuService();