/**
 * 评估服务
 * 处理评估报告和EPDS量表的API调用
 */
import api from './api';
import type { EvaluationReport, EPDSScale } from '../types/evaluation.types';

// 报告生成状态
export interface ReportStatus {
  report_id: string;
  session_id: string;
  status: 'pending' | 'generating' | 'completed' | 'failed';
  error_message?: string;
  created_at?: string;
  completed_at?: string;
  total_score?: number;
}

class EvaluationService {
  /**
   * 获取会话的评估报告
   */
  async getReport(sessionId: string): Promise<EvaluationReport> {
    const response = await api.get<any>(
      `/evaluation/sessions/${sessionId}/report`
    );

    // 手动检查状态码，404 应该抛出异常
    if (response.status === 404) {
      const error = new Error('评估报告不存在');
      console.error('获取评估报告失败:', error);
      throw error;
    }

    if (response.status !== 200) {
      const error = new Error(`获取评估报告失败: HTTP ${response.status}`);
      console.error('获取评估报告失败:', error);
      throw error;
    }

    return response.data;
  }

  /**
   * 异步生成评估报告
   * 返回202 Accepted，报告在后台生成
   */
  async generateReportAsync(sessionId: string): Promise<{
    message: string;
    session_id: string;
    report_id: string;
    status: string;
  }> {
    const response = await api.post(
      `/evaluation/sessions/${sessionId}/evaluate`
    );
    return response.data;
  }

  /**
   * 查询评估报告生成状态
   */
  async getReportStatus(sessionId: string): Promise<ReportStatus> {
    const response = await api.get<ReportStatus>(
      `/evaluation/sessions/${sessionId}/status`
    );
    return response.data;
  }

  /**
   * 轮询等待报告生成完成
   * @param sessionId 会话ID
   * @param onProgress 进度回调
   * @param maxAttempts 最大轮询次数（默认60次，即5分钟）
   * @param interval 轮询间隔（毫秒，默认5秒）
   */
  async waitForReportCompletion(
    sessionId: string,
    onProgress?: (status: ReportStatus) => void,
    maxAttempts: number = 60,
    interval: number = 5000
  ): Promise<EvaluationReport> {
    let attempts = 0;

    while (attempts < maxAttempts) {
      try {
        const status = await this.getReportStatus(sessionId);
        
        // 调用进度回调
        if (onProgress) {
          onProgress(status);
        }

        if (status.status === 'completed') {
          // 生成完成，获取完整报告
          return await this.getReport(sessionId);
        } else if (status.status === 'failed') {
          throw new Error(status.error_message || '评估报告生成失败');
        }

        // 等待后继续轮询
        await new Promise(resolve => setTimeout(resolve, interval));
        attempts++;
      } catch (error) {
        console.error('轮询报告状态失败:', error);
        throw error;
      }
    }

    throw new Error('评估报告生成超时，请稍后重试');
  }

  /**
   * 生成评估报告（旧版本，同步等待）
   * 已废弃，建议使用 generateReportAsync + waitForReportCompletion
   */
  async generateReport(sessionId: string): Promise<EvaluationReport> {
    const response = await api.post<EvaluationReport>(
      `/evaluation/sessions/${sessionId}/generate`
    );
    return response.data;
  }

  /**
   * 获取用户的所有评估报告
   */
  async getUserReports(): Promise<EvaluationReport[]> {
    const response = await api.get<EvaluationReport[]>('/evaluation/reports');
    return response.data;
  }

  /**
   * 保存EPDS量表数据
   */
  async saveEPDSScale(data: Partial<EPDSScale>): Promise<EPDSScale> {
    // TODO: 后端需要实现EPDS量表保存接口
    const response = await api.post<EPDSScale>('/evaluation/epds', data);
    return response.data;
  }

  /**
   * 获取EPDS量表
   */
  async getEPDSScale(sessionId: string): Promise<EPDSScale> {
    // TODO: 后端需要实现此接口
    const response = await api.get<EPDSScale>(`/evaluation/epds/${sessionId}`);
    return response.data;
  }
}

export default new EvaluationService();
