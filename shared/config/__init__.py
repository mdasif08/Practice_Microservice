"""
Shared Configuration - User Story 2.1.1: Behavior Tracker – Git Commit Logger

<<<<<<< HEAD
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
=======
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
>>>>>>> fcfbf36 (Actual Code Implementation)
