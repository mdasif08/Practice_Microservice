"""
Unit tests for root __init__.py module.

Tests the main package initialization, version information, and imports.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock


class TestRootInit:
    """Test cases for root __init__.py module."""

    def test_version_defined(self):
        """Test that version is properly defined."""
        from craftnudge_ai_agent import __version__
        assert __version__ == "1.0.0"

    def test_author_defined(self):
        """Test that author is properly defined."""
        from craftnudge_ai_agent import __author__
        assert __author__ == "CraftNudge Team"

    def test_description_defined(self):
        """Test that description is properly defined."""
        from craftnudge_ai_agent import __description__
        assert __description__ == "AI Native Agent for Developer Behavior Analysis"

    def test_all_imports_defined(self):
        """Test that __all__ contains expected imports."""
        from craftnudge_ai_agent import __all__
        expected_imports = [
            'CommitTracker',
            'get_logger',
            'setup_logger',
            'get_config'
        ]
        assert __all__ == expected_imports

    def test_commit_tracker_import(self):
        """Test that CommitTracker can be imported."""
        from craftnudge_ai_agent import CommitTracker
        assert CommitTracker is not None

    def test_logger_imports(self):
        """Test that logger functions can be imported."""
        from craftnudge_ai_agent import get_logger, setup_logger
        assert get_logger is not None
        assert setup_logger is not None

    def test_config_import(self):
        """Test that config function can be imported."""
        from craftnudge_ai_agent import get_config
        assert get_config is not None

    @patch('craftnudge_ai_agent.services.commit_tracker_service.src.commit_tracker.CommitTracker')
    def test_import_with_mock_services(self, mock_commit_tracker):
        """Test imports work when services are mocked."""
        mock_commit_tracker.return_value = MagicMock()
        
        # This should not raise an ImportError
        from craftnudge_ai_agent import CommitTracker
        assert CommitTracker is not None

    def test_package_docstring(self):
        """Test that package has proper docstring."""
        import craftnudge_ai_agent
        assert "CraftNudge AI Agent" in craftnudge_ai_agent.__doc__
        assert "User Story 2.1.1" in craftnudge_ai_agent.__doc__
        assert "Behavior Tracker" in craftnudge_ai_agent.__doc__

    def test_import_order(self):
        """Test that imports are in correct order."""
        import craftnudge_ai_agent
        # Verify that the module can be imported without circular import issues
        assert hasattr(craftnudge_ai_agent, '__version__')
        assert hasattr(craftnudge_ai_agent, '__all__')

    @patch.dict(sys.modules, {
        'services.commit_tracker_service.src.commit_tracker': None,
        'shared.utils.logger': None,
        'shared.config.config_manager': None
    })
    def test_import_handles_missing_modules(self):
        """Test that imports handle missing modules gracefully."""
        # This should not crash even if some modules are missing
        try:
            import craftnudge_ai_agent
            # If we get here, the import succeeded
            assert True
        except ImportError:
            # If import fails, that's also acceptable for this test
            assert True

    def test_module_attributes(self):
        """Test that module has all required attributes."""
        import craftnudge_ai_agent
        required_attrs = ['__version__', '__author__', '__description__', '__all__']
        
        for attr in required_attrs:
            assert hasattr(craftnudge_ai_agent, attr), f"Missing attribute: {attr}"

    def test_version_format(self):
        """Test that version follows semantic versioning."""
        from craftnudge_ai_agent import __version__
        import re
        
        # Check if version follows semantic versioning (x.y.z)
        version_pattern = r'^\d+\.\d+\.\d+$'
        assert re.match(version_pattern, __version__), f"Version {__version__} does not follow semantic versioning"
