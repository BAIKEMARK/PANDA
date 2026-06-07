"""
Redis cache service
轻量通用缓存封装（JSON）
"""
from typing import Any, Optional
import json

import redis
from redis import Redis

from backend.app.core.config.settings import settings


class RedisCache:
    """通用Redis缓存 - 单例模式"""

    _instance: Optional["RedisCache"] = None
    _redis_client: Optional[Redis] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            try:
                self._connection_pool = redis.ConnectionPool(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    decode_responses=settings.REDIS_DECODE_RESPONSES,
                    socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
                    socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
                    max_connections=settings.REDIS_MAX_CONNECTIONS,
                )
                self._client = redis.Redis(connection_pool=self._connection_pool)
                self._initialized = True
                print(f"[OK] Redis缓存连接池已初始化: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
            except Exception as e:
                print(f"[ERROR] Redis缓存连接失败: {e}")
                raise

    def get_json(self, key: str) -> Optional[Any]:
        """获取JSON缓存"""
        try:
            raw = self._client.get(key)
            if not raw:
                return None
            return json.loads(raw)
        except Exception as e:
            print(f"[ERROR] Redis缓存读取失败: {e}")
            return None

    def set_json(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """设置JSON缓存"""
        try:
            payload = json.dumps(value, ensure_ascii=False)
            ttl = ttl_seconds if ttl_seconds is not None else settings.CACHE_DEFAULT_TTL
            if ttl and ttl > 0:
                self._client.setex(key, ttl, payload)
            else:
                self._client.set(key, payload)
            return True
        except Exception as e:
            print(f"[ERROR] Redis缓存写入失败: {e}")
            return False

    def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            self._client.delete(key)
            return True
        except Exception as e:
            print(f"[ERROR] Redis缓存删除失败: {e}")
            return False


# 全局实例
redis_cache = RedisCache()
