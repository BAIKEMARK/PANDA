"""
LangChain 统一管理器
负责 LLM 实例化、配置管理和生命周期

使用单例模式确保全局只有一个 LLM 实例
"""
from typing import Optional
import httpx
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from backend.app.config.config import settings


def _create_httpx_client():
    """创建不使用代理的 httpx 客户端"""
    return httpx.Client(
        proxies=None,
        timeout=httpx.Timeout(
            connect=10.0,
            read=120.0,
            write=30.0,
            pool=30.0
        ),
        verify=True
    )


class LangChainManager:
    """LangChain 管理器 - 单例模式"""

    _instance: Optional['LangChainManager'] = None
    _llm: Optional[BaseChatModel] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化 LangChain 管理"""
        if self._llm is None:
            self._initialize_llm()

    def _initialize_llm(self):
        """初始化 LLM 实例"""
        if not settings.AI_TEXT_KEY:
            raise ValueError("AI_TEXT_KEY 未配置，请先配置 API Key")

        # 创建自定义 httpx 客户端（不使用代理）
        http_client = _create_httpx_client()

        try:
            # LLM（使用通义千问兼容模式）
            self._llm = ChatOpenAI(
                base_url=settings.AI_TEXT_URL,
                api_key=settings.AI_TEXT_KEY,
                model=settings.AI_TEXT_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                timeout=settings.LLM_TIMEOUT,
                max_retries=settings.LLM_MAX_RETRIES,
                http_client=http_client,
                verbose=True,  # 启用详细日志，打印完整的 API 请求和响应
            )
            print(f"[OK] LangChain LLM初始化: {settings.AI_TEXT_MODEL}")
        except Exception as e:
            print(f"[ERROR] LLM初始化失败: {e}")
            raise

    def get_llm(self) -> BaseChatModel:
        """获取 LLM 实例"""
        return self._llm

    def get_model_info(self) -> dict:
        """获取模型信息"""
        return {
            "model": settings.AI_TEXT_MODEL,
            "base_url": settings.AI_TEXT_URL,
            "temperature": settings.LLM_TEMPERATURE,
            "max_retries": settings.LLM_MAX_RETRIES,
            "streaming": settings.LLM_STREAMING,
        }


# 创建全局实例
langchain_manager = LangChainManager()
