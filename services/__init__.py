"""
Services - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This package contains all microservices for the CraftNudge AI Agent.
"""

# Import and expose the commit tracker service
try:
    from . import commit_tracker_service
    __all__ = ['commit_tracker_service']
except ImportError:
    # Handle case where the service might not be available
    __all__ = []
