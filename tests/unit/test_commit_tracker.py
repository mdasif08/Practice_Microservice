"""
Unit tests for services/commit-tracker-service/src/commit_tracker.py module.

Tests commit tracking functionality and orchestration.
"""

import pytest
import uuid

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from typing import Dict, Any

# Import the module under test
from services.commit_tracker_service.src.commit_tracker import (
    CommitTracker, GitRepositoryError, CommitExtractionError
)


class TestCommitTracker:
    """Test cases for CommitTracker class."""

    def setup_method(self):
        """Setup method to create test instances."""
        self.test_repo_path = Path("/test/repo")
        self.commit_tracker = CommitTracker(str(self.test_repo_path))

    def test_init_with_custom_path(self):
        """Test CommitTracker initialization with custom path."""
        tracker = CommitTracker("/custom/repo")
        assert tracker.repo_path == Path("/custom/repo")

    def test_init_with_default_path(self):
        """Test CommitTracker initialization with default path."""
        with patch('pathlib.Path.cwd', return_value=Path("/current/dir")):
            tracker = CommitTracker()
            assert tracker.repo_path == Path("/current/dir")

    def test_init_with_string_path(self):
        """Test CommitTracker initialization with string path."""
        tracker = CommitTracker("/string/path")
        assert isinstance(tracker.repo_path, Path)
        assert tracker.repo_path == Path("/string/path")

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.DataWriter')
    def test_init_creates_dependencies(self, mock_data_writer, mock_git_parser):
        """Test that CommitTracker creates its dependencies."""
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        
        mock_data_writer_instance = MagicMock()
        mock_data_writer.return_value = mock_data_writer_instance
        
        tracker = CommitTracker("/test/repo")
        
        mock_git_parser.assert_called_once_with(Path("/test/repo"))
        mock_data_writer.assert_called_once()
        
        assert tracker.git_parser == mock_git_parser_instance
        assert tracker.data_writer == mock_data_writer_instance

    @patch('services.commit_tracker_service.src.commit_tracker.uuid.uuid4')
    @patch('services.commit_tracker_service.src.commit_tracker.datetime')
    @patch('services.commit_tracker_service.src.commit_tracker.CommitTracker._validate_commit_data')
    @patch('services.commit_tracker_service.src.commit_tracker.DataWriter')
    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.logger')
    def test_log_latest_commit_success(self, mock_logger, mock_git_parser, mock_data_writer, mock_validate, mock_datetime, mock_uuid):
        """Test log_latest_commit with successful execution."""
        # Mock dependencies
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = True
        
        mock_data_writer_instance = MagicMock()
        mock_data_writer.return_value = mock_data_writer_instance
        
        # Mock commit data
        commit_data = {
            'hash': 'abc123def456',
            'author': 'Test Author',
            'author_email': 'test@example.com',
            'message': 'Test commit',
            'body': 'Test body',
            'commit_date': '2023-01-01T12:00:00+00:00',
            'changed_files': ['file1.py', 'file2.py'],
            'insertions': 10,
            'deletions': 5
        }
        mock_git_parser_instance.get_latest_commit.return_value = commit_data
        
        # Mock UUID and datetime
        mock_uuid.return_value = '12345678-1234-1234-1234-123456789abc'
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        tracker = CommitTracker("/test/repo")
        result = tracker.log_latest_commit()
        
        # Verify calls
        mock_git_parser_instance.is_git_repository.assert_called_once()
        mock_git_parser_instance.get_latest_commit.assert_called_once()
        mock_validate.assert_called_once()
        mock_data_writer_instance.write_commit.assert_called_once()
        
        # Verify result
        assert result['status'] == 'success'
        assert result['commit_data']['hash'] == 'abc123def456'
        assert result['commit_data']['id'] == '12345678-1234-1234-1234-123456789abc'
        assert "logged successfully" in result['message']
        mock_logger.info.assert_called()

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.logger')
    def test_log_latest_commit_no_git_repository(self, mock_logger, mock_git_parser):
        """Test log_latest_commit when no Git repository is found."""
        # Mock GitParser
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = False
        
        tracker = CommitTracker("/test/repo")
        result = tracker.log_latest_commit()
        
        # Verify result
        assert result['status'] == 'error'
        assert "No Git repository found" in result['error']
        mock_logger.error.assert_called()

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.handle_error')
    @patch('services.commit_tracker_service.src.commit_tracker.logger')
    def test_log_latest_commit_git_error(self, mock_logger, mock_handle_error, mock_git_parser):
        """Test log_latest_commit handles Git errors."""
        # Mock GitParser
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = True
        mock_git_parser_instance.get_latest_commit.side_effect = Exception("Git error")
        
        mock_handle_error.return_value = {'status': 'error', 'error': 'Git error'}
        
        tracker = CommitTracker("/test/repo")
        result = tracker.log_latest_commit()
        
        # Verify result
        assert result['status'] == 'error'
        mock_handle_error.assert_called_once()
        mock_logger.error.assert_called()

    @patch('services.commit_tracker_service.src.commit_tracker.uuid.uuid4')
    @patch('services.commit_tracker_service.src.commit_tracker.datetime')
    @patch('services.commit_tracker_service.src.commit_tracker.CommitTracker._validate_commit_data')
    @patch('services.commit_tracker_service.src.commit_tracker.DataWriter')
    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.logger')
    def test_log_commit_by_hash_success(self, mock_logger, mock_git_parser, mock_data_writer, mock_validate, mock_datetime, mock_uuid):
        """Test log_commit_by_hash with successful execution."""
        # Mock dependencies
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = True
        
        mock_data_writer_instance = MagicMock()
        mock_data_writer.return_value = mock_data_writer_instance
        
        # Mock commit data
        commit_data = {
            'hash': 'abc123def456',
            'author': 'Test Author',
            'author_email': 'test@example.com',
            'message': 'Test commit',
            'body': 'Test body',
            'commit_date': '2023-01-01T12:00:00+00:00',
            'changed_files': ['file1.py'],
            'insertions': 5,
            'deletions': 2
        }
        mock_git_parser_instance.get_commit_by_hash.return_value = commit_data
        
        # Mock UUID and datetime
        mock_uuid.return_value = '87654321-4321-4321-4321-cba987654321'
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        tracker = CommitTracker("/test/repo")
        result = tracker.log_commit_by_hash('abc123def456')
        
        # Verify calls
        mock_git_parser_instance.is_git_repository.assert_called_once()
        mock_git_parser_instance.get_commit_by_hash.assert_called_once_with('abc123def456')
        mock_validate.assert_called_once()
        mock_data_writer_instance.write_commit.assert_called_once()
        
        # Verify result
        assert result['status'] == 'success'
        assert result['commit_data']['hash'] == 'abc123def456'
        assert result['commit_data']['id'] == '87654321-4321-4321-4321-cba987654321'
        assert "logged successfully" in result['message']
        mock_logger.info.assert_called()

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.logger')
    def test_log_commit_by_hash_no_git_repository(self, mock_logger, mock_git_parser):
        """Test log_commit_by_hash when no Git repository is found."""
        # Mock GitParser
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = False
        
        tracker = CommitTracker("/test/repo")
        result = tracker.log_commit_by_hash('abc123def456')
        
        # Verify result
        assert result['status'] == 'error'
        assert "No Git repository found" in result['error']
        mock_logger.error.assert_called()

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.handle_error')
    @patch('services.commit_tracker_service.src.commit_tracker.logger')
    def test_log_commit_by_hash_git_error(self, mock_logger, mock_handle_error, mock_git_parser):
        """Test log_commit_by_hash handles Git errors."""
        # Mock GitParser
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = True
        mock_git_parser_instance.get_commit_by_hash.side_effect = Exception("Git error")
        
        mock_handle_error.return_value = {'status': 'error', 'error': 'Git error'}
        
        tracker = CommitTracker("/test/repo")
        result = tracker.log_commit_by_hash('abc123def456')
        
        # Verify result
        assert result['status'] == 'error'
        mock_handle_error.assert_called_once()
        mock_logger.error.assert_called()

    def test_validate_commit_data_valid(self):
        """Test _validate_commit_data with valid data."""
        valid_commit_data = {
            'hash': 'abc123def456',
            'author': 'Test Author',
            'message': 'Test commit',
            'timestamp': '2023-01-01T12:00:00+00:00',
            'changed_files': ['file1.py', 'file2.py']
        }
        
        # Should not raise an exception
        self.commit_tracker._validate_commit_data(valid_commit_data)

    @pytest.mark.parametrize("missing_field", [
        'hash', 'author', 'message', 'timestamp', 'changed_files'
    ])
    def test_validate_commit_data_missing_field(self, missing_field):
        """Test _validate_commit_data with missing required fields."""
        commit_data = {
            'hash': 'abc123def456',
            'author': 'Test Author',
            'message': 'Test commit',
            'timestamp': '2023-01-01T12:00:00+00:00',
            'changed_files': ['file1.py', 'file2.py']
        }
        
        # Remove the missing field
        del commit_data[missing_field]
        
        with pytest.raises(ValueError) as exc_info:
            self.commit_tracker._validate_commit_data(commit_data)
        
        assert f"Missing required field: {missing_field}" in str(exc_info.value)

    def test_validate_commit_data_none_field(self):
        """Test _validate_commit_data with None field."""
        commit_data = {
            'hash': 'abc123def456',
            'author': None,  # None field
            'message': 'Test commit',
            'timestamp': '2023-01-01T12:00:00+00:00',
            'changed_files': ['file1.py', 'file2.py']
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.commit_tracker._validate_commit_data(commit_data)
        
        assert "Missing required field: author" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_hash", [
        'abc',  # Too short
        '',  # Empty
        None  # None
    ])
    def test_validate_commit_data_invalid_hash(self, invalid_hash):
        """Test _validate_commit_data with invalid hash format."""
        commit_data = {
            'hash': invalid_hash,
            'author': 'Test Author',
            'message': 'Test commit',
            'timestamp': '2023-01-01T12:00:00+00:00',
            'changed_files': ['file1.py', 'file2.py']
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.commit_tracker._validate_commit_data(commit_data)
        
        # The validation checks for missing fields first, then format
        # For invalid but present values, it checks format
        # For None values, it treats them as missing fields
        if invalid_hash is None:
            assert "Missing required field: hash" in str(exc_info.value)
        else:
            assert "Invalid commit hash format" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_timestamp", [
        'invalid-date',
        '2023-13-01T12:00:00+00:00',  # Invalid month
        '2023-01-32T12:00:00+00:00',  # Invalid day
        '',
        None
    ])
    def test_validate_commit_data_invalid_timestamp(self, invalid_timestamp):
        """Test _validate_commit_data with invalid timestamp format."""
        commit_data = {
            'hash': 'abc123def456',
            'author': 'Test Author',
            'message': 'Test commit',
            'timestamp': invalid_timestamp,
            'changed_files': ['file1.py', 'file2.py']
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.commit_tracker._validate_commit_data(commit_data)
        
        # The validation checks for missing fields first, then format
        # For invalid but present values, it checks format
        # For None values, it treats them as missing fields
        if invalid_timestamp is None:
            assert "Missing required field: timestamp" in str(exc_info.value)
        else:
            assert "Invalid timestamp format" in str(exc_info.value)

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.logger')
    def test_get_repository_info_success(self, mock_logger, mock_git_parser):
        """Test get_repository_info with successful execution."""
        # Mock GitParser
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = True
        
        # Mock repository info
        repo_info = {
            'repository_path': '/test/repo',
            'remote_url': 'https://github.com/test/repo.git',
            'current_branch': 'main',
            'total_commits': 42,
            'last_commit_date': '2023-01-01T12:00:00+00:00'
        }
        mock_git_parser_instance.get_repository_info.return_value = repo_info
        
        tracker = CommitTracker("/test/repo")
        result = tracker.get_repository_info()
        
        # Verify calls
        mock_git_parser_instance.is_git_repository.assert_called_once()
        mock_git_parser_instance.get_repository_info.assert_called_once()
        
        # Verify result
        assert result['status'] == 'success'
        assert result['repository_info'] == repo_info
        assert "retrieved successfully" in result['message']

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    def test_get_repository_info_no_git_repository(self, mock_git_parser):
        """Test get_repository_info when no Git repository is found."""
        # Mock GitParser
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = False
        
        tracker = CommitTracker("/test/repo")
        result = tracker.get_repository_info()
        
        # Verify result
        assert result['status'] == 'error'
        assert "No Git repository found" in result['message']
        assert result['repository_info'] is None

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.handle_error')
    @patch('services.commit_tracker_service.src.commit_tracker.logger')
    def test_get_repository_info_error(self, mock_logger, mock_handle_error, mock_git_parser):
        """Test get_repository_info handles errors."""
        # Mock GitParser
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = True
        mock_git_parser_instance.get_repository_info.side_effect = Exception("Repository error")
        
        mock_handle_error.return_value = {'status': 'error', 'error': 'Repository error'}
        
        tracker = CommitTracker("/test/repo")
        result = tracker.get_repository_info()
        
        # Verify result
        assert result['status'] == 'error'
        mock_handle_error.assert_called_once()
        mock_logger.error.assert_called()


class TestGitRepositoryError:
    """Test cases for GitRepositoryError exception."""

    def test_git_repository_error_initialization(self):
        """Test GitRepositoryError initialization."""
        error = GitRepositoryError("No Git repository found")
        assert str(error) == "No Git repository found"

    def test_git_repository_error_inheritance(self):
        """Test GitRepositoryError inheritance."""
        error = GitRepositoryError("Test error")
        assert isinstance(error, Exception)


class TestCommitExtractionError:
    """Test cases for CommitExtractionError exception."""

    def test_commit_extraction_error_initialization(self):
        """Test CommitExtractionError initialization."""
        error = CommitExtractionError("Failed to extract commit")
        assert str(error) == "Failed to extract commit"

    def test_commit_extraction_error_inheritance(self):
        """Test CommitExtractionError inheritance."""
        error = CommitExtractionError("Test error")
        assert isinstance(error, Exception)


class TestCommitTrackerIntegration:
    """Integration tests for CommitTracker components."""

    def setup_method(self):
        """Setup method to create test instances."""
        self.commit_tracker = CommitTracker("/test/repo")

    @patch('services.commit_tracker_service.src.commit_tracker.uuid.uuid4')
    @patch('services.commit_tracker_service.src.commit_tracker.datetime')
    @patch('services.commit_tracker_service.src.commit_tracker.DataWriter')
    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    def test_full_commit_logging_workflow(self, mock_git_parser, mock_data_writer, mock_datetime, mock_uuid):
        """Test complete commit logging workflow."""
        # Mock dependencies
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = True
        
        mock_data_writer_instance = MagicMock()
        mock_data_writer.return_value = mock_data_writer_instance
        
        # Mock commit data
        commit_data = {
            'hash': 'abc123def456',
            'author': 'Test Author',
            'author_email': 'test@example.com',
            'message': 'Test commit',
            'body': 'Test body',
            'commit_date': '2023-01-01T12:00:00+00:00',
            'changed_files': ['file1.py', 'file2.py'],
            'insertions': 10,
            'deletions': 5
        }
        mock_git_parser_instance.get_latest_commit.return_value = commit_data
        
        # Mock UUID and datetime
        mock_uuid.return_value = '12345678-1234-1234-1234-123456789abc'
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        # Test workflow
        tracker = CommitTracker("/test/repo")
        
        # Test repository info
        repo_info = {
            'repository_path': '/test/repo',
            'remote_url': 'https://github.com/test/repo.git',
            'current_branch': 'main',
            'total_commits': 42,
            'last_commit_date': '2023-01-01T12:00:00+00:00'
        }
        mock_git_parser_instance.get_repository_info.return_value = repo_info
        
        repo_result = tracker.get_repository_info()
        assert repo_result['status'] == 'success'
        assert repo_result['repository_info'] == repo_info
        
        # Test commit logging
        result = tracker.log_latest_commit()
        assert result['status'] == 'success'
        assert result['commit_data']['hash'] == 'abc123def456'
        assert result['commit_data']['id'] == '12345678-1234-1234-1234-123456789abc'
        
        # Verify data writer was called
        mock_data_writer_instance.write_commit.assert_called_once()

    @pytest.mark.parametrize("commit_hash,expected_success", [
        ('abc123def456', True),
        ('def456ghi789', True),
        ('invalid-hash', False),
        ('', False)
    ])
    @patch('services.commit_tracker_service.src.commit_tracker.DataWriter')
    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    def test_commit_by_hash_variations(self, mock_git_parser, mock_data_writer, commit_hash, expected_success):
        """Test log_commit_by_hash with various commit hashes."""
        # Mock dependencies
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_git_parser_instance.is_git_repository.return_value = True
        
        mock_data_writer_instance = MagicMock()
        mock_data_writer.return_value = mock_data_writer_instance
        
        if expected_success:
            # Mock successful commit data
            commit_data = {
                'hash': commit_hash,
                'author': 'Test Author',
                'message': 'Test commit',
                'timestamp': '2023-01-01T12:00:00+00:00',
                'changed_files': ['file1.py']
            }
            mock_git_parser_instance.get_commit_by_hash.return_value = commit_data
        else:
            # Mock error
            mock_git_parser_instance.get_commit_by_hash.side_effect = Exception("Commit not found")
        
        tracker = CommitTracker("/test/repo")
        result = tracker.log_commit_by_hash(commit_hash)
        
        if expected_success:
            assert result['status'] == 'success'
            assert result['commit_data']['hash'] == commit_hash
        else:
            assert result['status'] == 'error'

    @pytest.mark.parametrize("timestamp_format", [
        '2023-01-01T12:00:00+00:00',
        '2023-01-01T12:00:00Z',
        '2023-01-01T12:00:00-05:00'
    ])
    def test_timestamp_validation_formats(self, timestamp_format):
        """Test timestamp validation with various formats."""
        commit_data = {
            'hash': 'abc123def456',
            'author': 'Test Author',
            'message': 'Test commit',
            'timestamp': timestamp_format,
            'changed_files': ['file1.py', 'file2.py']
        }
        
        # Should not raise an exception for valid formats
        self.commit_tracker._validate_commit_data(commit_data)

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    @patch('services.commit_tracker_service.src.commit_tracker.DataWriter')
    def test_commit_tracker_with_real_path(self, mock_data_writer, mock_git_parser):
        """Test CommitTracker with real path handling."""
        # Mock dependencies
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        mock_data_writer_instance = MagicMock()
        mock_data_writer.return_value = mock_data_writer_instance
        
        tracker = CommitTracker("/real/path")
        assert tracker.repo_path == Path("/real/path")
        assert isinstance(tracker.git_parser, MagicMock)  # Mocked in tests
        assert isinstance(tracker.data_writer, MagicMock)  # Mocked in tests


class TestCommitTrackerEdgeCases:
    """Test edge cases for CommitTracker."""

    def setup_method(self):
        """Setup method to create test instances."""
        self.commit_tracker = CommitTracker("/test/repo")

    def test_commit_tracker_empty_path(self):
        """Test CommitTracker with empty path."""
        tracker = CommitTracker("")
        assert tracker.repo_path == Path.cwd()  # Empty string becomes current directory

    def test_commit_tracker_none_path(self):
        """Test CommitTracker with None path."""
        with patch('pathlib.Path.cwd', return_value=Path("/current/dir")):
            tracker = CommitTracker(None)
            assert tracker.repo_path == Path("/current/dir")

    @patch('services.commit_tracker_service.src.commit_tracker.GitParser')
    def test_commit_tracker_relative_path(self, mock_git_parser):
        """Test CommitTracker with relative path."""
        mock_git_parser_instance = MagicMock()
        mock_git_parser.return_value = mock_git_parser_instance
        
        tracker = CommitTracker("./relative/path")
        assert tracker.repo_path == Path("./relative/path")

    def test_validate_commit_data_edge_cases(self):
        """Test _validate_commit_data with edge case data."""
        # Test with minimal valid data
        minimal_data = {
            'hash': 'abc123def456',
            'author': 'Test Author',
            'message': 'Test commit',
            'timestamp': '2023-01-01T12:00:00+00:00',
            'changed_files': []  # Empty list
        }
        
        # Should not raise an exception
        self.commit_tracker._validate_commit_data(minimal_data)
        
        # Test with long hash
        long_hash_data = {
            'hash': 'a' * 40,  # 40 character hash
            'author': 'Test Author',
            'message': 'Test commit',
            'timestamp': '2023-01-01T12:00:00+00:00',
            'changed_files': ['file1.py']
        }
        
        # Should not raise an exception
        self.commit_tracker._validate_commit_data(long_hash_data)
