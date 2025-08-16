"""
Commit Tracker Service - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This package contains the core commit tracking functionality.
"""

from .commit_tracker import CommitTracker, GitRepositoryError, CommitExtractionError
from .git_parser import GitParser, GitCommandError
from .data_writer import DataWriter

__version__ = "1.0.0"
__all__ = [
    'CommitTracker',
    'GitRepositoryError', 
    'CommitExtractionError',
    'GitParser',
    'GitCommandError',
    'DataWriter'
]
