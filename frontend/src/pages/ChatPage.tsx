/**
 * 聊天页面
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Layout, Typography, Button, Space, Tag, Modal } from 'antd';
import { StopOutlined, CommentOutlined } from '@ant-design/icons';
import { useChatStore } from '@/stores/chat.store';
import { ChatWindow } from '@/components/chat/ChatWindow';
import { ChatInput } from '@/components/chat/ChatInput';

const { Title, Text } = Typography;

export const ChatPage = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const { currentSession, messages, isLoading, isTyping, loadMessages, sendMessage, endSession, setTyping } = useChatStore();
  const [isEnding, setIsEnding] = useState(false);

  useEffect(() => {
    if (!sessionId) return;

    const fetchMessages = async () => {
      try {
        await loadMessages(sessionId); // sessionId是字符串UUID，不需要转数字
      } catch (err) {
        console.error('加载消息失败:', err);
      }
    };

    fetchMessages();
  }, [sessionId, loadMessages]);

  const handleSendMessage = async (content: string) => {
    if (!sessionId) return;

    try {
      setTyping(true);
      await sendMessage(sessionId, content); // sessionId是字符串UUID，不需要转数字
    } catch (err) {
      // Handle error
    } finally {
      setTyping(false);
    }
  };

  const handleEndSession = async () => {
    if (!sessionId) return;

    Modal.confirm({
      title: '确认结束对话',
      content: '确定要结束本次对话练习吗？结束后将无法继续发送消息。',
      okText: '确定',
      cancelText: '取消',
      onOk: async () => {
        try {
          setIsEnding(true);
          await endSession(sessionId); // sessionId是字符串UUID，不需要转数字
          navigate(`/evaluation/${sessionId}`);
        } catch (err) {
          console.error('结束会话失败:', err);
        } finally {
          setIsEnding(false);
        }
      },
    });
  };

  return (
    <div style={{ height: 'calc(100vh - 64px - 48px)', display: 'flex', flexDirection: 'column' }}>
      {/* Chat Header */}
      <div
        style={{
          background: '#fff',
          borderBottom: '1px solid #f0f0f0',
          padding: '16px 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <div style={{ flex: 1 }}>
          <Title level={4} style={{ margin: 0, marginBottom: '4px' }}>
            <CommentOutlined style={{ marginRight: '8px' }} />
            {currentSession?.scenario_title || '对话练习'}
          </Title>
          <Text type="secondary" style={{ fontSize: '13px' }}>
            与AI模拟患者进行对话练习
          </Text>
        </div>

        <Space size="middle">
          {currentSession && (
            <Space>
              <Tag color="blue">开始: {new Date(currentSession.start_time).toLocaleString('zh-CN')}</Tag>
              <Tag>消息: {messages.length}</Tag>
            </Space>
          )}

          <Button
            type="primary"
            danger
            icon={<StopOutlined />}
            onClick={handleEndSession}
            disabled={isEnding || isLoading}
            size="large"
          >
            结束对话
          </Button>
        </Space>
      </div>

      {/* Chat Window */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <ChatWindow messages={messages} isTyping={isTyping} />
      </div>

      {/* Chat Input */}
      <ChatInput onSend={handleSendMessage} disabled={isLoading} isLoading={isTyping} />
    </div>
  );
};
