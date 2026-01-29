"""
场景模块对外接口
chat 模块通过此接口访问场景数据，避免直接 import
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class ScenarioConfig:
    """场景配置数据类"""
    id: str
    title: str
    description: str
    system_prompt: str
    patient_background: str
    difficulty: int
    time_period: str


class ScenarioInterface(ABC):
    """场景模块抽象接口"""

    @abstractmethod
    def get_scenario_config(self, scenario_id: str) -> Optional[ScenarioConfig]:
        """
        获取场景配置

        Args:
            scenario_id: 场景ID

        Returns:
            ScenarioConfig 对象，不存在返回 None
        """
        pass

    @abstractmethod
    def get_patient_background(self, scenario_id: str) -> str:
        """
        获取患者背景

        Args:
            scenario_id: 场景ID

        Returns:
            患者背景文本
        """
        pass

    @abstractmethod
    def get_system_prompt(self, scenario_id: str) -> str:
        """
        获取系统提示词

        Args:
            scenario_id: 场景ID

        Returns:
            系统提示词
        """
        pass
