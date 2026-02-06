/**
 * 侧边栏导航组件 - 使用动态菜单
 */
import { useEffect, useMemo } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { Layout, Menu, Avatar, Typography, Spin } from 'antd';
import {
  BookOutlined,
  ExperimentOutlined,
  MessageOutlined,
  LineChartOutlined,
  SettingOutlined,
  UserOutlined,
  TeamOutlined,
  MenuOutlined,
} from '@ant-design/icons';
import { useAuthStore } from '@/stores/auth.store';
import { useMenuStore } from '@/stores/menu.store';

const { Sider } = Layout;
const { Text } = Typography;

// 图标映射
const iconMap: Record<string, React.ReactNode> = {
  BookOutlined: <BookOutlined />,
  ExperimentOutlined: <ExperimentOutlined />,  // 实验图标
  SimulationOutlined: <ExperimentOutlined />,  // 数据库中使用 SimulationOutlined，映射到 ExperimentOutlined
  MessageOutlined: <MessageOutlined />,
  LineChartOutlined: <LineChartOutlined />,
  SettingOutlined: <SettingOutlined />,
  UserOutlined: <UserOutlined />,
  TeamOutlined: <TeamOutlined />,
  MenuOutlined: <MenuOutlined />,
};

export const Sidebar = () => {
  const user = useAuthStore((state) => state.user);
  const { menus, isLoading, fetchUserMenus } = useMenuStore();
  const location = useLocation();

  // 加载用户菜单
  useEffect(() => {
    if (user?.id) {
      fetchUserMenus();
    }
  }, [user?.id, fetchUserMenus]);

  // 将菜单数据转换为 Ant Design Menu 格式
  const menuItems = useMemo(() => {
    if (!menus || menus.length === 0) return undefined;

    return menus.map((menu) => {
      const hasChildren = !!(menu.children && menu.children.length > 0);
      const key = menu.path || menu.id;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const item: any = {
        key,
        icon: iconMap[menu.icon] || <MenuOutlined />,
        label: hasChildren ? menu.title : (
          <NavLink to={menu.path} style={{ color: 'inherit' }}>
            {menu.title}
          </NavLink>
        ),
      };

      // 处理子菜单
      if (hasChildren) {
        item.children = menu.children.map((child) => ({
          key: child.path || child.id,
          icon: iconMap[child.icon] || <MenuOutlined />,
          label: (
            <NavLink to={child.path} style={{ color: 'inherit' }}>
              {child.title}
            </NavLink>
          ),
        }));
      }

      return item;
    });
  }, [menus]);

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
          PANDA
        </div>
        <Text style={{ color: 'rgba(255,255,255,0.6)', fontSize: '11px' }}>
          围产期抑郁管理培训系统
        </Text>
      </div>

      {/* Navigation */}
      {isLoading ? (
        <div style={{ padding: '20px', textAlign: 'center' }}>
          <Spin size="small" />
        </div>
      ) : (
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          style={{
            background: 'transparent',
            borderRight: 0,
            marginTop: '8px',
          }}
        />
      )}

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
              {user?.role || '普通用户'}
            </div>
          </div>
        </div>
      </div>
    </Sider>
  );
};