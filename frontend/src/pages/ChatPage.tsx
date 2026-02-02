/**
 * 聊天页面
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { Typography, Button, Space, Tag, Modal, message, Alert } from 'antd';
import { StopOutlined, CommentOutlined, PlayCircleOutlined, ArrowLeftOutlined } from '@ant-design/icons';
import { useChatStore } from '@/stores/chat.store';
import { ChatWindow } from '@/components/chat/ChatWindow';
import { ChatInput } from '@/components/chat/ChatInput';

const { Title } = Typography;

export const ChatPage = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { currentSession, messages, isLoading, isTyping, loadMessages, sendMessage, endSession, setTyping } = useChatStore();
  const [isEnding, setIsEnding] = useState(false);

  // 判断是否从历史记录进入（默认只读模式）
  // 如果从scenario页面新建会话进入，则不是只读
  const [isReadOnly, setIsReadOnly] = useState(() => {
    // 检查来源：如果是从 /progress 或 /dashboard 进入，则为只读模式
    const fromHistory = location.state?.fromHistory === true;
    return fromHistory;
  });

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
    if (!sessionId || isReadOnly) return;

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

          // 显示加载提示
          const hide = message.loading({
            content: '正在生成评估报告，请稍候（可能需要1-6分钟）...',
            duration: 0, // 不自动关闭
          });

          await endSession(sessionId); // sessionId是字符串UUID，不需要转数字

          hide(); // 关闭加载提示
          message.success('评估报告生成成功！');

          // 延迟跳转，让用户看到成功提示
          setTimeout(() => {
            navigate(`/evaluation/${sessionId}`);
          }, 500);
        } catch (err) {
          console.error('结束会话失败:', err);
          message.error('评估报告生成失败，请稍后重试');
        } finally {
          setIsEnding(false);
        }
      },
    });
  };

  const handleContinueChat = () => {
    setIsReadOnly(false);
    message.success('已进入对话模式，您可以继续对话了');
  };

  return (
    <div style={{
      height: 'calc(100vh - 64px - 40px)',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
      margin: '-20px',
      background: '#fff',
      borderRadius: '8px',
    }}>
      {/* Chat Header */}
      <div
        style={{
          background: '#fff',
          borderBottom: '1px solid #f0f0f0',
          padding: '12px 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexShrink: 0,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Button
            type="text"
            icon={<ArrowLeftOutlined />}
            onClick={() => navigate('/scenarios')}
            style={{ color: '#666' }}
          >
            返回
          </Button>
          <Title level={5} style={{ margin: 0 }}>
            <CommentOutlined style={{ marginRight: '8px' }} />
            {currentSession?.scenario_title || '对话练习'}
          </Title>
        </div>

        <Space>
          {currentSession && (
            <Tag color="blue">{messages.length} 条消息</Tag>
          )}
          {isReadOnly ? (
            <Tag color="orange">只读模式</Tag>
          ) : null}
          {isReadOnly ? (
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={handleContinueChat}
            >
              继续对话
            </Button>
          ) : (
            <Button
              type="primary"
              danger
              icon={<StopOutlined />}
              onClick={handleEndSession}
              disabled={isEnding || isLoading}
            >
              结束对话
            </Button>
          )}
        </Space>
      </div>

      {/* Chat Window - 可滚动区域 */}
      <div style={{ flex: 1, minHeight: 0, overflow: 'hidden' }}>
        <ChatWindow
          messages={messages}
          isTyping={isTyping}
          patientBackground={currentSession?.patient_background}
        />
      </div>

      {/* Chat Input or Read-only Notice */}
      <div style={{ flexShrink: 0 }}>
        {isReadOnly ? (
          <Alert
            message="您正在查看历史对话记录"
            description="点击右上角「继续对话」按钮可继续与患者交流"
            type="info"
            showIcon
            style={{ margin: '16px 24px' }}
            action={
              <Button type="primary" size="small" onClick={handleContinueChat}>
                继续对话
              </Button>
            }
          />
        ) : (
          <ChatInput onSend={handleSendMessage} disabled={isLoading} isLoading={isTyping} />
        )}
      </div>
    </div>
  );
};
