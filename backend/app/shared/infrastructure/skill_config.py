"""
技能配置管理服务
负责读取和管理全局对话技能配置
从 core/skill.py 迁移而来
"""
import json
from pathlib import Path
from typing import Dict, Optional


class SkillConfigManager:
    """技能配置管理器 - 单例模式"""

    _instance: Optional['SkillConfigManager'] = None
    _config: Optional[Dict] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化技能管理器"""
        if self._config is None:
            self._load_config()

    def _get_config_path(self) -> Path:
        """获取配置文件路径"""
        # 获取当前文件目录 (backend/app/shared/infrastructure/)
        current_dir = Path(__file__).parent.absolute()
        # 向上查找 backend/app/core/skill_config.json
        config_path = current_dir.parent.parent / "core" / "skill_config.json"
        return config_path

    def _load_config(self) -> None:
        """加载配置文件"""
        config_path = self._get_config_path()

        if not config_path.exists():
            print(f"⚠️  Skill配置文件不存在: {config_path}")
            self._config = self._get_default_config()
            return

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            print(f"✅ Skill配置加载成功: {config_path}")
        except Exception as e:
            print(f"❌ Skill配置加载失败: {e}")
            self._config = self._get_default_config()

    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            "global_skill": {
                "name": "默认技能",
                "description": "默认的全局对话技能",
                "version": "1.0.0",
                "enabled": True,
                "instructions": [
                    "保持专业和友善",
                    "提供有价值的建议"
                ],
                "system_prompt_template": "你是一位专业的健康顾问。",
                "evaluation_criteria": {}
            }
        }

    def reload_config(self) -> None:
        """重新加载配置文件"""
        self._load_config()

    def get_global_skill(self) -> Dict:
        """获取全局技能配置"""
        return self._config.get("global_skill", {})

    def is_enabled(self) -> bool:
        """检查全局技能是否启用"""
        return self.get_global_skill().get("enabled", False)

    def get_skill_prompt(self, current_state: dict = None) -> str:
        """获取技能提示词

        Args:
            current_state: 当前病人状态，包含mood_score, satisfaction_score等指标
        """
        if not self.is_enabled():
            return ""

        skill = self.get_global_skill()
        template = skill.get("system_prompt_template", "")

        # 获取行为指南
        behavior = skill.get("behavior_guidelines", {})
        language_style = behavior.get("language_style", "")
        emotional_response = behavior.get("emotional_response", "")
        rapport_building = behavior.get("rapport_building", "")

        # 获取核心原则
        core_principles = skill.get("core_principles", [])
        principles_text = "\n".join([f"• {p}" for p in core_principles])

        # 获取语气映射（基于当前心情）
        indicator_rules = skill.get("indicator_rules", {})
        mood_rules = indicator_rules.get("mood_score", {})
        tone_mapping = mood_rules.get("tone_mapping", {})

        # 根据当前状态确定语气
        current_tone = ""
        if current_state:
            mood = current_state.get("mood_score", 50)
            if mood < 30:
                current_tone = tone_mapping.get("<30", "低落")
            elif mood < 50:
                current_tone = tone_mapping.get("30-50", "焦虑")
            elif mood < 70:
                current_tone = tone_mapping.get("50-70", "谨慎")
            else:
                current_tone = tone_mapping.get(">70", "开放")
        else:
            # 默认显示所有映射
            current_tone = "\n".join([f"{k}: {v}" for k, v in tone_mapping.items()])

        # 替换模板中的占位符
        prompt = template
        prompt = prompt.replace("{core_principles}", principles_text)
        prompt = prompt.replace("{language_style}", language_style)
        prompt = prompt.replace("{emotional_response}", emotional_response)
        prompt = prompt.replace("{rapport_building}", rapport_building)
        prompt = prompt.replace("{tone_mapping}", current_tone)

        # 如果提供了当前状态，填充状态值
        if current_state:
            prompt = prompt.replace("{mood_score}", str(current_state.get("mood_score", 50)))
            prompt = prompt.replace("{satisfaction_score}", str(current_state.get("satisfaction_score", 40)))
            prompt = prompt.replace("{depression_level}", str(current_state.get("depression_level", 60)))
            prompt = prompt.replace("{rapport_score}", str(current_state.get("rapport_score", 40)))
        else:
            prompt = prompt.replace("{mood_score}", "50")
            prompt = prompt.replace("{satisfaction_score}", "40")
            prompt = prompt.replace("{depression_level}", "60")
            prompt = prompt.replace("{rapport_score}", "40")

        return prompt

    def get_crisis_thresholds(self) -> Dict:
        """获取危机阈值配置"""
        return self.get_global_skill().get("cris_thresholds", {})

    def get_crisis_response(self, crisis_type: str) -> str:
        """获取危机响应文本

        Args:
            crisis_type: 危机类型 (extreme_low_mood, dissatisfaction, rapport_broken, severe_depression)
        """
        responses = self.get_global_skill().get("crisis_responses", {})
        return responses.get(crisis_type, "（患者情绪异常，对话无法继续）")

    def get_indicator_rules(self) -> Dict:
        """获取指标变化规则"""
        return self.get_global_skill().get("indicator_rules", {})

    def get_evaluation_criteria(self) -> Dict:
        """获取评估标准"""
        return self.get_global_skill().get("evaluation_criteria", {})

    def get_skill_info(self) -> Dict:
        """获取技能完整信息（用于API返回）"""
        skill = self.get_global_skill()
        return {
            "name": skill.get("name", ""),
            "description": skill.get("description", ""),
            "version": skill.get("version", ""),
            "enabled": skill.get("enabled", False),
            "role_definition": skill.get("role_definition", ""),
            "core_principles": skill.get("core_principles", []),
            "behavior_guidelines": skill.get("behavior_guidelines", {}),
            "indicator_rules": skill.get("indicator_rules", {}),
            "cris_thresholds": skill.get("cris_thresholds", {}),
            "crisis_responses": skill.get("crisis_responses", {})
        }


# 创建全局实例
skill_config_manager = SkillConfigManager()
