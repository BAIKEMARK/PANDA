/**
 * 私有路由组件
 * 路由守卫:未登录用户自动跳转到登录页
 */
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../stores/auth.store';
import type { ReactNode } from 'react';

interface PrivateRouteProps {
  children: ReactNode;
}

export const PrivateRoute = ({ children }: PrivateRouteProps) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    // 未登录,重定向到登录页
    return <Navigate to="/login" replace />;
  }

  // 已登录,渲染子组件
  return <>{children}</>;
};
