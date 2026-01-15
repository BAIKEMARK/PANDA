/**
 * UI状态管理
 * 管理全局UI状态,如loading、toast、modal、sidebar等
 */
import { create } from 'zustand';

interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}

interface UIStore {
  // Loading state
  isLoading: boolean;
  setLoading: (loading: boolean) => void;

  // Toast notifications
  toasts: ToastMessage[];
  addToast: (message: string, type?: ToastMessage['type']) => void;
  removeToast: (id: string) => void;
  clearToasts: () => void;

  // Modal state
  activeModal: string | null;
  openModal: (modalId: string) => void;
  closeModal: () => void;

  // Sidebar state
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  closeSidebar: () => void;
}

export const useUIStore = create<UIStore>((set, get) => ({
  // Initial state
  isLoading: false,
  toasts: [],
  activeModal: null,
  isSidebarOpen: true,

  // Loading actions
  setLoading: (loading: boolean) => set({ isLoading: loading }),

  // Toast actions
  addToast: (message: string, type: ToastMessage['type'] = 'info') => {
    const id = `toast-${Date.now()}-${Math.random()}`;
    const toast: ToastMessage = { id, type, message, duration: 3000 };
    set((state) => ({ toasts: [...state.toasts, toast] }));

    // Auto remove after duration
    setTimeout(() => {
      get().removeToast(id);
    }, toast.duration);
  },

  removeToast: (id: string) => {
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    }));
  },

  clearToasts: () => set({ toasts: [] }),

  // Modal actions
  openModal: (modalId: string) => set({ activeModal: modalId }),
  closeModal: () => set({ activeModal: null }),

  // Sidebar actions
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  closeSidebar: () => set({ isSidebarOpen: false }),
}));
