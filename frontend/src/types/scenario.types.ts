/**
 * 场景相关类型定义
 * 对应后端 backend/app/schemas/scenario.py 和 backend/app/models/scenario.py
 */

// 场景类型
export interface Scenario {
  id: string;
  title: string;
  description: string | null;
  system_prompt: string;
  patient_background: string | null;
  knowledge_tags: string | string[] | null;
  difficulty: number;
  time_period: string | null;
  status: string;  // draft, pending, published, archived
  created_at: string;
}

// 场景创建DTO
export interface ScenarioCreate {
  title: string;
  description?: string;
  system_prompt: string;
  patient_background?: string;
  knowledge_tags?: string;
  difficulty?: number;
  time_period?: string;
}

// 场景更新DTO
export interface ScenarioUpdate {
  title?: string;
  description?: string;
  system_prompt?: string;
  patient_background?: string;
  knowledge_tags?: string;
  difficulty?: number;
  time_period?: string;
}
