"""
CraftNudge AI Agent - User Story 2.1.1: Behavior Tracker – Git Commit Logger

An AI Native Agent for tracking and analyzing developer behavior patterns.

This package implements User Story 2.1.1: Behavior Tracker – Git Commit Logger,
which provides functionality to log every Git commit with metadata for
behavioral analysis and pattern recognition.
"""

__version__ = "1.0.0"
__author__ = "CraftNudge Team"
__description__ = "AI Native Agent for Developer Behavior Analysis"

# Import main components for easy access
from services.commit_tracker_service.src.commit_tracker import CommitTracker
from shared.utils.logger import get_logger, setup_logger
from shared.config.config_manager import get_config

__all__ = [
    'CommitTracker',
    'get_logger',
    'setup_logger',
    'get_config'
]
