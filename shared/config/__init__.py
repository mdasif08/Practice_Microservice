"""
Shared Configuration - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This package contains configuration management utilities.
"""

from .config_manager import (
    get_config,
    get_config_value,
    reload_config,
    update_config,
    create_default_config
)

__version__ = "1.0.0"
__all__ = [
    'get_config',
    'get_config_value',
    'reload_config',
    'update_config',
    'create_default_config'
]
