/**
 * 空状态组件
 * 统一的空数据展示
 */
import { Empty, Button } from 'antd';
import { motion } from 'framer-motion';
import type { ReactNode } from 'react';

interface EmptyStateProps {
  description?: string;
  image?: ReactNode;
  action?: {
    text: string;
    onClick: () => void;
    icon?: ReactNode;
  };
}

export function EmptyState({ description = '暂无数据', image, action }: EmptyStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '300px',
        padding: '40px',
      }}
    >
      <Empty
        image={image || Empty.PRESENTED_IMAGE_SIMPLE}
        description={
          <span style={{ color: '#8c8c8c', fontSize: '14px' }}>{description}</span>
        }
      >
        {action && (
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button
              type="primary"
              icon={action.icon}
              onClick={action.onClick}
              style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
              }}
            >
              {action.text}
            </Button>
          </motion.div>
        )}
      </Empty>
    </motion.div>
  );
}
