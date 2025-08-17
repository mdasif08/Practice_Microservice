"""
Commit Tracker Service - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This package contains the commit tracking microservice.
"""
<<<<<<< HEAD
<<<<<<< HEAD:services/commit_tracker_service/__init__.py
=======
>>>>>>> 0a842f6 (Frontend Implemented)

# Import and expose the main modules
try:
    from .src import commit_tracker, data_writer, git_parser
    from .src.commit_tracker import CommitTracker
    from .src.data_writer import DataWriter
    from .src.git_parser import GitParser, GitCommandError
    
    __all__ = [
        'commit_tracker',
        'data_writer', 
        'git_parser',
        'CommitTracker',
        'DataWriter',
        'GitParser',
        'GitCommandError'
    ]
except ImportError:
    # Handle case where modules might not be available
    __all__ = []
<<<<<<< HEAD
=======
>>>>>>> fcfbf36 (Actual Code Implementation):services/commit-tracker-service/__init__.py
=======
>>>>>>> 0a842f6 (Frontend Implemented)
