"""
日志工具
提供基础的日志初始化与获取方法。
"""
import logging
import os
from typing import Optional

from .config_manager import config


_LEVEL_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def setup_logging(level: Optional[str] = None) -> None:
    """
    初始化全局日志配置。

    Args:
        level: 日志级别，默认为从配置读取 advanced.log_level
    """
    if level is None:
        level = config.get_log_level() or os.getenv("LOG_LEVEL", "INFO")

    log_level = _LEVEL_MAP.get(str(level).upper(), logging.INFO)

    # 避免重复添加 handler
    root = logging.getLogger()
    if root.handlers:
        root.setLevel(log_level)
        return

    fmt = (
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    logging.basicConfig(level=log_level, format=fmt)


def get_logger(name: str) -> logging.Logger:
    """获取命名 logger"""
    return logging.getLogger(name)
