/**
 * 聊天对话相关类型定义
 * 对应后端 backend/app/schemas/chat.py 和 backend/app/models/chat.py
 */

// 会话状态枚举
export enum SessionStatus {
  ACTIVE = 'active',
  COMPLETED = 'completed',
  ABANDONED = 'abandoned',
}

// 消息角色枚举
export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system',
}

// 会话类型
export interface ChatSession {
  id: string;
  user_id: string;
  scenario_id: string;
  scenario_title?: string;  // 场景标题，由后端join查询返回
  status: SessionStatus;
  start_time: string;
  end_time: string | null;
  final_score: number | null;
  meta_data: Record<string, any> | null;
  created_at: string;  // 创建时间
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
  meta_data: Record<string, any> | null;
  created_at: string;
}

// 消息创建DTO
export interface ChatMessageCreate {
  session_id: string;
  role: MessageRole;
  content: string;
  meta_data?: Record<string, any>;
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
