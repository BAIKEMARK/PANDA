/**
 * 评估报告相关类型定义
 */

// 能力维度分数
export interface DimensionScores {
  knowledge: number;      // 知识理解
  assessment: number;     // 评估技能
  communication: number;  // 沟通技能
  intervention: number;   // 干预决策
}

// 评估报告类型
export interface EvaluationReport {
  id: string;
  session_id: string;
  scores: DimensionScores;
  total_score: number;
  ai_feedback: string;
  created_at: string;
}

// EPDS量表数据
export interface EPDSScale {
  id?: string;
  session_id: string;
  responses: number[];      // 10个问题的回答
  total_score: number;      // 总分
  risk_level: string;       // 风险等级
  created_at?: string;
}

// EPDS风险等级
export enum EPDSRiskLevel {
  LOW = 'low',           // 0-9分
  MEDIUM = 'medium',     // 10-12分
  HIGH = 'high',         // 13-30分
}
