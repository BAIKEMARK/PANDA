/**
 * 用户认证相关类型定义
 * 对应后端 backend/app/schemas/user.py 和 backend/app/models/user.py
 */

// 用户角色类型（使用联合类型替代enum）
export type UserRole = 'student' | 'instructor' | 'admin';

// 用户基础类型
export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  org_id?: string;
  phone?: string;
  department?: string;
  title?: string;
  employee_id?: string;
  roles: string[];
  org_ids: string[];
  organizations: OrganizationInfo[];  // 机构信息列表
  permission_codes: string[];
  created_at: string;
}

// 机构信息
export interface OrganizationInfo {
  id: string;
  name: string;
  short_name?: string;
}

// 用户创建DTO
export interface UserCreate {
  email: string;
  name: string;
  password: string;
  role?: UserRole;
  org_id?: string;
  phone?: string;
  department?: string;
  title?: string;
  employee_id?: string;
}

// 用户更新DTO
export interface UserUpdate {
  name?: string;
  role?: UserRole;
  org_id?: string;
  phone?: string;
  department?: string;
  title?: string;
  employee_id?: string;
}

// 用户登录DTO (后端需要补充)
export interface UserLogin {
  email: string;
  password: string;
}

// JWT Token响应 (后端需要补充)
export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// 认证状态
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
