"""
Data Writer Module - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This module handles writing commit data to the local data store in JSONL format.
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pathlib import Path
import jsonlines

from ...shared.utils.logger import get_logger
from ...shared.utils.error_handler import handle_error
from ...shared.config.config_manager import get_config

logger = get_logger(__name__)


class DataWriter:
    """
    Data writer for storing commit information in JSONL format.
    
    Responsibilities:
    - Write commit data to JSONL files
    - Ensure data integrity
    - Handle file operations safely
    - Maintain data store structure
    """
    
    def __init__(self, data_store_path: Optional[str] = None):
        """
        Initialize data writer.
        
        Args:
            data_store_path: Path to data store directory
        """
        config = get_config()
        self.data_store_path = Path(data_store_path) if data_store_path else Path(config['data_store']['base_path'])
        self.commits_file = self.data_store_path / 'behaviors' / 'commits.jsonl'
        
        # Ensure data store directory exists
        self._ensure_data_store_exists()
        
    def write_commit(self, commit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Write commit data to the JSONL file.
        
        Args:
            commit_data: Commit data to write
            
        Returns:
            Dict containing write operation result
        """
        try:
            logger.info(f"Writing commit data: {commit_data.get('hash', 'unknown')[:8]}")
            
            # Validate commit data
            self._validate_commit_data(commit_data)
            
            # Ensure file exists
            self._ensure_commits_file_exists()
            
            # Write to JSONL file
            with jsonlines.open(self.commits_file, mode='a') as writer:
                writer.write(commit_data)
            
            logger.info(f"Successfully wrote commit to: {self.commits_file}")
            
            return {
                'status': 'success',
                'file_path': str(self.commits_file),
                'message': f"Commit {commit_data.get('hash', 'unknown')[:8]} written successfully"
            }
            
        except Exception as e:
            error_result = handle_error(e, "data_writer.write_commit")
            logger.error(f"Failed to write commit data: {error_result['error']}")
            return error_result
    
    def read_commits(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Read commit data from the JSONL file.
        
        Args:
            limit: Maximum number of commits to read (None for all)
            
        Returns:
            Dict containing commit data and status
        """
        try:
            if not self.commits_file.exists():
                return {
                    'status': 'success',
                    'commits': [],
                    'message': 'No commits file found'
                }
            
            commits = []
            with jsonlines.open(self.commits_file, mode='r') as reader:
                for commit in reader:
                    commits.append(commit)
                    if limit and len(commits) >= limit:
                        break
            
            # Reverse to get most recent first
            commits.reverse()
            
            return {
                'status': 'success',
                'commits': commits,
                'message': f"Read {len(commits)} commits successfully"
            }
            
        except Exception as e:
            error_result = handle_error(e, "data_writer.read_commits")
            logger.error(f"Failed to read commits: {error_result['error']}")
            return error_result
    
    def get_commit_count(self) -> Dict[str, Any]:
        """
        Get the total number of commits in the data store.
        
        Returns:
            Dict containing commit count and status
        """
        try:
            if not self.commits_file.exists():
                return {
                    'status': 'success',
                    'count': 0,
                    'message': 'No commits file found'
                }
            
            count = 0
            with jsonlines.open(self.commits_file, mode='r') as reader:
                for _ in reader:
                    count += 1
            
            return {
                'status': 'success',
                'count': count,
                'message': f"Total commits: {count}"
            }
            
        except Exception as e:
            error_result = handle_error(e, "data_writer.get_commit_count")
            logger.error(f"Failed to get commit count: {error_result['error']}")
            return error_result
    
    def search_commits(self, search_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search commits based on criteria.
        
        Args:
            search_criteria: Dictionary of search criteria
                - author: Author name or email
                - message: Commit message keywords
                - date_from: Start date (ISO format)
                - date_to: End date (ISO format)
                - files: Changed files keywords
            
        Returns:
            Dict containing matching commits and status
        """
        try:
            if not self.commits_file.exists():
                return {
                    'status': 'success',
                    'commits': [],
                    'message': 'No commits file found'
                }
            
            matching_commits = []
            
            with jsonlines.open(self.commits_file, mode='r') as reader:
                for commit in reader:
                    if self._matches_criteria(commit, search_criteria):
                        matching_commits.append(commit)
            
            # Reverse to get most recent first
            matching_commits.reverse()
            
            return {
                'status': 'success',
                'commits': matching_commits,
                'message': f"Found {len(matching_commits)} matching commits"
            }
            
        except Exception as e:
            error_result = handle_error(e, "data_writer.search_commits")
            logger.error(f"Failed to search commits: {error_result['error']}")
            return error_result
    
    def _validate_commit_data(self, commit_data: Dict[str, Any]) -> None:
        """
        Validate commit data before writing.
        
        Args:
            commit_data: Commit data to validate
            
        Raises:
            ValueError: If data is invalid
        """
        required_fields = ['id', 'hash', 'author', 'message', 'timestamp', 'changed_files']
        
        for field in required_fields:
            if field not in commit_data:
                raise ValueError(f"Missing required field: {field}")
            
            if commit_data[field] is None:
                raise ValueError(f"Field {field} cannot be None")
        
        # Validate ID format (should be UUID)
        if not isinstance(commit_data['id'], str) or len(commit_data['id']) != 36:
            raise ValueError("Invalid ID format (should be UUID)")
        
        # Validate hash format
        if not isinstance(commit_data['hash'], str) or len(commit_data['hash']) < 7:
            raise ValueError("Invalid commit hash format")
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(commit_data['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("Invalid timestamp format")
        
        # Validate changed_files is a list
        if not isinstance(commit_data['changed_files'], list):
            raise ValueError("changed_files must be a list")
    
    def _matches_criteria(self, commit: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """
        Check if a commit matches the search criteria.
        
        Args:
            commit: Commit data to check
            criteria: Search criteria
            
        Returns:
            True if commit matches criteria, False otherwise
        """
        # Author search
        if 'author' in criteria and criteria['author']:
            author_match = (
                criteria['author'].lower() in commit.get('author', '').lower() or
                criteria['author'].lower() in commit.get('author_email', '').lower()
            )
            if not author_match:
                return False
        
        # Message search
        if 'message' in criteria and criteria['message']:
            message_match = criteria['message'].lower() in commit.get('message', '').lower()
            if not message_match:
                return False
        
        # Date range search
        if 'date_from' in criteria and criteria['date_from']:
            try:
                commit_date = datetime.fromisoformat(commit.get('commit_date', '').replace('Z', '+00:00'))
                from_date = datetime.fromisoformat(criteria['date_from'].replace('Z', '+00:00'))
                if commit_date < from_date:
                    return False
            except ValueError:
                pass
        
        if 'date_to' in criteria and criteria['date_to']:
            try:
                commit_date = datetime.fromisoformat(commit.get('commit_date', '').replace('Z', '+00:00'))
                to_date = datetime.fromisoformat(criteria['date_to'].replace('Z', '+00:00'))
                if commit_date > to_date:
                    return False
            except ValueError:
                pass
        
        # Files search
        if 'files' in criteria and criteria['files']:
            files_match = any(
                criteria['files'].lower() in file.lower()
                for file in commit.get('changed_files', [])
            )
            if not files_match:
                return False
        
        return True
    
    def _ensure_data_store_exists(self) -> None:
        """Ensure the data store directory structure exists."""
        try:
            behaviors_dir = self.data_store_path / 'behaviors'
            behaviors_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Data store directory ensured: {behaviors_dir}")
            
        except Exception as e:
            logger.error(f"Failed to create data store directory: {e}")
            raise
    
    def _ensure_commits_file_exists(self) -> None:
        """Ensure the commits JSONL file exists."""
        try:
            if not self.commits_file.exists():
                # Create empty file
                self.commits_file.touch()
                logger.info(f"Created commits file: {self.commits_file}")
            
        except Exception as e:
            logger.error(f"Failed to create commits file: {e}")
            raise
