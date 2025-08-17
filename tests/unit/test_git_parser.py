"""
Unit tests for services/commit-tracker-service/src/git_parser.py module.

Tests Git repository parsing functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the module under test
from services.commit_tracker_service.src.git_parser import GitParser, GitCommandError


class TestGitParser:
    """Test cases for GitParser class."""

    def setup_method(self):
        """Setup method to create test instances."""
        self.test_repo_path = Path("/test/repo")
        self.git_parser = GitParser(self.test_repo_path)

    def test_init_with_path(self):
        """Test GitParser initialization with path."""
        parser = GitParser("/test/repo")
        assert parser.repo_path == Path("/test/repo")

    def test_is_git_repository(self):
        """Test is_git_repository method."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.is_dir', return_value=True):
                result = self.git_parser.is_git_repository()
                assert result is True

    def test_is_git_repository_not_exists(self):
        """Test is_git_repository when .git doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            result = self.git_parser.is_git_repository()
            assert result is False

    def test_is_git_repository_not_dir(self):
        """Test is_git_repository when .git is not a directory."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.is_dir', return_value=False):
                result = self.git_parser.is_git_repository()
                assert result is False

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_latest_commit_success(self, mock_run_command):
        """Test get_latest_commit with successful execution."""
        # Mock the git commands
        mock_run_command.side_effect = [
            "abc123def456",  # rev-parse HEAD
            "abc123def456\nTest Author\ntest@example.com\n2023-01-01T12:00:00+00:00\nTest commit\nTest body",  # show format
            "file1.py\nfile2.py",  # diff-tree
            " 2 files changed, 10 insertions(+), 5 deletions(-)"  # diff --stat
        ]
        
        result = self.git_parser.get_latest_commit()
        
        assert result is not None
        assert result['hash'] == 'abc123def456'
        assert result['author'] == 'Test Author'
        assert result['author_email'] == 'test@example.com'
        assert result['message'] == 'Test commit'
        assert result['body'] == 'Test body'
        assert result['changed_files'] == ['file1.py', 'file2.py']
        assert result['insertions'] == 10
        assert result['deletions'] == 5

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_latest_commit_git_error(self, mock_run_command):
        """Test get_latest_commit with git command error."""
        mock_run_command.side_effect = Exception("Git command failed")
        
        with pytest.raises(GitCommandError) as exc_info:
            self.git_parser.get_latest_commit()
        
        assert "Failed to extract latest commit" in str(exc_info.value)

    @patch('services.commit_tracker_service.src.git_parser.GitParser._commit_exists')
    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_by_hash_success(self, mock_run_command, mock_commit_exists):
        """Test get_commit_by_hash with successful execution."""
        mock_commit_exists.return_value = True
        mock_run_command.side_effect = [
            "abc123def456\nTest Author\ntest@example.com\n2023-01-01T12:00:00+00:00\nTest commit\nTest body",  # show format
            "file1.py\nfile2.py",  # diff-tree
            " 2 files changed, 10 insertions(+), 5 deletions(-)"  # diff --stat
        ]
        
        result = self.git_parser.get_commit_by_hash("abc123def456")
        
        assert result is not None
        assert result['hash'] == 'abc123def456'
        assert result['author'] == 'Test Author'
        assert result['author_email'] == 'test@example.com'
        assert result['message'] == 'Test commit'
        assert result['body'] == 'Test body'
        assert result['changed_files'] == ['file1.py', 'file2.py']
        assert result['insertions'] == 10
        assert result['deletions'] == 5

    @patch('services.commit_tracker_service.src.git_parser.GitParser._commit_exists')
    def test_get_commit_by_hash_not_found(self, mock_commit_exists):
        """Test get_commit_by_hash when commit doesn't exist."""
        mock_commit_exists.return_value = False
        
        with pytest.raises(GitCommandError) as exc_info:
            self.git_parser.get_commit_by_hash("nonexistent")
        
        assert "Commit nonexistent not found" in str(exc_info.value)

    @patch('services.commit_tracker_service.src.git_parser.GitParser._commit_exists')
    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_by_hash_git_error(self, mock_run_command, mock_commit_exists):
        """Test get_commit_by_hash with git command error."""
        mock_commit_exists.return_value = True
        mock_run_command.side_effect = Exception("Git command failed")
        
        with pytest.raises(GitCommandError) as exc_info:
            self.git_parser.get_commit_by_hash("abc123def456")
        
        assert "Failed to extract commit" in str(exc_info.value)

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_repository_info_success(self, mock_run_command):
        """Test get_repository_info with successful execution."""
        # Mock all the individual methods
        with patch.object(self.git_parser, '_get_remote_url', return_value="https://github.com/test/repo.git"), \
             patch.object(self.git_parser, '_get_current_branch', return_value="main"), \
             patch.object(self.git_parser, '_get_total_commits', return_value=100), \
             patch.object(self.git_parser, '_get_last_commit_date', return_value="2023-01-01T12:00:00+00:00"):
            
            result = self.git_parser.get_repository_info()
            
            assert result is not None
            assert result['repository_path'] == str(self.test_repo_path)
            assert result['remote_url'] == "https://github.com/test/repo.git"
            assert result['current_branch'] == "main"
            assert result['total_commits'] == 100
            assert result['last_commit_date'] == "2023-01-01T12:00:00+00:00"

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_repository_info_error(self, mock_run_command):
        """Test get_repository_info with error."""
        mock_run_command.side_effect = Exception("Git command failed")
        
        result = self.git_parser.get_repository_info()
        
        assert 'error' in result

    @patch('subprocess.run')
    def test_run_git_command_success(self, mock_run):
        """Test _run_git_command with successful execution."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "test output"  # String, not bytes
        mock_run.return_value = mock_result
        
        result = self.git_parser._run_git_command(['rev-parse', 'HEAD'])
        
        assert result == "test output"
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_run_git_command_failure(self, mock_run):
        """Test _run_git_command with command failure."""
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(1, ['git', 'invalid', 'command'], stderr="error message")
        
        with pytest.raises(GitCommandError) as exc_info:
            self.git_parser._run_git_command(['invalid', 'command'])
        
        assert "Git command failed" in str(exc_info.value)

    @patch('subprocess.run')
    def test_run_git_command_exception(self, mock_run):
        """Test _run_git_command with subprocess exception."""
        mock_run.side_effect = FileNotFoundError("git command not found")
        
        with pytest.raises(GitCommandError) as exc_info:
            self.git_parser._run_git_command(['rev-parse', 'HEAD'])
        
        assert "Git command not found" in str(exc_info.value)

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_commit_exists_true(self, mock_run_command):
        """Test _commit_exists when commit exists."""
        mock_run_command.return_value = "abc123def456"
        
        result = self.git_parser._commit_exists("abc123def456")
        assert result is True

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_commit_exists_false(self, mock_run_command):
        """Test _commit_exists when commit doesn't exist."""
        mock_run_command.side_effect = GitCommandError("Commit not found")
        
        result = self.git_parser._commit_exists("nonexistent")
        assert result is False

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_metadata_success(self, mock_run_command):
        """Test _get_commit_metadata with successful execution."""
        mock_run_command.return_value = "abc123def456\nTest Author\ntest@example.com\n2023-01-01T12:00:00+00:00\nTest commit\nTest body"
        
        result = self.git_parser._get_commit_metadata("abc123def456")
        
        assert result['hash'] == 'abc123def456'
        assert result['author'] == 'Test Author'
        assert result['author_email'] == 'test@example.com'
        assert result['commit_date'] == '2023-01-01T12:00:00+00:00'
        assert result['message'] == 'Test commit'
        assert result['body'] == 'Test body'

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_metadata_incomplete_data(self, mock_run_command):
        """Test _get_commit_metadata with incomplete data."""
        mock_run_command.return_value = "abc123def456\nTest Author\ntest@example.com\n2023-01-01T12:00:00+00:00\nTest commit"
        
        result = self.git_parser._get_commit_metadata("abc123def456")
        
        assert result['hash'] == 'abc123def456'
        assert result['author'] == 'Test Author'
        assert result['author_email'] == 'test@example.com'
        assert result['commit_date'] == '2023-01-01T12:00:00+00:00'
        assert result['message'] == 'Test commit'
        assert result['body'] == ''  # Should be empty when not provided

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_changed_files_success(self, mock_run_command):
        """Test _get_changed_files with successful execution."""
        mock_run_command.return_value = "file1.py\nfile2.py\nfile3.py"
        
        result = self.git_parser._get_changed_files("abc123def456")
        
        assert result == ['file1.py', 'file2.py', 'file3.py']

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_changed_files_empty(self, mock_run_command):
        """Test _get_changed_files with no changed files."""
        mock_run_command.return_value = ""
        
        result = self.git_parser._get_changed_files("abc123def456")
        
        assert result == []

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_stats_success(self, mock_run_command):
        """Test _get_commit_stats with successful execution."""
        mock_run_command.return_value = " 2 files changed, 10 insertions(+), 5 deletions(-)"
        
        result = self.git_parser._get_commit_stats("abc123def456")
        
        assert result['insertions'] == 10
        assert result['deletions'] == 5

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_stats_no_changes(self, mock_run_command):
        """Test _get_commit_stats with no changes."""
        mock_run_command.return_value = " 0 files changed, 0 insertions(+), 0 deletions(-)"
        
        result = self.git_parser._get_commit_stats("abc123def456")
        
        assert result['insertions'] == 0
        assert result['deletions'] == 0

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_stats_only_insertions(self, mock_run_command):
        """Test _get_commit_stats with only insertions."""
        mock_run_command.return_value = " 1 file changed, 5 insertions(+)"
        
        result = self.git_parser._get_commit_stats("abc123def456")
        
        assert result['insertions'] == 5
        assert result['deletions'] == 0

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_stats_only_deletions(self, mock_run_command):
        """Test _get_commit_stats with only deletions."""
        mock_run_command.return_value = " 1 file changed, 3 deletions(-)"
        
        result = self.git_parser._get_commit_stats("abc123def456")
        
        assert result['insertions'] == 0
        assert result['deletions'] == 3

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_stats_parse_error(self, mock_run_command):
        """Test _get_commit_stats with parsing error."""
        mock_run_command.return_value = "invalid format"
        
        result = self.git_parser._get_commit_stats("abc123def456")
        
        # Should handle parsing errors gracefully
        assert result['insertions'] == 0
        assert result['deletions'] == 0

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_commit_stats_exception(self, mock_run_command):
        """Test _get_commit_stats with git command exception."""
        mock_run_command.side_effect = GitCommandError("Git command failed")
        
        result = self.git_parser._get_commit_stats("abc123def456")
        
        # Should handle exceptions gracefully
        assert result['insertions'] == 0
        assert result['deletions'] == 0

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_remote_url_success(self, mock_run_command):
        """Test _get_remote_url with successful execution."""
        mock_run_command.return_value = "https://github.com/test/repo.git\n"
        
        result = self.git_parser._get_remote_url()
        
        assert result == "https://github.com/test/repo.git"

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_remote_url_error(self, mock_run_command):
        """Test _get_remote_url with error."""
        mock_run_command.side_effect = GitCommandError("No remote found")
        
        result = self.git_parser._get_remote_url()
        
        assert result is None

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_current_branch_success(self, mock_run_command):
        """Test _get_current_branch with successful execution."""
        mock_run_command.return_value = "main\n"
        
        result = self.git_parser._get_current_branch()
        
        assert result == "main"

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_current_branch_error(self, mock_run_command):
        """Test _get_current_branch with error."""
        mock_run_command.side_effect = GitCommandError("Branch command failed")
        
        result = self.git_parser._get_current_branch()
        
        assert result is None

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_total_commits_success(self, mock_run_command):
        """Test _get_total_commits with successful execution."""
        mock_run_command.return_value = "100\n"
        
        result = self.git_parser._get_total_commits()
        
        assert result == 100

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_total_commits_error(self, mock_run_command):
        """Test _get_total_commits with error."""
        mock_run_command.side_effect = GitCommandError("Rev-list command failed")
        
        result = self.git_parser._get_total_commits()
        
        assert result == 0

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_total_commits_invalid_output(self, mock_run_command):
        """Test _get_total_commits with invalid output."""
        mock_run_command.return_value = "invalid\n"
        
        result = self.git_parser._get_total_commits()
        
        assert result == 0

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_last_commit_date_success(self, mock_run_command):
        """Test _get_last_commit_date with successful execution."""
        mock_run_command.return_value = "2023-01-01T12:00:00+00:00\n"
        
        result = self.git_parser._get_last_commit_date()
        
        assert result == "2023-01-01T12:00:00+00:00"

    @patch('services.commit_tracker_service.src.git_parser.GitParser._run_git_command')
    def test_get_last_commit_date_error(self, mock_run_command):
        """Test _get_last_commit_date with error."""
        mock_run_command.side_effect = GitCommandError("Log command failed")
        
        result = self.git_parser._get_last_commit_date()
        
        assert result is None


class TestGitCommandError:
    """Test cases for GitCommandError."""

    def test_git_command_error_initialization(self):
        """Test GitCommandError initialization."""
        error = GitCommandError("Test error message")
        
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)
