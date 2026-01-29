"""
事件总线 - 模块间异步通信机制
实现发布-订阅模式，解耦模块间的直接依赖
"""
from typing import Callable, Dict, List, Optional
from threading import Lock


class EventBus:
    """事件总线 - 单例模式"""

    _instance: Optional['EventBus'] = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._subscribers: Dict[str, List[Callable]] = {}
                    cls._instance._event_log: List[Dict] = []
        return cls._instance

    def __init__(self):
        """初始化事件总线"""
        pass

    def publish(self, event_name: str, data: Dict) -> None:
        """
        发布事件

        Args:
            event_name: 事件名称
            data: 事件数据

        Example:
            event_bus.publish("chat.session_ended", {"session_id": "xxx"})
        """
        print(f"📢 [EventBus] 发布事件: {event_name}")

        # 记录事件日志
        self._event_log.append({
            "event": event_name,
            "data": data
        })

        # 获取订阅者
        handlers = self._subscribers.get(event_name, [])

        if not handlers:
            print(f"   (无订阅者)")
            return

        # 通知所有订阅者
        for handler in handlers:
            try:
                handler(data)
                print(f"   ✓ 已通知订阅者: {handler.__name__}")
            except Exception as e:
                print(f"   ✗ 订阅者处理失败: {handler.__name__} - {e}")

    def subscribe(self, event_name: str, handler: Callable) -> None:
        """
        订阅事件

        Args:
            event_name: 事件名称
            handler: 处理函数

        Example:
            event_bus.subscribe("chat.session_ended", self.handle_session_ended)
        """
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []

        if handler not in self._subscribers[event_name]:
            self._subscribers[event_name].append(handler)
            print(f"📌 [EventBus] 订阅事件: {event_name} -> {handler.__name__}")

    def unsubscribe(self, event_name: str, handler: Callable) -> None:
        """
        取消订阅

        Args:
            event_name: 事件名称
            handler: 处理函数
        """
        if event_name in self._subscribers:
            if handler in self._subscribers[event_name]:
                self._subscribers[event_name].remove(handler)
                print(f"🔌 [EventBus] 取消订阅: {event_name} -> {handler.__name__}")

    def get_subscribers(self, event_name: str) -> List[Callable]:
        """获取事件的订阅者列表"""
        return self._subscribers.get(event_name, [])

    def get_event_log(self, limit: int = 100) -> List[Dict]:
        """获取事件日志"""
        return self._event_log[-limit:]

    def clear_event_log(self) -> None:
        """清空事件日志"""
        self._event_log.clear()


# 创建全局实例
event_bus = EventBus()


# 事件名称常量定义
class Events:
    """事件名称常量"""

    # 对话模块事件
    CHAT_SESSION_CREATED = "chat.session_created"
    CHAT_MESSAGE_SENT = "chat.message_sent"
    CHAT_SESSION_ENDED = "chat.session_ended"

    # 评估模块事件
    EVALUATION_GENERATED = "evaluation.generated"
    EVALUATION_FAILED = "evaluation.failed"

    # 学习进度事件
    COURSE_STARTED = "course.started"
    COURSE_COMPLETED = "course.completed"
    SCENARIO_COMPLETED = "scenario.completed"
