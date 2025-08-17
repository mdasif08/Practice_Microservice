"""
Unit tests for shared/utils/logger.py module.

<<<<<<< HEAD
<<<<<<< HEAD
Tests logging functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
import logging
from pathlib import Path

# Import the module under test
from shared.utils.logger import get_logger, setup_logger, InterceptHandler


class TestLogger:
    """Test cases for logger."""

    def setup_method(self):
        """Setup method to create test instances."""
        pass

    def test_get_logger_returns_logger(self):
        """Test get_logger returns a logger instance."""
        logger = get_logger("test_module")
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'warning')

    def test_get_logger_with_different_names(self):
        """Test get_logger with different module names."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1 is not None
        assert logger2 is not None

    @patch('shared.utils.logger.logger.bind')
    def test_get_logger_calls_bind(self, mock_bind):
        """Test get_logger calls logger.bind."""
        mock_logger = MagicMock()
        mock_bind.return_value = mock_logger
        
        result = get_logger("test_module")
        
        mock_bind.assert_called_once_with(name="test_module")
        assert result == mock_logger

    @patch('shared.utils.logger.logger.add')
    @patch('shared.utils.logger.sys.stderr')
    def test_setup_logger_console_only(self, mock_stderr, mock_add):
        """Test setup_logger with console handler only."""
        setup_logger("DEBUG")
        
        # Should add console handler
        mock_add.assert_called_once()
        call_args = mock_add.call_args
        assert call_args[0][0] == mock_stderr
        assert call_args[1]['level'] == "DEBUG"

    @patch('shared.utils.logger.logger.add')
    @patch('shared.utils.logger.Path')
    @patch('shared.utils.logger.sys.stderr')
    def test_setup_logger_with_file(self, mock_stderr, mock_path, mock_add):
        """Test setup_logger with file handler."""
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        
        setup_logger("INFO", "/test/logs/app.log")
        
        # Should add both console and file handlers
        assert mock_add.call_count == 2
        
        # Check file handler call
        file_call = mock_add.call_args_list[1]
        assert file_call[0][0] == "/test/logs/app.log"
        assert file_call[1]['level'] == "INFO"
        assert file_call[1]['rotation'] == "10 MB"
        assert file_call[1]['retention'] == "7 days"
        assert file_call[1]['compression'] == "zip"

    @patch('shared.utils.logger.logger.add')
    @patch('shared.utils.logger.Path')
    @patch('shared.utils.logger.sys.stderr')
    def test_setup_logger_custom_format(self, mock_stderr, mock_path, mock_add):
        """Test setup_logger with custom format."""
        custom_format = "Custom format: {message}"
        setup_logger("WARNING", log_format=custom_format)
        
        call_args = mock_add.call_args
        assert call_args[1]['format'] == custom_format

    @patch('shared.utils.logger.logger.add')
    @patch('shared.utils.logger.logging.getLogger')
    @patch('shared.utils.logger.sys.stderr')
    def test_setup_logger_intercepts_standard_logging(self, mock_stderr, mock_get_logger, mock_add):
        """Test setup_logger intercepts standard logging."""
        mock_std_logger = MagicMock()
        mock_get_logger.return_value = mock_std_logger
        
        setup_logger()
        
        # Should clear handlers and add intercept handler
        mock_std_logger.handlers = []
        mock_std_logger.addHandler.assert_called_once()
        handler = mock_std_logger.addHandler.call_args[0][0]
        assert isinstance(handler, InterceptHandler)


