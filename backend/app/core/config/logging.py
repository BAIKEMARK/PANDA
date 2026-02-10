"""
统一日志配置模块

提供可配置的日志功能，支持：
- 动态日志级别调整
- 多种日志格式（text/json）
- 文件和控制台输出
- 按大小切割日志，文件命名包含日期
"""
import logging
import sys
import os
import glob
from pathlib import Path
from typing import Optional
from datetime import datetime

from backend.app.core.config.settings import settings


class ColoredFormatter(logging.Formatter):
    """带颜色的控制台日志格式化器"""

    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',      # 青色
        'INFO': '\033[32m',       # 绿色
        'WARNING': '\033[33m',    # 黄色
        'ERROR': '\033[31m',      # 红色
        'CRITICAL': '\033[35m',   # 紫色
    }
    RESET = '\033[0m'

    def format(self, record):
        # 添加颜色
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"

        # 调用父类格式化
        result = super().format(record)

        # 恢复原始levelname（避免影响其他handler）
        record.levelname = levelname

        return result


class SizedRotatingFileHandler(logging.Handler):
    """
    自定义日志文件处理器

    - 所有日志文件都使用 app.YYYY-MM-DD_N.log 格式
    - 当文件超过指定大小时自动切换到下一个序号
    - 自动清理超过保留天数的旧日志
    - 不存在 app.log 文件
    """

    def __init__(self, log_dir, maxBytes=1024*1024, backupDays=30, encoding=None):
        """
        初始化

        Args:
            log_dir: 日志目录
            maxBytes: 单文件最大大小（默认1MB）
            backupDays: 日志保留天数
            encoding: 编码
        """
        super().__init__()
        self.maxBytes = maxBytes
        self.backupDays = backupDays
        self.log_dir = log_dir
        self.encoding = encoding or 'utf-8'

        # 当前日志文件名和序号
        self.current_date = None
        self.current_index = 1
        self.current_filename = None
        self.stream = None

        # 初始化当前日志文件
        self._init_current_file()

    def _init_current_file(self):
        """初始化当前日志文件"""
        today = datetime.now().strftime("%Y-%m-%d")

        # 查找今天已有的日志文件
        pattern = os.path.join(self.log_dir, f"app.{today}_*.log")
        existing_files = glob.glob(pattern)

        if existing_files:
            # 提取序号，找到最大的
            indices = []
            for f in existing_files:
                try:
                    basename = os.path.basename(f)
                    idx = int(basename.split('_')[-1].replace('.log', ''))
                    indices.append(idx)
                except (ValueError, IndexError):
                    pass
            self.current_index = max(indices) + 1 if indices else 1
        else:
            self.current_index = 1

        self.current_date = today
        self.current_filename = os.path.join(self.log_dir, f"app.{today}_{self.current_index}.log")

        # 确保目录存在
        os.makedirs(self.log_dir, exist_ok=True)

        # 打开文件
        self.stream = open(self.current_filename, 'a', encoding=self.encoding)

    def emit(self, record):
        """写入日志记录"""
        try:
            # 检查是否需要切换日期
            today = datetime.now().strftime("%Y-%m-%d")
            if today != self.current_date:
                # 日期变更，关闭当前文件，创建新文件
                if self.stream:
                    self.stream.close()
                self._cleanup_old_logs()
                self._init_current_file()

            # 检查文件大小，如果超过限制则切换文件
            if self.stream and self.stream.tell() >= self.maxBytes:
                self._rotate_file()

            # 写入日志
            msg = self.format(record)
            self.stream.write(msg + '\n')
            self.stream.flush()
        except Exception:
            self.handleError(record)

    def _rotate_file(self):
        """切换到下一个日志文件"""
        if self.stream:
            self.stream.close()

        # 序号递增
        self.current_index += 1
        self.current_filename = os.path.join(self.log_dir, f"app.{self.current_date}_{self.current_index}.log")

        # 打开新文件
        self.stream = open(self.current_filename, 'a', encoding=self.encoding)

    def _cleanup_old_logs(self):
        """清理超过保留天数的日志文件"""
        try:
            from datetime import timedelta

            cutoff_date = datetime.now() - timedelta(days=self.backupDays)
            cutoff_str = cutoff_date.strftime("%Y-%m-%d")

            # 查找所有归档日志
            pattern = os.path.join(self.log_dir, "app.2*.log")
            for logfile in glob.glob(pattern):
                basename = os.path.basename(logfile)
                # 提取日期部分
                try:
                    # 文件名格式：app.YYYY-MM-DD.log 或 app.YYYY-MM-DD_N.log
                    date_part = basename.split('.')[1]  # YYYY-MM-DD 或 YYYY-MM-DD_N
                    if '_' in date_part:
                        date_part = date_part.split('_')[0]  # 去掉序号部分

                    if date_part < cutoff_str:
                        os.remove(logfile)
                except (ValueError, IndexError):
                    pass
        except Exception as e:
            # 清理失败不影响日志写入
            pass


def setup_logging(
    log_level: Optional[str] = None,
    log_dir: Optional[str] = None,
    log_format: str = "text"
) -> None:
    """
    配置应用日志系统

    支持按文件大小切割的日志文件，文件命名包含日期信息。

    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: 日志目录路径 (None则使用配置中的 LOG_DIR)
        log_format: 日志格式 (text, json)

    日志文件命名规则：
        - 所有日志: logs/app.2024-01-15_1.log
        - 超过大小后: logs/app.2024-01-15_2.log
        - 第二天: logs/app.2024-01-16_1.log
        - 不存在 app.log 文件
    """
    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # 设置最低级别，由handler控制

    # 清除现有handlers
    root_logger.handlers.clear()

    # 确定日志级别
    level = log_level or settings.LOG_LEVEL
    log_level_int = getattr(logging, level.upper(), logging.INFO)

    # 确定日志目录
    log_dir = log_dir or settings.LOG_DIR

    # 定义格式
    if log_format == "json":
        # JSON格式（用于日志分析）
        formatter = logging.Formatter(
            '{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s","path":"%(pathname)s:%(lineno)d"}',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
    else:
        # 文本格式（人类可读）
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)8s] [%(name)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # 控制台Handler
    if settings.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level_int)
        # 控制台使用彩色格式
        console_formatter = ColoredFormatter(
            '[%(asctime)s] [%(levelname)8s] [%(name)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

    # 文件Handler - 使用自定义的大小轮转
    # 确保目录存在
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # 创建自定义的文件handler：从配置读取单文件最大大小（KB）
    file_handler = SizedRotatingFileHandler(
        log_dir=str(log_path),
        maxBytes=settings.LOG_MAX_BYTES_KB * 1024,  # KB转换为字节
        backupDays=settings.LOG_BACKUP_DAYS,  # 保留天数
        encoding='utf-8',
    )

    file_handler.setLevel(log_level_int)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器

    Args:
        name: 日志记录器名称（通常使用 __name__）

    Returns:
        配置好的日志记录器
    """
    return logging.getLogger(name)


def set_log_level(level: str) -> None:
    """
    动态设置日志级别

    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    log_level_int = getattr(logging, level.upper(), logging.INFO)
    logging.getLogger().setLevel(log_level_int)

    # 同时设置所有handler的级别
    for handler in logging.getLogger().handlers:
        handler.setLevel(log_level_int)
