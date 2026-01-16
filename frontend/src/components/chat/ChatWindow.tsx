/**
 * 聊天窗口组件
 */
import { useEffect, useRef } from 'react';
import { Empty, Typography } from 'antd';
import { MessageOutlined } from '@ant-design/icons';
import type { ChatMessage } from '@/types/chat.types';
import { MessageBubble } from './MessageBubble';
import { MessageRole } from '@/types/chat.types';

const { Text } = Typography;

interface ChatWindowProps {
  messages: ChatMessage[];
  isTyping?: boolean;
  patientBackground?: string;
}

export const ChatWindow = ({ messages, isTyping = false, patientBackground }: ChatWindowProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  // 构造患者背景消息
  const backgroundMessage: ChatMessage | null = patientBackground ? {
    id: 'patient-background',
    session_id: '',
    role: MessageRole.ASSISTANT,
    content: `【患者背景】\n${patientBackground}`,
    meta_data: null,
    created_at: new Date().toISOString(),
  } : null;

  return (
    <div style={{
      height: '100%',
      overflowY: 'auto',
      padding: '16px 24px',
      background: '#fafafa'
    }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        {messages.length === 0 && !patientBackground ? (
          <Empty
            description={
              <div>
                <MessageOutlined style={{ fontSize: '48px', color: '#d9d9d9', marginBottom: '16px' }} />
                <div>开始对话</div>
                <Text type="secondary" style={{ fontSize: '14px' }}>输入消息开始练习</Text>
              </div>
            }
            style={{ marginTop: '60px' }}
          />
        ) : (
          <div>
            {/* 患者背景作为第一条气泡 */}
            {backgroundMessage && <MessageBubble key={backgroundMessage.id} message={backgroundMessage} />}
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
          </div>
        )}

        {/* Typing Indicator */}
        {isTyping && (
          <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: '16px' }}>
            <div style={{
              background: '#fff',
              border: '1px solid #d9d9d9',
              padding: '12px 16px',
              borderRadius: '12px 12px 12px 0',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <div style={{ display: 'flex', gap: '4px' }}>
                <div style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: '#1890ff',
                  animation: 'bounce 1.4s infinite ease-in-out both',
                  animationDelay: '0s'
                }} />
                <div style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: '#1890ff',
                  animation: 'bounce 1.4s infinite ease-in-out both',
                  animationDelay: '0.16s'
                }} />
                <div style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: '#1890ff',
                  animation: 'bounce 1.4s infinite ease-in-out both',
                  animationDelay: '0.32s'
                }} />
              </div>
              <Text type="secondary" style={{ fontSize: '13px', marginLeft: '8px' }}>
                PANDA助手正在输入...
              </Text>
            </div>
          </div>
        )}

        {/* Scroll Anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};
