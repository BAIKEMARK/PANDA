/**
 * 侧边栏导航组件
 */
import { NavLink, useLocation } from 'react-router-dom';
import { Layout, Menu, Avatar, Typography } from 'antd';
import {
  BookOutlined,
  MessageOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { useAuthStore } from '@/stores/auth.store';

const { Sider } = Layout;
const { Text } = Typography;

export const Sidebar = () => {
  const user = useAuthStore((state) => state.user);
  const location = useLocation();

  const navItems = [
    {
      key: '/courses',
      icon: <BookOutlined />,
      label: <NavLink to="/courses">课程学习</NavLink>,
    },
    {
      key: '/scenarios',
      icon: <MessageOutlined />,
      label: <NavLink to="/scenarios">情景模拟</NavLink>,
    },
    {
      key: '/profile',
      icon: <UserOutlined />,
      label: <NavLink to="/profile">个人中心</NavLink>,
    },
  ];

  return (
    <Sider
      width={240}
      style={{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        background: 'linear-gradient(180deg, #1a365d 0%, #2d3748 100%)',
      }}
    >
      {/* Logo */}
      <div
        style={{
          padding: '20px 16px',
          textAlign: 'center',
          borderBottom: '1px solid rgba(255,255,255,0.08)',
        }}
      >
        <div
          style={{
            fontSize: '22px',
            fontWeight: 700,
            color: '#fff',
            letterSpacing: '2px',
          }}
        >
          🐼 PANDA
        </div>
        <Text style={{ color: 'rgba(255,255,255,0.6)', fontSize: '11px' }}>
          围产期抑郁管理培训系统
        </Text>
      </div>

      {/* Navigation */}
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={[location.pathname]}
        items={navItems}
        style={{ 
          background: 'transparent', 
          borderRight: 0,
          marginTop: '8px',
        }}
      />

      {/* User Info */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          padding: '12px 16px',
          borderTop: '1px solid rgba(255,255,255,0.08)',
          background: 'rgba(0,0,0,0.15)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Avatar
            size={36}
            style={{ backgroundColor: '#667eea', flexShrink: 0 }}
            icon={<UserOutlined />}
          >
            {user?.name?.[0] || 'U'}
          </Avatar>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ color: '#fff', fontSize: '13px', fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {user?.name || '未登录'}
            </div>
            <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {user?.role === 'student' ? '学员' : user?.role === 'instructor' ? '讲师' : '管理员'}
            </div>
          </div>
        </div>
      </div>
    </Sider>
  );
};
