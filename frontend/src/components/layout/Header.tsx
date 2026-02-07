/**
 * 头部导航栏组件
 */
import { useNavigate } from 'react-router-dom';
import { Layout, Typography, Button, Space } from 'antd';
import { LogoutOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores/auth.store';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

export const Header = () => {
  const navigate = useNavigate();
  const { logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <AntHeader
      style={{
        background: 'linear-gradient(135deg, #fff 0%, #f8f9fa 100%)',
        padding: '0 24px',
        height: '56px',
        lineHeight: '56px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderBottom: '1px solid #e8e8e8',
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
      }}
    >
      <div />
      
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Text strong style={{ fontSize: '16px', color: '#1a365d', letterSpacing: '0.5px' }}>
          围产期抑郁管理智能培训系统
        </Text>
      </motion.div>

      <Space>
        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
          <Button
            type="text"
            danger
            icon={<LogoutOutlined />}
            onClick={handleLogout}
            style={{ borderRadius: '6px' }}
          >
            退出
          </Button>
        </motion.div>
      </Space>
    </AntHeader>
  );
};
