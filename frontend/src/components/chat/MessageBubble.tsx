/**
 * 消息气泡组件
 */
import { Avatar, Typography } from 'antd';
import { RobotOutlined } from '@ant-design/icons';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';
import type { ChatMessage } from '@/types/chat.types';
import { MessageRole } from '@/types/chat.types';

const { Text } = Typography;

interface MessageBubbleProps {
  message: ChatMessage;
  senderName?: string;
}

export const MessageBubble = ({ message, senderName }: MessageBubbleProps) => {
  // 使用枚举进行比较，而不是字符串
  const isUser = message.role === MessageRole.USER;
  const isSystem = message.role === MessageRole.SYSTEM;

  // Helper to parse date as UTC if no timezone specified
  const parseDate = (dateStr: string) => {
    if (!dateStr) return new Date();
    // If string doesn't contain Z or timezone offset, assume UTC and append Z
    // This fixes the "8 hours ago" bug caused by backend sending UTC without Z
    const isUTC = !dateStr.includes('Z') && !/\+\d{2}:\d{2}$/.test(dateStr);
    return new Date(isUTC ? `${dateStr}Z` : dateStr);
  };

  // 系统消息
  if (isSystem) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        style={{ textAlign: 'center', margin: '16px 0' }}
      >
        <Text
          type="secondary"
          style={{
            background: 'linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%)',
            padding: '8px 16px',
            borderRadius: '16px',
            fontSize: '13px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
          }}
        >
          {message.content}
        </Text>
      </motion.div>
    );
  }

  // 用户消息
  if (isUser) {
    return (
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
        style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '16px' }}
      >
        <div style={{ maxWidth: '70%' }}>
          <motion.div
            whileHover={{ scale: 1.02 }}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: '#fff',
              padding: '12px 16px',
              borderRadius: '12px 12px 0 12px',
              wordBreak: 'break-word',
              whiteSpace: 'pre-wrap',
              boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
            }}
          >
            {message.content}
          </motion.div>
          {message.created_at && (
            <div style={{ textAlign: 'right', marginTop: '4px' }}>
              <Text type="secondary" style={{ fontSize: '12px' }}>
                {formatDistanceToNow(parseDate(message.created_at), {
                  addSuffix: true,
                  locale: zhCN,
                })}
              </Text>
            </div>
          )}
        </div>
      </motion.div>
    );
  }

  // AI消息（支持Markdown渲染）
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: '16px' }}
    >
      <div style={{ maxWidth: '70%' }}>
        {/* Avatar */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.1, type: 'spring', stiffness: 200 }}
          style={{ display: 'flex', alignItems: 'center', marginBottom: '8px', gap: '8px' }}
        >
          <Avatar
            size="small"
            icon={<RobotOutlined />}
            style={{ backgroundColor: '#722ed1' }}
          />
          <Text style={{ fontSize: '13px', color: '#595959' }}>{senderName || 'PANDA助手'}</Text>
        </motion.div>

        {/* Message with Markdown */}
        <motion.div
          whileHover={{ scale: 1.01 }}
          style={{
            background: '#fff',
            border: '1px solid #e8e8e8',
            padding: '12px 16px',
            borderRadius: '12px 12px 12px 0',
            wordBreak: 'break-word',
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
          }}
        >
          <div
            className="markdown-content"
            style={{
              color: '#262626',
              lineHeight: '1.6'
            }}
          >
            <ReactMarkdown
              components={{
                p: ({ children }: { children?: React.ReactNode }) => <p style={{ margin: '0 0 8px 0' }}>{children}</p>,
                ul: ({ children }: { children?: React.ReactNode }) => <ul style={{ margin: '0 0 8px 0', paddingLeft: '20px' }}>{children}</ul>,
                ol: ({ children }: { children?: React.ReactNode }) => <ol style={{ margin: '0 0 8px 0', paddingLeft: '20px' }}>{children}</ol>,
                li: ({ children }: { children?: React.ReactNode }) => <li style={{ marginBottom: '4px' }}>{children}</li>,
                strong: ({ children }: { children?: React.ReactNode }) => <strong style={{ fontWeight: 600, color: '#262626' }}>{children}</strong>,
                code: ({ inline, children }: { inline?: boolean; children?: React.ReactNode }) =>
                  inline ? (
                    <code style={{
                      background: '#f5f5f5',
                      padding: '2px 6px',
                      borderRadius: '4px',
                      fontSize: '14px',
                      color: '#eb2f96'
                    }}>{children}</code>
                  ) : (
                    <code style={{
                      display: 'block',
                      background: '#f5f5f5',
                      padding: '12px',
                      borderRadius: '6px',
                      fontSize: '14px',
                      overflow: 'auto',
                      margin: '8px 0'
                    }}>{children}</code>
                  ),
                h1: ({ children }: { children?: React.ReactNode }) => <h1 style={{ fontSize: '18px', fontWeight: 600, margin: '12px 0 8px 0' }}>{children}</h1>,
                h2: ({ children }: { children?: React.ReactNode }) => <h2 style={{ fontSize: '16px', fontWeight: 600, margin: '12px 0 8px 0' }}>{children}</h2>,
                h3: ({ children }: { children?: React.ReactNode }) => <h3 style={{ fontSize: '15px', fontWeight: 600, margin: '12px 0 8px 0' }}>{children}</h3>,
                blockquote: ({ children }: { children?: React.ReactNode }) => (
                  <blockquote style={{
                    borderLeft: '3px solid #d9d9d9',
                    paddingLeft: '12px',
                    margin: '8px 0',
                    color: '#595959',
                    fontStyle: 'italic'
                  }}>{children}</blockquote>
                )
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </motion.div>

        {message.created_at && (
          <div style={{ marginTop: '4px' }}>
            <Text type="secondary" style={{ fontSize: '12px' }}>
              {formatDistanceToNow(parseDate(message.created_at), {
                addSuffix: true,
                locale: zhCN,
              })}
            </Text>
          </div>
        )}
      </div>
    </motion.div>
  );
};
