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
import { motion, AnimatePresence } from 'framer-motion';
import { useChatStore } from '@/stores/chat.store';
import { ChatWindow } from '@/components/chat/ChatWindow';
import { ChatInput } from '@/components/chat/ChatInput';
import chatService from '@/services/chat.service';
import evaluationService from '@/services/evaluation.service';
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
    if (!sessionId) {
      // 如果没有sessionId，重定向到场景列表页面
      navigate('/scenarios', { replace: true });
      return;
    }

    const fetchMessages = async () => {
      try {
        await loadMessages(sessionId);
      } catch (err) {
        console.error('加载消息失败:', err);
        message.error('加载对话失败，请重试');
        // 如果加载失败，重定向到场景列表
        navigate('/scenarios', { replace: true });
      }
    };

    fetchMessages();
  }, [sessionId, loadMessages, navigate]);

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
            onOk: async () => {
              try {
                // 先结束会话
                await endSession(sessionId);

                // 提交异步评估报告生成任务
                await evaluationService.generateReportAsync(sessionId);

                message.success('评估报告生成任务已提交，完成后将通知您');

                // 开始后台轮询状态
                pollEvaluationStatus(sessionId);
              } catch (err) {
                console.error('提交评估任务失败:', err);
                message.error('提交评估任务失败，请稍后重试');
              }
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

          // 先结束会话
          await endSession(sessionId);

          // 提交异步评估报告生成任务
          await evaluationService.generateReportAsync(sessionId);

          message.success('评估报告生成任务已提交，完成后将通知您');

          // 将页面状态置为只读
          setIsReadOnly(true);

          // 开始后台轮询状态
          pollEvaluationStatus(sessionId);
        } catch (err) {
          console.error('结束会话失败:', err);
          message.error('操作失败，请稍后重试');
        } finally {
          setIsEnding(false);
        }
      },
    });
  };

  // 轮询评估报告生成状态
  const pollEvaluationStatus = (sessionId: string) => {
    let attempts = 0;
    const maxAttempts = 120; // 最多轮询10分钟（每5秒一次）
    const interval = 5000; // 5秒轮询一次

    const poll = async () => {
      try {
        const status = await evaluationService.getReportStatus(sessionId);

        if (status.status === 'completed') {
          // 生成完成，弹出通知
          Modal.success({
            title: '评估报告生成完成',
            content: '评估报告已生成完成，点击查看详情',
            okText: '查看报告',
            cancelText: '继续留在本页',
            onOk: () => {
              navigate(`/evaluation/${sessionId}`);
            },
          });
          return; // 停止轮询
        } else if (status.status === 'failed') {
          message.error(status.error_message || '评估报告生成失败，请稍后重试');
          return; // 停止轮询
        }

        // 继续轮询
        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(poll, interval);
        } else {
          message.warning('评估报告生成超时，请稍后在评估页面查看');
        }
      } catch (err) {
        console.error('查询评估状态失败:', err);
        // 即使查询失败也继续尝试
        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(poll, interval);
        }
      }
    };

    // 开始轮询
    setTimeout(poll, interval);
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
          // 处理报警（这会自动结束会话）
          await chatService.alertSuicideRisk(sessionId);

          // 提交异步评估报告生成任务
          await evaluationService.generateReportAsync(sessionId);

          message.success('已记录报警，评估报告生成任务已提交，完成后将通知您');

          // 将页面置于只读模式
          setIsReadOnly(true);

          // 开始后台轮询状态
          pollEvaluationStatus(sessionId);
        } catch (err) {
          console.error('报警失败:', err);
          message.error('报警失败，请稍后重试');
        }
      },
    });
  };

  const handleContinueChat = async () => {
    if (!sessionId) return;

    try {
      // 立刻切换为可输入状态，用户无感
      setIsReadOnly(false);
      // 后台静默 fork 出新 session
      const newSession = await chatService.forkSession(sessionId);
      // 静默替换 URL，不触发页面刷新
      window.history.replaceState(null, '', `/chat/${newSession.id}`);
    } catch (err) {
      console.error('继续对话失败:', err);
      message.error('继续对话失败，请稍后重试');
      setIsReadOnly(true);
    }
  };

  const handleViewReport = async () => {
    if (!sessionId) return;
    try {
      const status = await evaluationService.getReportStatus(sessionId);
      if (status.status === 'generating') {
        message.info('报告正在后台生成中，请耐心等待15秒左右...', 3);
        // Start polling if not already polling
        pollEvaluationStatus(sessionId);
      } else if (status.status === 'completed') {
        navigate(`/evaluation/${sessionId}`);
      } else {
        message.warning('报告生成失败或未找到，请重试');
      }
    } catch (err) {
      console.error('获取状态失败', err);
      // Fallback
      navigate(`/evaluation/${sessionId}`);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      style={{
        height: 'calc(100vh - 64px - 40px)',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        margin: '-20px',
        background: '#fff',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
      }}
    >
      {/* Chat Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.3 }}
        style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
          padding: '16px 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexShrink: 0,
          boxShadow: '0 2px 8px rgba(102, 126, 234, 0.15)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button
              type="text"
              icon={<ArrowLeftOutlined />}
              onClick={() => navigate('/scenarios')}
              style={{ color: '#fff', borderColor: 'rgba(255,255,255,0.3)' }}
            >
              返回
            </Button>
          </motion.div>
          <Title level={5} style={{ margin: 0, color: '#fff' }}>
            <CommentOutlined style={{ marginRight: '8px' }} />
            {currentSession?.scenario_title || '对话练习'}
          </Title>
        </div>

        <Space>
          {currentSession && (
            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 }}>
              <Tag color="blue" style={{ background: 'rgba(255,255,255,0.2)', border: 'none', color: '#fff' }}>
                {messages.length} 条消息
              </Tag>
            </motion.div>
          )}
          <AnimatePresence mode="wait">
            {isReadOnly ? (
              <motion.div
                key="readonly"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                style={{ display: 'flex', gap: '8px', alignItems: 'center' }}
              >
                <Tag color="orange" style={{ background: 'rgba(255,152,0,0.2)', border: 'none', color: '#fff' }}>
                  已结束/只读模式
                </Tag>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    type="primary"
                    onClick={handleViewReport}
                    style={{ background: '#fff', color: '#667eea', border: 'none' }}
                  >
                    查看评估报告
                  </Button>
                </motion.div>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    type="default"
                    icon={<PlayCircleOutlined />}
                    onClick={handleContinueChat}
                    style={{ background: 'rgba(255,255,255,0.2)', color: '#fff', border: 'none' }}
                  >
                    继续对话
                  </Button>
                </motion.div>
              </motion.div>
            ) : (
              <motion.div
                key="active"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                style={{ display: 'flex', gap: '8px' }}
              >
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    danger
                    icon={<AlertIcon />}
                    onClick={handleAlert}
                    style={{ background: 'rgba(255,77,79,0.9)', border: 'none', color: '#fff' }}
                  >
                    报警
                  </Button>
                </motion.div>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    type="primary"
                    icon={<StopOutlined />}
                    onClick={handleEndSession}
                    disabled={isEnding || isLoading}
                    style={{ background: '#fff', color: '#667eea', border: 'none' }}
                  >
                    结束对话
                  </Button>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>
        </Space>
      </motion.div>

      {/* 报警提示横幅 */}
      <AnimatePresence>
        {!isReadOnly && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Alert
              message="提示"
              description="如观察到患者存在自杀倾向，请及时点击「报警」按钮记录处理。"
              type="info"
              showIcon
              closable
              style={{ margin: '12px 24px', borderRadius: '8px', background: 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)', border: 'none' }}
            />
          </motion.div>
        )}
      </AnimatePresence>

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
        <AnimatePresence mode="wait">
          {isReadOnly ? (
            <motion.div
              key="readonly-notice"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <Alert
                message="本对话已结束或处于只读记录模式"
                description="正在生成或已生成评估报告，您可以点击右上角按钮查看。"
                type="info"
                showIcon
                style={{ margin: '16px 24px', borderRadius: '8px' }}
              />
            </motion.div>
          ) : (
            <motion.div
              key="chat-input"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <ChatInput onSend={handleSendMessage} disabled={isLoading} isLoading={isTyping} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};
