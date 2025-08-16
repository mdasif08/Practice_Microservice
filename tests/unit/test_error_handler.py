"""
Unit tests for shared/utils/error_handler.py module.

Tests error handling, validation, and utility functions.
"""

import pytest
import time
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock, call
from typing import Dict, Any

# Import the module under test
from shared.utils.error_handler import (
    CraftNudgeError, GitRepositoryError, DataStoreError, ValidationError,
    ConfigurationError, handle_error, validate_required_fields,
    validate_field_type, safe_execute, retry_on_error
)


class TestCraftNudgeError:
    """Test cases for CraftNudgeError base class."""

    def test_craft_nudge_error_initialization(self):
        """Test CraftNudgeError initialization with all parameters."""
        error = CraftNudgeError(
            message="Test error",
            error_code="TEST_ERROR",
            details={"key": "value"}
        )
        
        assert error.message == "Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.details == {"key": "value"}
        assert isinstance(error.timestamp, str)

    def test_craft_nudge_error_default_parameters(self):
        """Test CraftNudgeError initialization with default parameters."""
        error = CraftNudgeError("Test error")
        
        assert error.message == "Test error"
        assert error.error_code is None
        assert error.details == {}
        assert isinstance(error.timestamp, str)

    def test_craft_nudge_error_timestamp_format(self):
        """Test that timestamp is in ISO format with UTC timezone."""
        error = CraftNudgeError("Test error")
        
        # Parse timestamp to verify format
        parsed_timestamp = datetime.fromisoformat(error.timestamp)
        assert parsed_timestamp.tzinfo is not None
        assert parsed_timestamp.tzinfo == timezone.utc

    def test_craft_nudge_error_inheritance(self):
        """Test that CraftNudgeError inherits from Exception."""
        error = CraftNudgeError("Test error")
        assert isinstance(error, Exception)

    def test_craft_nudge_error_str_representation(self):
        """Test string representation of CraftNudgeError."""
        error = CraftNudgeError("Test error message")
        assert str(error) == "Test error message"


class TestSpecificErrors:
    """Test cases for specific error types."""

    def test_git_repository_error_inheritance(self):
        """Test GitRepositoryError inheritance."""
        error = GitRepositoryError("Git error")
        assert isinstance(error, CraftNudgeError)
        assert isinstance(error, Exception)

    def test_data_store_error_inheritance(self):
        """Test DataStoreError inheritance."""
        error = DataStoreError("Data store error")
        assert isinstance(error, CraftNudgeError)
        assert isinstance(error, Exception)

    def test_validation_error_inheritance(self):
        """Test ValidationError inheritance."""
        error = ValidationError("Validation error")
        assert isinstance(error, CraftNudgeError)
        assert isinstance(error, Exception)

    def test_configuration_error_inheritance(self):
        """Test ConfigurationError inheritance."""
        error = ConfigurationError("Configuration error")
        assert isinstance(error, CraftNudgeError)
        assert isinstance(error, Exception)

    def test_specific_errors_with_details(self):
        """Test specific errors with details."""
        details = {"field": "value", "code": 123}
        
        git_error = GitRepositoryError("Git error", "GIT_001", details)
        data_error = DataStoreError("Data error", "DATA_001", details)
        validation_error = ValidationError("Validation error", "VAL_001", details)
        config_error = ConfigurationError("Config error", "CONFIG_001", details)
        
        assert git_error.details == details
        assert data_error.details == details
        assert validation_error.details == details
        assert config_error.details == details


