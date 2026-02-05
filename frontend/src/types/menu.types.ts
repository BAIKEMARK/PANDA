/**
 * 菜单相关类型定义
 */

export interface MenuItem {
  id: string;
  parent_id: string | null;
  title: string;
  icon: string;
  path: string;
  component?: string;
  sort_order: number;
  is_visible: boolean;
  is_enabled: boolean;
  permission_codes?: string[];
  children?: MenuItem[];
  created_at: string;
  updated_at: string;
}

export interface MenuResponse {
  id: string;
  parent_id: string | null;
  title: string;
  icon: string;
  path: string;
  component?: string;
  sort_order: number;
  is_visible: boolean;
  is_enabled: boolean;
  permission_codes?: string[];
  children?: MenuResponse[];
  created_at: string;
  updated_at: string;
}

export interface MenuTreeNode extends MenuResponse {
  children?: MenuTreeNode[];
}

export interface RoleMenuPermission {
  id: string;
  role: 'student' | 'instructor' | 'admin';
  menu_id: string;
  can_view: boolean;
  created_at: string;
}