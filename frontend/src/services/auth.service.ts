/**
 * 用户认证服务
 * 处理用户注册、登录、Token管理等
 */
import api from './api';
import type { UserCreate, UserLogin, TokenResponse, User } from '../types/auth.types';

class AuthService {
  /**
   * 用户注册
   */
  async register(data: UserCreate): Promise<User> {
    const response = await api.post<User>('/users/', data);
    return response.data;
  }

  /**
   * 用户登录 (后端需要补充此接口)
   */
  async login(data: UserLogin): Promise<TokenResponse> {
    // TODO: 后端需要实现 POST /api/auth/login 接口
    const response = await api.post<TokenResponse>('/auth/login', data);
    return response.data;
  }

  /**
   * 获取当前用户信息
   */
  async getCurrentUser(): Promise<User> {
    // TODO: 后端需要实现 GET /api/auth/me 接口
    const response = await api.get<User>('/auth/me');
    return response.data;
  }

  /**
   * 保存Token到本地存储
   */
  saveToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  /**
   * 保存用户信息
   */
  saveUser(user: User): void {
    localStorage.setItem('user', JSON.stringify(user));
  }

  /**
   * 获取本地Token
   */
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * 获取本地用户信息
   */
  getUser(): User | null {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  /**
   * 清除认证信息
   */
  clearAuth(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  }

  /**
   * 检查是否已认证
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export default new AuthService();
