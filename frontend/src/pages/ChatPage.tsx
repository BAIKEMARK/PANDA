/**
 * 聊天页面
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { Typography, Button, Space, Tag, Modal, message, Alert } from 'antd';
import {
  StopOutlined,
  CommentOutlined,
  PlayCircleOutlined,
  ArrowLeftOutlined,
  WarningOutlined,
  ExclamationCircleOutlined,
  AlertOutlined as AlertIcon
} from '@ant-design/icons';
import { useChatStore } from '@/stores/chat.store';
import { ChatWindow } from '@/components/chat/ChatWindow';
import { ChatInput } from '@/components/chat/ChatInput';
import chatService from '@/services/chat.service';
import type { ChatMessage } from '@/types/chat.types';

const { Title } = Typography;

export const ChatPage = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { currentSession, messages, isLoading, isTyping, loadMessages, sendMessage, endSession, setTyping } = useChatStore();
  const [isEnding, setIsEnding] = useState(false);

  // 判断是否从历史记录进入（默认只读模式）
  const [isReadOnly, setIsReadOnly] = useState(() => {
    const fromHistory = location.state?.fromHistory === true;
    return fromHistory;
  });

  useEffect(() => {
    if (!sessionId) return;

    const fetchMessages = async () => {
      try {
        await loadMessages(sessionId);
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
      const result = await sendMessage(sessionId, content);

      // 检查是否患者想离开（通过meta_data）
      const lastMessage = result as ChatMessage;
      if (lastMessage?.meta_data?.patient_leaving) {
        // 患者表示要离开，延迟弹窗让用户选择
        setTimeout(() => {
          Modal.confirm({
            title: '患者表示要离开',
            icon: <ExclamationCircleOutlined />,
            content: '患者表示要结束对话并离开。您可以选择进行评估，或继续尝试挽留患者。',
            okText: '进行评估',
            cancelText: '继续对话',
            onOk: () => {
              navigate(`/evaluation/${sessionId}`);
            },
            onCancel: () => {
              message.info('您可以继续发送消息尝试与患者交流');
            },
          });
        }, 1500); // 延迟1.5秒，让用户看到告别消息
      }
    } catch (err) {
      console.error('发送消息失败:', err);
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

          const hide = message.loading({
            content: '正在生成评估报告，请稍候（可能需要1-6分钟）...',
            duration: 0,
          });

          await endSession(sessionId);

          hide();
          message.success('评估报告生成成功！');

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

  const handleAlert = async () => {
    if (!sessionId) return;

    Modal.confirm({
      title: '确认报警',
      icon: <WarningOutlined style={{ color: '#ff4d4f' }} />,
      content: '确认患者存在自杀倾向需要报警吗？报警后将自动结束对话并生成评估报告。',
      okText: '确认报警',
      okButtonProps: { danger: true },
      cancelText: '取消',
      onOk: async () => {
        try {
          const hide = message.loading({
            content: '正在处理报警并生成评估报告...',
            duration: 0,
          });

          await chatService.alertSuicideRisk(sessionId);

          hide();
          message.success('已记录报警，正在生成评估报告...');

          setTimeout(() => {
            navigate(`/evaluation/${sessionId}`);
          }, 500);
        } catch (err) {
          console.error('报警失败:', err);
          message.error('报警失败，请稍后重试');
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
            <>
              {/* 报警按钮 - 一直显示，让用户自己判断 */}
              <Button
                danger
                icon={<AlertIcon />}
                onClick={handleAlert}
                style={{ marginRight: '8px' }}
              >
                报警
              </Button>
              <Button
                type="primary"
                icon={<StopOutlined />}
                onClick={handleEndSession}
                disabled={isEnding || isLoading}
              >
                结束对话
              </Button>
            </>
          )}
        </Space>
      </div>

      {/* 报警提示横幅 */}
      {!isReadOnly && (
        <Alert
          message="提示"
          description="如观察到患者存在自杀倾向，请及时点击「报警」按钮记录处理。"
          type="info"
          showIcon
          closable
          style={{ margin: '12px 24px', borderRadius: '4px' }}
        />
      )}

      {/* Chat Window */}
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