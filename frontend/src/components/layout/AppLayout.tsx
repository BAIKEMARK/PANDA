/**
 * 主布局组件
 * 包含侧边栏和头部导航
 */
import { Outlet } from 'react-router-dom';
import { Layout } from 'antd';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

const { Content } = Layout;

export const AppLayout = () => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      {/* 侧边栏 */}
      <Sidebar />

      {/* 主内容区域 */}
      <Layout style={{ marginLeft: '240px' }}>
        {/* 头部 - 固定在顶部 */}
        <div style={{ 
          position: 'fixed', 
          top: 0, 
          right: 0, 
          left: '240px', 
          zIndex: 100 
        }}>
          <Header />
        </div>

        {/* 主内容区 */}
        <Content
          style={{
            marginTop: '64px',
            padding: '20px',
            background: '#f5f7fa',
            minHeight: 'calc(100vh - 64px)',
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};