class TestHandleError:
    """Test cases for handle_error function."""

    @patch('shared.utils.error_handler.logger')
    def test_handle_error_basic_exception(self, mock_logger):
        """Test handle_error with basic exception."""
        test_error = ValueError("Test value error")
        result = handle_error(test_error, "test_context")
        
        assert result['status'] == 'error'
        assert result['error'] == "Test value error"
        assert result['error_type'] == 'ValueError'
        assert result['context'] == 'test_context'
        assert 'timestamp' in result
        assert 'traceback' in result
        
        # Verify logging was called
        mock_logger.error.assert_called_once()
        mock_logger.debug.assert_called_once()

    @patch('shared.utils.error_handler.logger')
    def test_handle_error_with_error_code(self, mock_logger):
        """Test handle_error with custom error code."""
        test_error = ValueError("Test error")
        result = handle_error(test_error, "test_context", "CUSTOM_ERROR")
        
        assert result['error_code'] == "CUSTOM_ERROR"

    @patch('shared.utils.error_handler.logger')
    def test_handle_error_with_details(self, mock_logger):
        """Test handle_error with additional details."""
        test_error = ValueError("Test error")
        details = {"key": "value", "number": 42}
        result = handle_error(test_error, "test_context", details=details)
        
        assert result['details'] == details

    @patch('shared.utils.error_handler.logger')
    def test_handle_error_craft_nudge_error(self, mock_logger):
        """Test handle_error with CraftNudgeError."""
        error = CraftNudgeError(
            "Test error",
            error_code="TEST_CODE",
            details={"test": "data"}
        )
        result = handle_error(error, "test_context")
        
        assert result['error_code'] == "TEST_CODE"
        assert result['details'] == {"test": "data"}
        assert result['timestamp'] == error.timestamp

    @patch('shared.utils.error_handler.logger')
    def test_handle_error_timestamp_format(self, mock_logger):
        """Test that handle_error returns proper timestamp format."""
        test_error = ValueError("Test error")
        result = handle_error(test_error, "test_context")
        
        # Verify timestamp is in ISO format
        parsed_timestamp = datetime.fromisoformat(result['timestamp'])
        assert parsed_timestamp.tzinfo is not None

    @patch('shared.utils.error_handler.logger')
    def test_handle_error_traceback_included(self, mock_logger):
        """Test that traceback is included in error info."""
        test_error = ValueError("Test error")
        result = handle_error(test_error, "test_context")
        
        assert 'traceback' in result
        assert isinstance(result['traceback'], str)
        assert len(result['traceback']) > 0


class TestValidateRequiredFields:
    """Test cases for validate_required_fields function."""

    def test_validate_required_fields_success(self):
        """Test validate_required_fields with all fields present."""
        data = {"field1": "value1", "field2": "value2", "field3": None}
        required_fields = ["field1", "field2"]
        
        # Should not raise an exception
        validate_required_fields(data, required_fields, "test_context")

    def test_validate_required_fields_missing_field(self):
        """Test validate_required_fields with missing field."""
        data = {"field1": "value1"}
        required_fields = ["field1", "field2"]
        
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields(data, required_fields, "test_context")
        
        error = exc_info.value
        assert "Missing required fields" in str(error)
        assert error.error_code == "MISSING_FIELDS"
        assert "field2" in error.details['missing_fields']

    def test_validate_required_fields_none_value(self):
        """Test validate_required_fields with None value."""
        data = {"field1": "value1", "field2": None}
        required_fields = ["field1", "field2"]
        
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields(data, required_fields, "test_context")
        
        error = exc_info.value
        assert "field2" in error.details['missing_fields']

    def test_validate_required_fields_empty_data(self):
        """Test validate_required_fields with empty data."""
        data = {}
        required_fields = ["field1", "field2"]
        
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields(data, required_fields, "test_context")
        
        error = exc_info.value
        assert "field1" in error.details['missing_fields']
        assert "field2" in error.details['missing_fields']

    def test_validate_required_fields_empty_required_list(self):
        """Test validate_required_fields with empty required fields list."""
        data = {"field1": "value1"}
        required_fields = []
        
        # Should not raise an exception
        validate_required_fields(data, required_fields, "test_context")

    def test_validate_required_fields_context_in_error(self):
        """Test that context is included in error message."""
        data = {"field1": "value1"}
        required_fields = ["field1", "field2"]
        
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields(data, required_fields, "custom_context")
        
        error = exc_info.value
        assert "custom_context" in str(error)
        assert error.details['context'] == "custom_context"


