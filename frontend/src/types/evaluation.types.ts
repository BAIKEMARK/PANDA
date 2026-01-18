/**
 * 评估报告相关类型定义 - THP五维评分系统
 */

// 能力维度分数 (旧格式,保留用于向后兼容)
export interface DimensionScores {
  knowledge: number;      // 知识理解
  assessment: number;     // 评估技能
  communication: number;  // 沟通技能
  intervention: number;   // 干预决策
}

// THP五维雷达图数据 (新格式)
export interface RadarChart {
  A_risk_identification: number;      // A类-风险识别能力
  B_communication: number;            // B类-沟通支持能力
  C_skill_application: number;        // C类-THP技能应用
  D_safety_management: number;        // D类-安全管理能力
  E_self_efficacy: number;            // E类-自我效能感
}

// 状态变化分析
export interface StateAnalysis {
  mood_change: number;                // 心情变化
  rapport_change: number;             // 信任关系变化
  depression_change: number;          // 抑郁程度变化
  overall_performance: string;        // 整体表现评价
}

// 详细反馈项
export interface FeedbackItem {
  dimension: string;                           // 评估维度
  status: 'pass' | 'fail';                    // 通过/失败
  dialogue_ref_id?: number;                   // 对话轮次引用
  user_input?: string;                        // 用户输入
  patient_state_snapshot?: string | Record<string, any>;  // 患者状态快照 (可以是字符串或对象)
  critique: string;                           // 批评意见
  expert_suggestion: string;                  // 专家建议
}

// 评估报告类型 (THP五维评分系统)
export interface EvaluationReport {
  id: string;
  session_id: string;
  total_score: number;               // 总分 (0-100)
  level_assessment?: string;         // 等级评定: 优秀/良好/合格/不合格
  radar_chart?: RadarChart;          // 五维雷达图数据
  dimension_scores?: DimensionScores; // 旧格式的维度分数(向后兼容)
  state_analysis?: StateAnalysis;    // 状态变化分析
  detailed_feedback?: FeedbackItem[]; // 详细反馈列表
  technical_guidance?: string;       // 技术指导建议
  meta_data?: Record<string, any>;   // 其他元数据
  created_at: string;
  updated_at?: string;
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
