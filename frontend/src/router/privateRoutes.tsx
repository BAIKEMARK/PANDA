/**
 * 路由守卫组件
 * PrivateRoute: 未登录用户自动跳转到登录页
 * PublicRoute: 已登录用户自动跳转到首页
 */
import { useEffect, useRef } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { message } from 'antd';
import { useAuthStore } from '../stores/auth.store';
import type { ReactNode } from 'react';

interface RouteProps {
  children: ReactNode;
}

/**
 * 私有路由守卫
 * 未登录时重定向到登录页，并记录原始路径
 */
export const PrivateRoute = ({ children }: RouteProps) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const location = useLocation();
  const hasShownMessage = useRef(false);

  useEffect(() => {
    if (!isAuthenticated && !hasShownMessage.current) {
      message.warning('请登录后重试');
      hasShownMessage.current = true;
    }
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    // 未登录，重定向到登录页，保存原始路径用于登录后跳转
    return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  }

  return <>{children}</>;
};

/**
 * 公开路由守卫
 * 已登录时重定向到首页或之前访问的页面
 */
export const PublicRoute = ({ children }: RouteProps) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const token = useAuthStore((state) => state.token);
  const location = useLocation();

  // 只有在真正有有效 token 且已认证时才重定向
  // 避免因为 localStorage 中的过期数据导致登录页一闪而过
  if (isAuthenticated && token) {
    // 已登录，重定向到之前的页面或首页
    const from = (location.state as { from?: string })?.from || '/courses';
    return <Navigate to={from} replace />;
  }

  return <>{children}</>;
};
