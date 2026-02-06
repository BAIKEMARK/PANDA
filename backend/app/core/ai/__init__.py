"""
LangChain AI 基础设施
提供 LLM 管理功能
"""

# 从 langchain_manager 导出
try:
    from backend.app.core.ai.langchain_manager import langchain_manager, LangChainManager

    __all__ = [
        "langchain_manager",
        "LangChainManager",
    ]
except ImportError:
    # 如果导入失败（比如在测试环境），导出为空
    __all__ = []
