"""
Unit tests for shared/utils/logger.py module.

Tests logging functionality, setup, and intercept handler.
"""

import pytest
import logging
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from loguru import logger

# Import the module under test
from shared.utils.logger import setup_logger, get_logger, InterceptHandler


class TestLogger:
    """Test cases for logger module."""

    def setup_method(self):
        """Setup method to reset logger state before each test."""
        # Remove all existing handlers
        logger.remove()
        # Reset standard logging
        logging.getLogger().handlers = []

    def teardown_method(self):
        """Teardown method to clean up after each test."""
        # Remove all handlers
        logger.remove()
        # Reset standard logging
        logging.getLogger().handlers = []

    def test_setup_logger_default_parameters(self):
        """Test setup_logger with default parameters."""
        with patch('loguru.logger.add') as mock_add:
            setup_logger()
            
            # Verify console handler was added
            mock_add.assert_called_once()
            call_args = mock_add.call_args
            assert call_args[0][0] == sys.stderr
            assert call_args[1]['level'] == "INFO"
            assert call_args[1]['colorize'] is True

    def test_setup_logger_custom_level(self):
        """Test setup_logger with custom log level."""
        with patch('loguru.logger.add') as mock_add:
            setup_logger(log_level="DEBUG")
            
            # Verify correct level was set
            call_args = mock_add.call_args
            assert call_args[1]['level'] == "DEBUG"

    def test_setup_logger_with_file(self):
        """Test setup_logger with log file specified."""
        test_log_file = "/tmp/test.log"
        
        with patch('loguru.logger.add') as mock_add, \
             patch('pathlib.Path') as mock_path, \
             patch('pathlib.Path.mkdir') as mock_mkdir:
            
            mock_path_instance = MagicMock()
            mock_path.return_value = mock_path_instance
            mock_path_instance.parent = mock_path_instance
            
            setup_logger(log_file=test_log_file)
            
            # Verify both console and file handlers were added
            assert mock_add.call_count == 2
            
            # Verify file handler parameters
            file_call = mock_add.call_args_list[1]
            assert file_call[0][0] == test_log_file
            assert file_call[1]['rotation'] == "10 MB"
            assert file_call[1]['retention'] == "7 days"
            assert file_call[1]['compression'] == "zip"

    def test_setup_logger_custom_format(self):
        """Test setup_logger with custom log format."""
        custom_format = "Custom format: {message}"
        
        with patch('loguru.logger.add') as mock_add:
            setup_logger(log_format=custom_format)
            
            # Verify custom format was used
            call_args = mock_add.call_args
            assert call_args[1]['format'] == custom_format

    def test_setup_logger_creates_log_directory(self):
        """Test that setup_logger creates log directory if it doesn't exist."""
        test_log_file = "/tmp/nonexistent/dir/test.log"
        
        with patch('loguru.logger.add'), \
             patch('pathlib.Path') as mock_path:
            
            mock_path_instance = MagicMock()
            mock_path.return_value = mock_path_instance
            mock_path_instance.parent = mock_path_instance
            
            setup_logger(log_file=test_log_file)
            
            # Verify mkdir was called
            mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_get_logger_returns_logger_instance(self):
        """Test that get_logger returns a logger instance."""
        test_name = "test_module"
        logger_instance = get_logger(test_name)
        
        assert logger_instance is not None
        assert hasattr(logger_instance, 'bind')

    def test_get_logger_with_module_name(self):
        """Test get_logger with different module names."""
        module_names = ["test_module", "another.module", "deeply.nested.module"]
        
        for name in module_names:
            logger_instance = get_logger(name)
            assert logger_instance is not None

    def test_intercept_handler_emit(self):
        """Test InterceptHandler emit method."""
        handler = InterceptHandler()
        
        # Create a mock record
        record = MagicMock()
        record.levelname = "INFO"
        record.levelno = 20
        record.getMessage.return_value = "Test message"
        record.exc_info = None
        
        with patch('loguru.logger.opt') as mock_opt, \
             patch('loguru.logger.level') as mock_level, \
             patch('logging.currentframe') as mock_frame:
            
            mock_level_instance = MagicMock()
            mock_level_instance.name = "INFO"
            mock_level.return_value = mock_level_instance
            
            mock_frame_instance = MagicMock()
            mock_frame_instance.f_code.co_filename = "test_file.py"
            mock_frame_instance.f_back = None
            mock_frame.return_value = mock_frame_instance
            
            mock_opt_instance = MagicMock()
            mock_opt.return_value = mock_opt_instance
            
            # Call emit
            handler.emit(record)
            
            # Verify loguru was called correctly
            mock_opt.assert_called_once_with(depth=2, exception=None)
            mock_opt_instance.log.assert_called_once_with("INFO", "Test message")

    def test_intercept_handler_emit_with_exception(self):
        """Test InterceptHandler emit method with exception info."""
        handler = InterceptHandler()
        
        # Create a mock record with exception
        record = MagicMock()
        record.levelname = "ERROR"
        record.levelno = 40
        record.getMessage.return_value = "Error message"
        record.exc_info = (Exception, Exception("Test error"), None)
        
        with patch('loguru.logger.opt') as mock_opt, \
             patch('loguru.logger.level') as mock_level, \
             patch('logging.currentframe') as mock_frame:
            
            mock_level_instance = MagicMock()
            mock_level_instance.name = "ERROR"
            mock_level.return_value = mock_level_instance
            
            mock_frame_instance = MagicMock()
            mock_frame_instance.f_code.co_filename = "test_file.py"
            mock_frame_instance.f_back = None
            mock_frame.return_value = mock_frame_instance
            
            mock_opt_instance = MagicMock()
            mock_opt.return_value = mock_opt_instance
            
            # Call emit
            handler.emit(record)
            
            # Verify exception info was passed
            mock_opt.assert_called_once_with(depth=2, exception=record.exc_info)

    def test_intercept_handler_emit_unknown_level(self):
        """Test InterceptHandler emit method with unknown log level."""
        handler = InterceptHandler()
        
        # Create a mock record with unknown level
        record = MagicMock()
        record.levelname = "UNKNOWN_LEVEL"
        record.levelno = 25
        record.getMessage.return_value = "Unknown level message"
        record.exc_info = None
        
        with patch('loguru.logger.opt') as mock_opt, \
             patch('loguru.logger.level') as mock_level, \
             patch('logging.currentframe') as mock_frame:
            
            # Mock level to raise ValueError
            mock_level.side_effect = ValueError("Unknown level")
            
            mock_frame_instance = MagicMock()
            mock_frame_instance.f_code.co_filename = "test_file.py"
            mock_frame_instance.f_back = None
            mock_frame.return_value = mock_frame_instance
            
            mock_opt_instance = MagicMock()
            mock_opt.return_value = mock_opt_instance
            
            # Call emit
            handler.emit(record)
            
            # Verify level number was used instead of level name
            mock_opt.assert_called_once_with(depth=2, exception=None)
            mock_opt_instance.log.assert_called_once_with(25, "Unknown level message")

    def test_intercept_handler_emit_logging_file_frame(self):
        """Test InterceptHandler emit method with logging.py frames."""
        handler = InterceptHandler()
        
        # Create a mock record
        record = MagicMock()
        record.levelname = "INFO"
        record.levelno = 20
        record.getMessage.return_value = "Test message"
        record.exc_info = None
        
        with patch('loguru.logger.opt') as mock_opt, \
             patch('loguru.logger.level') as mock_level, \
             patch('logging.currentframe') as mock_frame:
            
            mock_level_instance = MagicMock()
            mock_level_instance.name = "INFO"
            mock_level.return_value = mock_level_instance
            
            # Create frames that look like logging.py
            logging_frame = MagicMock()
            logging_frame.f_code.co_filename = logging.__file__
            logging_frame.f_back = MagicMock()
            logging_frame.f_back.f_code.co_filename = "test_file.py"
            logging_frame.f_back.f_back = None
            
            mock_frame.return_value = logging_frame
            
            mock_opt_instance = MagicMock()
            mock_opt.return_value = mock_opt_instance
            
            # Call emit
            handler.emit(record)
            
            # Verify depth was adjusted for logging.py frames
            mock_opt.assert_called_once_with(depth=3, exception=None)

    def test_setup_logger_integration(self):
        """Test setup_logger integration with actual logging."""
        # Setup logger
        setup_logger(log_level="DEBUG")
        
        # Get a logger instance
        test_logger = get_logger("test_module")
        
        # Verify logger is functional
        assert test_logger is not None
        assert hasattr(test_logger, 'debug')
        assert hasattr(test_logger, 'info')
        assert hasattr(test_logger, 'warning')
        assert hasattr(test_logger, 'error')

    def test_logger_removes_default_handler(self):
        """Test that logger removes default loguru handler."""
        with patch('loguru.logger.remove') as mock_remove:
            # Re-import to trigger the remove call
            import importlib
            import shared.utils.logger
            importlib.reload(shared.utils.logger)
            
            # Verify remove was called
            mock_remove.assert_called()

    def test_setup_logger_clears_standard_logging_handlers(self):
        """Test that setup_logger clears standard logging handlers."""
        # Add a handler to standard logging
        test_handler = logging.StreamHandler()
        logging.getLogger().addHandler(test_handler)
        
        # Verify handler was added
        assert test_handler in logging.getLogger().handlers
        
        with patch('loguru.logger.add'):
            setup_logger()
            
            # Verify handlers were cleared
            assert len(logging.getLogger().handlers) == 0

    def test_setup_logger_adds_intercept_handler(self):
        """Test that setup_logger adds InterceptHandler to standard logging."""
        with patch('loguru.logger.add'):
            setup_logger()
            
            # Verify InterceptHandler was added
            handlers = logging.getLogger().handlers
            assert len(handlers) == 1
            assert isinstance(handlers[0], InterceptHandler)

    @pytest.mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    def test_setup_logger_valid_levels(self, log_level):
        """Test setup_logger with all valid log levels."""
        with patch('loguru.logger.add') as mock_add:
            setup_logger(log_level=log_level)
            
            # Verify correct level was set
            call_args = mock_add.call_args
            assert call_args[1]['level'] == log_level

    def test_setup_logger_invalid_level(self):
        """Test setup_logger with invalid log level."""
        with patch('loguru.logger.add') as mock_add:
            # This should not raise an exception, but use the invalid level as-is
            setup_logger(log_level="INVALID_LEVEL")
            
            # Verify the invalid level was passed through
            call_args = mock_add.call_args
            assert call_args[1]['level'] == "INVALID_LEVEL"

    def test_get_logger_edge_cases(self):
        """Test get_logger with edge case names."""
        edge_cases = ["", "a" * 1000, "module.with.dots", "module-with-dashes", "module_with_underscores"]
        
        for name in edge_cases:
            logger_instance = get_logger(name)
            assert logger_instance is not None

    def test_intercept_handler_edge_cases(self):
        """Test InterceptHandler with edge case records."""
        handler = InterceptHandler()
        
        # Test with None record
        with pytest.raises(AttributeError):
            handler.emit(None)
        
        # Test with record missing required attributes
        incomplete_record = MagicMock()
        incomplete_record.levelname = "INFO"
        # Missing other attributes
        
        with pytest.raises(AttributeError):
            handler.emit(incomplete_record)
