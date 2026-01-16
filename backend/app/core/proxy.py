"""
Proxy Configuration
代理配置工具模块
"""
import os
from .config import settings


def setup_proxy():
    """设置系统代理"""
    if settings.HTTP_PROXY:
        os.environ["http_proxy"] = settings.HTTP_PROXY
        os.environ["HTTP_PROXY"] = settings.HTTP_PROXY
        print(f"✅ HTTP代理已设置: {settings.HTTP_PROXY}")

    if settings.HTTPS_PROXY:
        os.environ["https_proxy"] = settings.HTTPS_PROXY
        os.environ["HTTPS_PROXY"] = settings.HTTPS_PROXY
        print(f"✅ HTTPS代理已设置: {settings.HTTPS_PROXY}")

    if not settings.HTTP_PROXY and not settings.HTTPS_PROXY:
        print("ℹ️  未配置代理，将使用直连")


def get_proxies() -> dict:
    """获取代理配置字典"""
    proxies = {}
    if settings.HTTP_PROXY:
        proxies["http://"] = settings.HTTP_PROXY
    if settings.HTTPS_PROXY:
        proxies["https://"] = settings.HTTPS_PROXY
    return proxies


# 应用启动时自动设置代理
setup_proxy()
