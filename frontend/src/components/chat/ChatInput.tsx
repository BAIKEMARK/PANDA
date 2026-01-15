/**
 * 聊天输入框组件
 */
import { useState, useRef, useEffect } from 'react';
import { Input, Button } from 'antd';
import { SendOutlined } from '@ant-design/icons';

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
    if (textAreaRef.current) {
      textAreaRef.current.style.height = 'auto';
      textAreaRef.current.style.height = `${Math.min(textAreaRef.current.scrollHeight, 200)}px`;
    }
  }, [content]);

  const handleSend = () => {
    const trimmed = content.trim();
    if (!trimmed || disabled || isLoading) return;

    onSend(trimmed);
    setContent('');

    if (textAreaRef.current) {
      textAreaRef.current.style.height = 'auto';
    }
  };

  return (
    <div style={{
      borderTop: '1px solid #f0f0f0',
      background: '#fff',
      padding: '16px 24px'
    }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-end' }}>
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
            style={{ flex: 1 }}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleSend}
            disabled={disabled || isLoading || !content.trim()}
            loading={isLoading}
            style={{ height: 'auto', minHeight: '38px' }}
          >
            发送
          </Button>
        </div>
        <div style={{ textAlign: 'center', marginTop: '8px' }}>
          <small style={{ color: '#8c8c8c', fontSize: '12px' }}>
            按 Enter 发送消息，Shift+Enter 换行
          </small>
        </div>
      </div>
    </div>
  );
};
