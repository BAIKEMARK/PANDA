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
import { motion } from 'framer-motion';
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
        item.children = menu.children?.map((child) => ({
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
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        background: 'linear-gradient(180deg, #1a365d 0%, #2d3748 100%)',
        boxShadow: '2px 0 8px rgba(0,0,0,0.15)'
      }}
    >
      {/* Logo */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        style={{
          padding: '20px 16px',
          textAlign: 'center',
          borderBottom: '1px solid rgba(255,255,255,0.08)',
          flexShrink: 0,
        }}
      >
        <motion.div
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 3, repeat: Infinity, repeatDelay: 2 }}
          style={{
            fontSize: '24px',
            fontWeight: 700,
            color: '#fff',
            letterSpacing: '3px',
            textShadow: '0 2px 4px rgba(0,0,0,0.3)'
          }}
        >
          PANDA
        </motion.div>
        <Text style={{ color: 'rgba(255,255,255,0.7)', fontSize: '11px' }}>
          围产期抑郁管理培训系统
        </Text>
      </motion.div>

      {/* Navigation */}
      {isLoading ? (
        <div style={{ padding: '20px', textAlign: 'center', flex: 1 }}>
          <Spin size="small" />
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.4 }}
          style={{ paddingBottom: '20px', flex: 1, overflowY: 'auto' }}
        >
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
        </motion.div>
      )}

      {/* User Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        style={{
          padding: '12px 16px',
          borderTop: '1px solid rgba(255,255,255,0.08)',
          background: 'rgba(0,0,0,0.2)',
          flexShrink: 0,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <motion.div whileHover={{ scale: 1.1 }} transition={{ type: 'spring', stiffness: 300 }}>
            <Avatar
              size={36}
              style={{ backgroundColor: '#667eea', flexShrink: 0 }}
              icon={<UserOutlined />}
            >
              {user?.name?.[0] || 'U'}
            </Avatar>
          </motion.div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ color: '#fff', fontSize: '13px', fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {user?.name || '未登录'}
            </div>
            <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '11px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {user?.role || '普通用户'}
            </div>
          </div>
        </div>
      </motion.div>
    </Sider>
  );
};
