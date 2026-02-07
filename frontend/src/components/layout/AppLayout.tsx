/**
 * 主布局组件
 * 包含侧边栏和头部导航
 */
import { Outlet, useLocation } from 'react-router-dom';
import { Layout } from 'antd';
import { motion, AnimatePresence } from 'framer-motion';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

const { Content } = Layout;

export const AppLayout = () => {
  const location = useLocation();

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
            background: 'linear-gradient(180deg, #f5f7fa 0%, #e8ecf1 100%)',
            minHeight: 'calc(100vh - 64px)',
          }}
        >
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </Content>
      </Layout>
    </Layout>
  );
};
