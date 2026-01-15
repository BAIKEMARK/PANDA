/**
 * 评估服务
 * 处理评估报告和EPDS量表的API调用
 */
import api from './api';
import type { EvaluationReport, EPDSScale } from '../types/evaluation.types';

class EvaluationService {
  /**
   * 获取会话的评估报告
   * TODO: 后端需要实现此接口
   */
  async getReport(sessionId: string): Promise<EvaluationReport> {
    const response = await api.get<EvaluationReport>(
      `/evaluation/sessions/${sessionId}/report`
    );
    return response.data;
  }

  /**
   * 生成评估报告
   * TODO: 后端需要实现此接口
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
