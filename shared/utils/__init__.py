"""
Shared Utilities - User Story 2.1.1: Behavior Tracker – Git Commit Logger

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
