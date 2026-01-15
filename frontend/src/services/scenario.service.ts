/**
 * 场景服务
 * 处理训练场景相关的API调用
 */
import api from './api';
import type { Scenario } from '../types/scenario.types';

class ScenarioService {
  /**
   * 获取场景列表
   */
  async getScenarios(): Promise<Scenario[]> {
    const response = await api.get<Scenario[]>('/scenarios/');
    return response.data;
  }

  /**
   * 获取单个场景详情
   */
  async getScenario(scenarioId: string): Promise<Scenario> {
    const response = await api.get<Scenario>(`/scenarios/${scenarioId}`);
    return response.data;
  }

  /**
   * 按难度筛选场景
   */
  async getScenariosByDifficulty(difficulty: number): Promise<Scenario[]> {
    const response = await api.get<Scenario[]>('/scenarios/', {
      params: { difficulty }
    });
    return response.data;
  }

  /**
   * 按时间节点筛选场景
   */
  async getScenariosByTimePeriod(timePeriod: string): Promise<Scenario[]> {
    const allScenarios = await this.getScenarios();
    return allScenarios.filter(s => s.time_period === timePeriod);
  }

  /**
   * 创建场景 (管理员功能)
   */
  async createScenario(data: Partial<Scenario>): Promise<Scenario> {
    const response = await api.post<Scenario>('/scenarios/', data);
    return response.data;
  }
}

export default new ScenarioService();
