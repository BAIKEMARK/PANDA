/**
 * 头部导航栏组件
 */
import { useNavigate } from 'react-router-dom';
import { Layout, Typography, Button, Badge, Space } from 'antd';
import {
  BellOutlined,
  LogoutOutlined,
} from '@ant-design/icons';
import { useAuthStore } from '@/stores/auth.store';

const { Header: AntHeader } = Layout;
const { Title } = Typography;

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
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderBottom: '1px solid #f0f0f0',
      }}
    >
      {/* 左侧 - 空白占位 */}
      <div style={{ width: '200px' }}></div>

      {/* 中间 - 标题 */}
      <Title
        level={4}
        style={{
          margin: 0,
          color: '#262626',
          fontWeight: 600,
        }}
      >
        围产期抑郁管理智能培训系统
      </Title>

      {/* 右侧 - 操作按钮 */}
      <Space size="middle">
        <Badge count={0} showZero={false}>
          <Button
            type="text"
            icon={<BellOutlined />}
            size="large"
            style={{ color: '#595959' }}
          />
        </Badge>

        <Button
          type="primary"
          danger
          icon={<LogoutOutlined />}
          onClick={handleLogout}
          size="large"
        >
          退出登录
        </Button>
      </Space>
    </AntHeader>
  );
};
