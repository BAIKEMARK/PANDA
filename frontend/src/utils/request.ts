/**
 * 统一请求工具
 * 处理请求拦截、响应拦截、错误处理
 */
import axios, { AxiosError } from 'axios';
import type { AxiosRequestConfig, AxiosResponse } from 'axios';
import { message } from 'antd';

// 创建axios实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 添加token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // 添加请求ID用于追踪
    config.headers['X-Request-ID'] = `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    
    return config;
  },
  (error) => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data } = response;
    
    // 统一处理响应格式
    if (data && typeof data === 'object') {
      // 如果后端返回了success字段
      if ('success' in data) {
        if (!data.success) {
          message.error(data.message || '操作失败');
          return Promise.reject(new Error(data.message || '操作失败'));
        }
        return data.data !== undefined ? data.data : data;
      }
    }
    
    return data;
  },
  (error: AxiosError) => {
    // 错误处理
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          message.error((data as any)?.detail || '请求参数错误');
          break;
        case 401:
          message.error('未授权，请重新登录');
          localStorage.removeItem('token');
          window.location.href = '/login';
          break;
        case 403:
          message.error('没有权限访问');
          break;
        case 404:
          message.error('请求的资源不存在');
          break;
        case 500:
          message.error('服务器错误，请稍后重试');
          break;
        case 502:
        case 503:
        case 504:
          message.error('服务暂时不可用，请稍后重试');
          break;
        default:
          message.error((data as any)?.detail || '请求失败');
      }
    } else if (error.request) {
      message.error('网络错误，请检查网络连接');
    } else {
      message.error('请求配置错误');
    }
    
    return Promise.reject(error);
  }
);

// 导出请求方法
export default request;

// 导出类型
export type { AxiosRequestConfig, AxiosResponse };
