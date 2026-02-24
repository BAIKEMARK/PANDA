/**
 * 聊天对话服务
 * 处理AI对话会话和消息的API调用
 */
import api from './api';
import type {
  ChatSession,
  ChatSessionCreate,
  ChatMessage,
  ChatMessageCreate
} from '../types/chat.types';

class ChatService {
  /**
   * 创建新会话
   */
  async createSession(data: ChatSessionCreate): Promise<ChatSession> {
    const response = await api.post<ChatSession>('/chat/sessions', data);
    return response.data;
  }

  /**
   * 获取会话详情
   */
  async getSession(sessionId: string): Promise<ChatSession> {
    const response = await api.get<ChatSession>(`/chat/sessions/${sessionId}`);
    return response.data;
  }

  /**
   * 获取会话的所有消息
   */
  async getMessages(sessionId: string): Promise<ChatMessage[]> {
    const response = await api.get<ChatMessage[]>(
      `/chat/sessions/${sessionId}/messages`
    );
    return response.data;
  }

  /**
   * 发送消息
   */
  async sendMessage(data: ChatMessageCreate): Promise<ChatMessage> {
    const response = await api.post<ChatMessage>('/chat/messages', data);
    return response.data;
  }

  /**
   * 结束会话
   */
  async endSession(sessionId: string, finalScore?: number): Promise<ChatSession> {
    const response = await api.put<ChatSession>(
      `/chat/sessions/${sessionId}/end`,
      { final_score: finalScore }
    );
    return response.data;
  }

  /**
   * 重新开启已结束的会话（继续对话）
   */
  async reopenSession(sessionId: string): Promise<ChatSession> {
    const response = await api.put<ChatSession>(`/chat/sessions/${sessionId}/reopen`);
    return response.data;
  }

  /**
   * 自杀倾向报警
   */
  async alertSuicideRisk(sessionId: string): Promise<ChatSession> {
    const response = await api.post<ChatSession>(`/chat/sessions/${sessionId}/alert`);
    return response.data;
  }

  /**
   * 流式发送消息 (SSE - 需要后端支持)
   * TODO: 后端需要实现流式响应接口
   */
  async sendMessageStream(
    data: ChatMessageCreate,
    onChunk: (chunk: string) => void,
    onComplete: (fullMessage: ChatMessage) => void,
    onError: (error: Error) => void
  ): Promise<void> {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Stream request failed');
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let fullContent = '';

      while (true) {
        const { done, value } = await reader!.read();

        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));

            if (data.type === 'chunk') {
              fullContent += data.content;
              onChunk(data.content);
            } else if (data.type === 'complete') {
              onComplete({
                ...data.message,
                content: fullContent,
              } as ChatMessage);
            }
          }
        }
      }
    } catch (error) {
      onError(error as Error);
    }
  }
}

export default new ChatService();
