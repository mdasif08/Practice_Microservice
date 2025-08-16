"""
Shared Utilities - User Story 2.1.1: Behavior Tracker – Git Commit Logger

<<<<<<< HEAD
This package contains shared utility functions and classes.
"""

# Import and expose the main modules
try:
    from . import logger, error_handler
    from .logger import Logger
    from .error_handler import ErrorHandler, CraftNudgeError
    
    __all__ = [
        'logger',
        'error_handler',
        'Logger',
        'ErrorHandler',
        'CraftNudgeError'
    ]
except ImportError:
    # Handle case where modules might not be available
    __all__ = []
=======
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
>>>>>>> fcfbf36 (Actual Code Implementation)