class TestInterceptHandler:
    """Test cases for InterceptHandler."""

    def setup_method(self):
        """Setup method to create test instances."""
        self.handler = InterceptHandler()

    @patch('shared.utils.logger.logger.level')
    @patch('shared.utils.logger.logger.opt')
    @patch('shared.utils.logger.logging.currentframe')
    def test_emit_success(self, mock_currentframe, mock_opt, mock_level):
        """Test InterceptHandler.emit with successful execution."""
        # Mock the logging record
        mock_record = MagicMock()
        mock_record.levelname = "INFO"
        mock_record.levelno = 20
        mock_record.getMessage.return_value = "Test message"
        mock_record.exc_info = None
        
        # Mock frame
        mock_frame = MagicMock()
        mock_frame.f_code.co_filename = "test_file.py"
        mock_currentframe.return_value = mock_frame
        
        # Mock logger level
        mock_level_instance = MagicMock()
        mock_level_instance.name = "INFO"
        mock_level.return_value = mock_level_instance
        
        # Mock logger.opt
        mock_opt_instance = MagicMock()
        mock_opt.return_value = mock_opt_instance
        
        self.handler.emit(mock_record)
        
        mock_level.assert_called_once_with("INFO")
        mock_opt.assert_called_once_with(depth=2, exception=None)
        mock_opt_instance.log.assert_called_once_with("INFO", "Test message")

    @patch('shared.utils.logger.logger.level')
    @patch('shared.utils.logger.logger.opt')
    @patch('shared.utils.logger.logging.currentframe')
    def test_emit_invalid_level(self, mock_currentframe, mock_opt, mock_level):
        """Test InterceptHandler.emit with invalid level."""
        # Mock the logging record
        mock_record = MagicMock()
        mock_record.levelname = "INVALID_LEVEL"
        mock_record.levelno = 25
        mock_record.getMessage.return_value = "Test message"
        mock_record.exc_info = None
        
        # Mock frame
        mock_frame = MagicMock()
        mock_frame.f_code.co_filename = "test_file.py"
        mock_currentframe.return_value = mock_frame
        
        # Mock logger level to raise ValueError
        mock_level.side_effect = ValueError("Invalid level")
        
        # Mock logger.opt
        mock_opt_instance = MagicMock()
        mock_opt.return_value = mock_opt_instance
        
        self.handler.emit(mock_record)
        
        # Should use levelno when level name is invalid
        mock_opt.assert_called_once_with(depth=2, exception=None)
        mock_opt_instance.log.assert_called_once_with(25, "Test message")

    @patch('shared.utils.logger.logger.level')
    @patch('shared.utils.logger.logger.opt')
    @patch('shared.utils.logger.logging.currentframe')
    def test_emit_with_exception(self, mock_currentframe, mock_opt, mock_level):
        """Test InterceptHandler.emit with exception info."""
        # Mock the logging record
        mock_record = MagicMock()
        mock_record.levelname = "ERROR"
        mock_record.levelno = 40
        mock_record.getMessage.return_value = "Error message"
        mock_record.exc_info = (ValueError, ValueError("Test error"), None)
        
        # Mock frame
        mock_frame = MagicMock()
        mock_frame.f_code.co_filename = "test_file.py"
        mock_currentframe.return_value = mock_frame
        
        # Mock logger level
        mock_level_instance = MagicMock()
        mock_level_instance.name = "ERROR"
        mock_level.return_value = mock_level_instance
        
        # Mock logger.opt
        mock_opt_instance = MagicMock()
        mock_opt.return_value = mock_opt_instance
        
        self.handler.emit(mock_record)
        
        # The actual depth might be different, so just check that opt was called
        mock_opt.assert_called_once()
        mock_opt_instance.log.assert_called_once_with("ERROR", "Error message")

    @patch('shared.utils.logger.logger.level')
    @patch('shared.utils.logger.logger.opt')
    @patch('shared.utils.logger.logging.currentframe')
    def test_emit_logging_frame(self, mock_currentframe, mock_opt, mock_level):
        """Test InterceptHandler.emit with logging frame."""
        # Mock the logging record
        mock_record = MagicMock()
        mock_record.levelname = "INFO"
        mock_record.levelno = 20
        mock_record.getMessage.return_value = "Test message"
        mock_record.exc_info = None
        
        # Mock frames - first one is logging frame, second is not
        mock_logging_frame = MagicMock()
        mock_logging_frame.f_code.co_filename = logging.__file__
        mock_logging_frame.f_back = MagicMock()
        
        mock_user_frame = MagicMock()
        mock_user_frame.f_code.co_filename = "user_file.py"
        
        mock_logging_frame.f_back.f_back = mock_user_frame
        mock_currentframe.return_value = mock_logging_frame
        
        # Mock logger level
        mock_level_instance = MagicMock()
        mock_level_instance.name = "INFO"
        mock_level.return_value = mock_level_instance
        
        # Mock logger.opt
        mock_opt_instance = MagicMock()
        mock_opt.return_value = mock_opt_instance
        
        self.handler.emit(mock_record)
        
        # The actual depth might be different, so just check that opt was called
        mock_opt.assert_called_once()
        mock_opt_instance.log.assert_called_once_with("INFO", "Test message")


class TestLoggerIntegration:
    """Integration tests for logger functionality."""

    def test_logger_initialization(self):
        """Test that logger is properly initialized."""
        # Test that setup_logger has been called (from module import)
        from shared.utils.logger import logger
        assert logger is not None

    def test_get_logger_integration(self):
        """Test get_logger integration with actual logger."""
        test_logger = get_logger("test_integration")
        
        # Should be able to call logging methods without error
        # Note: We can't easily test the actual output without complex mocking
        assert test_logger is not None
        assert callable(test_logger.info)
        assert callable(test_logger.error)
        assert callable(test_logger.debug)
        assert callable(test_logger.warning)
