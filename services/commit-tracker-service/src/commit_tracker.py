"""
Commit Tracker Module - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This module logs every Git commit with metadata including hash, author, message, 
timestamp, and changed files for behavioral analysis.
"""

import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import uuid

from .git_parser import GitParser
from .data_writer import DataWriter
from ...shared.utils.logger import get_logger
from ...shared.utils.error_handler import handle_error

logger = get_logger(__name__)


class CommitTracker:
    """
    Main commit tracking service that orchestrates Git commit logging.
    
    Responsibilities:
    - Detect Git repository
    - Extract commit metadata
    - Log commits to data store
    - Handle errors gracefully
    """
    
    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize the commit tracker.
        
        Args:
            repo_path: Path to Git repository (defaults to current directory)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.git_parser = GitParser(self.repo_path)
        self.data_writer = DataWriter()
        
    def log_latest_commit(self) -> Dict[str, Any]:
        """
        Log the most recent Git commit with full metadata.
        
        Returns:
            Dict containing commit data and status
            
        Raises:
            GitRepositoryError: If not in a Git repository
            CommitExtractionError: If commit data cannot be extracted
        """
        try:
            logger.info(f"Starting commit logging for repository: {self.repo_path}")
            
            # Validate Git repository
            if not self.git_parser.is_git_repository():
                error_msg = f"No Git repository found at: {self.repo_path}"
                logger.error(error_msg)
                raise GitRepositoryError(error_msg)
            
            # Extract latest commit data
            commit_data = self.git_parser.get_latest_commit()
            
            # Generate unique ID and timestamp
            commit_data['id'] = str(uuid.uuid4())
            commit_data['timestamp'] = datetime.now(timezone.utc).isoformat()
            
            # Validate commit data
            self._validate_commit_data(commit_data)
            
            # Write to data store
            self.data_writer.write_commit(commit_data)
            
            logger.info(f"Successfully logged commit: {commit_data['hash'][:8]}")
            
            return {
                'status': 'success',
                'commit_data': commit_data,
                'message': f"Commit {commit_data['hash'][:8]} logged successfully"
            }
            
        except Exception as e:
            error_result = handle_error(e, "commit_tracker.log_latest_commit")
            logger.error(f"Failed to log commit: {error_result['error']}")
            return error_result
    
    def log_commit_by_hash(self, commit_hash: str) -> Dict[str, Any]:
        """
        Log a specific commit by its hash.
        
        Args:
            commit_hash: Git commit hash to log
            
        Returns:
            Dict containing commit data and status
        """
        try:
            logger.info(f"Logging specific commit: {commit_hash}")
            
            if not self.git_parser.is_git_repository():
                error_msg = f"No Git repository found at: {self.repo_path}"
                logger.error(error_msg)
                raise GitRepositoryError(error_msg)
            
            # Extract specific commit data
            commit_data = self.git_parser.get_commit_by_hash(commit_hash)
            
            # Generate unique ID and timestamp
            commit_data['id'] = str(uuid.uuid4())
            commit_data['timestamp'] = datetime.now(timezone.utc).isoformat()
            
            # Validate commit data
            self._validate_commit_data(commit_data)
            
            # Write to data store
            self.data_writer.write_commit(commit_data)
            
            logger.info(f"Successfully logged commit: {commit_data['hash'][:8]}")
            
            return {
                'status': 'success',
                'commit_data': commit_data,
                'message': f"Commit {commit_data['hash'][:8]} logged successfully"
            }
            
        except Exception as e:
            error_result = handle_error(e, "commit_tracker.log_commit_by_hash")
            logger.error(f"Failed to log commit {commit_hash}: {error_result['error']}")
            return error_result
    
    def _validate_commit_data(self, commit_data: Dict[str, Any]) -> None:
        """
        Validate that commit data contains all required fields.
        
        Args:
            commit_data: Commit data to validate
            
        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ['hash', 'author', 'message', 'timestamp', 'changed_files']
        
        for field in required_fields:
            if field not in commit_data or commit_data[field] is None:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate hash format (should be 40 characters for full hash)
        if len(commit_data['hash']) < 7:
            raise ValueError("Invalid commit hash format")
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(commit_data['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("Invalid timestamp format")
    
    def get_repository_info(self) -> Dict[str, Any]:
        """
        Get information about the current Git repository.
        
        Returns:
            Dict containing repository information
        """
        try:
            if not self.git_parser.is_git_repository():
                return {
                    'status': 'error',
                    'message': f"No Git repository found at: {self.repo_path}",
                    'repository_info': None
                }
            
            repo_info = self.git_parser.get_repository_info()
            
            return {
                'status': 'success',
                'repository_info': repo_info,
                'message': 'Repository information retrieved successfully'
            }
            
        except Exception as e:
            error_result = handle_error(e, "commit_tracker.get_repository_info")
            logger.error(f"Failed to get repository info: {error_result['error']}")
            return error_result


class GitRepositoryError(Exception):
    """Raised when no Git repository is found."""
    pass


class CommitExtractionError(Exception):
    """Raised when commit data cannot be extracted."""
    pass


if __name__ == "__main__":
    # CLI entry point for testing
    tracker = CommitTracker()
    result = tracker.log_latest_commit()
    print(json.dumps(result, indent=2))
