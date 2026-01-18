/**
 * Axios实例配置
 * 统一的API调用基础配置,包含请求/响应拦截器
 */
import axios from 'axios';

// 创建Axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 420000, // 7分钟（评估生成需要较长时间，后端设置为6分钟，前端给1分钟缓冲）
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器 - 自动添加Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 统一错误处理
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 统一错误处理
    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 401:
          // Token过期或未授权 - 清除所有认证相关存储
          console.error('未授权,请重新登录');
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          localStorage.removeItem('auth-storage'); // 清除 Zustand persist 存储
          // 不要在这里跳转，让路由守卫处理
          if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
            window.location.href = '/login';
          }
          break;
        case 403:
          console.error('没有权限访问此资源');
          break;
        case 404:
          console.error('请求的资源不存在');
          break;
        case 500:
          console.error('服务器错误,请稍后重试');
          break;
        default:
          console.error(data?.detail || '请求失败');
      }
    } else if (error.request) {
      console.error('网络连接失败,请检查网络');
    } else {
      console.error('请求配置错误');
    }

    return Promise.reject(error);
  }
);

export default api;