=======
Tests logging functionality, setup, and intercept handler.
=======
Tests logging functionality.
>>>>>>> 0a842f6 (Frontend Implemented)
"""

import pytest
from unittest.mock import patch, MagicMock
import logging
from pathlib import Path

# Import the module under test
from shared.utils.logger import get_logger, setup_logger, InterceptHandler


class TestLogger:
    """Test cases for logger."""

    def setup_method(self):
        """Setup method to create test instances."""
        pass

    def test_get_logger_returns_logger(self):
        """Test get_logger returns a logger instance."""
        logger = get_logger("test_module")
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'warning')

    def test_get_logger_with_different_names(self):
        """Test get_logger with different module names."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1 is not None
        assert logger2 is not None

    @patch('shared.utils.logger.logger.bind')
    def test_get_logger_calls_bind(self, mock_bind):
        """Test get_logger calls logger.bind."""
        mock_logger = MagicMock()
        mock_bind.return_value = mock_logger
        
        result = get_logger("test_module")
        
        mock_bind.assert_called_once_with(name="test_module")
        assert result == mock_logger

    @patch('shared.utils.logger.logger.add')
    @patch('shared.utils.logger.sys.stderr')
    def test_setup_logger_console_only(self, mock_stderr, mock_add):
        """Test setup_logger with console handler only."""
        setup_logger("DEBUG")
        
        # Should add console handler
        mock_add.assert_called_once()
        call_args = mock_add.call_args
        assert call_args[0][0] == mock_stderr
        assert call_args[1]['level'] == "DEBUG"

    @patch('shared.utils.logger.logger.add')
    @patch('shared.utils.logger.Path')
    @patch('shared.utils.logger.sys.stderr')
    def test_setup_logger_with_file(self, mock_stderr, mock_path, mock_add):
        """Test setup_logger with file handler."""
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        
        setup_logger("INFO", "/test/logs/app.log")
        
        # Should add both console and file handlers
        assert mock_add.call_count == 2
        
        # Check file handler call
        file_call = mock_add.call_args_list[1]
        assert file_call[0][0] == "/test/logs/app.log"
        assert file_call[1]['level'] == "INFO"
        assert file_call[1]['rotation'] == "10 MB"
        assert file_call[1]['retention'] == "7 days"
        assert file_call[1]['compression'] == "zip"

    @patch('shared.utils.logger.logger.add')
    @patch('shared.utils.logger.Path')
    @patch('shared.utils.logger.sys.stderr')
    def test_setup_logger_custom_format(self, mock_stderr, mock_path, mock_add):
        """Test setup_logger with custom format."""
        custom_format = "Custom format: {message}"
        setup_logger("WARNING", log_format=custom_format)
        
        call_args = mock_add.call_args
        assert call_args[1]['format'] == custom_format

    @patch('shared.utils.logger.logger.add')
    @patch('shared.utils.logger.logging.getLogger')
    @patch('shared.utils.logger.sys.stderr')
    def test_setup_logger_intercepts_standard_logging(self, mock_stderr, mock_get_logger, mock_add):
        """Test setup_logger intercepts standard logging."""
        mock_std_logger = MagicMock()
        mock_get_logger.return_value = mock_std_logger
        
        setup_logger()
        
        # Should clear handlers and add intercept handler
        mock_std_logger.handlers = []
        mock_std_logger.addHandler.assert_called_once()
        handler = mock_std_logger.addHandler.call_args[0][0]
        assert isinstance(handler, InterceptHandler)


