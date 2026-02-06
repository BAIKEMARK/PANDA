"""
Core Configuration Module
配置管理模块 - 使用 pydantic-settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
from pathlib import Path
import os


class Settings(BaseSettings):
    """应用配置类"""

    # ==================== 应用基础配置 ====================
    APP_NAME: str = "PANDA - 围产期抑郁管理智能培训系统"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    APP_DESCRIPTION: str = "基于THP的围产期抑郁管理智能培训系统"

    # ==================== 数据库配置 ====================
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "test0000"
    DB_NAME: str = "panda"
    DB_CHARSET: str = "utf8mb4"

    @property
    def DATABASE_URL(self) -> str:
        """获取数据库连接URL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"

    # ==================== JWT认证配置 ====================
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # ==================== AI模型配置 ====================
    AI_TEXT_URL: Optional[str] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    AI_TEXT_KEY: Optional[str] = "sk-*******************"
    AI_TEXT_MODEL: str = "qwen-max"
    AI_TIMEOUT: int = 30

    # ==================== LLM 高级配置 ====================
    LLM_MAX_RETRIES: int = 3
    LLM_TIMEOUT: int = 120
    LLM_TEMPERATURE: float = 0.7
    LLM_STREAMING: bool = False

    # ==================== Redis配置 ====================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DECODE_RESPONSES: bool = True
    REDIS_SOCKET_CONNECT_TIMEOUT: int = 5
    REDIS_SOCKET_TIMEOUT: int = 5
    REDIS_MAX_CONNECTIONS: int = 50

    @property
    def REDIS_URL(self) -> str:
        """获取Redis连接URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # ==================== CORS配置 ====================
    CORS_ORIGINS_STR: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174,http://localhost:5175,http://127.0.0.1:5175"

    @property
    def CORS_ORIGINS(self) -> List[str]:
        """将CORS_ORIGINS_STR解析为列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(",")]

    # ==================== Pydantic配置 ====================
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


def _find_env_file() -> str:
    """
    查找 .env 文件，支持多个位置
    优先级: backend/.env > backend/app/.env > .env
    """
    # 获取当前文件的目录 (backend/app/core/)
    current_dir = Path(__file__).parent.absolute()

    # 可能的 .env 文件位置
    possible_locations = [
        current_dir.parent.parent / ".env",  # backend/.env
        current_dir.parent / ".env",         # backend/app/.env
        Path(".env"),                         # 当前工作目录
    ]

    for location in possible_locations:
        if location.exists():
            print(f"[OK] 找到 .env 文件: {location}")
            return str(location)

    print("[WARN] 未找到 .env 文件，使用默认配置")
    return ".env"


# 创建全局配置实例
settings = Settings(_env_file=_find_env_file())
