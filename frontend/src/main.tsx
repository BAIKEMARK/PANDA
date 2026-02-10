/**
 * 应用入口文件
 */
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';

// Zustand persist 会自动处理状态恢复，无需手动调用 loadUser()
createRoot(document.getElementById('root')!).render(<App />);
