/**
 * 头部导航栏组件
 */
import { useNavigate } from 'react-router-dom';
import { Layout, Typography, Button, Space } from 'antd';
import { LogoutOutlined } from '@ant-design/icons';
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
        background: '#fff',
        padding: '0 24px',
        height: '56px',
        lineHeight: '56px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderBottom: '1px solid #e8e8e8',
        boxShadow: '0 1px 4px rgba(0,0,0,0.05)',
      }}
    >
      <div />
      
      <Text strong style={{ fontSize: '15px', color: '#1a365d' }}>
        围产期抑郁管理智能培训系统
      </Text>

      <Space>
        <Button
          type="text"
          danger
          icon={<LogoutOutlined />}
          onClick={handleLogout}
        >
          退出
        </Button>
      </Space>
    </AntHeader>
  );
};
