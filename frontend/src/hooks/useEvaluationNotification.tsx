/**
 * 评估报告生成通知Hook
 * 用于在报告生成完成后显示通知
 */
import { useCallback, useEffect, useRef, useState } from 'react';
import { message, notification } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, LoadingOutlined } from '@ant-design/icons';
import evaluationService from '../services/evaluation.service';
import type { ReportStatus } from '../services/evaluation.service';

interface UseEvaluationNotificationOptions {
  sessionId: string;
  onCompleted?: (reportId: string) => void;
  onFailed?: (error: string) => void;
  autoStart?: boolean;
  pollingInterval?: number;
  maxAttempts?: number;
}

const getFailureMessage = (errorMessage?: string) => {
  if (!errorMessage) {
    return '未知错误';
  }
  return errorMessage.length > 160 ? `${errorMessage.slice(0, 160)}...` : errorMessage;
};

export const useEvaluationNotification = ({
  sessionId,
  onCompleted,
  onFailed,
  autoStart = false,
  pollingInterval = 5000,
  maxAttempts = 60,
}: UseEvaluationNotificationOptions) => {
  const [status, setStatus] = useState<ReportStatus | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const pollingTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const attemptsRef = useRef(0);
  const notificationKeyRef = useRef<string>('');
  const pollStatusRef = useRef<(() => Promise<void>) | null>(null);

  // 清理轮询
  const stopPolling = useCallback(() => {
    if (pollingTimerRef.current) {
      clearTimeout(pollingTimerRef.current);
      pollingTimerRef.current = null;
    }
    setIsPolling(false);
  }, []);

  // 轮询状态
  const pollStatus = useCallback(async () => {
    if (attemptsRef.current >= maxAttempts) {
      stopPolling();
      notification.error({
        message: '评估报告生成超时',
        description: '报告生成时间过长，请稍后刷新页面查看',
        duration: 0,
      });
      if (onFailed) {
        onFailed('生成超时');
      }
      return;
    }

    try {
      const reportStatus = await evaluationService.getReportStatus(sessionId);
      setStatus(reportStatus);
      attemptsRef.current++;

      if (reportStatus.status === 'completed') {
        // 生成完成
        stopPolling();
        
        // 关闭进度通知
        if (notificationKeyRef.current) {
          notification.destroy(notificationKeyRef.current);
        }

        // 显示成功通知
        notification.success({
          message: '评估报告已生成',
          description: (
            <div>
              <p>您的评估报告已生成完成！</p>
              <p>总分: <strong>{reportStatus.total_score}</strong></p>
              <a
                onClick={() => {
                  if (onCompleted) {
                    onCompleted(reportStatus.report_id);
                  }
                }}
                style={{ color: '#1890ff', cursor: 'pointer' }}
              >
                点击查看报告
              </a>
            </div>
          ),
          duration: 0,
          icon: <CheckCircleOutlined style={{ color: '#52c41a' }} />,
        });

        if (onCompleted) {
          onCompleted(reportStatus.report_id);
        }
      } else if (reportStatus.status === 'failed') {
        // 生成失败
        stopPolling();
        
        // 关闭进度通知
        if (notificationKeyRef.current) {
          notification.destroy(notificationKeyRef.current);
        }

        const failureMessage = getFailureMessage(reportStatus.error_message);
        notification.error({
          message: '评估报告生成失败',
          description: failureMessage,
          duration: 0,
          icon: <CloseCircleOutlined style={{ color: '#ff4d4f' }} />,
        });

        if (onFailed) {
          onFailed(failureMessage || '生成失败');
        }
      } else {
        // 继续轮询
        pollingTimerRef.current = setTimeout(() => {
          pollStatusRef.current?.();
        }, pollingInterval);
      }
    } catch (error) {
      console.error('查询报告状态失败:', error);
      // 继续轮询，不中断
      pollingTimerRef.current = setTimeout(() => {
        pollStatusRef.current?.();
      }, pollingInterval);
    }
  }, [maxAttempts, onCompleted, onFailed, pollingInterval, sessionId, stopPolling]);

  useEffect(() => {
    pollStatusRef.current = pollStatus;
    return () => {
      pollStatusRef.current = null;
    };
  }, [pollStatus]);

  // 开始生成报告
  const startGeneration = useCallback(async () => {
    try {
      // 提交生成任务
      const result = await evaluationService.generateReportAsync(sessionId);
      
      if (result.status === 'completed') {
        // 已经完成
        message.success('评估报告已存在');
        if (onCompleted) {
          onCompleted(result.report_id);
        }
        return;
      }

      // 显示进度通知
      const key = `evaluation-${sessionId}`;
      notificationKeyRef.current = key;
      
      notification.info({
        key,
        message: '正在生成评估报告',
        description: '报告生成需要一些时间，您可以继续使用系统，完成后会通知您',
        duration: 0,
        icon: <LoadingOutlined style={{ color: '#1890ff' }} />,
      });

      // 开始轮询
      setIsPolling(true);
      attemptsRef.current = 0;
      pollStatus();
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '提交评估任务失败';
      message.error(errorMessage);
      if (onFailed) {
        onFailed(errorMessage);
      }
    }
  }, [onCompleted, onFailed, pollStatus, sessionId]);

  // 自动开始
  useEffect(() => {
    let startTimer: ReturnType<typeof setTimeout> | null = null;
    if (autoStart && sessionId) {
      startTimer = setTimeout(() => {
        startGeneration();
      }, 0);
    }

    // 清理
    return () => {
      if (startTimer) {
        clearTimeout(startTimer);
      }
      stopPolling();
      if (notificationKeyRef.current) {
        notification.destroy(notificationKeyRef.current);
      }
    };
  }, [sessionId, autoStart, startGeneration, stopPolling]);

  return {
    status,
    isPolling,
    startGeneration,
    stopPolling,
  };
};
