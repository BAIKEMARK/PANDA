"""
AI 服务统一接口
封装所有 AI 调用，为业务模块提供统一的 AI 访问接口
"""
import httpx
from typing import List, Dict, Optional
from backend.app.core.config import settings


class AIService:
    """AI 服务统一接口 - 单例模式"""

    _instance: Optional['AIService'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化 AI 服务"""
        self.api_key = settings.AI_TEXT_KEY
        self.model = settings.AI_TEXT_MODEL
        self.url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    def generate_conversation_response(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: List[Dict],
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """
        生成对话回复

        Args:
            system_prompt: 系统提示词
            user_message: 用户最新消息
            conversation_history: 对话历史 [{role: "user/assistant", content: "..."}]
            max_tokens: 最大token数
            temperature: 温度参数

        Returns:
            AI 生成的回复文本
        """
        if not self.api_key:
            return "抱歉，AI服务未配置。请联系管理员配置AI_TEXT_KEY。"

        # 构建消息列表
        messages = []

        # 添加系统提示
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # 添加历史对话
        messages.extend(conversation_history)

        # 添加最新用户消息
        messages.append({"role": "user", "content": user_message})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": self.model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        }

        try:
            print(f"📡 正在调用 AI API...")
            print(f"   模型: {self.model}")

            timeout_config = httpx.Timeout(
                connect=10.0,
                read=120.0,
                write=30.0,
                pool=30.0
            )

            with httpx.Client(timeout=timeout_config) as client:
                response = client.post(
                    self.url,
                    headers=headers,
                    json=body
                )

            if response.status_code == 200:
                data = response.json()

                # 尝试多种可能的响应格式
                if "output" in data and "choices" in data["output"] and len(data["output"]["choices"]) > 0:
                    result = data["output"]["choices"][0]["message"]["content"].strip()
                    return result
                elif "output" in data and "text" in data["output"]:
                    result = data["output"]["text"].strip()
                    return result
                elif "choices" in data and len(data["choices"]) > 0:
                    result = data["choices"][0]["message"]["content"].strip()
                    return result
                else:
                    return f"AI生成回复格式错误。响应数据: {str(data)[:200]}"

            else:
                return f"AI调用失败: HTTP {response.status_code}"

        except Exception as e:
            raise Exception(f"AI调用异常: {type(e).__name__} - {str(e)}")

    def generate_evaluation_report(
        self,
        conversation_text: str,
        evaluation_criteria: Dict,
        max_retries: int = 2
    ) -> Dict:
        """
        生成评估报告

        Args:
            conversation_text: 对话历史文本
            evaluation_criteria: 评估标准
            max_retries: 最大重试次数

        Returns:
            评估报告字典
        """
        # 构建 prompt
        prompt = f"""
你是一位围产期抑郁护理培训专家导师。请基于以下信息，对护士的对话表现进行专业评估。

# 评分标准 (THP五维评分法)
{evaluation_criteria}

# 对话历史
{conversation_text}

# 任务要求
请以JSON格式返回评估报告。请直接返回JSON，不要有其他说明文字。
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": self.model,
            "input": {
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "max_tokens": 3000,
                "temperature": 0.7
            }
        }

        # 重试逻辑
        for attempt in range(max_retries + 1):
            try:
                print(f"📡 正在调用 AI 评估生成 (尝试 {attempt + 1}/{max_retries + 1})...")

                timeout_config = httpx.Timeout(
                    connect=10.0,
                    read=360.0,
                    write=30.0,
                    pool=30.0
                )

                with httpx.Client(timeout=timeout_config) as client:
                    response = client.post(
                        self.url,
                        headers=headers,
                        json=body
                    )

                if response.status_code == 200:
                    data = response.json()

                    # 尝试多种可能的响应格式
                    result_text = ""
                    if "output" in data and "choices" in data["output"] and len(data["output"]["choices"]) > 0:
                        result_text = data["output"]["choices"][0]["message"]["content"].strip()
                    elif "output" in data and "text" in data["output"]:
                        result_text = data["output"]["text"].strip()
                    elif "choices" in data and len(data["choices"]) > 0:
                        result_text = data["choices"][0]["message"]["content"].strip()

                    # 解析 JSON
                    import json
                    try:
                        return json.loads(result_text)
                    except json.JSONDecodeError:
                        # 尝试提取 JSON 部分
                        start_idx = result_text.find('{')
                        end_idx = result_text.rfind('}') + 1
                        if start_idx != -1 and end_idx > start_idx:
                            json_str = result_text[start_idx:end_idx]
                            return json.loads(json_str)
                        else:
                            raise ValueError("无法找到有效的JSON内容")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text[:500]}")

            except Exception as e:
                if attempt < max_retries:
                    print(f"⚠️ AI评估调用异常，准备重试: {type(e).__name__} - {str(e)}")
                    continue
                else:
                    raise Exception(f"AI评估生成失败（已重试 {max_retries} 次）: {type(e).__name__} - {str(e)}")


# 创建全局实例
ai_service = AIService()