class TestValidateFieldType:
    """Test cases for validate_field_type function."""

    def test_validate_field_type_success(self):
        """Test validate_field_type with correct type."""
        data = {"field1": "string_value", "field2": 42, "field3": [1, 2, 3]}
        
        # Should not raise an exception
        validate_field_type(data, "field1", str, "test_context")
        validate_field_type(data, "field2", int, "test_context")
        validate_field_type(data, "field3", list, "test_context")

    def test_validate_field_type_missing_field(self):
        """Test validate_field_type with missing field."""
        data = {"field1": "value1"}
        
        with pytest.raises(ValidationError) as exc_info:
            validate_field_type(data, "field2", str, "test_context")
        
        error = exc_info.value
        assert "Field 'field2' not found" in str(error)
        assert error.error_code == "MISSING_FIELD"

    def test_validate_field_type_wrong_type(self):
        """Test validate_field_type with wrong type."""
        data = {"field1": "string_value"}
        
        with pytest.raises(ValidationError) as exc_info:
            validate_field_type(data, "field1", int, "test_context")
        
        error = exc_info.value
        assert "must be of type int" in str(error)
        assert error.error_code == "INVALID_TYPE"
        assert error.details['expected_type'] == "int"
        assert error.details['actual_type'] == "str"

    def test_validate_field_type_complex_types(self):
        """Test validate_field_type with complex types."""
        data = {
            "dict_field": {"key": "value"},
            "list_field": [1, 2, 3],
            "tuple_field": (1, 2, 3),
            "bool_field": True
        }
        
        # Should not raise an exception
        validate_field_type(data, "dict_field", dict, "test_context")
        validate_field_type(data, "list_field", list, "test_context")
        validate_field_type(data, "tuple_field", tuple, "test_context")
        validate_field_type(data, "bool_field", bool, "test_context")

    def test_validate_field_type_none_value(self):
        """Test validate_field_type with None value."""
        data = {"field1": None}
        
        with pytest.raises(ValidationError) as exc_info:
            validate_field_type(data, "field1", str, "test_context")
        
        error = exc_info.value
        assert error.details['actual_type'] == "NoneType"

    def test_validate_field_type_context_in_error(self):
        """Test that context is included in error message."""
        data = {"field1": "string_value"}
        
        with pytest.raises(ValidationError) as exc_info:
            validate_field_type(data, "field1", int, "custom_context")
        
        error = exc_info.value
        assert "custom_context" in str(error)
        assert error.details['context'] == "custom_context"


class TestSafeExecute:
    """Test cases for safe_execute function."""

    def test_safe_execute_success(self):
        """Test safe_execute with successful function execution."""
        def test_func(a, b):
            return a + b
        
        result = safe_execute(test_func, 2, 3)
        
        assert result['status'] == 'success'
        assert result['result'] == 5

    def test_safe_execute_with_kwargs(self):
        """Test safe_execute with keyword arguments."""
        def test_func(a, b, multiplier=1):
            return (a + b) * multiplier
        
        result = safe_execute(test_func, 2, 3, multiplier=2)
        
        assert result['status'] == 'success'
        assert result['result'] == 10

    def test_safe_execute_function_failure(self):
        """Test safe_execute with function that raises an exception."""
        def test_func():
            raise ValueError("Test error")
        
        result = safe_execute(test_func)
        
        assert result['status'] == 'error'
        assert result['error'] == "Test error"
        assert result['error_type'] == 'ValueError'

    def test_safe_execute_with_complex_return_value(self):
        """Test safe_execute with complex return value."""
        def test_func():
            return {"key": "value", "list": [1, 2, 3]}
        
        result = safe_execute(test_func)
        
        assert result['status'] == 'success'
        assert result['result'] == {"key": "value", "list": [1, 2, 3]}

    def test_safe_execute_function_name_in_context(self):
        """Test that function name is included in error context."""
        def test_func():
            raise ValueError("Test error")
        
        result = safe_execute(test_func)
        
        assert "safe_execute(test_func)" in result['context']


