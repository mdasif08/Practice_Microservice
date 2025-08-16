"""
Shared Utilities - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This package contains shared utilities used across all services.
"""

from .logger import get_logger, setup_logger
from .error_handler import (
    CraftNudgeError,
    GitRepositoryError,
    DataStoreError,
    ValidationError,
    ConfigurationError,
    handle_error,
    validate_required_fields,
    validate_field_type,
    safe_execute,
    retry_on_error
)

__version__ = "1.0.0"
__all__ = [
    'get_logger',
    'setup_logger',
    'CraftNudgeError',
    'GitRepositoryError',
    'DataStoreError',
    'ValidationError',
    'ConfigurationError',
    'handle_error',
    'validate_required_fields',
    'validate_field_type',
    'safe_execute',
    'retry_on_error'
]
