"""
Shared Components - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This package contains shared components used across all services.
"""

# Import and expose the main modules
try:
    from . import utils, config
    from .utils import logger, error_handler
    from .config import config_manager
    
    __all__ = [
        'utils',
        'config',
        'logger',
        'error_handler',
        'config_manager'
    ]
except ImportError:
    # Handle case where modules might not be available
    __all__ = []
