/**
 * 聊天窗口组件 - 优化版
 */
import { useEffect, useRef } from 'react';
import { Empty, Typography } from 'antd';
import { MessageOutlined } from '@ant-design/icons';
import { motion, AnimatePresence } from 'framer-motion';
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

  // 提取患者姓名
  const patientName = patientBackground ? patientBackground.split(/[,\uff0c\s]/)[0] : '患者';

  return (
    <div style={{
      height: '100%',
      overflowY: 'auto',
      padding: '20px 24px',
      background: 'linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%)',
    }}>
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        {messages.length === 0 && !patientBackground ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Empty
              description={
                <motion.div
                  initial={{ scale: 0.9 }}
                  animate={{ scale: 1 }}
                  transition={{ duration: 0.3, delay: 0.2 }}
                >
                  <MessageOutlined style={{ 
                    fontSize: '64px', 
                    color: '#d9d9d9', 
                    marginBottom: '20px',
                  }} />
                  <div style={{ fontSize: '18px', fontWeight: 500, marginBottom: '8px' }}>
                    开始对话
                  </div>
                  <Text type="secondary" style={{ fontSize: '14px' }}>
                    输入消息开始练习
                  </Text>
                </motion.div>
              }
              style={{ marginTop: '80px' }}
            />
          </motion.div>
        ) : (
          <AnimatePresence mode="popLayout">
            {/* 患者背景 */}
            {backgroundMessage && (
              <motion.div
                key={backgroundMessage.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <MessageBubble
                  message={backgroundMessage}
                  senderName="PANDA助手"
                />
              </motion.div>
            )}
            
            {/* 消息列表 */}
            {messages.map((message, index) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, x: message.role === MessageRole.USER ? 20 : -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ 
                  duration: 0.3,
                  delay: index * 0.05,
                }}
              >
                <MessageBubble
                  message={message}
                  senderName={message.role === MessageRole.ASSISTANT ? patientName : undefined}
                />
              </motion.div>
            ))}
          </AnimatePresence>
        )}

        {/* Typing Indicator */}
        <AnimatePresence>
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: '16px' }}
            >
              <div style={{
                background: '#fff',
                border: '1px solid #e8e8e8',
                padding: '14px 18px',
                borderRadius: '16px 16px 16px 4px',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
              }}>
                <div className="typing-indicator">
                  <motion.span
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
                    style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      display: 'inline-block',
                    }}
                  />
                  <motion.span
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
                    style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      display: 'inline-block',
                      marginLeft: '4px',
                    }}
                  />
                  <motion.span
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
                    style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      display: 'inline-block',
                      marginLeft: '4px',
                    }}
                  />
                </div>
                <Text type="secondary" style={{ fontSize: '13px', fontWeight: 500 }}>
                  {patientName}正在输入...
                </Text>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Scroll Anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};
