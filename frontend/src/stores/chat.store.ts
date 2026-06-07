/**
 * 聊天状态管理
 * 使用persist中间件实现消息持久化
 */
import
{ create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  ChatSession,
  ChatMessage,
  ChatState
} from '../types/chat.types';
import { MessageRole } from '../types/chat.types';
import chatService from '../services/chat.service';

interface ChatStore extends ChatState {
  // Additional state
  currentScenarioId: string | null;
  // 用于持久化的当前会话ID
  lastSessionId: string | null;

  // Actions
  createSession: (scenarioId: number | string) => Promise<ChatSession>;
  loadMessages: (sessionId: number | string) => Promise<void>;
  sendMessage: (sessionId: number | string, content: string) => Promise<ChatMessage & { meta_data?: { force_end?: boolean; reason?: string; crisis_alert?: { suicide_risk?: boolean } } }>;
  endSession: (sessionId: number | string) => Promise<void>;
  resetChat: () => void;
  setTyping: (isTyping: boolean) => void;
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      // Initial state
      currentSession: null,
      messages: [],
      isLoading: false,
      isTyping: false,
      error: null,
      currentScenarioId: null,
      lastSessionId: null,

      // Create new session
      createSession: async (scenarioId: number | string): Promise<ChatSession> => {
        set({ isLoading: true, error: null });
        try {
          const session = await chatService.createSession({ scenario_id: String(scenarioId) });
          set({
            currentSession: session,
            messages: [],
            currentScenarioId: String(scenarioId),
            lastSessionId: session.id,
            isLoading: false,
          });
          return session;
        } catch (error: unknown) {
          const errorMessage = error instanceof Error ? error.message : '创建会话失败';
          set({
            error: errorMessage,
            isLoading: false,
          });
          throw error;
        }
      },

      // Load messages for a session
      loadMessages: async (sessionId: number | string) => {
        set({ isLoading: true, error: null });
        try {
          // Also load the session info
          const [messages, session] = await Promise.all([
            chatService.getMessages(String(sessionId)),
            chatService.getSession(String(sessionId)),
          ]);
          set({ messages, currentSession: session, lastSessionId: String(sessionId), isLoading: false });
        } catch (error: unknown) {
          const errorMessage = error instanceof Error ? error.message : '加载消息失败';
          set({
            error: errorMessage,
            isLoading: false,
          });
          throw error;
        }
      },

      // Send message
      sendMessage: async (sessionId: number | string, content: string) => {
        const sid = String(sessionId);

        set({ isLoading: true, error: null, isTyping: true });

        // Add user message immediately (optimistic update)
        const userMessage: ChatMessage = {
          id: `temp-${Date.now()}`,
          session_id: sid,
          role: MessageRole.USER,
          content,
          meta_data: null,
          created_at: new Date().toISOString(),
        };

        set((state) => ({
          messages: [...state.messages, userMessage],
        }));

        try {
          // Send message to backend
          const response = await chatService.sendMessage({
            session_id: sid,
            role: MessageRole.USER,
            content,
          });

          // Add assistant message
          set((state) => ({
            messages: [...state.messages, response],
            isLoading: false,
            isTyping: false,
          }));

          // Return full response data including crisis_alert and force_end
          return response as ChatMessage & { meta_data?: { force_end?: boolean; reason?: string; crisis_alert?: { suicide_risk?: boolean } } };
        } catch (error: unknown) {
          const errorMessage = error instanceof Error ? error.message : '发送消息失败';
          set({
            error: errorMessage,
            isLoading: false,
            isTyping: false,
          });
          throw error;
        }
      },

      // End session
      endSession: async (sessionId: number | string) => {
        set({ isLoading: true, error: null });
        try {
          const updatedSession = await chatService.endSession(String(sessionId));
          set({
            currentSession: updatedSession,
            isLoading: false,
          });
        } catch (error: unknown) {
          const errorMessage = error instanceof Error ? error.message : '结束会话失败';
          set({
            error: errorMessage,
            isLoading: false,
          });
          throw error;
        }
      },

      // Reset chat state
      resetChat: () => {
        set({
          currentSession: null,
          messages: [],
          isLoading: false,
          isTyping: false,
          error: null,
          currentScenarioId: null,
          lastSessionId: null,
        });
      },

      // Set typing state
      setTyping: (isTyping: boolean) => {
        set({ isTyping });
      },
    }),
    {
      name: 'chat-storage',
      // 只持久化最后访问的会话ID，用于追踪用户的聊天状态
      // 不持久化messages和currentSession，避免旧会话数据污染新会话
      partialize: (state) => ({
        lastSessionId: state.lastSessionId,
      }),
    }
  )
);
