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
import { OrganizationPage } from '../pages/admin/OrganizationPage';
import { UserManagePage } from '../pages/admin/UserManagePage';
import { TrainingClassPage } from '../pages/admin/TrainingClassPage';
import { RoleManagePage } from '../pages/admin/RoleManagePage';
import { MenuManagePage } from '../pages/admin/MenuManagePage';
import { QuestionBankPage } from '../pages/admin/QuestionBankPage';
import { CertificatePage } from '../pages/admin/CertificatePage';
import { CourseManagePage } from '../pages/admin/CourseManagePage';
import { ScenarioManagePage } from '../pages/admin/ScenarioManagePage';
import { LearningDashboardPage } from '../pages/LearningDashboardPage';
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
        element: <Navigate to="/progress" replace />,
      },
      {
        path: 'progress',
        element: <LearningDashboardPage />,
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
      {
        path: 'admin',
        children: [
          {
            path: 'organizations',
            element: <OrganizationPage />,
          },
          {
            path: 'users',
            element: <UserManagePage />,
          },
          {
            path: 'classes',
            element: <TrainingClassPage />,
          },
          {
            path: 'roles',
            element: <RoleManagePage />,
          },
          {
            path: 'menus',
            element: <MenuManagePage />,
          },
          {
            path: 'questions',
            element: <QuestionBankPage />,
          },
          {
            path: 'certificates',
            element: <CertificatePage />,
          },
          {
            path: 'courses',
            element: <CourseManagePage />,
          },
          {
            path: 'scenarios',
            element: <ScenarioManagePage />,
          },
        ],
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
