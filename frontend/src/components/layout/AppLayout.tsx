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
      {/* 侧边栏 - Fixed 定位 */}
      <Sidebar />

      {/* 主内容区域 - 左边距256px避开侧边栏 */}
      <Layout style={{ marginLeft: '256px' }}>
        {/* 头部 */}
        <Header />

        {/* 主内容区 */}
        <Content
          style={{
            margin: '24px',
            padding: '24px',
            background: '#f0f2f5',
            minHeight: 'calc(100vh - 64px - 48px)',
            borderRadius: '8px'
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};
