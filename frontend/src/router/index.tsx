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
import { PrivateRoute } from './privateRoutes';

// 路由配置
export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
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
        element: (
          <PrivateRoute>
            <ScenarioListPage />
          </PrivateRoute>
        ),
      },
      {
        path: 'chat/:sessionId',
        element: (
          <PrivateRoute>
            <ChatPage />
          </PrivateRoute>
        ),
      },
      {
        path: 'evaluation/:sessionId',
        element: (
          <PrivateRoute>
            <EvaluationReportPage />
          </PrivateRoute>
        ),
      },
      {
        path: 'profile',
        element: (
          <PrivateRoute>
            <ProfilePage />
          </PrivateRoute>
        ),
      },
    ],
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },
]);
