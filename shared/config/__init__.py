"""
Shared Configuration - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This package contains shared configuration management.
"""

# Import and expose the main modules
try:
    from . import config_manager
    from .config_manager import ConfigManager
    
    __all__ = [
        'config_manager',
        'ConfigManager'
    ]
except ImportError:
    # Handle case where modules might not be available
    __all__ = []
