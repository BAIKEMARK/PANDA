/**
 * 聊天对话相关类型定义
 * 对应后端 backend/app/schemas/chat.py 和 backend/app/models/chat.py
 */

// 会话状态
export const SessionStatus = {
  ACTIVE: 'active',
  COMPLETED: 'completed',
  ABANDONED: 'abandoned',
} as const;
export type SessionStatus = (typeof SessionStatus)[keyof typeof SessionStatus];

// 消息角色
export const MessageRole = {
  USER: 'user',
  ASSISTANT: 'assistant',
  SYSTEM: 'system',
} as const;
export type MessageRole = (typeof MessageRole)[keyof typeof MessageRole];

// 会话类型
export interface ChatSession {
  id: string;
  user_id: string;
  scenario_id: string;
  scenario_title?: string;  // 场景标题，由后端join查询返回
  patient_background?: string;  // 患者背景信息
  status: SessionStatus;
  start_time: string;  // 开始时间
  end_time: string | null;  // 结束时间
  final_score: number | null;
  meta_data: Record<string, unknown> | null;
}

// 会话创建DTO
export interface ChatSessionCreate {
  scenario_id: string;
}

// 消息类型
export interface ChatMessage {
  id: string;
  session_id: string;
  role: MessageRole;
  content: string;
  meta_data: Record<string, unknown> | null;
  created_at: string;
}

// 消息创建DTO
export interface ChatMessageCreate {
  session_id: string;
  role: MessageRole;
  content: string;
  meta_data?: Record<string, unknown>;
}

// 聊天状态
export interface ChatState {
  currentSession: ChatSession | null;
  messages: ChatMessage[];
  isLoading: boolean;
  isTyping: boolean;
  error: string | null;
  currentScenarioId: string | null;
}
