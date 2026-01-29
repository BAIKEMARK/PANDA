"""
基础设施服务模块
提供 AI 服务、技能配置、事件总线等共享能力
"""
from backend.app.shared.infrastructure.ai_service import AIService, ai_service
from backend.app.shared.infrastructure.skill_config import SkillConfigManager, skill_config_manager
from backend.app.shared.infrastructure.event_bus import EventBus, Events, event_bus

__all__ = [
    "AIService",
    "ai_service",
    "SkillConfigManager",
    "skill_config_manager",
    "EventBus",
    "Events",
    "event_bus",
]
