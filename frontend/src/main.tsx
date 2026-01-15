/**
 * 应用入口文件
 */
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { useAuthStore } from './stores/auth.store';

// 初始化认证状态（从localStorage恢复）
useAuthStore.getState().loadUser();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
