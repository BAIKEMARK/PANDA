/**
 * 加载遮罩组件
 * 提供统一的加载状态展示
 */
import { Spin } from 'antd';
import { motion, AnimatePresence } from 'framer-motion';

interface LoadingOverlayProps {
  loading: boolean;
  tip?: string;
  fullScreen?: boolean;
}

export function LoadingOverlay({ loading, tip = '加载中...', fullScreen = false }: LoadingOverlayProps) {
  return (
    <AnimatePresence>
      {loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          style={{
            position: fullScreen ? 'fixed' : 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'rgba(255, 255, 255, 0.8)',
            backdropFilter: 'blur(4px)',
            zIndex: 1000,
          }}
        >
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.1, duration: 0.3 }}
          >
            <Spin size="large" tip={tip} />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
