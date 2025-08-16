"""
Unit Tests for Commit Tracker - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This module contains unit tests for the commit tracker functionality.
"""

import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

import sys
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.commit_tracker_service.src.commit_tracker import CommitTracker, GitRepositoryError, CommitExtractionError
from services.commit_tracker_service.src.git_parser import GitParser, GitCommandError
from services.commit_tracker_service.src.data_writer import DataWriter


class TestCommitTracker:
    """Test cases for CommitTracker class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_path = Path(self.temp_dir)
        
        # Mock dependencies
        self.mock_git_parser = Mock(spec=GitParser)
        self.mock_data_writer = Mock(spec=DataWriter)
        
        # Sample commit data
        self.sample_commit_data = {
            'hash': 'a1b2c3d4e5f6789012345678901234567890abcd',
            'author': 'Test Author',
            'author_email': 'test@example.com',
            'commit_date': '2024-01-01T12:00:00+00:00',
            'message': 'Test commit message',
            'body': 'Test commit body',
            'changed_files': ['test_file.py', 'README.md'],
            'insertions': 10,
            'deletions': 5
        }
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init_with_default_path(self):
        """Test initialization with default path."""
        with patch('services.commit_tracker_service.src.commit_tracker.GitParser') as mock_git_parser_class, \
             patch('services.commit_tracker_service.src.commit_tracker.DataWriter') as mock_data_writer_class:
            
            tracker = CommitTracker()
            
            mock_git_parser_class.assert_called_once()
            mock_data_writer_class.assert_called_once()
            assert tracker.repo_path == Path.cwd()
    
    def test_init_with_custom_path(self):
        """Test initialization with custom path."""
        custom_path = "/custom/repo/path"
        
        with patch('services.commit_tracker_service.src.commit_tracker.GitParser') as mock_git_parser_class, \
             patch('services.commit_tracker_service.src.commit_tracker.DataWriter') as mock_data_writer_class:
            
            tracker = CommitTracker(repo_path=custom_path)
            
            mock_git_parser_class.assert_called_once()
            mock_data_writer_class.assert_called_once()
            assert tracker.repo_path == Path(custom_path)
    
    def test_log_latest_commit_success(self):
        """Test successful logging of latest commit."""
        # Setup mocks
        tracker = CommitTracker(repo_path=str(self.repo_path))
        tracker.git_parser = self.mock_git_parser
        tracker.data_writer = self.mock_data_writer
        
        # Configure mocks
        self.mock_git_parser.is_git_repository.return_value = True
        self.mock_git_parser.get_latest_commit.return_value = self.sample_commit_data
        self.mock_data_writer.write_commit.return_value = {
            'status': 'success',
            'file_path': '/path/to/commits.jsonl',
            'message': 'Commit written successfully'
        }
        
        # Execute
        result = tracker.log_latest_commit()
        
        # Verify
        assert result['status'] == 'success'
        assert 'commit_data' in result
        assert result['commit_data']['hash'] == self.sample_commit_data['hash']
        assert 'id' in result['commit_data']
        assert 'timestamp' in result['commit_data']
        
        self.mock_git_parser.is_git_repository.assert_called_once()
        self.mock_git_parser.get_latest_commit.assert_called_once()
        self.mock_data_writer.write_commit.assert_called_once()
    
    def test_log_latest_commit_no_git_repository(self):
        """Test logging when no Git repository is found."""
        # Setup mocks
        tracker = CommitTracker(repo_path=str(self.repo_path))
        tracker.git_parser = self.mock_git_parser
        
        # Configure mocks
        self.mock_git_parser.is_git_repository.return_value = False
        
        # Execute and verify
        result = tracker.log_latest_commit()
        
        assert result['status'] == 'error'
        assert 'No Git repository found' in result['error']
        
        self.mock_git_parser.is_git_repository.assert_called_once()
    
    def test_log_latest_commit_git_error(self):
        """Test logging when Git command fails."""
        # Setup mocks
        tracker = CommitTracker(repo_path=str(self.repo_path))
        tracker.git_parser = self.mock_git_parser
        
        # Configure mocks
        self.mock_git_parser.is_git_repository.return_value = True
        self.mock_git_parser.get_latest_commit.side_effect = GitCommandError("Git command failed")
        
        # Execute and verify
        result = tracker.log_latest_commit()
        
        assert result['status'] == 'error'
        assert 'Git command failed' in result['error']
        
        self.mock_git_parser.is_git_repository.assert_called_once()
        self.mock_git_parser.get_latest_commit.assert_called_once()
    
    def test_log_commit_by_hash_success(self):
        """Test successful logging of commit by hash."""
        # Setup mocks
        tracker = CommitTracker(repo_path=str(self.repo_path))
        tracker.git_parser = self.mock_git_parser
        tracker.data_writer = self.mock_data_writer
        
        commit_hash = 'a1b2c3d4e5f6789012345678901234567890abcd'
        
        # Configure mocks
        self.mock_git_parser.is_git_repository.return_value = True
        self.mock_git_parser.get_commit_by_hash.return_value = self.sample_commit_data
        self.mock_data_writer.write_commit.return_value = {
            'status': 'success',
            'file_path': '/path/to/commits.jsonl',
            'message': 'Commit written successfully'
        }
        
        # Execute
        result = tracker.log_commit_by_hash(commit_hash)
        
        # Verify
        assert result['status'] == 'success'
        assert 'commit_data' in result
        assert result['commit_data']['hash'] == self.sample_commit_data['hash']
        
        self.mock_git_parser.is_git_repository.assert_called_once()
        self.mock_git_parser.get_commit_by_hash.assert_called_once_with(commit_hash)
        self.mock_data_writer.write_commit.assert_called_once()
    
    def test_log_commit_by_hash_invalid_hash(self):
        """Test logging commit with invalid hash."""
        # Setup mocks
        tracker = CommitTracker(repo_path=str(self.repo_path))
        tracker.git_parser = self.mock_git_parser
        
        commit_hash = 'invalid_hash'
        
        # Configure mocks
        self.mock_git_parser.is_git_repository.return_value = True
        self.mock_git_parser.get_commit_by_hash.side_effect = GitCommandError("Commit not found")
        
        # Execute and verify
        result = tracker.log_commit_by_hash(commit_hash)
        
        assert result['status'] == 'error'
        assert 'Commit not found' in result['error']
        
        self.mock_git_parser.is_git_repository.assert_called_once()
        self.mock_git_parser.get_commit_by_hash.assert_called_once_with(commit_hash)
    
    def test_validate_commit_data_valid(self):
        """Test validation of valid commit data."""
        tracker = CommitTracker()
        
        valid_data = {
            'hash': 'a1b2c3d4e5f6789012345678901234567890abcd',
            'author': 'Test Author',
            'message': 'Test message',
            'timestamp': '2024-01-01T12:00:00+00:00',
            'changed_files': ['file1.py', 'file2.py']
        }
        
        # Should not raise any exception
        tracker._validate_commit_data(valid_data)
    
    def test_validate_commit_data_missing_fields(self):
        """Test validation of commit data with missing fields."""
        tracker = CommitTracker()
        
        invalid_data = {
            'hash': 'a1b2c3d4e5f6789012345678901234567890abcd',
            'author': 'Test Author',
            # Missing 'message', 'timestamp', 'changed_files'
        }
        
        with pytest.raises(ValueError, match="Missing required field"):
            tracker._validate_commit_data(invalid_data)
    
    def test_validate_commit_data_invalid_hash(self):
        """Test validation of commit data with invalid hash."""
        tracker = CommitTracker()
        
        invalid_data = {
            'hash': 'abc',  # Too short
            'author': 'Test Author',
            'message': 'Test message',
            'timestamp': '2024-01-01T12:00:00+00:00',
            'changed_files': ['file1.py']
        }
        
        with pytest.raises(ValueError, match="Invalid commit hash format"):
            tracker._validate_commit_data(invalid_data)
    
    def test_validate_commit_data_invalid_timestamp(self):
        """Test validation of commit data with invalid timestamp."""
        tracker = CommitTracker()
        
        invalid_data = {
            'hash': 'a1b2c3d4e5f6789012345678901234567890abcd',
            'author': 'Test Author',
            'message': 'Test message',
            'timestamp': 'invalid-timestamp',
            'changed_files': ['file1.py']
        }
        
        with pytest.raises(ValueError, match="Invalid timestamp format"):
            tracker._validate_commit_data(invalid_data)
    
    def test_get_repository_info_success(self):
        """Test successful retrieval of repository information."""
        # Setup mocks
        tracker = CommitTracker(repo_path=str(self.repo_path))
        tracker.git_parser = self.mock_git_parser
        
        repo_info = {
            'repository_path': str(self.repo_path),
            'remote_url': 'https://github.com/test/repo.git',
            'current_branch': 'main',
            'total_commits': 100,
            'last_commit_date': '2024-01-01T12:00:00+00:00'
        }
        
        # Configure mocks
        self.mock_git_parser.is_git_repository.return_value = True
        self.mock_git_parser.get_repository_info.return_value = repo_info
        
        # Execute
        result = tracker.get_repository_info()
        
        # Verify
        assert result['status'] == 'success'
        assert 'repository_info' in result
        assert result['repository_info'] == repo_info
        
        self.mock_git_parser.is_git_repository.assert_called_once()
        self.mock_git_parser.get_repository_info.assert_called_once()
    
    def test_get_repository_info_no_git_repository(self):
        """Test repository info when no Git repository is found."""
        # Setup mocks
        tracker = CommitTracker(repo_path=str(self.repo_path))
        tracker.git_parser = self.mock_git_parser
        
        # Configure mocks
        self.mock_git_parser.is_git_repository.return_value = False
        
        # Execute
        result = tracker.get_repository_info()
        
        # Verify
        assert result['status'] == 'error'
        assert 'No Git repository found' in result['message']
        
        self.mock_git_parser.is_git_repository.assert_called_once()


class TestGitRepositoryError:
    """Test cases for GitRepositoryError exception."""
    
    def test_git_repository_error_message(self):
        """Test GitRepositoryError message."""
        error = GitRepositoryError("No Git repository found")
        assert str(error) == "No Git repository found"
        assert error.message == "No Git repository found"


class TestCommitExtractionError:
    """Test cases for CommitExtractionError exception."""
    
    def test_commit_extraction_error_message(self):
        """Test CommitExtractionError message."""
        error = CommitExtractionError("Failed to extract commit data")
        assert str(error) == "Failed to extract commit data"
        assert error.message == "Failed to extract commit data"


if __name__ == "__main__":
    pytest.main([__file__])
