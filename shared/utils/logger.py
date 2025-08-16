"""
Shared Logger Utility - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This module provides consistent logging functionality across all services.
"""

import os
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path
import logging
from loguru import logger

# Remove default loguru handler
logger.remove()


def setup_logger(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
) -> None:
    """
    Setup the logger with console and optional file handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        log_format: Log message format
    """
    # Add console handler
    logger.add(
        sys.stderr,
        format=log_format,
        level=log_level,
        colorize=True
    )
    
    # Add file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_file,
            format=log_format,
            level=log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip"
        )
    
    # Set loguru as the default logger
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(InterceptHandler())


def get_logger(name: str) -> logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


class InterceptHandler(logging.Handler):
    """
    Intercept standard logging and redirect to loguru.
    """
    
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# Initialize default logger
setup_logger()

__all__ = ['logger', 'get_logger', 'setup_logger']
