/**
 * 缓存工具
 * 提供内存缓存和LocalStorage缓存
 */

interface CacheItem<T> {
  data: T;
  timestamp: number;
  expiry: number; // 过期时间（毫秒）
}

class CacheManager {
  private memoryCache: Map<string, CacheItem<unknown>> = new Map();
  private readonly DEFAULT_EXPIRY = 5 * 60 * 1000; // 默认5分钟

  /**
   * 设置缓存
   */
  set<T>(key: string, data: T, expiry: number = this.DEFAULT_EXPIRY): void {
    const item: CacheItem<T> = {
      data,
      timestamp: Date.now(),
      expiry,
    };
    
    // 内存缓存
    this.memoryCache.set(key, item);
    
    // LocalStorage缓存（仅缓存可序列化的数据）
    try {
      localStorage.setItem(`cache_${key}`, JSON.stringify(item));
    } catch (error) {
      console.warn('LocalStorage缓存失败:', error);
    }
  }

  /**
   * 获取缓存
   */
  get<T>(key: string): T | null {
    // 先从内存缓存获取
    let item = this.memoryCache.get(key);
    
    // 如果内存缓存没有，尝试从LocalStorage获取
    if (!item) {
      try {
        const stored = localStorage.getItem(`cache_${key}`);
        if (stored) {
          item = JSON.parse(stored);
          // 恢复到内存缓存
          if (item) {
            this.memoryCache.set(key, item);
          }
        }
      } catch (error) {
        console.warn('LocalStorage读取失败:', error);
      }
    }
    
    if (!item) {
      return null;
    }
    
    // 检查是否过期
    const now = Date.now();
    if (now - item.timestamp > item.expiry) {
      this.delete(key);
      return null;
    }
    
    return item.data as T;
  }

  /**
   * 删除缓存
   */
  delete(key: string): void {
    this.memoryCache.delete(key);
    try {
      localStorage.removeItem(`cache_${key}`);
    } catch (error) {
      console.warn('LocalStorage删除失败:', error);
    }
  }

  /**
   * 清空所有缓存
   */
  clear(): void {
    this.memoryCache.clear();
    
    // 清空LocalStorage中的缓存
    try {
      const keys = Object.keys(localStorage);
      keys.forEach(key => {
        if (key.startsWith('cache_')) {
          localStorage.removeItem(key);
        }
      });
    } catch (error) {
      console.warn('LocalStorage清空失败:', error);
    }
  }

  /**
   * 检查缓存是否存在且有效
   */
  has(key: string): boolean {
    return this.get(key) !== null;
  }

  /**
   * 获取或设置缓存（如果不存在则执行fetcher）
   */
  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    expiry: number = this.DEFAULT_EXPIRY
  ): Promise<T> {
    const cached = this.get<T>(key);
    if (cached !== null) {
      return cached;
    }
    
    const data = await fetcher();
    this.set(key, data, expiry);
    return data;
  }
}

// 导出单例
export const cache = new CacheManager();

// 导出缓存键常量
export const CACHE_KEYS = {
  USER_INFO: 'user_info',
  COURSES: 'courses',
  SCENARIOS: 'scenarios',
  MENUS: 'menus',
  ROLES: 'roles',
  ORGANIZATIONS: 'organizations',
} as const;
