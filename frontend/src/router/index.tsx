/**
 * 路由配置
 * 定义应用的所有路由和私有路由守卫
 */
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';

// 页面组件
import { LoginPage } from '../pages/LoginPage';
import { RegisterPage } from '../pages/RegisterPage';
import { CourseListPage } from '../pages/CourseListPage';
import { CourseDetailPage } from '../pages/CourseDetailPage';
import { ScenarioListPage } from '../pages/ScenarioListPage';
import { ChatPage } from '../pages/ChatPage';
import { EvaluationReportPage } from '../pages/EvaluationReportPage';
import { ProfilePage } from '../pages/ProfilePage';
import { NotFoundPage } from '../pages/NotFoundPage';
import { PrivateRoute, PublicRoute } from './privateRoutes';

// 路由配置
export const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <PrivateRoute>
        <AppLayout />
      </PrivateRoute>
    ),
    errorElement: <NotFoundPage />,
    children: [
      {
        index: true,
        element: <Navigate to="/courses" replace />,
      },
      {
        path: 'courses',
        element: <CourseListPage />,
      },
      {
        path: 'courses/:courseId',
        element: <CourseDetailPage />,
      },
      {
        path: 'scenarios',
        element: <ScenarioListPage />,
      },
      {
        path: 'chat/:sessionId',
        element: <ChatPage />,
      },
      {
        path: 'evaluation/:sessionId',
        element: <EvaluationReportPage />,
      },
      {
        path: 'profile',
        element: <ProfilePage />,
      },
    ],
  },
  {
    path: '/login',
    element: (
      <PublicRoute>
        <LoginPage />
      </PublicRoute>
    ),
  },
  {
    path: '/register',
    element: (
      <PublicRoute>
        <RegisterPage />
      </PublicRoute>
    ),
  },
]);
