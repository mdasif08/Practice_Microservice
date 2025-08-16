"""
Git Parser Module - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This module handles Git repository interaction and commit metadata extraction.
"""

import os
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

from ...shared.utils.logger import get_logger
from ...shared.utils.error_handler import handle_error

logger = get_logger(__name__)


class GitParser:
    """
    Git repository parser for extracting commit metadata.
    
    Responsibilities:
    - Detect Git repositories
    - Extract commit information
    - Parse commit metadata
    - Handle Git command execution
    """
    
    def __init__(self, repo_path: Path):
        """
        Initialize Git parser.
        
        Args:
            repo_path: Path to Git repository
        """
        self.repo_path = repo_path
        self.git_dir = repo_path / '.git'
        
    def is_git_repository(self) -> bool:
        """
        Check if the current directory is a Git repository.
        
        Returns:
            True if Git repository exists, False otherwise
        """
        try:
            return self.git_dir.exists() and self.git_dir.is_dir()
        except Exception as e:
            logger.error(f"Error checking Git repository: {e}")
            return False
    
    def get_latest_commit(self) -> Dict[str, Any]:
        """
        Extract metadata from the most recent commit.
        
        Returns:
            Dict containing commit metadata
            
        Raises:
            GitCommandError: If Git command fails
        """
        try:
            logger.info(f"Extracting latest commit from: {self.repo_path}")
            
            # Get commit hash
            commit_hash = self._run_git_command(['rev-parse', 'HEAD']).strip()
            
            # Get commit metadata
            commit_data = self._get_commit_metadata(commit_hash)
            
            # Get changed files
            changed_files = self._get_changed_files(commit_hash)
            commit_data['changed_files'] = changed_files
            
            # Get commit statistics
            stats = self._get_commit_stats(commit_hash)
            commit_data.update(stats)
            
            logger.info(f"Successfully extracted commit: {commit_hash[:8]}")
            
            return commit_data
            
        except Exception as e:
            error_result = handle_error(e, "git_parser.get_latest_commit")
            logger.error(f"Failed to extract latest commit: {error_result['error']}")
            raise GitCommandError(f"Failed to extract latest commit: {error_result['error']}")
    
    def get_commit_by_hash(self, commit_hash: str) -> Dict[str, Any]:
        """
        Extract metadata from a specific commit by hash.
        
        Args:
            commit_hash: Git commit hash
            
        Returns:
            Dict containing commit metadata
            
        Raises:
            GitCommandError: If Git command fails
        """
        try:
            logger.info(f"Extracting commit by hash: {commit_hash}")
            
            # Validate commit hash exists
            if not self._commit_exists(commit_hash):
                raise GitCommandError(f"Commit {commit_hash} not found")
            
            # Get commit metadata
            commit_data = self._get_commit_metadata(commit_hash)
            
            # Get changed files
            changed_files = self._get_changed_files(commit_hash)
            commit_data['changed_files'] = changed_files
            
            # Get commit statistics
            stats = self._get_commit_stats(commit_hash)
            commit_data.update(stats)
            
            logger.info(f"Successfully extracted commit: {commit_hash[:8]}")
            
            return commit_data
            
        except Exception as e:
            error_result = handle_error(e, "git_parser.get_commit_by_hash")
            logger.error(f"Failed to extract commit {commit_hash}: {error_result['error']}")
            raise GitCommandError(f"Failed to extract commit {commit_hash}: {error_result['error']}")
    
    def get_repository_info(self) -> Dict[str, Any]:
        """
        Get general information about the Git repository.
        
        Returns:
            Dict containing repository information
        """
        try:
            info = {
                'repository_path': str(self.repo_path),
                'remote_url': self._get_remote_url(),
                'current_branch': self._get_current_branch(),
                'total_commits': self._get_total_commits(),
                'last_commit_date': self._get_last_commit_date()
            }
            
            return info
            
        except Exception as e:
            error_result = handle_error(e, "git_parser.get_repository_info")
            logger.error(f"Failed to get repository info: {error_result['error']}")
            return {'error': error_result['error']}
    
    def _get_commit_metadata(self, commit_hash: str) -> Dict[str, Any]:
        """
        Extract basic commit metadata.
        
        Args:
            commit_hash: Git commit hash
            
        Returns:
            Dict containing commit metadata
        """
        # Get commit details using git show
        commit_info = self._run_git_command([
            'show', '--format=format:%H%n%an%n%ae%n%ad%n%s%n%b', 
            '--no-patch', commit_hash
        ]).split('\n')
        
        # Parse commit information
        hash_value = commit_info[0]
        author_name = commit_info[1]
        author_email = commit_info[2]
        commit_date = commit_info[3]
        subject = commit_info[4]
        body = '\n'.join(commit_info[5:]) if len(commit_info) > 5 else ''
        
        # Parse commit date
        try:
            parsed_date = datetime.strptime(commit_date, '%a %b %d %H:%M:%S %Y %z')
            formatted_date = parsed_date.isoformat()
        except ValueError:
            formatted_date = commit_date
        
        return {
            'hash': hash_value,
            'author': author_name,
            'author_email': author_email,
            'commit_date': formatted_date,
            'message': subject,
            'body': body.strip()
        }
    
    def _get_changed_files(self, commit_hash: str) -> List[str]:
        """
        Get list of files changed in the commit.
        
        Args:
            commit_hash: Git commit hash
            
        Returns:
            List of changed file paths
        """
        try:
            # Get list of changed files
            files_output = self._run_git_command([
                'show', '--name-only', '--format=format:', commit_hash
            ]).strip()
            
            if files_output:
                return [f.strip() for f in files_output.split('\n') if f.strip()]
            else:
                return []
                
        except Exception as e:
            logger.warning(f"Failed to get changed files for commit {commit_hash}: {e}")
            return []
    
    def _get_commit_stats(self, commit_hash: str) -> Dict[str, int]:
        """
        Get commit statistics (insertions, deletions).
        
        Args:
            commit_hash: Git commit hash
            
        Returns:
            Dict containing insertions and deletions
        """
        try:
            # Get commit statistics
            stats_output = self._run_git_command([
                'show', '--stat', '--format=format:', commit_hash
            ])
            
            # Parse statistics (simplified parsing)
            lines = stats_output.strip().split('\n')
            insertions = 0
            deletions = 0
            
            for line in lines:
                if 'insertions' in line and 'deletions' in line:
                    # Extract numbers from line like " 2 files changed, 10 insertions(+), 5 deletions(-)"
                    parts = line.split(',')
                    for part in parts:
                        if 'insertions' in part:
                            insertions = int(''.join(filter(str.isdigit, part)))
                        elif 'deletions' in part:
                            deletions = int(''.join(filter(str.isdigit, part)))
                    break
            
            return {
                'insertions': insertions,
                'deletions': deletions
            }
            
        except Exception as e:
            logger.warning(f"Failed to get commit stats for commit {commit_hash}: {e}")
            return {'insertions': 0, 'deletions': 0}
    
    def _run_git_command(self, args: List[str]) -> str:
        """
        Execute a Git command and return the output.
        
        Args:
            args: Git command arguments
            
        Returns:
            Command output as string
            
        Raises:
            GitCommandError: If command fails
        """
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Git command failed: {' '.join(['git'] + args)} - {e.stderr}"
            logger.error(error_msg)
            raise GitCommandError(error_msg)
        except FileNotFoundError:
            error_msg = "Git command not found. Please ensure Git is installed."
            logger.error(error_msg)
            raise GitCommandError(error_msg)
    
    def _commit_exists(self, commit_hash: str) -> bool:
        """
        Check if a commit exists in the repository.
        
        Args:
            commit_hash: Git commit hash
            
        Returns:
            True if commit exists, False otherwise
        """
        try:
            self._run_git_command(['cat-file', '-e', commit_hash])
            return True
        except GitCommandError:
            return False
    
    def _get_remote_url(self) -> Optional[str]:
        """Get the remote URL of the repository."""
        try:
            return self._run_git_command(['config', '--get', 'remote.origin.url']).strip()
        except GitCommandError:
            return None
    
    def _get_current_branch(self) -> Optional[str]:
        """Get the current branch name."""
        try:
            return self._run_git_command(['branch', '--show-current']).strip()
        except GitCommandError:
            return None
    
    def _get_total_commits(self) -> int:
        """Get the total number of commits in the repository."""
        try:
            output = self._run_git_command(['rev-list', '--count', 'HEAD'])
            return int(output.strip())
        except (GitCommandError, ValueError):
            return 0
    
    def _get_last_commit_date(self) -> Optional[str]:
        """Get the date of the last commit."""
        try:
            date_str = self._run_git_command([
                'log', '-1', '--format=format:%ad', '--date=iso'
            ]).strip()
            return date_str
        except GitCommandError:
            return None


class GitCommandError(Exception):
    """Raised when a Git command fails."""
    pass
