"""
共享核心模块
引用原有 core 模块
"""
from backend.app.core.config import settings
from backend.app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from backend.app.core.proxy import setup_proxy, get_proxies

__all__ = [
    "settings",
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "decode_access_token",
    "setup_proxy",
    "get_proxies"
]
