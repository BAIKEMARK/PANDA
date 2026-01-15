/**
 * 消息气泡组件
 */
import { Avatar, Typography } from 'antd';
import { UserOutlined, RobotOutlined } from '@ant-design/icons';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import type { ChatMessage } from '@/types/chat.types';

const { Text } = Typography;

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble = ({ message }: MessageBubbleProps) => {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  // 系统消息
  if (isSystem) {
    return (
      <div style={{ textAlign: 'center', margin: '16px 0' }}>
        <Text
          type="secondary"
          style={{
            background: '#f5f5f5',
            padding: '8px 16px',
            borderRadius: '16px',
            fontSize: '13px'
          }}
        >
          {message.content}
        </Text>
      </div>
    );
  }

  // 用户消息
  if (isUser) {
    return (
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '16px' }}>
        <div style={{ maxWidth: '70%' }}>
          <div
            style={{
              background: '#1890ff',
              color: '#fff',
              padding: '12px 16px',
              borderRadius: '12px 12px 0 12px',
              wordBreak: 'break-word',
              whiteSpace: 'pre-wrap'
            }}
          >
            {message.content}
          </div>
          {message.created_at && (
            <div style={{ textAlign: 'right', marginTop: '4px' }}>
              <Text type="secondary" style={{ fontSize: '12px' }}>
                {formatDistanceToNow(new Date(message.created_at), {
                  addSuffix: true,
                  locale: zhCN,
                })}
              </Text>
            </div>
          )}
        </div>
      </div>
    );
  }

  // AI消息
  return (
    <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: '16px' }}>
      <div style={{ maxWidth: '70%' }}>
        {/* Avatar */}
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '8px', gap: '8px' }}>
          <Avatar
            size="small"
            icon={<RobotOutlined />}
            style={{ backgroundColor: '#722ed1' }}
          />
          <Text style={{ fontSize: '13px', color: '#595959' }}>PANDA助手</Text>
        </div>

        {/* Message */}
        <div
          style={{
            background: '#fff',
            border: '1px solid #d9d9d9',
            padding: '12px 16px',
            borderRadius: '12px 12px 12px 0',
            wordBreak: 'break-word',
            whiteSpace: 'pre-wrap',
            boxShadow: '0 1px 2px rgba(0,0,0,0.03)'
          }}
        >
          {message.content}
        </div>

        {message.created_at && (
          <div style={{ marginTop: '4px' }}>
            <Text type="secondary" style={{ fontSize: '12px' }}>
              {formatDistanceToNow(new Date(message.created_at), {
                addSuffix: true,
                locale: zhCN,
              })}
            </Text>
          </div>
        )}
      </div>
    </div>
  );
};
