/**
 * 聊天状态管理
 * 使用persist中间件实现消息持久化
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  ChatSession,
  ChatMessage,
  ChatState,
  ChatMessageCreate
} from '../types/chat.types';
import { MessageRole } from '../types/chat.types';
import chatService from '../services/chat.service';

interface ChatStore extends ChatState {
  // Additional state
  currentScenarioId: string | null;

  // Actions
  createSession: (scenarioId: number | string) => Promise<ChatSession>;
  loadMessages: (sessionId: number | string) => Promise<void>;
  sendMessage: (sessionId: number | string, content: string) => Promise<void>;
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

      // Create new session
      createSession: async (scenarioId: number | string): Promise<ChatSession> => {
        set({ isLoading: true, error: null });
        try {
          const session = await chatService.createSession({ scenario_id: String(scenarioId) });
          set({
            currentSession: session,
            messages: [],
            currentScenarioId: String(scenarioId),
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
          set({ messages, currentSession: session, isLoading: false });
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
        const { currentSession } = get();
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
        });
      },

      // Set typing state
      setTyping: (isTyping: boolean) => {
        set({ isTyping });
      },
    }),
    {
      name: 'chat-storage',
      partialize: (state) => ({
        currentSession: state.currentSession,
        messages: state.messages,
      }),
    }
  )
);
