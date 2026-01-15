/**
 * 侧边栏导航组件
 */
import { NavLink } from 'react-router-dom';
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
      width={256}
      style={{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        background: '#001529',
      }}
    >
      {/* Logo */}
      <div
        style={{
          padding: '24px',
          textAlign: 'center',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
        }}
      >
        <div
          style={{
            fontSize: '24px',
            fontWeight: 'bold',
            color: '#fff',
            marginBottom: '4px',
          }}
        >
          PANDA
        </div>
        <Text style={{ color: 'rgba(255,255,255,0.65)', fontSize: '12px' }}>
          围产期抑郁培训系统
        </Text>
      </div>

      {/* Navigation */}
      <Menu
        theme="dark"
        mode="inline"
        defaultSelectedKeys={['/courses']}
        items={navItems}
        style={{ borderRight: 0 }}
      />

      {/* User Info */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          padding: '16px',
          borderTop: '1px solid rgba(255,255,255,0.1)',
          background: 'rgba(0,0,0,0.2)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Avatar
            size={40}
            style={{
              backgroundColor: '#1890ff',
              flexShrink: 0,
            }}
            icon={<UserOutlined />}
          >
            {user?.name?.[0] || 'U'}
          </Avatar>
          <div style={{ flex: 1, minWidth: 0, overflow: 'hidden' }}>
            <div
              style={{
                color: '#fff',
                fontSize: '14px',
                fontWeight: 500,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {user?.name || '未登录'}
            </div>
            <div
              style={{
                color: 'rgba(255,255,255,0.45)',
                fontSize: '12px',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {user?.email || ''}
            </div>
          </div>
        </div>
      </div>
    </Sider>
  );
};
