/**
 * 聊天输入框组件
 */
import { useState, useRef, useEffect } from 'react';
import { Input, Button } from 'antd';
import { SendOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';

const { TextArea } = Input;

interface ChatInputProps {
  onSend: (content: string) => void;
  disabled?: boolean;
  isLoading?: boolean;
}

export const ChatInput = ({ onSend, disabled = false, isLoading = false }: ChatInputProps) => {
  const [content, setContent] = useState('');
  const textAreaRef = useRef<any>(null);

  useEffect(() => {
    if (textAreaRef.current && textAreaRef.current.resizableTextArea) {
      const textArea = textAreaRef.current.resizableTextArea.textArea;
      if (textArea) {
        textArea.style.height = 'auto';
        textArea.style.height = `${Math.min(textArea.scrollHeight, 200)}px`;
      }
    }
  }, [content]);

  const handleSend = () => {
    const trimmed = content.trim();
    if (!trimmed || disabled || isLoading) return;

    onSend(trimmed);
    setContent('');

    // 重置textarea高度
    if (textAreaRef.current && textAreaRef.current.resizableTextArea) {
      const textArea = textAreaRef.current.resizableTextArea.textArea;
      if (textArea) {
        textArea.style.height = 'auto';
      }
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      style={{
        borderTop: '1px solid #f0f0f0',
        background: 'linear-gradient(180deg, #fff 0%, #fafafa 100%)',
        padding: '16px 24px',
        boxShadow: '0 -2px 8px rgba(0,0,0,0.05)'
      }}
    >
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-end' }}>
          <motion.div
            style={{ flex: 1 }}
            whileFocus={{ scale: 1.01 }}
            transition={{ duration: 0.2 }}
          >
            <TextArea
              ref={textAreaRef}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              onPressEnter={(e) => {
                if (!e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="输入消息... (Enter 发送, Shift+Enter 换行)"
              disabled={disabled || isLoading}
              autoSize={{ minRows: 1, maxRows: 6 }}
              style={{
                borderRadius: '8px',
                border: '1px solid #d9d9d9',
                boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
              }}
            />
          </motion.div>
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={handleSend}
              disabled={disabled || isLoading || !content.trim()}
              loading={isLoading}
              style={{
                height: 'auto',
                minHeight: '38px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
              }}
            >
              发送
            </Button>
          </motion.div>
        </div>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          style={{ textAlign: 'center', marginTop: '8px' }}
        >
          <small style={{ color: '#8c8c8c', fontSize: '12px' }}>
            按 Enter 发送消息，Shift+Enter 换行
          </small>
        </motion.div>
      </div>
    </motion.div>
  );
};
