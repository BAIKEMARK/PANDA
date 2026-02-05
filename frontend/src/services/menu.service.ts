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
   */
  async getUserMenus(): Promise<MenuItem[]> {
    const { data } = await apiClient.get<MenuItem[]>('/menus/user');
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

  async createMenu(payload: Partial<MenuItem> & { id: string; title: string }): Promise<MenuItem> {
    const { data } = await apiClient.post<MenuItem>('/menus/', payload);
    return data;
  }

  async updateMenu(id: string, payload: Partial<MenuItem>): Promise<MenuItem> {
    const { data } = await apiClient.put<MenuItem>(`/menus/${id}`, payload);
    return data;
  }

  async deleteMenu(id: string): Promise<void> {
    await apiClient.delete(`/menus/${id}`);
  }

  /**
   * 获取菜单详情
   */
  async getMenuById(id: string): Promise<MenuItem> {
    const { data } = await apiClient.get<MenuItem>(`/menus/${id}`);
    return data;
  }

  /**
   * 创建菜单
   */
  async createMenu(data: Partial<MenuItem>): Promise<MenuItem> {
    const { data: result } = await apiClient.post<MenuItem>('/menus/', data);
    return result;
  }

  /**
   * 更新菜单
   */
  async updateMenu(id: string, data: Partial<MenuItem>): Promise<MenuItem> {
    const { data: result } = await apiClient.put<MenuItem>(`/menus/${id}`, data);
    return result;
  }

  /**
   * 删除菜单
   */
  async deleteMenu(id: string): Promise<void> {
    await apiClient.delete(`/menus/${id}`);
  }
}

// 导出单例
export default new MenuService();