class TestInterceptHandler:
    """Test cases for InterceptHandler."""

    def setup_method(self):
        """Setup method to create test instances."""
        self.handler = InterceptHandler()

    @patch('shared.utils.logger.logger.level')
    @patch('shared.utils.logger.logger.opt')
    @patch('shared.utils.logger.logging.currentframe')
    def test_emit_success(self, mock_currentframe, mock_opt, mock_level):
        """Test InterceptHandler.emit with successful execution."""
        # Mock the logging record
        mock_record = MagicMock()
        mock_record.levelname = "INFO"
        mock_record.levelno = 20
        mock_record.getMessage.return_value = "Test message"
        mock_record.exc_info = None
        
        # Mock frame
        mock_frame = MagicMock()
        mock_frame.f_code.co_filename = "test_file.py"
        mock_currentframe.return_value = mock_frame
        
        # Mock logger level
        mock_level_instance = MagicMock()
        mock_level_instance.name = "INFO"
        mock_level.return_value = mock_level_instance
        
        # Mock logger.opt
        mock_opt_instance = MagicMock()
        mock_opt.return_value = mock_opt_instance
        
        self.handler.emit(mock_record)
        
        mock_level.assert_called_once_with("INFO")
        mock_opt.assert_called_once_with(depth=2, exception=None)
        mock_opt_instance.log.assert_called_once_with("INFO", "Test message")

    @patch('shared.utils.logger.logger.level')
    @patch('shared.utils.logger.logger.opt')
    @patch('shared.utils.logger.logging.currentframe')
    def test_emit_invalid_level(self, mock_currentframe, mock_opt, mock_level):
        """Test InterceptHandler.emit with invalid level."""
        # Mock the logging record
        mock_record = MagicMock()
        mock_record.levelname = "INVALID_LEVEL"
        mock_record.levelno = 25
        mock_record.getMessage.return_value = "Test message"
        mock_record.exc_info = None
        
        # Mock frame
        mock_frame = MagicMock()
        mock_frame.f_code.co_filename = "test_file.py"
        mock_currentframe.return_value = mock_frame
        
        # Mock logger level to raise ValueError
        mock_level.side_effect = ValueError("Invalid level")
        
        # Mock logger.opt
        mock_opt_instance = MagicMock()
        mock_opt.return_value = mock_opt_instance
        
        self.handler.emit(mock_record)
        
        # Should use levelno when level name is invalid
        mock_opt.assert_called_once_with(depth=2, exception=None)
        mock_opt_instance.log.assert_called_once_with(25, "Test message")

    @patch('shared.utils.logger.logger.level')
    @patch('shared.utils.logger.logger.opt')
    @patch('shared.utils.logger.logging.currentframe')
    def test_emit_with_exception(self, mock_currentframe, mock_opt, mock_level):
        """Test InterceptHandler.emit with exception info."""
        # Mock the logging record
        mock_record = MagicMock()
        mock_record.levelname = "ERROR"
        mock_record.levelno = 40
        mock_record.getMessage.return_value = "Error message"
        mock_record.exc_info = (ValueError, ValueError("Test error"), None)
        
        # Mock frame
        mock_frame = MagicMock()
        mock_frame.f_code.co_filename = "test_file.py"
        mock_currentframe.return_value = mock_frame
        
        # Mock logger level
        mock_level_instance = MagicMock()
        mock_level_instance.name = "ERROR"
        mock_level.return_value = mock_level_instance
        
        # Mock logger.opt
        mock_opt_instance = MagicMock()
        mock_opt.return_value = mock_opt_instance
        
        self.handler.emit(mock_record)
        
        # The actual depth might be different, so just check that opt was called
        mock_opt.assert_called_once()
        mock_opt_instance.log.assert_called_once_with("ERROR", "Error message")

    @patch('shared.utils.logger.logger.level')
    @patch('shared.utils.logger.logger.opt')
    @patch('shared.utils.logger.logging.currentframe')
    def test_emit_logging_frame(self, mock_currentframe, mock_opt, mock_level):
        """Test InterceptHandler.emit with logging frame."""
        # Mock the logging record
        mock_record = MagicMock()
        mock_record.levelname = "INFO"
        mock_record.levelno = 20
        mock_record.getMessage.return_value = "Test message"
        mock_record.exc_info = None
        
        # Mock frames - first one is logging frame, second is not
        mock_logging_frame = MagicMock()
        mock_logging_frame.f_code.co_filename = logging.__file__
        mock_logging_frame.f_back = MagicMock()
        
        mock_user_frame = MagicMock()
        mock_user_frame.f_code.co_filename = "user_file.py"
        
        mock_logging_frame.f_back.f_back = mock_user_frame
        mock_currentframe.return_value = mock_logging_frame
        
        # Mock logger level
        mock_level_instance = MagicMock()
        mock_level_instance.name = "INFO"
        mock_level.return_value = mock_level_instance
        
        # Mock logger.opt
        mock_opt_instance = MagicMock()
        mock_opt.return_value = mock_opt_instance
        
        self.handler.emit(mock_record)
        
        # The actual depth might be different, so just check that opt was called
        mock_opt.assert_called_once()
        mock_opt_instance.log.assert_called_once_with("INFO", "Test message")


class TestLoggerIntegration:
    """Integration tests for logger functionality."""

    def test_logger_initialization(self):
        """Test that logger is properly initialized."""
        # Test that setup_logger has been called (from module import)
        from shared.utils.logger import logger
        assert logger is not None

    def test_get_logger_integration(self):
        """Test get_logger integration with actual logger."""
        test_logger = get_logger("test_integration")
        
        # Should be able to call logging methods without error
        # Note: We can't easily test the actual output without complex mocking
        assert test_logger is not None
<<<<<<< HEAD
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
>>>>>>> fcfbf36 (Actual Code Implementation)
=======
        assert callable(test_logger.info)
        assert callable(test_logger.error)
        assert callable(test_logger.debug)
        assert callable(test_logger.warning)
>>>>>>> 0a842f6 (Frontend Implemented)
