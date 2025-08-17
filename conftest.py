"""
Pytest configuration and fixtures for CraftNudge AI Agent tests.

This file sets up the test environment, import paths, and common fixtures
used across all test modules.
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Mock external dependencies that may not be available during testing
@pytest.fixture(autouse=True)
def mock_external_dependencies():
    """Mock external dependencies to prevent import errors during testing."""
    with patch.dict('sys.modules', {
        'loguru': MagicMock(),
        'jsonlines': MagicMock(),
        'yaml': MagicMock(),
        'PyYAML': MagicMock(),
    }):
        yield

@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for test files."""
    return tmp_path

@pytest.fixture
def mock_git_repo(tmp_path):
    """Create a mock git repository structure for testing."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    (repo_path / ".git").mkdir()
    (repo_path / ".git" / "HEAD").write_text("ref: refs/heads/main")
    return repo_path

@pytest.fixture
def sample_config():
    """Provide a sample configuration for testing."""
    return {
        "app": {
            "name": "CraftNudge AI Agent",
            "version": "1.0.0"
        },
        "data_store": {
            "base_path": "./data"
        },
        "services": {
            "commit_tracker": {
                "enabled": True,
                "batch_size": 100
            },
            "analytics": {
                "enabled": True,
                "batch_size": 50
            },
            "notifications": {
                "enabled": False,
                "providers": ["console"]
            },
            "api_gateway": {
                "enabled": True,
                "host": "localhost",
                "port": 8000
            }
        },
        "logging": {
            "level": "INFO",
            "file": "logs/app.log"
        }
    }

@pytest.fixture
def mock_commit_data():
    """Provide sample commit data for testing."""
    return {
        "hash": "abc123def456",
        "author": "Test Author <test@example.com>",
        "date": "2024-01-01T12:00:00Z",
        "message": "Test commit message",
        "files": ["test_file.py"],
        "stats": {
            "insertions": 10,
            "deletions": 5
        }
    }

@pytest.fixture
def mock_logger():
    """Provide a mock logger for testing."""
    logger = MagicMock()
    logger.info = MagicMock()
    logger.error = MagicMock()
    logger.warning = MagicMock()
    logger.debug = MagicMock()
    return logger

# Configure pytest to handle import errors gracefully
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle import issues."""
    for item in items:
        # Add unit marker to all tests by default
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)
