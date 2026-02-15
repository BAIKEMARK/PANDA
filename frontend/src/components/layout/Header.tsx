/**
 * 头部导航栏组件
 */
import { Layout, Typography } from 'antd';
import { motion } from 'framer-motion';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

export const Header = () => {
  return (
    <AntHeader
      style={{
        background: 'linear-gradient(135deg, #fff 0%, #f8f9fa 100%)',
        padding: '0 24px',
        height: '56px',
        lineHeight: '56px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderBottom: '1px solid #e8e8e8',
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
      }}
    >
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Text strong style={{ fontSize: '16px', color: '#1a365d', letterSpacing: '0.5px' }}>
          围产期抑郁管理智能培训系统
        </Text>
      </motion.div>
    </AntHeader>
  );
};
