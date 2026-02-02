"""
Redis状态管理器
管理患者动态状态的Redis存储，支持快速读写
"""
from typing import Dict, Optional

import redis
from redis import Redis

from backend.app.config.config import settings
from backend.app.modules.agent.models.patient_state import PatientState


class RedisStateManager:
    """
    Redis状态管理器 - 单例模式

    负责患者动态状态的Redis存储，包括：
    - 实时状态读写 (<10ms目标)
    - TTL自动过期管理
    """

    _instance: Optional['RedisStateManager'] = None
    _redis_client: Optional[Redis] = None

    # Redis Key 前缀
    STATE_KEY_PREFIX = "patient:state:"

    # TTL 配置
    STATE_TTL_SECONDS = 24 * 60 * 60  # 24小时

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化Redis连接池"""
        if not hasattr(self, '_initialized'):
            try:
                self._redis_client = redis.ConnectionPool(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    decode_responses=settings.REDIS_DECODE_RESPONSES,
                    socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
                    socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
                    max_connections=settings.REDIS_MAX_CONNECTIONS
                )
                self._client = redis.Redis(connection_pool=self._redis_client)
                self._initialized = True
                print(f"✅ Redis连接池已初始化: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
            except Exception as e:
                print(f"❌ Redis连接失败: {e}")
                raise

    def _get_state_key(self, session_id: str) -> str:
        """获取状态Redis Key"""
        return f"{self.STATE_KEY_PREFIX}{session_id}"

    def get_patient_state(self, session_id: str) -> Optional[PatientState]:
        """
        获取患者当前状态

        Args:
            session_id: 会话ID

        Returns:
            PatientState对象，不存在返回None
        """
        try:
            key = self._get_state_key(session_id)
            data = self._client.hgetall(key)

            if not data:
                return None

            return PatientState(
                mood_score=int(data.get('mood_score', 50)),
                satisfaction_score=int(data.get('satisfaction_score', 50)),
                depression_level=int(data.get('depression_level', 50)),
                rapport_score=int(data.get('rapport_score', 50)),
                message_count=int(data.get('message_count', 0))
            )
        except Exception as e:
            print(f"❌ 获取患者状态失败: {e}")
            return None

    def update_patient_state(
        self,
        session_id: str,
        updates: Dict,
        extend_ttl: bool = True
    ) -> Optional[PatientState]:
        """
        更新患者状态

        Args:
            session_id: 会话ID
            updates: 状态更新字典，如 {'mood_score': 60, 'message_count': 5}
            extend_ttl: 是否延长TTL

        Returns:
            更新后的PatientState对象
        """
        try:
            key = self._get_state_key(session_id)

            # 获取当前状态
            current = self.get_patient_state(session_id)
            if current is None:
                # 首次创建，使用默认值
                current = PatientState()

            # 应用更新
            update_data = {}
            for field, value in updates.items():
                if hasattr(current, field):
                    setattr(current, field, value)
                    update_data[field] = value

            if not update_data:
                return current

            # 写入Redis
            self._client.hset(key, mapping={
                'mood_score': str(current.mood_score),
                'satisfaction_score': str(current.satisfaction_score),
                'depression_level': str(current.depression_level),
                'rapport_score': str(current.rapport_score),
                'message_count': str(current.message_count)
            })

            # 设置TTL
            if extend_ttl:
                self._client.expire(key, self.STATE_TTL_SECONDS)

            return current
        except Exception as e:
            print(f"❌ 更新患者状态失败: {e}")
            return None

    def increment_message_count(self, session_id: str) -> int:
        """
        增加消息计数

        Args:
            session_id: 会话ID

        Returns:
            新的消息计数
        """
        try:
            key = self._get_state_key(session_id)
            new_count = self._client.hincrby(key, 'message_count', 1)
            self._client.expire(key, self.STATE_TTL_SECONDS)
            return new_count
        except Exception as e:
            print(f"❌ 增加消息计数失败: {e}")
            return 0

    def delete_session(self, session_id: str) -> bool:
        """
        删除会话数据

        Args:
            session_id: 会话ID

        Returns:
            是否成功
        """
        try:
            state_key = self._get_state_key(session_id)
            self._client.delete(state_key)
            return True
        except Exception as e:
            print(f"❌ 删除会话数据失败: {e}")
            return False

    def check_health(self) -> bool:
        """
        检查Redis健康状态

        Returns:
            Redis是否可用
        """
        try:
            return self._client.ping()
        except Exception as e:
            print(f"❌ Redis健康检查失败: {e}")
            return False


# 创建全局实例
redis_state_manager = RedisStateManager()
