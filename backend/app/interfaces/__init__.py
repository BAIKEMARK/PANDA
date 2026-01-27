"""
模块间接口定义层
定义业务模块之间的抽象接口，实现模块间解耦
"""
from backend.app.interfaces.scenario_interface import ScenarioInterface, ScenarioConfig

__all__ = ["ScenarioInterface", "ScenarioConfig"]
