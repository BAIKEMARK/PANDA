/**
 * 网络状态指示器
 * 在页面顶部显示网络状态
 */
import { Alert } from 'antd';
import { WifiOutlined } from '@ant-design/icons';
import { motion, AnimatePresence } from 'framer-motion';
import { useNetworkStatus } from '@/hooks/useNetworkStatus';

export function NetworkStatus() {
  const { isOnline } = useNetworkStatus();

  return (
    <AnimatePresence>
      {!isOnline && (
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -50, opacity: 0 }}
          transition={{ duration: 0.3 }}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            zIndex: 9999,
          }}
        >
          <Alert
            message="网络连接已断开"
            description="您当前处于离线状态，部分功能可能不可用"
            type="warning"
            icon={<WifiOutlined />}
            banner
            closable={false}
          />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