class TestRetryOnError:
    """Test cases for retry_on_error function."""

    @patch('shared.utils.error_handler.time.sleep')
    @patch('shared.utils.error_handler.logger')
    def test_retry_on_error_success_first_attempt(self, mock_logger, mock_sleep):
        """Test retry_on_error with successful first attempt."""
        def test_func():
            return "success"
        
        result = retry_on_error(test_func)
        
        assert result['status'] == 'success'
        assert result['result'] == "success"
        assert result['attempts'] == 1
        mock_sleep.assert_not_called()

    @patch('shared.utils.error_handler.time.sleep')
    @patch('shared.utils.error_handler.logger')
    def test_retry_on_error_success_after_retries(self, mock_logger, mock_sleep):
        """Test retry_on_error with success after retries."""
        call_count = 0
        
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary error")
            return "success"
        
        result = retry_on_error(test_func, max_retries=3, delay=0.1)
        
        assert result['status'] == 'success'
        assert result['result'] == "success"
        assert result['attempts'] == 3
        assert mock_sleep.call_count == 2  # Sleep after first two failures

    @patch('shared.utils.error_handler.time.sleep')
    @patch('shared.utils.error_handler.logger')
    def test_retry_on_error_all_attempts_fail(self, mock_logger, mock_sleep):
        """Test retry_on_error with all attempts failing."""
        def test_func():
            raise ValueError("Persistent error")
        
        result = retry_on_error(test_func, max_retries=2, delay=0.1)
        
        assert result['status'] == 'error'
        assert result['error'] == "Persistent error"
        assert result['error_code'] == "MAX_RETRIES_EXCEEDED"
        assert result['details']['max_retries'] == 2
        assert result['details']['attempts'] == 3
        assert mock_sleep.call_count == 2

    @patch('shared.utils.error_handler.time.sleep')
    @patch('shared.utils.error_handler.logger')
    def test_retry_on_error_custom_parameters(self, mock_logger, mock_sleep):
        """Test retry_on_error with custom retry parameters."""
        call_count = 0
        
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Temporary error")
            return "success"
        
        result = retry_on_error(test_func, max_retries=1, delay=0.5, backoff_factor=3.0)
        
        assert result['status'] == 'success'
        assert result['result'] == "success"
        assert result['attempts'] == 2
        
        # Verify sleep calls with backoff
        expected_sleep_calls = [call(0.5)]
        mock_sleep.assert_has_calls(expected_sleep_calls)

    @patch('shared.utils.error_handler.time.sleep')
    @patch('shared.utils.error_handler.logger')
    def test_retry_on_error_with_args_kwargs(self, mock_logger, mock_sleep):
        """Test retry_on_error with function arguments."""
        def test_func(a, b, multiplier=1):
            return (a + b) * multiplier
        
        result = retry_on_error(test_func, 2, 3, multiplier=2)
        
        assert result['status'] == 'success'
        assert result['result'] == 10

    @patch('shared.utils.error_handler.time.sleep')
    @patch('shared.utils.error_handler.logger')
    def test_retry_on_error_logging(self, mock_logger, mock_sleep):
        """Test that retry_on_error logs appropriately."""
        def test_func():
            raise ValueError("Test error")
        
        retry_on_error(test_func, max_retries=1, delay=0.1)
        
        # Verify warning and error logs were called
        assert mock_logger.warning.call_count == 2  # Two failed attempts
        assert mock_logger.error.call_count == 1   # Final failure
        assert mock_logger.info.call_count == 1    # Retry message

    @patch('shared.utils.error_handler.time.sleep')
    @patch('shared.utils.error_handler.logger')
    def test_retry_on_error_zero_retries(self, mock_logger, mock_sleep):
        """Test retry_on_error with zero retries."""
        def test_func():
            raise ValueError("Test error")
        
        result = retry_on_error(test_func, max_retries=0, delay=0.1)
        
        assert result['status'] == 'error'
        assert result['details']['attempts'] == 1
        mock_sleep.assert_not_called()

    @pytest.mark.parametrize("max_retries,expected_attempts", [
        (0, 1), (1, 2), (2, 3), (5, 6)
    ])
    @patch('shared.utils.error_handler.time.sleep')
    @patch('shared.utils.error_handler.logger')
    def test_retry_on_error_attempt_counting(self, mock_logger, mock_sleep, max_retries, expected_attempts):
        """Test retry_on_error attempt counting with different max_retries."""
        def test_func():
            raise ValueError("Test error")
        
        result = retry_on_error(test_func, max_retries=max_retries, delay=0.1)
        
        assert result['details']['attempts'] == expected_attempts
        assert result['details']['max_retries'] == max_retries


class TestErrorHandlerIntegration:
    """Integration tests for error handler components."""

    def test_error_chain_with_validation(self):
        """Test error handling chain with validation functions."""
        data = {"field1": "value1"}  # Missing field2
        
        try:
            validate_required_fields(data, ["field1", "field2"], "test_context")
        except ValidationError as e:
            error_info = handle_error(e, "validation_context")
            
            assert error_info['status'] == 'error'
            assert error_info['error_code'] == "MISSING_FIELDS"
            assert "field2" in error_info['details']['missing_fields']

    def test_safe_execute_with_validation(self):
        """Test safe_execute with validation functions."""
        def validate_data(data):
            validate_required_fields(data, ["required_field"], "validation")
            return "valid"
        
        # Test with invalid data
        result = safe_execute(validate_data, {})
        
        assert result['status'] == 'error'
        assert result['error_type'] == 'ValidationError'

    def test_retry_on_error_with_safe_execute(self):
        """Test retry_on_error with safe_execute."""
        call_count = 0
        
        def unreliable_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Connection failed")
            return "connected"
        
        result = retry_on_error(safe_execute, unreliable_function)
        
        assert result['status'] == 'success'
        assert result['result']['status'] == 'success'
        assert result['result']['result'] == "connected"
