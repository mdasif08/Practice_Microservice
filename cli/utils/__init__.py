"""
CLI Utilities - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This package contains utility functions for CLI functionality.
"""

from .cli_helpers import (
    format_commit_message,
    validate_repository_path,
    get_repository_status,
    format_timestamp,
    calculate_commit_stats,
    export_commits_to_format,
    interactive_commit_selection,
    setup_logging_for_cli,
    display_progress_bar,
    confirm_action,
    get_user_input
)

__version__ = "1.0.0"
__all__ = [
    'format_commit_message',
    'validate_repository_path',
    'get_repository_status',
    'format_timestamp',
    'calculate_commit_stats',
    'export_commits_to_format',
    'interactive_commit_selection',
    'setup_logging_for_cli',
    'display_progress_bar',
    'confirm_action',
    'get_user_input'
]
