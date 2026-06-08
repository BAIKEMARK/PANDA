"""
状态更新规则引擎
基于skill_config.json的规则计算患者状态变化
"""
import json
import re
from typing import Dict, Optional, List
from pathlib import Path

from backend.app.modules.conversation.agent.models.patient_state import PatientStateUpdate, CrisisEvent
from backend.app.core.config.logging import get_logger

logger = get_logger(__name__)


class StateUpdateEngine:
    """
    状态更新引擎 - 基于skill_config.json规则

    负责根据护士输入和患者回复，计算患者动态指标的变化
    """

    def __init__(self, config_path: str = None):
        """初始化规则引擎，加载配置文件"""
        if config_path is None:
            config_path = Path(__file__).resolve().parents[1] / "config" / "skill_config.json"
        self.config_path = Path(config_path)
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict:
        """加载skill配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('global_skill', {})
        except FileNotFoundError:
            logger.warning(f"配置文件未找到: {self.config_path}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"配置文件解析失败: {e}")
            return {}

    def calculate_state_update(
        self,
        current_state: Dict,
        user_input: str,
        agent_response: Optional[str] = None
    ) -> PatientStateUpdate:
        """
        计算状态更新

        根据用户输入和配置规则，计算各项指标的变化

        Args:
            current_state: 当前状态字典
            user_input: 护士/用户输入
            agent_response: 患者回复（可选，用于更精确的判断）

        Returns:
            PatientStateUpdate对象
        """
        update = PatientStateUpdate(trigger="rule_engine")

        # 获取各项指标的变化规则
        update.mood_score_delta = self._calculate_indicator_delta(
            indicator="mood_score",
            user_input=user_input,
            current_value=current_state.get("mood_score", 50)
        )

        update.satisfaction_score_delta = self._calculate_indicator_delta(
            indicator="satisfaction_score",
            user_input=user_input,
            current_value=current_state.get("satisfaction_score", 50)
        )

        update.depression_level_delta = self._calculate_indicator_delta(
            indicator="depression_level",
            user_input=user_input,
            current_value=current_state.get("depression_level", 50)
        )

        update.rapport_score_delta = self._calculate_indicator_delta(
            indicator="rapport_score",
            user_input=user_input,
            current_value=current_state.get("rapport_score", 50)
        )

        return update

    def _calculate_indicator_delta(
        self,
        indicator: str,
        user_input: str,
        current_value: int
    ) -> Optional[int]:
        """
        计算单个指标的变化值

        Args:
            indicator: 指标名称
            user_input: 用户输入
            current_value: 当前值

        Returns:
            变化量（正数表示增加，负数表示减少）
        """
        indicator_rules = self.rules.get('indicator_rules', {}).get(indicator, {})
        change_rules = indicator_rules.get('change_rules', [])

        if not change_rules:
            return None

        # 遍历规则，计算匹配度
        total_delta = 0
        match_count = 0

        for rule in change_rules:
            delta, match = self._parse_and_match_rule(rule, user_input)
            if match:
                total_delta += delta
                match_count += 1

        # 如果有匹配的规则，返回平均值
        if match_count > 0:
            # 考虑当前值的边界效应
            avg_delta = total_delta / match_count

            # 边界衰减：接近极值时变化减缓
            if current_value < 20 and avg_delta < 0:
                avg_delta *= 0.5
            elif current_value > 80 and avg_delta > 0:
                avg_delta *= 0.5

            return int(round(avg_delta))

        return None

    def _parse_and_match_rule(self, rule: str, user_input: str) -> tuple:
        """
        解析并匹配规则

        规则格式: "描述 (+X~Y)" 或 "描述 (-X~-Y)"
        返回: (变化中值, 是否匹配)
        """
        # 解析规则
        match = re.search(r'([+-]?\d+)~([+-]?\d+)', rule)
        if not match:
            return (0, False)

        min_delta = int(match.group(1))
        max_delta = int(match.group(2))

        # 提取关键词（括号前的部分）
        keyword_part = rule.split('(')[0].strip()

        # 检查关键词是否在用户输入中
        # 这里使用简单的关键词匹配，可以扩展为更复杂的NLP分析
        is_match = self._check_keyword_match(keyword_part, user_input)

        if is_match:
            # 返回变化范围的中值
            avg_delta = (min_delta + max_delta) / 2
            return (avg_delta, True)

        return (0, False)

    def _check_keyword_match(self, keyword_part: str, user_input: str) -> bool:
        """
        检查关键词是否匹配（智能语义匹配）

        匹配策略：
        1. 从规则描述中提取关键词
        2. 检查用户输入的语义特征（长度、语气、句式）
        3. 使用多维特征判断，而非简单关键词匹配

        Args:
            keyword_part: 规则关键词部分（如"护士表现出同理心"）
            user_input: 用户输入

        Returns:
            是否匹配
        """
        user_input_lower = user_input.lower()
        user_input_stripped = user_input.strip()

        # ============== 积极行为规则匹配 ==============
        positive_patterns = {
            "同理心": ["理解", "明白", "懂", "感受", "不容易", "辛苦", "艰难"],
            "共情": ["和你", "一起", "陪", "不是你一个人", "我们都", "我来听"],
            "关心": ["担心", "注意", "观察", "最近", "怎么样", "还好吗", "还好吗"],
            "倾听": ["说说", "告诉我", "想听", "分享", "讲讲", "聊聊"],
            "支持": ["帮你", "支持", "陪着", "在一起", "不是一个人", "有我"],
            "鼓励": ["可以", "能行", "已经做得", "很棒", "很好", "进步"],
            "认同": ["是的", "对的", "没错", "确实", "就是这样"],
        }

        negative_patterns = {
            "说教": ["你应该", "你不应该", "必须", "一定要", "要知道", "你要明白"],
            "否定": ["不对", "不是", "没有", "别想", "不要", "不用"],
            "打断": ["好了", "行了", "算了", "别说", "停"],
            "评判": ["这样做不对", "你这样不行", "你应该", "不能这样"],
            "冷漠": ["哦", "嗯", "好吧", "随便", "无所谓"],
            "敷衍": ["好的", "知道了", "行吧", "嗯嗯"],
        }

        question_patterns = {
            "吗": user_input_stripped.endswith("吗") or user_input_stripped.endswith("?"),
            "呢": user_input_stripped.endswith("呢") or user_input_stripped.endswith("？"),
            "怎么": "怎么" in user_input_lower or "如何" in user_input_lower,
            "什么": "什么" in user_input,
            "为什么": "为什么" in user_input or "为啥" in user_input,
            "哪": "哪" in user_input,
        }

        # ============== 积极规则匹配 ==============
        for rule_name, keywords in positive_patterns.items():
            if rule_name in keyword_part:
                # 检查是否包含相关关键词
                for kw in keywords:
                    if kw in user_input:
                        return True
                # 特殊处理：如果是共情/理解类规则，检查输入长度和语气
                if rule_name in ["同理心", "共情", "关心", "倾听"]:
                    # 长文本且语气柔和，倾向于匹配
                    if len(user_input) > 20 and any(punct in user_input for punct in ["，", "。", "、", "…"]):
                        return True

        # ============== 消极规则匹配 ==============
        for rule_name, patterns in negative_patterns.items():
            if rule_name in keyword_part or any(n in keyword_part for n in ["否定", "忽视", "不耐烦"]):
                for pattern in patterns:
                    if pattern in user_input:
                        return True
                # 特殊处理：冷漠/敷衍规则，检查回复长度
                if rule_name in ["冷漠", "敷衍"]:
                    if len(user_input_stripped) <= 5:
                        return True

        # ============== 提问规则匹配 ==============
        if any(kw in keyword_part for kw in ["提问", "问"]):
            # 检查是否包含疑问词或问号
            for is_question in question_patterns.values():
                if is_question:
                    return True
            # 检查是否有疑问语气
            if len(user_input) > 5 and any(punct in user_input for punct in ["？", "?"]):
                return True

        # ============== 默认匹配：检查输入长度 ==============
        # 如果用户输入较长（>15字符），给予一定默认加分（表示在交流）
        if len(user_input_stripped) > 15:
            # 排除明显的负面输入
            negative_signs = ["傻鸟", "很菜", "不行", "笨", "蠢"]
            if not any(sign in user_input for sign in negative_signs):
                return True

        return False

    def get_crisis_thresholds(self) -> Dict[str, int]:
        """获取危机阈值配置"""
        return self.rules.get('cris_thresholds', {
            'mood_too_low': 15,
            'satisfaction_too_low': 10,
            'depression_too_high': 85,
            'rapport_broken': 10
        })

    def get_crisis_response(self, crisis_type: str) -> str:
        """
        获取危机响应模板

        Args:
            crisis_type: 危机类型

        Returns:
            危机响应文本
        """
        responses = self.rules.get('crisis_responses', {})

        response_map = {
            'mood_crisis': responses.get('extreme_low_mood', '（沉默不语）'),
            'satisfaction_crisis': responses.get('dissatisfaction', '你根本不理解我...'),
            'rapport_crisis': responses.get('rapport_broken', '...（低头不语）'),
            'depression_crisis': responses.get('severe_depression', '我觉得活着没什么意义...')
        }

        return response_map.get(crisis_type, '...')

    def get_tone_for_state(self, mood_score: int) -> str:
        """根据心情分数获取语气描述"""
        tone_mapping = self.rules.get('indicator_rules', {}).get('mood_score', {}).get('tone_mapping', {})

        if mood_score < 30:
            return tone_mapping.get('<30', '低落')
        elif mood_score < 50:
            return tone_mapping.get('30-50', '焦虑')
        elif mood_score < 70:
            return tone_mapping.get('50-70', '谨慎')
        else:
            return tone_mapping.get('>70', '开放')


# 创建全局实例
state_update_engine = StateUpdateEngine()
